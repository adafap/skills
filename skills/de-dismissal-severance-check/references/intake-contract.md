# Typed Intake Contract

Use exact enum values. Never classify case state through substring checks, keyword matching, or regular expressions. Ask the user to confirm a proposed value or preserve `unknown`.

## Core enums

### `matter_stage`

- `planning`
- `dismissal_received`
- `termination_agreement_offered`
- `offer_negotiation`
- `already_signed`
- `post_settlement`

### `dismissal_reason`

- `operational`
- `conduct`
- `personal`
- `probation`
- `unknown`

### `dismissal_mode`

- `ordinary`
- `extraordinary`
- `unknown`

### `document_type`

- `dismissal_notice`
- `termination_agreement`
- `social_plan`
- `settlement_offer`
- `none`
- `unknown`

### Tri-state answers

Use `yes`, `no`, or `unknown` for every fact that has not been independently verified.

### `company_size_band`

- `up_to_5`
- `6_to_10`
- `more_than_10`
- `unknown`

Do not decide KSchG coverage from this band alone. Part-time weighting and the pre-2004 transitional rule can change the result.

### `user_goal`

- `preserve_employment`
- `improve_package`
- `leave_quickly`
- `unknown`

## Calculator input

Pass a JSON object to `scripts/calculate_case.py`.

```json
{
  "assessment_date": "2026-07-31",
  "matter_stage": "dismissal_received",
  "document_type": "dismissal_notice",
  "dismissal_reason": "operational",
  "dismissal_mode": "ordinary",
  "dismissal_received_date": "2026-07-15",
  "employment_start_date": "2018-01-10",
  "employment_end_date": "2026-10-31",
  "end_date_known_date": "2026-07-15",
  "gross_monthly_pay": "5000.00",
  "offer_amount": "26000.00",
  "section_1a_notice_statement": "yes",
  "probation_clause_active": "no",
  "public_holidays_verified": "no",
  "public_holiday_dates": []
}
```

All dates use ISO `YYYY-MM-DD`. Money values are gross euro amounts expressed as JSON strings or numbers. `gross_monthly_pay` is a user-supplied comparison basis and may not equal the complete statutory monthly-earnings definition. Record regular cash and non-cash components separately. Supply locally applicable public-holiday dates only after verifying them against an official calendar.

## Extended intake fields

Keep these fields in the working case record even though the calculator does not consume all of them:

```json
{
  "written_original_received": "unknown",
  "signed_any_document": "unknown",
  "signature_deadline": null,
  "dismissal_mode": "unknown",
  "company_size_band": "unknown",
  "service_over_six_months": "unknown",
  "works_council_exists": "unknown",
  "works_council_consulted": "unknown",
  "collective_agreement_applies": "unknown",
  "social_plan_applies": "unknown",
  "pregnancy_or_protected_postpartum_period": "unknown",
  "parental_leave_protection": "unknown",
  "severe_disability_status": "unknown",
  "works_council_or_election_role": "unknown",
  "suspected_discrimination": "unknown",
  "whistleblowing_or_retaliation": "unknown",
  "residence_depends_on_employment": "unknown",
  "legal_expenses_insurance": "unknown",
  "user_goal": "unknown"
}
```

## Evidence object

Attach evidence to every document-derived value:

```json
{
  "field": "employment_end_date",
  "value": "2026-10-31",
  "source_file": "dismissal-notice.pdf",
  "page": 1,
  "supporting_text": "Employment ends on 31 October 2026.",
  "confidence": "confirmed"
}
```

Allowed confidence values are `confirmed`, `uncertain`, and `not_found`.

## Validation rules

- Preserve unknown facts; do not fill gaps with typical market practice.
- Treat oral statements, unsigned drafts, and executed documents as different evidence classes.
- Record receipt date separately from the date printed on a document.
- Record salary components separately before deciding whether a monthly-earnings figure is complete.
- Record the employer's stated reason separately from any legal assessment of that reason.
- Record the ordinary notice baseline separately from contractual or collective notice rules.
- Record every consent step for lawyer handoff and document transfer.
