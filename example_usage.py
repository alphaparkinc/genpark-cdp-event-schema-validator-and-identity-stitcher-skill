"""Example usage for CDP Event Schema Validator & Identity Stitcher."""
from client import CDPEventPipeline

if __name__ == "__main__":
    pipeline = CDPEventPipeline()

    # 1. Identity Stitching
    stitch = pipeline.stitch_identity(
        anonymous_id="anon_cookie_99812",
        user_id="usr_david_01",
        traits={"email": "david@tech.io", "tier": "gold"},
    )
    print("Identity Stitch Status:", stitch["status"])
    print("Canonical User:", pipeline.resolve_canonical_user("anon_cookie_99812"))

    # 2. Tracking Plan Schema Validation (Valid Event)
    valid_event = {
        "type": "track",
        "event": "Order Completed",
        "anonymous_id": "anon_cookie_99812",
        "properties": {
            "order_id": "ord_102",
            "total": 99.50,
            "currency": "USD",
            "products": [{"id": "p1", "price": 99.50}],
        },
    }
    v_res = pipeline.validate_event_payload(valid_event)
    print("\nEvent Validation (Valid):", v_res["valid"])

    # 3. Invalid Event (Missing required total and products)
    bad_event = {
        "type": "track",
        "event": "Order Completed",
        "anonymous_id": "anon_cookie_99812",
        "properties": {"order_id": "ord_103"},
    }
    bad_res = pipeline.validate_event_payload(bad_event)
    print("Event Validation (Bad):", bad_res["valid"], "Errors:", bad_res["errors"])
