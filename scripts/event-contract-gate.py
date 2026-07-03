#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_DIR = REPO_ROOT / "contracts" / "fate" / "delivery"
REGISTRY_PATH = DELIVERY_DIR / "events.json"
ASYNCAPI_PATH = DELIVERY_DIR / "events.asyncapi.json"
DELIVERY_REGISTRY_PATH = DELIVERY_DIR / "registry.json"
SCHEMA_PATH = DELIVERY_DIR / "schemas" / "async-event.schema.json"
RESOURCE_SCHEMA_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "resource.schema.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "event-contract-gate.json"

SENSITIVE_EXAMPLE_PATTERN = re.compile(
    r"(https?://[^/\s:@]+:[^/\s@]+@|"
    r"secret\s*[:=]\s*[^,\s]+|password\s*[:=]\s*[^,\s]+|token\s*[:=]\s*[^,\s]+|"
    r"BEGIN (?:RSA|OPENSSH|PRIVATE)|"
    r"reportMarkdown|birthPlace|出生地区|用户输入)",
    re.IGNORECASE,
)


class EventContractGateError(RuntimeError):
    """Async event contract gate failed."""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _append_check(checks: list[dict[str, Any]], name: str, ok: bool, details: str) -> None:
    checks.append({"name": name, "ok": ok, "details": details})


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    _append_check(checks, name, condition, details)
    if not condition:
        raise EventContractGateError(f"{name}: {details}")


def _allowed(schema: dict[str, Any], key: str) -> set[str]:
    return {str(item) for item in schema.get(key, [])}


def _safe_repo_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts:
        raise EventContractGateError(f"unsafe path: {raw_path}")
    return REPO_ROOT / path


def _contains_sensitive_example_value(payload: Any) -> bool:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return bool(SENSITIVE_EXAMPLE_PATTERN.search(text))


def _resolve_asyncapi_ref(ref: str) -> str:
    return ref.rsplit("/", 1)[-1]


def _validate_schema_links(
    *,
    registry: dict[str, Any],
    asyncapi: dict[str, Any],
    delivery_registry: dict[str, Any],
    resource_schema: dict[str, Any],
    checks: list[dict[str, Any]],
) -> None:
    _check(
        checks,
        "schema_links:async_event_schema",
        registry.get("schemas", {}).get("asyncEvent") == "contracts/fate/delivery/schemas/async-event.schema.json",
        str(registry.get("schemas", {})),
    )
    _check(
        checks,
        "schema_links:resource_schema",
        registry.get("schemas", {}).get("resource") == "contracts/fate/capabilities/schemas/resource.schema.json",
        str(registry.get("schemas", {})),
    )
    _check(
        checks,
        "delivery_registry:async_event_schema",
        delivery_registry.get("schemas", {}).get("asyncEvent")
        == "contracts/fate/delivery/schemas/async-event.schema.json",
        str(delivery_registry.get("schemas", {})),
    )
    _check(
        checks,
        "delivery_registry:async_event_contract",
        delivery_registry.get("asyncEventRegistry", {}).get("contract") == "contracts/fate/delivery/events.json",
        str(delivery_registry.get("asyncEventRegistry", {})),
    )
    _check(
        checks,
        "delivery_registry:asyncapi_document",
        delivery_registry.get("asyncEventRegistry", {}).get("asyncApiDocument")
        == "contracts/fate/delivery/events.asyncapi.json",
        str(delivery_registry.get("asyncEventRegistry", {})),
    )
    _check(
        checks,
        "resource_schema:async_event_resource_type",
        "AsyncEvent" in resource_schema.get("resourceTypes", []),
        str(resource_schema.get("resourceTypes", [])),
    )
    _check(
        checks,
        "resource_schema:async_event_fields",
        "asyncEventResourceFields" in resource_schema,
        str(resource_schema.keys()),
    )
    _check(checks, "asyncapi:version", asyncapi.get("asyncapi") == "3.1.0", str(asyncapi.get("asyncapi")))


def _validate_replay_example(path_value: str, *, kind: str, checks: list[dict[str, Any]]) -> dict[str, Any]:
    path = _safe_repo_path(path_value)
    _check(checks, f"replay_example:{kind}:exists", path.is_file(), path_value)
    example = _load_json(path)
    _check(
        checks,
        f"replay_example:{kind}:kind",
        str(example.get("kind", "")).startswith("fatecat.event_"),
        str(example.get("kind")),
    )
    _check(checks, f"replay_example:{kind}:redacted_ref", "redactedPayloadRef" in example, str(example.keys()))
    _check(
        checks,
        f"replay_example:{kind}:no_sensitive_values",
        not _contains_sensitive_example_value(example),
        path_value,
    )
    _check(
        checks,
        f"replay_example:{kind}:local_only",
        example.get("externalConnectivity") == "not_required",
        str(example.get("externalConnectivity")),
    )
    return example


def _validate_registry(
    *,
    registry: dict[str, Any],
    asyncapi: dict[str, Any],
    schema: dict[str, Any],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    missing_registry = sorted(set(schema["requiredRegistryFields"]) - set(registry))
    _check(checks, "registry:required_fields", not missing_registry, str(missing_registry))
    _check(checks, "registry:resource_type", registry["resourceType"] == "AsyncEventRegistry", registry["resourceType"])
    _check(checks, "registry:schema_version", registry["schemaVersion"] == 1, str(registry["schemaVersion"]))

    standards = registry["standards"]
    missing_standards = sorted(set(schema["requiredStandardsFields"]) - set(standards))
    _check(checks, "standards:required_fields", not missing_standards, str(missing_standards))
    _check(
        checks,
        "standards:cloudevents_version",
        standards["cloudEvents"]["version"] == "1.0",
        standards["cloudEvents"]["version"],
    )
    _check(
        checks,
        "standards:asyncapi_version",
        standards["asyncApi"]["version"] == "3.1.0",
        standards["asyncApi"]["version"],
    )

    async_api_contract = registry["asyncApi"]
    missing_asyncapi = sorted(set(schema["requiredAsyncApiFields"]) - set(async_api_contract))
    _check(checks, "registry_asyncapi:required_fields", not missing_asyncapi, str(missing_asyncapi))
    _check(
        checks,
        "registry_asyncapi:document_path",
        async_api_contract["documentPath"] == "contracts/fate/delivery/events.asyncapi.json",
        async_api_contract["documentPath"],
    )
    _check(
        checks,
        "registry_asyncapi:contract_baseline",
        async_api_contract["status"] == "contract_baseline",
        async_api_contract["status"],
    )

    consumer_policy = registry["consumerCompatibility"]
    missing_consumer_policy = sorted(set(schema["requiredConsumerCompatibilityFields"]) - set(consumer_policy))
    _check(checks, "consumer_policy:required_fields", not missing_consumer_policy, str(missing_consumer_policy))
    _check(
        checks,
        "consumer_policy:local_contract_only",
        consumer_policy["status"] == "local_contract_only",
        consumer_policy["status"],
    )
    _check(
        checks,
        "consumer_policy:min_required_consumers",
        int(consumer_policy["minimumRequiredConsumersPerEvent"]) >= 1,
        str(consumer_policy["minimumRequiredConsumersPerEvent"]),
    )
    required_negative_cases = set(consumer_policy["negativeCases"])
    _check(
        checks,
        "consumer_policy:negative_cases",
        {
            "missing_cloudevents_context_rejected",
            "unknown_event_type_rejected",
            "sensitive_payload_rejected",
            "consumer_without_required_contract_rejected",
        }
        <= required_negative_cases,
        str(sorted(required_negative_cases)),
    )
    _check(
        checks,
        "consumer_policy:external_connectivity",
        consumer_policy["externalConnectivity"] == "not_required",
        consumer_policy["externalConnectivity"],
    )

    replay_policy = registry["replayPolicy"]
    missing_replay_policy = sorted(set(schema["requiredReplayPolicyFields"]) - set(replay_policy))
    _check(checks, "replay_policy:required_fields", not missing_replay_policy, str(missing_replay_policy))
    _check(
        checks,
        "replay_policy:status",
        replay_policy["status"] in set(schema["allowedReplayPolicyStatus"]),
        replay_policy["status"],
    )
    _check(
        checks,
        "replay_policy:idempotency_fields",
        {"id", "source", "type"} <= set(replay_policy["eventIdempotency"].get("keyFields", [])),
        str(replay_policy["eventIdempotency"]),
    )
    replay_sources = set(replay_policy["sources"])
    _check(
        checks,
        "replay_policy:sources",
        {"synthetic_examples", "report_job_event_history"} <= replay_sources,
        str(sorted(replay_sources)),
    )
    dead_letter = replay_policy["deadLetter"]
    missing_dead_letter = sorted(set(schema["requiredDeadLetterPolicyFields"]) - set(dead_letter))
    _check(checks, "dead_letter:required_fields", not missing_dead_letter, str(missing_dead_letter))
    _check(
        checks,
        "dead_letter:status",
        dead_letter["status"] in set(schema["allowedDeadLetterStatus"]),
        dead_letter["status"],
    )
    _check(
        checks,
        "dead_letter:required_payload_ref",
        "redactedPayloadRef" in set(dead_letter["requiredFields"]),
        str(dead_letter["requiredFields"]),
    )
    replay_examples = replay_policy["examples"]
    _check(
        checks,
        "replay_policy:examples",
        {"replayRequest", "deadLetterRecord"} <= set(replay_examples),
        str(replay_examples),
    )
    for example_kind, example_path in replay_examples.items():
        _validate_replay_example(str(example_path), kind=str(example_kind), checks=checks)

    channels = registry["channels"]
    operations = registry["operations"]
    events = registry["events"]
    event_ids = [str(item.get("id")) for item in events]
    _check(checks, "events:unique_ids", len(event_ids) == len(set(event_ids)), str(event_ids))
    _check(checks, "events:min_count", len(events) >= 5, str(len(events)))

    asyncapi_channels = asyncapi.get("channels", {})
    asyncapi_operations = asyncapi.get("operations", {})
    asyncapi_messages = asyncapi.get("components", {}).get("messages", {})
    _check(checks, "asyncapi:channels_present", bool(asyncapi_channels), str(asyncapi_channels.keys()))
    _check(checks, "asyncapi:operations_present", bool(asyncapi_operations), str(asyncapi_operations.keys()))
    _check(checks, "asyncapi:messages_present", bool(asyncapi_messages), str(asyncapi_messages.keys()))

    required_domains = {"job", "webhook", "evaluation", "release"}
    allowed_domains = _allowed(schema, "allowedEventDomain")
    allowed_connectivity = _allowed(schema, "allowedExternalConnectivity")
    allowed_delivery = _allowed(schema, "allowedDeliverySemantics")
    required_context = set(schema["requiredCloudEventsContextFields"])
    event_type_prefixes = tuple(schema["eventTypePrefixes"])
    domain_counts = dict.fromkeys(required_domains, 0)
    live_required = 0
    consumer_contract_count = 0
    required_consumer_count = 0
    dead_letter_eligible_count = 0

    for channel_id, channel in channels.items():
        missing_channel = sorted(set(schema["requiredChannelFields"]) - set(channel))
        _check(checks, f"channel:{channel_id}:required_fields", not missing_channel, str(missing_channel))
        _check(checks, f"channel:{channel_id}:asyncapi_exists", channel_id in asyncapi_channels, channel_id)
        _check(
            checks,
            f"channel:{channel_id}:messages",
            set(channel["messages"]) <= set(asyncapi_messages),
            str(channel["messages"]),
        )

    for operation_id, operation in operations.items():
        missing_operation = sorted(set(schema["requiredOperationFields"]) - set(operation))
        _check(checks, f"operation:{operation_id}:required_fields", not missing_operation, str(missing_operation))
        _check(checks, f"operation:{operation_id}:asyncapi_exists", operation_id in asyncapi_operations, operation_id)
        _check(
            checks, f"operation:{operation_id}:channel_exists", operation["channel"] in channels, operation["channel"]
        )
        _check(
            checks,
            f"operation:{operation_id}:action",
            operation["action"] in set(schema["allowedOperationAction"]),
            operation["action"],
        )
        _check(
            checks,
            f"operation:{operation_id}:messages",
            set(operation["messages"]) <= set(channels[operation["channel"]]["messages"]),
            str(operation["messages"]),
        )

    for event in events:
        event_id = str(event.get("id", "<missing>"))
        missing_event = sorted(set(schema["requiredEventFields"]) - set(event))
        _check(checks, f"{event_id}:required_fields", not missing_event, str(missing_event))
        _check(checks, f"{event_id}:resource_type", event["resourceType"] == "AsyncEvent", event["resourceType"])
        _check(checks, f"{event_id}:domain", event["eventDomain"] in allowed_domains, event["eventDomain"])
        _check(
            checks,
            f"{event_id}:event_type_prefix",
            str(event["eventType"]).startswith(event_type_prefixes),
            event["eventType"],
        )
        _check(
            checks,
            f"{event_id}:cloud_type_prefix",
            str(event["cloudEventsType"]).startswith(registry["standards"]["cloudEvents"]["typePrefix"]),
            event["cloudEventsType"],
        )
        _check(checks, f"{event_id}:channel_exists", event["channel"] in channels, event["channel"])
        _check(checks, f"{event_id}:operation_exists", event["operation"] in operations, event["operation"])
        _check(
            checks,
            f"{event_id}:operation_channel_match",
            operations[event["operation"]]["channel"] == event["channel"],
            f"{event['operation']} -> {operations[event['operation']]['channel']}",
        )
        message_id = str(event["metadata"]["messageId"])
        _check(
            checks,
            f"{event_id}:message_in_operation",
            message_id in operations[event["operation"]]["messages"],
            message_id,
        )
        _check(checks, f"{event_id}:message_in_asyncapi", message_id in asyncapi_messages, message_id)
        asyncapi_message_refs = asyncapi_operations[event["operation"]].get("messages", [])
        operation_message_ids = {_resolve_asyncapi_ref(item.get("$ref", "")) for item in asyncapi_message_refs}
        _check(
            checks,
            f"{event_id}:asyncapi_operation_message",
            message_id in operation_message_ids,
            str(operation_message_ids),
        )
        _check(
            checks,
            f"{event_id}:delivery_semantics",
            event["deliverySemantics"] in allowed_delivery,
            event["deliverySemantics"],
        )
        _check(
            checks,
            f"{event_id}:external_connectivity",
            event["externalConnectivity"] in allowed_connectivity,
            event["externalConnectivity"],
        )
        producer_path = _safe_repo_path(event["producer"])
        _check(checks, f"{event_id}:producer_exists", producer_path.is_file(), event["producer"])
        consumer_contract = event["consumerContract"]
        missing_consumer_contract = sorted(set(schema["requiredConsumerContractFields"]) - set(consumer_contract))
        _check(
            checks,
            f"{event_id}:consumer_contract_required_fields",
            not missing_consumer_contract,
            str(missing_consumer_contract),
        )
        required_consumers = list(consumer_contract["requiredConsumers"])
        consumer_contract_count += 1
        required_consumer_count += len(required_consumers)
        _check(checks, f"{event_id}:required_consumers_present", bool(required_consumers), str(required_consumers))
        _check(
            checks,
            f"{event_id}:required_consumers_declared",
            set(required_consumers) <= set(event["consumers"]),
            str({"required": required_consumers, "consumers": event["consumers"]}),
        )
        _check(
            checks,
            f"{event_id}:required_consumers_not_future_only",
            any(not str(consumer).startswith("future.") for consumer in required_consumers),
            str(required_consumers),
        )
        _check(
            checks,
            f"{event_id}:accepts_additive_fields",
            consumer_contract["acceptsAdditiveFields"] is True,
            str(consumer_contract["acceptsAdditiveFields"]),
        )
        _check(
            checks,
            f"{event_id}:consumer_idempotency_key",
            consumer_contract["idempotencyKey"] == "id",
            str(consumer_contract["idempotencyKey"]),
        )
        _check(
            checks,
            f"{event_id}:consumer_negative_cases",
            required_negative_cases <= set(consumer_contract["negativeCases"]),
            str(consumer_contract["negativeCases"]),
        )
        consumer_replay = consumer_contract["replay"]
        missing_consumer_replay = sorted(set(schema["requiredConsumerReplayFields"]) - set(consumer_replay))
        _check(
            checks,
            f"{event_id}:consumer_replay_required_fields",
            not missing_consumer_replay,
            str(missing_consumer_replay),
        )
        _check(
            checks, f"{event_id}:consumer_replay_supported", consumer_replay["supported"] is True, str(consumer_replay)
        )
        _check(
            checks,
            f"{event_id}:consumer_replay_source_allowed",
            consumer_replay["source"] in replay_sources,
            str(consumer_replay["source"]),
        )
        if consumer_replay["deadLetterEligible"] is True:
            dead_letter_eligible_count += 1
        if event["externalConnectivity"] == "requires_real_receiver":
            live_required += 1
            _check(
                checks,
                f"{event_id}:live_pending",
                event["metadata"]["liveEvidence"] == "外部连通验证待执行",
                event["metadata"]["liveEvidence"],
            )
        example_path = _safe_repo_path(event["example"])
        _check(checks, f"{event_id}:example_exists", example_path.is_file(), event["example"])
        example = _load_json(example_path)
        _check(
            checks,
            f"{event_id}:cloudevents_required_context",
            required_context <= set(example),
            str(sorted(set(example))),
        )
        _check(checks, f"{event_id}:example_specversion", example["specversion"] == "1.0", example["specversion"])
        _check(checks, f"{event_id}:example_type_match", example["type"] == event["cloudEventsType"], example["type"])
        _check(
            checks,
            f"{event_id}:example_source",
            str(example["source"]).startswith("/fatecat/"),
            example["source"],
        )
        _check(
            checks, f"{event_id}:example_data_object", isinstance(example.get("data"), dict), str(example.get("data"))
        )
        _check(
            checks,
            f"{event_id}:example_no_sensitive_values",
            not _contains_sensitive_example_value(example),
            event["example"],
        )
        _check(
            checks,
            f"{event_id}:privacy_boundary_mentions_sensitive_classes",
            all(term.lower() in event["privacyBoundary"].lower() for term in ("user input", "secret", "token")),
            event["privacyBoundary"],
        )
        domain_counts[str(event["eventDomain"])] = domain_counts.get(str(event["eventDomain"]), 0) + 1

    _check(
        checks,
        "events:required_domains",
        required_domains <= {k for k, v in domain_counts.items() if v},
        str(domain_counts),
    )
    _check(checks, "events:webhook_live_pending", live_required >= 1, str(live_required))
    _check(checks, "events:consumer_contracts", consumer_contract_count == len(events), str(consumer_contract_count))
    _check(
        checks, "events:required_consumer_count", required_consumer_count >= len(events), str(required_consumer_count)
    )
    _check(checks, "events:dead_letter_eligible", dead_letter_eligible_count >= 1, str(dead_letter_eligible_count))

    return {
        "eventCount": len(events),
        "channelCount": len(channels),
        "operationCount": len(operations),
        "messageCount": len(asyncapi_messages),
        "domainCounts": domain_counts,
        "liveRequiredCount": live_required,
        "consumerContractCount": consumer_contract_count,
        "requiredConsumerCount": required_consumer_count,
        "deadLetterEligibleCount": dead_letter_eligible_count,
        "replayPolicyStatus": replay_policy["status"],
        "deadLetterStatus": dead_letter["status"],
        "replayExampleCount": len(replay_examples),
        "negativeCaseCount": len(required_negative_cases),
        "asyncApiVersion": asyncapi["asyncapi"],
    }


def run_gate() -> dict[str, Any]:
    registry = _load_json(REGISTRY_PATH)
    asyncapi = _load_json(ASYNCAPI_PATH)
    schema = _load_json(SCHEMA_PATH)
    delivery_registry = _load_json(DELIVERY_REGISTRY_PATH)
    resource_schema = _load_json(RESOURCE_SCHEMA_PATH)
    checks: list[dict[str, Any]] = []
    started = time.perf_counter()

    _validate_schema_links(
        registry=registry,
        asyncapi=asyncapi,
        delivery_registry=delivery_registry,
        resource_schema=resource_schema,
        checks=checks,
    )
    event_summary = _validate_registry(registry=registry, asyncapi=asyncapi, schema=schema, checks=checks)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.event_contract_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "gate": "event_contract",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "summary": event_summary,
        "checks": checks,
        "privacyBoundary": "Event contract gate 只读取 tracked contract metadata 和 synthetic examples，不读取真实 webhook URL、secret、token、用户输入、报告正文或生产事件日志。",
        "limits": [
            "不实现真实公网 webhook live delivery。",
            "不接入外部 broker、消息队列或第三方事件消费端。",
            "不证明 at-least-once 生产投递、exactly-once 或事件平台生产可用。",
            "不替代 report job event history、webhook outbox 或 live release gate 运行时实现。",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat async event contract gate，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate()
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "events": summary["summary"]["eventCount"],
                    "channels": summary["summary"]["channelCount"],
                    "operations": summary["summary"]["operationCount"],
                    "checks": len(summary["checks"]),
                    "elapsedMs": summary["elapsedMs"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except EventContractGateError as exc:
        print(f"event contract gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
