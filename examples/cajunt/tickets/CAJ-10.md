Status: Backlog

# CAJ-10 Phone usability pass

Blocked by: CAJ-7, CAJ-9

## Goal
The app is usable one-handed on a phone while standing in a kitchen or a store.

## Context
- Viewport 390x844. Touch targets, no horizontal scroll, readable text, grocery list with tick-off.
- Make the grocery list page (from CAJ-7) tickable and add a web app manifest so the app installs to the home screen.
- Checked with Playwright using a phone device profile, plus a Lighthouse PWA installability check.

## Acceptance criteria
- [ ] No page scrolls horizontally at 390px — checked by: tests/e2e/phone.spec.ts::no horizontal scroll on any page
- [ ] Every button and link is at least 44x44 px — checked by: tests/e2e/phone.spec.ts::touch targets are at least 44px
- [ ] Body text is at least 16px — checked by: tests/e2e/phone.spec.ts::body text is 16px or larger
- [ ] Tapping a grocery item toggles its checked state and it stays checked after reload — checked by: tests/e2e/phone.spec.ts::grocery items can be ticked off
- [ ] The manifest is valid and the app passes the installability audit — checked by: make pwa-check

## Verify
`make verify` and `make e2e`

## Out of scope
Offline mode and service-worker caching, push notifications, native wrappers, visual redesign.

## Escalation
none
