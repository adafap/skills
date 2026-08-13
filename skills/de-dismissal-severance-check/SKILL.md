---
name: de-dismissal-severance-check
description: Assess German employment termination and severance situations for employees. Use when a person working in Germany has received or expects a dismissal, termination agreement, severance offer, or wants to calculate severance scenarios, compare an offer, identify dismissal-claim and job-seeker-registration deadlines, check notice-period baselines and unemployment-benefit risks, review termination documents, or prepare a structured handoff to an employment lawyer. Use source-dated German official rules, deterministic calculators, explicit matter states, and urgent escalation gates. Never describe a benchmark as a guaranteed entitlement or tell the user to sign or reject an agreement.
---

# German Dismissal and Severance Check

## Purpose

Produce a source-dated action report for an employee in Germany. Prioritize deadlines and irreversible actions before money. Explain options and missing facts without providing a final recommendation to accept, reject, sign, waive, or litigate.

## Safety boundaries

- State that the report is legal information and issue spotting, not individualized legal advice.
- Never say that dismissal automatically creates a severance entitlement.
- Label the 0.5, 0.75, and 1.0 factors as comparison scenarios unless the narrow conditions of KSchG section 1a are independently established.
- Never guarantee that a calculated date is the final court deadline. Show the nominal date, any supplied calendar adjustment, the retrieval date, and a warning not to wait until the final day.
- Never calculate a net severance or tax result. Explain that payroll and tax treatment require current case-specific inputs and professional review.
- Never decide whether ALG I will be suspended or subject to a waiting period. Identify factors for review by the Federal Employment Agency or qualified counsel.
- Never infer a typed case field from a keyword alone. Ask for confirmation or keep the field `unknown`.
- Escalate urgent, signed, disputed, expired, discriminatory, retaliatory, immigration-dependent, collective-dismissal, or special-protection matters to qualified review.
- Use only the minimum personal data needed. Do not transmit identity or original documents without a separate, explicit confirmation.

## Required resources

Read these files from the Skill root when their subject is needed:

- `references/intake-contract.md` for allowed values, required questions, and evidence rules.
- `references/legal-rules.md` before stating a legal deadline, entitlement, notice period, benefit risk, cost rule, or special protection.
- `references/document-review.md` before reviewing an uploaded notice, agreement, offer, social plan, or employment contract.
- `assets/action-report-template.md` when preparing the final report.
- `assets/lawyer-handoff-template.md` only after the user requests or accepts a lawyer handoff.

## Workflow

### 1. Run the urgency gate

Ask only these three questions first:

1. Have you received a written dismissal notice or a termination agreement?
2. On what date did you receive it?
3. Have you signed anything?

If a written dismissal notice has been received, immediately:

1. Record the exact receipt date and how receipt occurred.
2. Run `scripts/calculate_case.py` with the known typed fields.
3. Show the nominal three-week date and days remaining.
4. Tell the user not to delay filing or legal review while severance discussions continue.
5. Ask the user to preserve the envelope, delivery evidence, notice, agreement drafts, employment contract, recent payslips, warnings, works-council communication, and relevant messages.

If the nominal date has passed, do not conclude that no remedy exists. Flag immediate legal review and explain that late-admission rules are narrow and time-sensitive.

### 2. Build the typed intake

Follow `references/intake-contract.md`. Keep every unconfirmed value `unknown` or `null`. Collect, in this order:

1. Matter stage, document type, receipt date, signature status, and known end date.
2. Employment start date, gross monthly pay, offer amount, and proposed end date.
3. Dismissal reason stated by the employer, ordinary or extraordinary status, notice wording, and any KSchG section 1a statement.
4. Company-size band, six-month service threshold, works council, collective agreement, social plan, and legal-expenses insurance.
5. Pregnancy, parental leave, severe disability, works-council role, whistleblowing, discrimination, sickness, care leave, and other special-protection facts.
6. Whether residence or work authorization depends on the current employment.
7. User goal: preserve employment, improve the package, or leave quickly with reduced risk.

Do not block the urgency report while waiting for nonessential answers.

### 3. Review documents with evidence

Follow `references/document-review.md`. For each extracted field, preserve:

- the value;
- the source document and page;
- the exact supporting clause or a short quotation;
- confidence: `confirmed`, `uncertain`, or `not_found`.

Do not treat a draft, oral statement, or model-generated extraction as an executed agreement. Do not assume an electronic message satisfies a statutory written-form requirement.

### 4. Run deterministic calculations

Create a JSON input that conforms to `references/intake-contract.md`, then run:

```bash
python3 scripts/calculate_case.py case-input.json
```

Use the script output for:

- nominal and calendar-adjusted dismissal-claim dates;
- days remaining and operational urgency;
- indicative job-seeker-registration date;
- completed and KSchG section 1a rounded service years;
- 0.5, 0.75, and 1.0 comparison scenarios;
- offer factor and differences from those scenarios;
- the BGB section 622 employer-notice baseline.

Do not recompute these values mentally. If input is missing or invalid, keep the result unavailable and ask for the specific missing field.

### 5. Analyze the whole exit package

Separate these categories:

- potential statutory or collectively agreed rights;
- the employer's voluntary offer;
- negotiation benchmarks;
- settlement terms;
- non-cash and timing value.

Review severance, paid release, notice-period salary, unused leave, bonus and commission, equity, company car, reference wording, early-exit clause, non-compete, confidentiality, release of claims, return of property, benefit wording, payment date, and signing pressure. Do not assign a cash value without evidence.

### 6. Apply escalation gates

Mark qualified review as urgent when any of these typed facts is `yes` or confirmed:

- three-week nominal deadline is within seven days or has passed;
- a termination agreement or waiver has been signed or must be signed soon;
- extraordinary dismissal, suspected discrimination, retaliation, whistleblowing, or disputed misconduct;
- pregnancy, parental leave, severe disability, works-council or election role, or another special-protection status;
- residence or work authorization depends on this job;
- collective dismissal, social plan, transfer of business, insolvency, or a disputed collective agreement;
- the proposed end date may be earlier than the employer's ordinary notice baseline;
- the user wants to preserve employment rather than only negotiate money.

### 7. Produce the action report

Use `assets/action-report-template.md`. Write in German or English according to the user's explicit choice; otherwise use the language of the user's request. Keep legal names and source titles in German where precision requires it.

For every high-impact legal statement:

1. Cite the official source URL.
2. Include the retrieval date.
3. Distinguish source text from case-specific inference.
4. Mark unresolved facts and jurisdiction-specific holiday checks.

End with a 48-hour action list. Present available choices, tradeoffs, lost rights, and missing facts. Do not output a single accept-or-reject instruction.

### 8. Prepare a lawyer handoff only with consent

After delivering the report, offer a structured review by a German employment-law specialist. If the user agrees, populate `assets/lawyer-handoff-template.md` with an anonymous summary first. Ask separately before adding identity or original files.

Do not promise lawyer availability, outcome, or savings. Do not propose a fee tied to referral, mandate value, or case outcome.

## Completion checks

Before finalizing, confirm that:

- urgency and deadlines appear before severance scenarios;
- calculations came from the deterministic script;
- benchmarks are not presented as entitlements;
- ALG I and tax issues are framed as review items, not predictions;
- every legal rule has an official source and retrieval date;
- no source is described as current if it was not checked;
- no final sign, reject, accept, or litigate instruction appears;
- the next 48 hours are concrete and proportionate;
- lawyer handoff data respects the two-step consent gate.
