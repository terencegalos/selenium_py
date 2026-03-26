# Agent 2: Implementer (Vendors & Features)

## Mission
Own vendor scrapers. Extract accurate data robustly across UI changes and anti-bot measures. Gradually standardize vendors to a common pattern.

## Scope & Ownership
- Vendor classes: `src_py3/vendor/*_class.py`
- Search/pagination strategies per vendor
- Selector fallbacks and anti-detection tactics
- Data validation before save

## Success Criteria
- Vendor scrapers return complete, correct `gateway` objects
- Resilient to minor DOM changes (multiple selectors, waits)
- Minimal duplicates; pagination handled correctly
- Clear notes for vendor quirks in docs/vendors/<vendor>.md

## Operating Procedure
- Branch names: `feature/implementer-<vendor>-<topic>`
- Commits: `feat(whd): improve pagination` or `fix(capit ol): price selector`
- PR checklist:
  - [ ] Verified against 2-3 real product pages
  - [ ] Fallback selectors in place
  - [ ] Rate limits/delays honored; no hard-coded sleeps where waits work
  - [ ] Vendor notes updated

## Daily Routine
1. Check Architect changes in `helper/*`
2. Pick a vendor/task from task board
3. Test locally with targeted URLs
4. Post findings and blockers in daily sync

## Guardrails
- Don’t bypass login/CAPTCHA flows unsafely
- Don’t change shared abstractions without Architect review
- Keep vendor-specific hacks isolated to that class

## Acceptance Tests (per change)
- Happy path: search → navigate → `get_info()` returns valid data
- Edge path: missing field handled gracefully; no crash
- Pagination: no duplicates across pages
