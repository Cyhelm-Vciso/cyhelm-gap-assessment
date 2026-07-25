# CyHelm Compliance Gap Assessment

An evidence-aware API that turns control implementation statements into ranked remediation findings. It makes priority arithmetic explicit and checks whether implemented/not-applicable claims have supporting evidence or rationale.

## MVP

- Implemented, partial, missing and not-applicable states
- Business-impact and remediation-effort scoring
- Evidence completeness checks
- Ranked findings with action guidance

```bash
docker compose up --build
curl -X POST http://localhost:8000/v1/assessments/findings \
  -H "Content-Type: application/json" \
  -d '[{"control_id":"A.5.9","title":"Inventory of information and assets","status":"partial","evidence":["asset-export.csv"],"business_impact":5,"effort":2,"owner":"IT"}]'
```

## Production roadmap

Add assessment campaigns, framework imports, evidence links, reviewer sign-off, due dates, immutable history, exports and role-based tenant isolation. Document-scanning or AI classification should create suggestions only; reviewers remain accountable for control status.

This tool supports an assessment. It does not certify compliance and is not legal or audit advice.

