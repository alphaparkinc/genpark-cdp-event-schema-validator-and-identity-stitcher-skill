"""MCP server for CDP Event Schema Validator & Identity Stitcher."""
import sys
import json
from client import CDPEventPipeline

_pipeline = CDPEventPipeline()


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "validate_cdp_event",
                    "description": "Validates a CDP telemetry event against tracking plan schema rules",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "event": {"type": "object", "description": "CDP event payload with type, event, and properties"}
                        },
                        "required": ["event"],
                    },
                },
                {
                    "name": "stitch_customer_identity",
                    "description": "Binds an anonymous session ID to an authenticated canonical user ID with profile traits",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "anonymous_id": {"type": "string"},
                            "user_id": {"type": "string"},
                            "traits": {"type": "object"},
                        },
                        "required": ["anonymous_id", "user_id"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "validate_cdp_event":
            res = _pipeline.validate_event_payload(args.get("event", {}))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "stitch_customer_identity":
            res = _pipeline.stitch_identity(
                args.get("anonymous_id", ""),
                args.get("user_id", ""),
                traits=args.get("traits"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
