"""Phase 3 gate support: automated tests for the MVP.

Deterministic checks only, so the build gate cannot be argued past.
"""
from __future__ import annotations

import hashlib
import re

import guardrails
from agents.base import Agent, StepResult, footer

PLACEHOLDERS = re.compile(r"(lorem ipsum|\bTODO\b|\bTBD\b|\[insert|xx+x|<placeholder>)", re.IGNORECASE)


def run_tests(product_md: str, guide_md: str, modules: list[str], product_title: str) -> list[dict]:
    results = []
    sections = re.split(r"^## Module \d+: ", product_md, flags=re.MULTILINE)[1:]
    results.append({"name": "all_modules_present", "passed": len(sections) == len(modules) and len(modules) >= 3,
                    "value": len(sections), "threshold": f"{len(modules)} (min 3)"})
    short = [i + 1 for i, s in enumerate(sections) if len(s.split()) < 120]
    results.append({"name": "each_module_has_substance", "passed": not short, "value": f"short modules: {short or 'none'}",
                    "threshold": ">= 120 words each"})
    has_steps = all(re.search(r"^\s*\d+\.\s", s, re.MULTILINE) for s in sections) if sections else False
    results.append({"name": "each_module_has_numbered_steps", "passed": has_steps, "value": has_steps, "threshold": True})
    has_check = all(("- [ ]" in s) or ("checklist" in s.lower()) for s in sections) if sections else False
    results.append({"name": "each_module_has_checklist", "passed": has_check, "value": has_check, "threshold": True})
    scan = guardrails.scan_output(product_md + "\n" + guide_md)
    results.append({"name": "no_income_promises_fake_proof_or_urgency", "passed": scan.clean, "value": len(scan.violations), "threshold": 0,
                    "note": "; ".join(v["category"] for v in scan.violations)})
    ph = PLACEHOLDERS.findall(product_md + guide_md)
    results.append({"name": "no_placeholder_text", "passed": not ph, "value": len(ph), "threshold": 0})
    results.append({"name": "user_guide_has_usage_and_support", "passed": "how to use" in guide_md.lower() and "help" in guide_md.lower(),
                    "value": True, "threshold": "sections present"})
    allowed = guardrails.screen_brief({"idea": product_title}).allowed
    results.append({"name": "product_in_allowed_category", "passed": allowed, "value": allowed, "threshold": True})
    sentences = [s for s in re.split(r"[.!?]\s", re.sub(r"[#*|`\-\[\]]", " ", product_md)) if s.strip()]
    avg = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
    results.append({"name": "readable_sentence_length", "passed": avg <= 28, "value": round(avg, 1), "threshold": "<= 28 words"})
    results.append({"name": "deliverable_package_builds", "passed": len(product_md) > 500,
                    "value": "sha256:" + hashlib.sha256(product_md.encode()).hexdigest()[:16], "threshold": "non-empty"})
    return results


class QA(Agent):
    role = "qa"

    def run_step(self, product_md: str, guide_md: str, modules: list[str], product_title: str) -> StepResult:
        results = run_tests(product_md, guide_md, modules, product_title)
        passed = sum(r["passed"] for r in results)
        md = [f"# Phase 3, step 4: MVP test report ({passed}/{len(results)} passed)", "",
              "| Test | Result | Value | Threshold |", "|---|---|---|---|"]
        for r in results:
            md.append(f"| {r['name']} | {'PASS' if r['passed'] else 'FAIL'} | {r['value']} | {r['threshold']} |")
        md += ["", "These checks are deterministic code in `agents/qa.py`, not model opinions.", footer(None)]
        return self.result("qa-report", "test_mvp", "\n".join(md), data={"tests": results})
