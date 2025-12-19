import sys
import yaml
from datetime import datetime

REQUIRED_FIELDS = {
    "mtm_version": str,
    "model_name": str,
    "model_description": str,
    "aathman_fingerprint": str,
    "intended_use": str,
    "allowed_domains": list,
    "prohibited_uses": list,
    "owner": str,
    "contact": str,
    "created_at": str,
    "updated_at": str,
}

ALLOWED_DEPLOYMENT_KEYS = {
    "offline_only": bool,
    "no_user_facing_output": bool,
    "requires_human_review": bool,
}

def parse_iso8601(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        raise ValueError(f"Invalid ISO8601 timestamp: {ts}")

def validate_mtm(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("MTM must be a YAML mapping")

    # Required fields
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(data[field], expected_type):
            raise ValueError(f"Field '{field}' must be of type {expected_type.__name__}")

    # Version check
    if data["mtm_version"] != "mtm-v0.1":
        raise ValueError("Unsupported mtm_version")

    # allowed_domains / prohibited_uses contents
    for field in ("allowed_domains", "prohibited_uses"):
        if not all(isinstance(x, str) for x in data[field]):
            raise ValueError(f"All entries in '{field}' must be strings")

    # deployment_constraints
    if "deployment_constraints" in data:
        dc = data["deployment_constraints"]
        if not isinstance(dc, dict):
            raise ValueError("deployment_constraints must be a mapping")

        for k, v in dc.items():
            if k not in ALLOWED_DEPLOYMENT_KEYS:
                raise ValueError(f"Invalid deployment_constraints key: {k}")
            if not isinstance(v, bool):
                raise ValueError(f"deployment_constraints.{k} must be boolean")

    # timestamps
    created = parse_iso8601(data["created_at"])
    updated = parse_iso8601(data["updated_at"])
    if updated < created:
        raise ValueError("updated_at must not be earlier than created_at")

def main():
    if len(sys.argv) != 2:
        print("Usage: python validator.py model.mtm.yaml")
        sys.exit(1)

    try:
        validate_mtm(sys.argv[1])
    except Exception as e:
        print("INVALID")
        print(str(e))
        sys.exit(1)

    print("VALID")
    sys.exit(0)

if __name__ == "__main__":
    main()
