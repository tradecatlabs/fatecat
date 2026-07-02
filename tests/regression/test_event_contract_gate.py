from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "event-contract-gate.py"
DELIVERY_DIR = ROOT / "contracts" / "fate" / "delivery"
RESOURCE_SCHEMA = ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "resource.schema.json"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_event_contract_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_event_contract_gate_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "event-contract-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = _load_json(output_json)

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.event_contract_gate"
    assert stored["status"] == "passed"
    assert stored["gate"] == "event_contract"
    assert stored["summary"]["eventCount"] == 5
    assert stored["summary"]["channelCount"] == 4
    assert stored["summary"]["operationCount"] == 4
    assert stored["summary"]["messageCount"] == 5
    assert stored["summary"]["asyncApiVersion"] == "3.1.0"
    assert stored["summary"]["domainCounts"] == {"evaluation": 1, "job": 2, "release": 1, "webhook": 1}
    assert stored["summary"]["liveRequiredCount"] == 1
    assert "webhook URL" in stored["privacyBoundary"]
    assert any("公网 webhook" in item for item in stored["limits"])


def test_event_contract_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "event-contract-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["status"] == "passed"
    assert stored["summary"]["eventCount"] == 5


def test_event_contract_registry_links_delivery_and_resource_schema():
    delivery_registry = _load_json(DELIVERY_DIR / "registry.json")
    resource_schema = _load_json(RESOURCE_SCHEMA)
    event_schema = _load_json(DELIVERY_DIR / "schemas" / "async-event.schema.json")
    registry = _load_json(DELIVERY_DIR / "events.json")

    assert delivery_registry["schemas"]["asyncEvent"] == "contracts/fate/delivery/schemas/async-event.schema.json"
    assert delivery_registry["asyncEventRegistry"]["contract"] == "contracts/fate/delivery/events.json"
    assert delivery_registry["asyncEventRegistry"]["asyncApiDocument"] == (
        "contracts/fate/delivery/events.asyncapi.json"
    )
    assert "AsyncEvent" in resource_schema["resourceTypes"]
    assert "asyncEventResourceFields" in resource_schema
    assert event_schema["requiredCloudEventsContextFields"] == ["id", "source", "specversion", "type"]
    assert registry["standards"]["cloudEvents"]["version"] == "1.0"
    assert registry["standards"]["asyncApi"]["version"] == "3.1.0"


def test_event_examples_are_synthetic_cloudevents():
    registry = _load_json(DELIVERY_DIR / "events.json")
    required_context = {"id", "source", "specversion", "type"}

    for event in registry["events"]:
        example = _load_json(ROOT / event["example"])
        assert required_context <= set(example)
        assert example["specversion"] == "1.0"
        assert example["type"] == event["cloudEventsType"]
        assert example["source"].startswith("/fatecat/")
        assert "data" in example
        serialized = json.dumps(example, ensure_ascii=False)
        assert "reportMarkdown" not in serialized
        assert "birthPlace" not in serialized
        assert "webhookUrl" not in serialized
        assert "secret" not in serialized.lower()
        assert "token" not in serialized.lower()
