"""Test setup: no model, no network. Research results come from a fixed fixture."""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
_tmp = tempfile.mkdtemp(prefix="vb-tests-")
os.environ["LLM_PROVIDER"] = "none"
os.environ["RESEARCH_ONLINE"] = "false"
os.environ["DATA_DIR"] = _tmp
os.environ["DECISION_LOG_PATH"] = str(Path(_tmp) / "decision_log.json")

import pytest  # noqa: E402

import config  # noqa: E402
from tools import sources  # noqa: E402


def _fake_search(queries, sources_list=None):
    """Strong evidence for SQL interview prep, weak evidence for anything else."""
    q = " ".join(queries).lower()
    items = []
    if "sql" in q:
        for i in range(8):
            items.append(sources.Evidence("reddit" if i % 2 else "hackernews", f"https://example.org/sql/{i}",
                                          f"Struggling to prepare for SQL interview questions as a junior data analyst #{i}",
                                          engagement=120 + i * 30, comments=40, snippet="any practice resources? would pay for a good one",
                                          query=queries[0], community=f"c{i}", signals=["pain", "willingness_to_pay"]))
    else:
        items.append(sources.Evidence("github", "https://example.org/quotes/1", "Random quotes API",
                                      engagement=3, comments=0, query=queries[0], community="x", signals=["existing_solution"]))
    return items, {"fixture": {"ok": len(queries), "failed": 0, "error": ""}}


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "DECISION_LOG_PATH", tmp_path / "decision_log.json")
    monkeypatch.setattr(sources, "search", _fake_search)
    yield tmp_path
