from fastapi.testclient import TestClient

from cyhelm.main import app

client = TestClient(app)


def test_findings_are_prioritized():
    response = client.post("/v1/assessments/findings", json=[
        {"control_id": "A.1", "title": "Low gap", "status": "partial",
         "evidence": [], "business_impact": 2, "effort": 5},
        {"control_id": "A.2", "title": "Major gap", "status": "missing",
         "evidence": [], "business_impact": 5, "effort": 2}
    ])
    assert response.status_code == 200
    assert response.json()[0]["control_id"] == "A.2"
    assert response.json()[0]["priority"] == "urgent"


def test_na_requires_rationale_as_evidence():
    response = client.post("/v1/assessments/findings", json=[
        {"control_id": "A.3", "title": "Not applicable control", "status": "not_applicable",
         "business_impact": 2, "effort": 2}
    ])
    assert response.json()[0]["evidence_complete"] is False
