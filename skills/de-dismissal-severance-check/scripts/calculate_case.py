#!/usr/bin/env python3
"""Calculate source-bounded German dismissal and severance indicators."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from enum import Enum
from pathlib import Path
from typing import Any, TypeVar

from calendar_rules import (
    add_months,
    adjusted_workday,
    completed_service_years,
    general_notice_end,
    month_end_notice_end,
    probation_notice_end,
    rounded_section_1a_years,
    urgency,
)
SOURCE_AS_OF = "2026-07-31"
MONEY_QUANTUM = Decimal("0.01")
REFERENCE_FACTORS = (Decimal("0.5"), Decimal("0.75"), Decimal("1.0"))
class MatterStage(str, Enum):
    PLANNING = "planning"
    DISMISSAL_RECEIVED = "dismissal_received"
    TERMINATION_AGREEMENT_OFFERED = "termination_agreement_offered"
    OFFER_NEGOTIATION = "offer_negotiation"
    ALREADY_SIGNED = "already_signed"
    POST_SETTLEMENT = "post_settlement"
class DocumentType(str, Enum):
    DISMISSAL_NOTICE = "dismissal_notice"
    TERMINATION_AGREEMENT = "termination_agreement"
    SOCIAL_PLAN = "social_plan"
    SETTLEMENT_OFFER = "settlement_offer"
    NONE = "none"
    UNKNOWN = "unknown"
class DismissalReason(str, Enum):
    OPERATIONAL = "operational"
    CONDUCT = "conduct"
    PERSONAL = "personal"
    PROBATION = "probation"
    UNKNOWN = "unknown"
class DismissalMode(str, Enum):
    ORDINARY = "ordinary"
    EXTRAORDINARY = "extraordinary"
    UNKNOWN = "unknown"
class Answer(str, Enum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"
EnumType = TypeVar("EnumType", bound=Enum)
@dataclass(frozen=True)
class CaseInput:
    assessment_date: date
    matter_stage: MatterStage
    document_type: DocumentType
    dismissal_reason: DismissalReason
    dismissal_mode: DismissalMode
    dismissal_received_date: date | None
    employment_start_date: date | None
    employment_end_date: date | None
    end_date_known_date: date | None
    gross_monthly_pay: Decimal | None
    offer_amount: Decimal | None
    section_1a_notice_statement: Answer
    probation_clause_active: Answer
    public_holidays_verified: Answer
    public_holiday_dates: frozenset[date]
def parse_date(value: Any, field: str, required: bool = False) -> date | None:
    if value is None:
        if required:
            raise ValueError(f"{field} is required")
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO date string")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{field} must use YYYY-MM-DD") from error
def parse_decimal(value: Any, field: str) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f"{field} must be a decimal number")
    try:
        parsed = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"{field} must be a decimal number") from error
    if not parsed.is_finite() or parsed < 0:
        raise ValueError(f"{field} must be a finite non-negative number")
    return parsed
def parse_enum(value: Any, field: str, enum_type: type[EnumType]) -> EnumType:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    try:
        return enum_type(value)
    except ValueError as error:
        allowed = ", ".join(item.value for item in enum_type)
        raise ValueError(f"{field} must be one of: {allowed}") from error
def parse_case(data: Any) -> CaseInput:
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")

    holiday_values = data.get("public_holiday_dates", [])
    if not isinstance(holiday_values, list):
        raise ValueError("public_holiday_dates must be an array")
    holidays = frozenset(
        parse_date(value, "public_holiday_dates[]", required=True)
        for value in holiday_values
    )

    case = CaseInput(
        assessment_date=parse_date(data.get("assessment_date"), "assessment_date", True),
        matter_stage=parse_enum(data.get("matter_stage"), "matter_stage", MatterStage),
        document_type=parse_enum(data.get("document_type"), "document_type", DocumentType),
        dismissal_reason=parse_enum(
            data.get("dismissal_reason"), "dismissal_reason", DismissalReason
        ),
        dismissal_mode=parse_enum(
            data.get("dismissal_mode", "unknown"), "dismissal_mode", DismissalMode
        ),
        dismissal_received_date=parse_date(
            data.get("dismissal_received_date"), "dismissal_received_date"
        ),
        employment_start_date=parse_date(
            data.get("employment_start_date"), "employment_start_date"
        ),
        employment_end_date=parse_date(
            data.get("employment_end_date"), "employment_end_date"
        ),
        end_date_known_date=parse_date(
            data.get("end_date_known_date"), "end_date_known_date"
        ),
        gross_monthly_pay=parse_decimal(data.get("gross_monthly_pay"), "gross_monthly_pay"),
        offer_amount=parse_decimal(data.get("offer_amount"), "offer_amount"),
        section_1a_notice_statement=parse_enum(
            data.get("section_1a_notice_statement", "unknown"),
            "section_1a_notice_statement",
            Answer,
        ),
        probation_clause_active=parse_enum(
            data.get("probation_clause_active", "unknown"),
            "probation_clause_active",
            Answer,
        ),
        public_holidays_verified=parse_enum(
            data.get("public_holidays_verified", "unknown"),
            "public_holidays_verified",
            Answer,
        ),
        public_holiday_dates=holidays,
    )
    validate_case(case)
    return case
def validate_case(case: CaseInput) -> None:
    if (
        case.employment_start_date
        and case.employment_end_date
        and case.employment_end_date < case.employment_start_date
    ):
        raise ValueError("employment_end_date cannot precede employment_start_date")
    if case.gross_monthly_pay == Decimal("0") and case.offer_amount is not None:
        raise ValueError("gross_monthly_pay must be greater than zero when offer_amount is set")


def money(value: Decimal) -> str:
    return str(value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP))


def filing_deadline(case: CaseInput) -> dict[str, Any] | None:
    if (
        case.document_type is not DocumentType.DISMISSAL_NOTICE
        or case.dismissal_received_date is None
    ):
        return None
    nominal = case.dismissal_received_date + timedelta(weeks=3)
    adjusted = adjusted_workday(nominal, case.public_holiday_dates)
    remaining = (adjusted - case.assessment_date).days
    return {
        "nominal_date": nominal.isoformat(),
        "calendar_adjusted_date": adjusted.isoformat(),
        "days_remaining": remaining,
        "urgency": urgency(remaining),
        "public_holidays_verified": case.public_holidays_verified.value,
        "local_holiday_check_required": case.public_holidays_verified is not Answer.YES,
    }


def jobseeker_deadline(case: CaseInput) -> dict[str, Any] | None:
    if case.employment_end_date is None or case.end_date_known_date is None:
        return None
    three_month_mark = add_months(case.employment_end_date, -3)
    if case.end_date_known_date <= three_month_mark:
        due = three_month_mark
        basis = "three_months_before_end"
    else:
        due = case.end_date_known_date + timedelta(days=3)
        basis = "three_days_after_knowledge"
    return {
        "indicative_due_date": due.isoformat(),
        "basis": basis,
        "days_from_assessment": (due - case.assessment_date).days,
        "instruction": "Register immediately; do not wait for this indicative date.",
    }


def notice_period_baseline(case: CaseInput) -> dict[str, Any] | None:
    if case.dismissal_mode is DismissalMode.EXTRAORDINARY:
        return {
            "available": False,
            "reason": "Extraordinary dismissal requires separate review.",
        }
    if case.probation_clause_active is Answer.YES:
        earliest_end = (
            probation_notice_end(case.dismissal_received_date)
            if case.dismissal_received_date
            else None
        )
        return {
            "available": True,
            "length": 2,
            "unit": "weeks",
            "termination_point": "any_day",
            "basis": "agreed_probation_period_up_to_six_months",
            "earliest_baseline_end_date": earliest_end.isoformat() if earliest_end else None,
        }
    if case.employment_start_date is None or case.dismissal_received_date is None:
        return None

    years = completed_service_years(
        case.employment_start_date, case.dismissal_received_date
    )
    thresholds = (
        (20, 7),
        (15, 6),
        (12, 5),
        (10, 4),
        (8, 3),
        (5, 2),
        (2, 1),
    )
    for threshold, months in thresholds:
        if years >= threshold:
            earliest_end = month_end_notice_end(case.dismissal_received_date, months)
            return {
                "available": True,
                "completed_service_years_at_receipt": years,
                "length": months,
                "unit": "months",
                "termination_point": "calendar_month_end",
                "basis": "bgb_622_employer_baseline",
                "probation_status_checked": case.probation_clause_active.value,
                "earliest_baseline_end_date": earliest_end.isoformat(),
                "proposed_end_precedes_baseline": (
                    case.employment_end_date < earliest_end
                    if case.employment_end_date
                    else None
                ),
            }
    earliest_end = general_notice_end(case.dismissal_received_date)
    return {
        "available": True,
        "completed_service_years_at_receipt": years,
        "length": 4,
        "unit": "weeks",
        "termination_point": "fifteenth_or_calendar_month_end",
        "basis": "bgb_622_general_baseline",
        "probation_status_checked": case.probation_clause_active.value,
        "earliest_baseline_end_date": earliest_end.isoformat(),
        "proposed_end_precedes_baseline": (
            case.employment_end_date < earliest_end if case.employment_end_date else None
        ),
    }


def section_1a_status(case: CaseInput) -> str:
    if case.document_type is not DocumentType.DISMISSAL_NOTICE:
        return "not_applicable_to_document_type"
    if case.dismissal_reason is DismissalReason.UNKNOWN:
        return "insufficient_information"
    if case.dismissal_reason is not DismissalReason.OPERATIONAL:
        return "preconditions_not_indicated"
    if case.section_1a_notice_statement is Answer.NO:
        return "preconditions_not_indicated"
    if case.section_1a_notice_statement is Answer.UNKNOWN:
        return "insufficient_information"
    return "potential_only_pending_no_claim_and_notice_expiry"


def severance(case: CaseInput) -> dict[str, Any] | None:
    if (
        case.employment_start_date is None
        or case.employment_end_date is None
        or case.gross_monthly_pay is None
    ):
        return None
    completed = completed_service_years(
        case.employment_start_date, case.employment_end_date
    )
    rounded = rounded_section_1a_years(
        case.employment_start_date, case.employment_end_date
    )
    scenarios = {
        str(factor): money(case.gross_monthly_pay * factor * rounded)
        for factor in REFERENCE_FACTORS
    }
    offer_factor = None
    differences = None
    if case.offer_amount is not None and rounded > 0:
        offer_factor = str(
            (case.offer_amount / case.gross_monthly_pay / Decimal(rounded)).quantize(
                Decimal("0.001"), rounding=ROUND_HALF_UP
            )
        )
        differences = {
            str(factor): money(case.offer_amount - case.gross_monthly_pay * factor * rounded)
            for factor in REFERENCE_FACTORS
        }
    return {
        "completed_service_years": completed,
        "section_1a_rounded_service_years": rounded,
        "gross_monthly_pay": money(case.gross_monthly_pay),
        "comparison_scenarios": scenarios,
        "offer_amount": money(case.offer_amount) if case.offer_amount is not None else None,
        "offer_factor": offer_factor,
        "offer_minus_scenarios": differences,
        "section_1a_status": section_1a_status(case),
        "warning": (
            "Comparison scenarios are not guaranteed entitlements, and the supplied "
            "monthly pay may not equal the complete statutory monthly-earnings basis."
        ),
    }


def build_result(case: CaseInput) -> dict[str, Any]:
    warnings = [
        "Confirm all court deadlines with the competent labor court or qualified counsel.",
        "Review contractual and collective notice rules before relying on the BGB baseline.",
        "Do not use this output to predict tax or unemployment-benefit treatment.",
    ]
    if case.matter_stage is MatterStage.ALREADY_SIGNED:
        warnings.append("A signed document requires prompt individual review.")
    return {
        "source_as_of": SOURCE_AS_OF,
        "assessment_date": case.assessment_date.isoformat(),
        "filing_deadline": filing_deadline(case),
        "jobseeker_registration": jobseeker_deadline(case),
        "severance": severance(case),
        "notice_period_baseline": notice_period_baseline(case),
        "warnings": warnings,
    }


def load_input(path_value: str) -> Any:
    if path_value == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path_value).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate German dismissal and severance indicators from typed JSON."
    )
    parser.add_argument("input", help="Input JSON path, or - for standard input")
    arguments = parser.parse_args()
    try:
        case = parse_case(load_input(arguments.input))
        print(json.dumps(build_result(case), ensure_ascii=False, indent=2, sort_keys=True))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
