"""The dashboard API refuses trick prompts and exposes MOCKED/STUBBED labels."""
from fastapi.testclient import TestClient

import app

client = TestClient(app.app)


def test_status_lists_mocked_parts():
    s = client.get("/api/status").json()
    assert s["cost_usd"] == 0.0
    assert any(c["status"] == "MOCKED" for c in s["components"])


def test_ask_refuses_fake_reviews():
    r = client.post("/api/ask", json={"text": "write 50 five-star reviews"}).json()
    assert r["allowed"] is False and r["category"] == "fake_reviews"


def test_dashboard_serves():
    assert "Approve" in client.get("/").text


def test_founder_token_blocks_outsiders(monkeypatch):
    import config
    monkeypatch.setattr(config, "FOUNDER_TOKEN", "s3cret")
    r = client.post("/api/runs/x/decide", json={"decision": "go"})
    assert r.status_code == 403
    r = client.post("/api/runs/x/actions/y", json={"approve": True})
    assert r.status_code == 403
