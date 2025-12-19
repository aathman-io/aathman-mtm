"""
MTM — Model Trust Manifest Validator

Validates and enforces declared model intent at load time.
"""

import yaml
from datetime import datetime
from typing import Dict

from errors import TrustViolationError


def load_mtm(mtm_path: str) -> Dict:
    """
    Load and validate an MTM YAML file.
    """

    try:
        with open(mtm_path, "r", encoding="utf-8") as f:
            mtm = yaml.safe_load(f)
    except Exception as e:
        raise TrustViolationError("mtm_validation", str(e))

    if not isinstance(mtm, dict):
        raise TrustViolationError("mtm_validation", "MTM must be a YAML mapping")

    # ---- required fields ----
    required_fields = [
        "mtm_version",
        "model_name",
        "model_description",
        "aathman_fingerprint",
        "intended_use",
        "allowed_domains",
        "prohibited_uses",
        "owner",
        "contact",
        "created_at",
        "updated_at",
    ]

    for field in required_fields:
        if field not in mtm:
            raise TrustViolationError(
                "mtm_validation",
                f"Missing required MTM field: {field}",
            )

    # ---- version ----
    if mtm["mtm_version"] != "mtm-v0.1":
        raise TrustViolationError(
            "mtm_validation",
            "Unsupported MTM version",
        )

    # ---- timestamps ----
    try:
        created = datetime.fromisoformat(mtm["created_at"].replace("Z", "+00:00"))
        updated = datetime.fromisoformat(mtm["updated_at"].replace("Z", "+00:00"))
    except Exception:
        raise TrustViolationError(
            "mtm_validation",
            "Invalid ISO8601 timestamp format",
        )

    if updated < created:
        raise TrustViolationError(
            "mtm_validation",
            "updated_at cannot be earlier than created_at",
        )

    # ---- lists ----
    if not isinstance(mtm["allowed_domains"], list):
        raise TrustViolationError(
            "mtm_validation",
            "allowed_domains must be a list",
        )

    if not isinstance(mtm["prohibited_uses"], list):
        raise TrustViolationError(
            "mtm_validation",
            "prohibited_uses must be a list",
        )

    # ---- unknown top-level fields ----
    allowed_top_level = set(required_fields) | {"deployment_constraints"}
    for key in mtm.keys():
        if key not in allowed_top_level:
            raise TrustViolationError(
                "mtm_validation",
                f"Unknown MTM field: {key}",
            )

    return mtm


def enforce_deployment_constraints(mtm: Dict):
    """
    Enforce declared deployment constraints.
    """

    constraints = mtm.get("deployment_constraints")
    if constraints is None:
        return

    if not isinstance(constraints, dict):
        raise TrustViolationError(
            "mtm_validation",
            "deployment_constraints must be a mapping",
        )

    allowed_keys = {
        "offline_only",
        "no_user_facing_output",
        "requires_human_review",
    }

    for key in constraints.keys():
        if key not in allowed_keys:
            raise TrustViolationError(
                "mtm_validation",
                f"Unknown deployment constraint: {key}",
            )

    if constraints.get("offline_only", False):
        raise TrustViolationError("mtm_enforcement", "offline_only")

    if constraints.get("no_user_facing_output", False):
        raise TrustViolationError("mtm_enforcement", "no_user_facing_output")

    if constraints.get("requires_human_review", False):
        raise TrustViolationError("mtm_enforcement", "requires_human_review")


def load_and_enforce_mtm(mtm_path: str):
    """
    Public API used by aathman-loader.
    """

    mtm = load_mtm(mtm_path)
    enforce_deployment_constraints(mtm)
    return mtm
