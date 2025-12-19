##Aathman MTM

Model Trust Manifest (MTM) is a lightweight, human-readable declaration that describes what a machine-learning model is intended to be used for, and under what constraints. It complements Aathman Core and Aathman PaCM by adding declared intent to verified identity and enforced policy.

MTM does not verify models.
MTM does not enforce policy.
MTM declares intent and constraints.

##Why MTM Exists

Modern ML governance requires more than integrity checks and permission rules. Models also need clearly stated intent.

Aathman Core answers:
“Is this exact model authentic and unchanged?”

PaCM answers:
“Is this model allowed under organizational policy?”

MTM answers:
“What is this model meant to be used for, and what should it not be used for?”

Together, they form a complete governance triangle: identity, intent, and permission.

##What MTM Is

MTM is a small YAML file that travels with a model artifact.
It declares intended use, prohibited use, and operational constraints in clear language.

MTM is:

human-readable

declarative

portable

independent of enforcement

What MTM Is Not

##MTM is not:

a security mechanism

a verifier

a policy engine

a risk assessment

an attestation log

MTM does not make trust decisions. Other systems consume it.

##MTM File Placement

An MTM file is stored alongside the model and its certificate.

Typical layout:

model/

├── model.pth

├── model.pth.aathman.json

└── model.mtm.yaml

This keeps identity, intent, and policy inputs visible and reviewable.

##Schema

MTM v0.1 is defined in schema.yaml.
The schema specifies required fields, optional constraints, and validation rules.

##The schema is:

versioned

strict

intentionally minimal

Semantic meaning is left to policy and human review.

##Validator

This repository includes a minimal structural validator.

##Usage:

python validator.py model.mtm.yaml

##Results:

VALID → exit code 0

INVALID → exit code 1, with an error message

##The validator checks:

required fields

field types

timestamp ordering

allowed constraint keys

It does not verify fingerprints or enforce policy.

##Relationship to Aathman Core and PaCM

Aathman Core verifies model authenticity.
PaCM enforces organizational policy.
MTM declares intent and constraints.

MTM is optional but powerful.
If MTM conflicts with policy, policy wins.
If MTM is missing, enforcement behavior is defined by PaCM.

##Repository Contents

validator.py — minimal MTM structural validator

schema.yaml — MTM v0.1 schema specification

examples/model.mtm.yaml — example manifest

README.md — documentation

LICENSE — Apache License 2.0

CLA.md — Contributor License Agreement

##Status

MTM v0.1 is complete and intentionally minimal.
It is designed to support governance discussions, audits, and policy enforcement without coupling or overreach.

##License

This project is licensed under the Apache License 2.0.
See LICENSE for details.

##Contributing

All contributions require signing the Contributor License Agreement (CLA).
See CLA.md before submitting changes.
