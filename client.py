"""CDP Event Schema Validator and Identity Stitcher Engine.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Optional, Set
from datetime import datetime


class CDPEventPipeline:
    """Validates Customer Data Platform (CDP) telemetry payloads (`track`, `identify`, `page`)
    against tracking plan schemas and stitches anonymous cookies to authenticated user IDs."""

    TRACKING_PLAN_SCHEMAS = {
        "Order Completed": {
            "required_properties": ["order_id", "total", "currency", "products"],
            "property_types": {
                "order_id": str,
                "total": (int, float),
                "currency": str,
                "products": list,
            },
        },
        "Sign Up": {
            "required_properties": ["method"],
            "property_types": {
                "method": str,
            },
        },
    }

    def __init__(self):
        # Maps anonymous_id -> user_id
        self.identity_graph: Dict[str, str] = {}
        # Maps user_id -> profile traits
        self.user_profiles: Dict[str, Dict[str, Any]] = {}

    def validate_event_payload(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Validates that a track or identify event satisfies schema invariants."""
        event_type = event.get("type", "track")
        event_name = event.get("event")
        properties = event.get("properties", {})

        errors = []

        if not event.get("anonymous_id") and not event.get("user_id"):
            errors.append("Event must include at least 'anonymous_id' or 'user_id'.")

        if event_type == "track" and event_name in self.TRACKING_PLAN_SCHEMAS:
            schema = self.TRACKING_PLAN_SCHEMAS[event_name]
            for req in schema["required_properties"]:
                if req not in properties:
                    errors.append(f"Missing required property '{req}' for event '{event_name}'.")
                else:
                    expected_types = schema["property_types"].get(req)
                    if expected_types and not isinstance(properties[req], expected_types):
                        errors.append(f"Property '{req}' must be of type {expected_types}.")

        is_valid = len(errors) == 0
        return {
            "valid": is_valid,
            "event_name": event_name,
            "errors": errors,
            "received_timestamp": datetime.utcnow().isoformat() + "Z",
        }

    def stitch_identity(self, anonymous_id: str, user_id: str, traits: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Binds an anonymous session cookie ID to an authenticated canonical user account."""
        self.identity_graph[anonymous_id] = user_id

        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {"associated_anonymous_ids": []}

        if anonymous_id not in self.user_profiles[user_id]["associated_anonymous_ids"]:
            self.user_profiles[user_id]["associated_anonymous_ids"].append(anonymous_id)

        if traits:
            self.user_profiles[user_id].update(traits)

        return {
            "status": "IDENTITY_STITCHED",
            "canonical_user_id": user_id,
            "linked_anonymous_id": anonymous_id,
            "total_linked_devices": len(self.user_profiles[user_id]["associated_anonymous_ids"]),
            "traits": self.user_profiles[user_id],
        }

    def resolve_canonical_user(self, identifier: str) -> str:
        """Resolves an anonymous_id or user_id to the canonical user ID."""
        return self.identity_graph.get(identifier, identifier)
