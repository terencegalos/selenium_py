# Two-Agent Collaboration Playbook

## Roles
- Architect: Core framework, infra, tests, DX
- Implementer: Vendor classes, extraction quality, resilience

## Branching
- `feature/architect-<topic>` and `feature/implementer-<vendor>-<topic>`
- Keep PRs small (<300 lines diff preferred)

## Commits (Conventional)
- feat/fix/refactor/docs/test/chore/perf
- `feat(core): add progress tracker`
- `fix(whd): robust price selector`

## Reviews
- All PRs require the other agent as reviewer
- Provide: context, before/after behavior, test results, risks

## Testing Policy
- Unit tests for helpers
- Smoke test at least 1 vendor per core change
- Implementer validates vendor changes on 2-3 product URLs

## Coding Standards
- Prefer WebDriverWait over raw sleeps
- Use multiple selectors for brittle elements
- Log actionable info; avoid swallowing exceptions

## Artifacts
- Daily sync: docs/collaboration/sync-YYYY-MM-DD.md
- Decisions: docs/collaboration/decisions.md (use template)
- Task board: docs/collaboration/task-board.md

## Definition of Done
- Code + tests + docs updated
- CI lint/tests green (when added)
- Data shape unchanged unless explicitly versioned
