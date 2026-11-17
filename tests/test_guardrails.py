"""Trick prompts from evals/trick_prompts.json must be refused; normal requests must pass."""
import json

import pytest

import guardrails
from conftest import ROOT

EVALS = json.loads((ROOT / "evals" / "trick_prompts.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", EVALS["requests_blocked"], ids=lambda c: c["text"][:40])
def test_trick_requests_are_refused(case):
    v = guardrails.screen_request(case["text"])
    assert not v.allowed
    assert v.category == case["expect"]
    assert v.safe_alternative


@pytest.mark.parametrize("text", EVALS["requests_allowed"])
def test_normal_requests_pass(text):
    assert guardrails.screen_request(text).allowed


@pytest.mark.parametrize("case", EVALS["briefs_blocked"], ids=lambda c: c["idea"][:40])
def test_excluded_products_are_refused(case):
    v = guardrails.screen_brief({"idea": case["idea"]})
    assert not v.allowed and v.category == case["expect"]


@pytest.mark.parametrize("idea", EVALS["briefs_allowed"])
def test_digital_products_are_allowed(idea):
    assert guardrails.screen_brief({"idea": idea}).allowed


@pytest.mark.parametrize("text", [
    "Hurry, offer ends tonight!",
    "You will earn $3,000 a month with this guide.",
    "Join 5,000+ happy students.",
    '"This changed my career, highly recommend it" — Sarah K.',
    "Rated ★★★★★ by our buyers.",
])
def test_output_scanner_removes_bad_sentences(text):
    r = guardrails.scan_output("Intro line.\n" + text)
    assert r.violations and text.split()[0] not in r.text


def test_output_scanner_keeps_our_own_limits():
    text = "No countdown timers, no fake reviews and no income promises."
    assert guardrails.scan_output(text).clean
