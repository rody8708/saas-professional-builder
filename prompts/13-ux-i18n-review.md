# 13 · Review experience, accessibility and localization

## Scope
{{Screens, flows, supported devices, locales and themes}}
Read the project profile and [UX guidance](../core/ux-i18n-assistant.md). Review-only requests remain read-only.

## Inspect
- Workflow clarity, hierarchy, spacing, typography and consistent components/tokens.
- Reachable states: loading, empty, success, validation, error, denial, commercial limit and offline where applicable.
- Agreed devices/viewports, long content, zoom and orientation where relevant.
- Accessibility target: keyboard, focus order, labels, errors, contrast, touch targets and assistive technology.
- Localized copy, placeholders, UTF-8, fallback and correct dates/timezones/numbers/currency.
- Dynamic plans/limits from their source; plain language rather than implementation terminology.
- Destructive actions identify object/impact with proportional confirmation.
- Help reflects actual capabilities and does not claim authorization or completion.

## Verify
Open actual screens in the supported browser/client using synthetic data. Record route, viewport, locale, theme, state, expected and observed result. Run available checks and report absent guards. For authorized fixes, recheck the affected matrix after editing.

## Deliver
Actionable findings with evidence, verified combinations and explicit gaps. Sanitize captures. Component tests or static screenshots alone do not demonstrate the entire workflow.
