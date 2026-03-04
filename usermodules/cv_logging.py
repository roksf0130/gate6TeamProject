from __future__ import annotations
import csv
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

import requests


@dataclass(frozen=True)
class CVConfig:
    url: str
    prediction_key: str
    log_path: Path
    threshold: float = 0.75


COLUMNS = [
    "ts",
    "client_id",
    "filename",
    "pred_label",
    "pred_prob",
    "decision",
    "latency_ms",
    "error",
]


def now_utc_iso_no_microseconds() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def ensure_log_file(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(COLUMNS)


def append_log(log_path: Path, row: Dict[str, Any]) -> None:

    ensure_log_file(log_path)
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([row.get(c, "") for c in COLUMNS])
        f.flush()


def decision_rule(tag_name: str, prob: float, threshold: float) -> str:

    if not tag_name:
        return "ERROR"
    if prob < threshold:
        return "UNCERTAIN"
    return "ALLOW" if tag_name == "반입 가능한 물품" else "DENY"


def parse_top1(result_json: Dict[str, Any]) -> Tuple[str, Optional[float]]:
    preds = result_json.get("predictions", []) or []
    if not preds:
        return "", None
    top1 = max(preds, key=lambda x: float(x.get("probability", 0.0)))
    return str(top1.get("tagName", "")), float(top1.get("probability", 0.0))


def predict_and_log(
    image_bytes: bytes,
    filename: str,
    client_id: str,
    config: CVConfig,
    timeout_sec: int = 30,
) -> Dict[str, Any]:

    start = time.time()
    error_msg = ""
    raw: Dict[str, Any] = {}

    headers = {
        "Prediction-Key": config.prediction_key,
        "Content-Type": "application/octet-stream",
    }

    try:
        resp = requests.post(
            config.url, headers=headers, data=image_bytes, timeout=timeout_sec
        )
        resp.raise_for_status()
        raw = resp.json()

        pred_label, pred_prob = parse_top1(raw)
        if pred_prob is None:
            error_msg = "no_predictions"
            decision = "ERROR"
        else:
            decision = decision_rule(pred_label, pred_prob, threshold=config.threshold)

    except Exception as e:
        pred_label, pred_prob, decision = "", None, "ERROR"
        error_msg = str(e)

    latency_ms = int((time.time() - start) * 1000)

    append_log(
        config.log_path,
        {
            "ts": now_utc_iso_no_microseconds(),
            "client_id": client_id,
            "filename": filename,
            "pred_label": pred_label,
            "pred_prob": pred_prob if pred_prob is not None else "",
            "decision": decision,
            "latency_ms": latency_ms,
            "error": error_msg,
        },
    )

    return {
        "pred_label": pred_label,
        "pred_prob": pred_prob,
        "decision": decision,
        "latency_ms": latency_ms,
        "error": error_msg,
        "raw": raw,
    }
