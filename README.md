# genpark-cdp-event-schema-validator-and-identity-stitcher-skill

Customer Data Platform (CDP) tracking plan schema validator and deterministic identity graph stitcher.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **CDP Tracking Plan Validation**: Enforces strict property schema constraints and type validation for standard analytics events.
- **Deterministic Identity Stitching**: Maps anonymous session cookies to authenticated user IDs to create a unified customer journey.
- **Identity Graph Resolution**: Resolves arbitrary touchpoint cookies to canonical enterprise customer profiles.

## Architecture

```
[Inbound CDP Event Stream (Track / Identify / Page)]
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                 CDPEventPipeline                    │
│  - Tracking Plan Schema Invariant Validator         │
│  - Identity Graph Stitcher (Anonymous -> User ID)   │
│  - Unified Customer Profile Trait Aggregator        │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
[Clean Validated Telemetry Event + Canonical Identity]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `validate_cdp_event`: Validates a CDP telemetry event against tracking plan schema rules.
- `stitch_customer_identity`: Binds an anonymous session ID to an authenticated canonical user ID with profile traits.

## Quickstart (Python API)

```python
from client import CDPEventPipeline

pipeline = CDPEventPipeline()
res = pipeline.stitch_identity("anon_1", "usr_100", {"email": "user@corp.com"})
print(res["status"])
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
