"""Webhook callback 配置加密存储工具。

该模块只提供本地 encrypted-at-rest baseline：用成熟 Fernet 实现加密/解密和 key rotation。
外部 Vault/KMS、分布式租约和生产密钥生命周期管理仍属于后续能力。
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from cryptography.fernet import Fernet, InvalidToken

CIPHER_SUITE = "fernet-v1"


class WebhookConfigStoreError(RuntimeError):
    """Webhook 配置加密存储失败。"""


@dataclass(frozen=True)
class EncryptedWebhookDeliveryConfig:
    cipher_suite: str
    key_id: str
    ciphertext: str


@dataclass(frozen=True)
class StoredWebhookDeliveryConfig:
    """解密后的运行时 callback 配置。

    仅在内存中短暂存在，用于 webhook dispatcher；不得写入 event、日志或 API 响应。
    """

    url: str
    secret: str | None = None

    @property
    def signature_mode(self) -> str:
        return "hmac-sha256" if self.secret else "none"


class FernetWebhookConfigCodec:
    """Fernet key ring codec。

    `keys` 是 key id -> Fernet key 的映射；`active_key_id` 用于新写入和 rotation。
    """

    def __init__(self, *, keys: Mapping[str, str | bytes], active_key_id: str | None = None) -> None:
        normalized: dict[str, bytes] = {}
        for key_id, raw_key in keys.items():
            normalized_id = str(key_id or "").strip()
            if not normalized_id:
                raise WebhookConfigStoreError("Fernet key id 不能为空")
            if ":" in normalized_id or "," in normalized_id:
                raise WebhookConfigStoreError("Fernet key id 不能包含分隔符")
            if isinstance(raw_key, bytes):
                key_bytes = raw_key.strip()
            else:
                key_bytes = str(raw_key or "").strip().encode("utf-8")
            if not key_bytes:
                raise WebhookConfigStoreError(f"Fernet key 不能为空: {normalized_id}")
            Fernet(key_bytes)
            normalized[normalized_id] = key_bytes
        if not normalized:
            raise WebhookConfigStoreError("至少需要一个 Fernet key")
        selected = str(active_key_id or next(iter(normalized))).strip()
        if selected not in normalized:
            raise WebhookConfigStoreError("active Fernet key id 不存在")
        self.keys = normalized
        self.active_key_id = selected

    @classmethod
    def from_raw(cls, raw_keys: str | None, *, active_key_id: str | None = None) -> FernetWebhookConfigCodec | None:
        """解析 `key-id:key,key-id-2:key` 形式的运行时 key ring。"""

        raw = str(raw_keys or "").strip()
        if not raw:
            return None
        keys: dict[str, str] = {}
        for item in raw.split(","):
            entry = item.strip()
            if not entry:
                continue
            key_id, sep, key_value = entry.partition(":")
            if not sep:
                raise WebhookConfigStoreError("Fernet key ring 条目必须使用 key-id:key 格式")
            keys[key_id.strip()] = key_value.strip()
        return cls(keys=keys, active_key_id=active_key_id)

    def encrypt_config(self, config: Any) -> EncryptedWebhookDeliveryConfig:
        payload = {
            "url": str(getattr(config, "url", "") or ""),
            "secret": getattr(config, "secret", None),
        }
        if not payload["url"]:
            raise WebhookConfigStoreError("webhook config 缺少 URL")
        return self.encrypt_payload(payload)

    def encrypt_payload(self, payload: Mapping[str, Any]) -> EncryptedWebhookDeliveryConfig:
        body = json.dumps(dict(payload), ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
        token = Fernet(self.keys[self.active_key_id]).encrypt(body).decode("ascii")
        return EncryptedWebhookDeliveryConfig(
            cipher_suite=CIPHER_SUITE,
            key_id=self.active_key_id,
            ciphertext=token,
        )

    def decrypt_config(self, encrypted: EncryptedWebhookDeliveryConfig) -> StoredWebhookDeliveryConfig:
        payload = self.decrypt_payload(encrypted)
        url = str(payload.get("url") or "")
        if not url:
            raise WebhookConfigStoreError("解密后的 webhook config 缺少 URL")
        raw_secret = payload.get("secret")
        secret = str(raw_secret).strip() if raw_secret is not None else None
        return StoredWebhookDeliveryConfig(url=url, secret=secret or None)

    def decrypt_payload(self, encrypted: EncryptedWebhookDeliveryConfig) -> dict[str, Any]:
        if encrypted.cipher_suite != CIPHER_SUITE:
            raise WebhookConfigStoreError(f"不支持的 cipher suite: {encrypted.cipher_suite}")
        key_ids = [encrypted.key_id] + [key_id for key_id in self.keys if key_id != encrypted.key_id]
        last_error: Exception | None = None
        for key_id in key_ids:
            raw_key = self.keys.get(key_id)
            if not raw_key:
                continue
            try:
                body = Fernet(raw_key).decrypt(encrypted.ciphertext.encode("ascii"))
                payload = json.loads(body.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise WebhookConfigStoreError("webhook config payload 必须是对象")
                return payload
            except (InvalidToken, json.JSONDecodeError, UnicodeDecodeError) as exc:
                last_error = exc
        raise WebhookConfigStoreError("无法解密 webhook config") from last_error

    def rotate(self, encrypted: EncryptedWebhookDeliveryConfig) -> EncryptedWebhookDeliveryConfig:
        payload = self.decrypt_payload(encrypted)
        return self.encrypt_payload(payload)
