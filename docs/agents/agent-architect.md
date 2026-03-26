# Agent 1: Architect (Refactoring & Infrastructure)

## Mission
Own the core scraping framework and developer experience. Improve reliability, maintainability, testability, and performance without breaking vendor behavior.

## Scope & Ownership
- Core entry and flow: `src_py3/scraper_seleniumv3.py`
- Abstractions & utils: `src_py3/helper/*`
- Data model: `src_py3/helper/table_gateway.py`, `src_py3/helper/active_record.py`
- WebDriver lifecycle: `src_py3/helper/webdriver_config.py`
- Cross-cutting concerns: logging, retry, config, progress tracking

## Success Criteria
- Changes are backward compatible (existing vendors continue to run)
- Tests pass; coverage improves over time
- Clear logs and actionable errors (no silent failures)
- Performance improves or stays flat

## Operating Procedure
- Branch names: `feature/architect-<short-topic>`
- Commits: Conventional style (e.g., `feat(core): add retry handler`)
- PR checklist:
  - [ ] Unit tests updated/added
  - [ ] Backward compatibility verified with 2 vendors
  - [ ] Docs updated when user-facing behavior changes
  - [ ] Logs and errors are actionable

## Daily Routine
1. Review yesterday's sync and Implementer notes
2. Work in small, mergeable increments
3. Run unit tests + a smoke run against one vendor
4. Post updates in the daily sync

## Guardrails
- Avoid tight coupling to any single vendor
- Prefer composition over inheritance when adding features
- Design for timeouts, retries, and manual CAPTCHAs

## Acceptance Tests (per change)
- Happy path: one vendor scrapes a product end-to-end
- Failure path: simulated timeout surfaces a clear error and retry
- Data integrity: `gateway.retrieve()` output remains shaped the same
