"""Turns a founder brief (JSON or free text) into the structured brief every agent uses."""
from __future__ import annotations

import re

import llm
from agents.base import load_prompt

FIELDS = ("founder_name", "idea", "skills", "budget_usd", "hours_per_week", "target_market", "values", "constraints")


def _num(rx: str, text: str) -> float | None:
    m = re.search(rx, text, re.IGNORECASE)
    return float(m.group(1).replace(",", "")) if m else None


def _list(v) -> list[str]:
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    if isinstance(v, str):
        return [x.strip() for x in re.split(r"[,;\n]", v) if x.strip()]
    return []


def fallback_parse(text: str) -> dict:
    def field(label: str) -> str:
        m = re.search(rf"{label}\s*[:\-]\s*(.+)", text, re.IGNORECASE)
        return m.group(1).strip() if m else ""
    idea = field("idea") or field("starting idea") or text.strip().split("\n")[0][:300]
    return {
        "founder_name": field("name") or field("founder") or "Founder",
        "idea": idea,
        "skills": _list(field("skills")),
        "budget_usd": _num(r"\$\s?([\d,]+)", text) or _num(r"budget\D{0,15}([\d,]+)", text) or 0,
        "hours_per_week": _num(r"(\d+)\s*(?:h|hours?)\s*(?:/|a|per)\s*week", text) or _num(r"time\D{0,15}(\d+)", text) or 5,
        "target_market": field("target market") or field("market") or field("audience"),
        "values": _list(field("values")),
        "constraints": field("constraints"),
    }


def normalize(brief: dict) -> dict:
    out = {k: brief.get(k) for k in FIELDS}
    out["founder_name"] = str(out.get("founder_name") or "Founder")[:60]
    out["idea"] = str(out.get("idea") or "").strip()[:600]
    out["skills"] = _list(out.get("skills"))
    out["values"] = _list(out.get("values"))
    for k in ("budget_usd", "hours_per_week"):
        try:
            out[k] = float(re.sub(r"[^\d.]", "", str(out.get(k))) or 0)
        except ValueError:
            out[k] = 0.0
    out["target_market"] = str(out.get("target_market") or "")[:300]
    out["constraints"] = str(out.get("constraints") or "")[:300]
    for k in ("waitlist_target", "waitlist_window_days", "slug"):
        if brief.get(k):
            out[k] = brief[k]
    return out


def parse(raw: dict | str) -> tuple[dict, str | None]:
    """Returns (brief, model used or None)."""
    if isinstance(raw, dict) and raw.get("idea"):
        return normalize(raw), None
    text = raw if isinstance(raw, str) else str(raw)
    fb = fallback_parse(text)
    data, res = llm.complete_json(load_prompt("intake"),
                                  "Founder brief text:\n" + text[:3000] + "\n\nExtract JSON with keys: " + ", ".join(FIELDS) +
                                  ". skills and values are lists of strings; budget_usd and hours_per_week are numbers. "
                                  "Use the founder's own words. Unknown fields: empty string, 0 or [].", fb, max_tokens=500)
    merged = {**fb, **{k: v for k, v in data.items() if v not in (None, "", [], 0)}}
    return normalize(merged), res.model
