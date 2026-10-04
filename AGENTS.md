# Working agreements

- Read `docs/implementation-plan.md` and `docs/architecture.md` before task work.
- Implement only the sub-stage explicitly agreed with the user. An approved
  roadmap does not authorize implementing every stage.
- Discuss important library, technology, data-model, and external-service
  decisions with the user before implementing them.
- Keep code small, readable, and limited to the agreed functionality. Add
  abstractions and dependencies only when a current requirement needs them.
- Stop after the agreed sub-stage, explain the result and verification, and
  let the user review before moving on.
- Do not restore the archived scaffold or its features without explicit user
  direction. It exists only for recovery.
- Preserve Python 3.11 compatibility.
- After the final code edit, run relevant tests, `ruff check .`, and
  `ruff format --check .`. Report checks that were unavailable or not run.
- Add meaningful tests for implemented behavior; do not create placeholder tests
  merely to make an empty test suite pass.

## Current boundary

Stages 1.1 through 1.3 are complete: legacy archive, agreed roadmap, working rules,
documented record relationships, and a minimal Flask app with environment-based
data-directory configuration and one health API test. Stage 1.4 (SQLite profile
persistence and local media directory) is next, pending user review. Profile
preferences are an optional free-text note. Saved outfits may be incomplete but must contain at
least one clothing item; generation checks its own required pieces. Private
wardrobe items belong to one user and can remain unidentified. Future published
outfits have a creator; every public garment must resolve to a verified shared
product identity, reusing an existing product when present. Unidentified public
garments are no longer allowed. Reuse does not save an item automatically;
explicit saving creates a considering entry linked to the shared product.
Shared product identity distinguishes model and color; different sizes share the
same product. Sharing implementation is deferred. Verification mechanisms must
be agreed before sharing implementation.
Only `GET /health` is implemented. No database schema, media-directory creation,
AI integration, or frontend exists yet.
