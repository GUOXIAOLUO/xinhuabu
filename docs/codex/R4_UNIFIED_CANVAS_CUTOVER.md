# R4 Task — Unified Canvas Cutover

Execute R4 only after R3 explicitly authorizes it.

Goal:

Complete U7 against the R3 canonical persistence authority.

Required work:

- validate/back up source records
- migrate/cut over to canonical Project/Canvas authority
- verify workflow import/export
- verify revision conflicts
- verify Legacy nodes/functions through adapters
- verify 100/300-node performance budget
- remove duplicate Classic/Smart runtime/page/CSS only after acceptance
- keep required Legacy import/read adapters

Important:

Do not create a second "canonical JSON" authority.
U7 canonical persistence means the R3-approved authority.

Gate:

- one Canvas page/runtime/catalog
- canonical persistence active
- old records readable/importable
- no source-mode product distinction
- duplicate runtime removal complete only after tests
- performance budget passes
- rollback backup tested
- status authorizes R5
