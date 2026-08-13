from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).parents[2]
    / "skills"
    / "de-dismissal-severance-check"
    / "scripts"
    / "calculate_case.py"
)
sys.path.insert(0, str(SCRIPT_PATH.parent))
SPEC = importlib.util.spec_from_file_location("calculate_case", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load calculate_case.py")
CALCULATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CALCULATOR
SPEC.loader.exec_module(CALCULATOR)


def valid_input() -> dict[str, object]:
    return {
        "assessment_date": "2026-07-31",
        "matter_stage": "dismissal_received",
        "document_type": "dismissal_notice",
        "dismissal_reason": "operational",
        "dismissal_mode": "ordinary",
        "dismissal_received_date": "2026-07-13",
        "employment_start_date": "2018-01-01",
        "employment_end_date": "2026-10-31",
        "end_date_known_date": "2026-07-13",
        "gross_monthly_pay": "5000.00",
        "offer_amount": "30000.00",
        "section_1a_notice_statement": "yes",
        "probation_clause_active": "no",
        "public_holidays_verified": "yes",
        "public_holiday_dates": [],
    }


class CalendarTests(unittest.TestCase):
    def test_add_months_clamps_to_month_end(self) -> None:
        self.assertEqual(
            CALCULATOR.add_months(date(2026, 1, 31), 1), date(2026, 2, 28)
        )

    def test_section_1a_rounds_only_more_than_six_months(self) -> None:
        start = date(2018, 1, 1)
        self.assertEqual(
            CALCULATOR.rounded_section_1a_years(start, date(2026, 7, 1)), 8
        )
        self.assertEqual(
            CALCULATOR.rounded_section_1a_years(start, date(2026, 7, 2)), 9
        )

    def test_weekend_and_supplied_holiday_adjustment(self) -> None:
        data = valid_input()
        data["dismissal_received_date"] = "2026-07-18"
        data["public_holiday_dates"] = ["2026-08-10"]
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertEqual(result["filing_deadline"]["nominal_date"], "2026-08-08")
        self.assertEqual(
            result["filing_deadline"]["calendar_adjusted_date"], "2026-08-11"
        )


class DeadlineTests(unittest.TestCase):
    def test_three_week_deadline_and_urgency(self) -> None:
        result = CALCULATOR.build_result(CALCULATOR.parse_case(valid_input()))
        deadline = result["filing_deadline"]
        self.assertEqual(deadline["nominal_date"], "2026-08-03")
        self.assertEqual(deadline["days_remaining"], 3)
        self.assertEqual(deadline["urgency"], "critical")

    def test_passed_nominal_deadline_is_not_treated_as_safe(self) -> None:
        data = valid_input()
        data["assessment_date"] = "2026-08-04"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertEqual(
            result["filing_deadline"]["urgency"], "nominal_deadline_passed"
        )

    def test_termination_agreement_does_not_create_dismissal_deadline(self) -> None:
        data = valid_input()
        data["document_type"] = "termination_agreement"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertIsNone(result["filing_deadline"])

    def test_jobseeker_deadline_uses_three_day_rule(self) -> None:
        data = valid_input()
        data["employment_end_date"] = "2026-09-30"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        registration = result["jobseeker_registration"]
        self.assertEqual(registration["indicative_due_date"], "2026-07-16")
        self.assertEqual(registration["basis"], "three_days_after_knowledge")

    def test_jobseeker_deadline_uses_three_month_mark(self) -> None:
        data = valid_input()
        data["employment_end_date"] = "2026-12-31"
        data["end_date_known_date"] = "2026-07-01"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertEqual(
            result["jobseeker_registration"]["indicative_due_date"], "2026-09-30"
        )


class SeveranceTests(unittest.TestCase):
    def test_scenarios_offer_factor_and_section_1a_status(self) -> None:
        result = CALCULATOR.build_result(CALCULATOR.parse_case(valid_input()))
        severance = result["severance"]
        self.assertEqual(severance["section_1a_rounded_service_years"], 9)
        self.assertEqual(severance["comparison_scenarios"]["0.5"], "22500.00")
        self.assertEqual(severance["comparison_scenarios"]["0.75"], "33750.00")
        self.assertEqual(severance["offer_factor"], "0.667")
        self.assertEqual(
            severance["section_1a_status"],
            "potential_only_pending_no_claim_and_notice_expiry",
        )

    def test_non_operational_reason_does_not_indicate_section_1a(self) -> None:
        data = valid_input()
        data["dismissal_reason"] = "conduct"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertEqual(
            result["severance"]["section_1a_status"],
            "preconditions_not_indicated",
        )

    def test_offer_requires_positive_salary(self) -> None:
        data = valid_input()
        data["gross_monthly_pay"] = "0"
        with self.assertRaises(ValueError):
            CALCULATOR.parse_case(data)


class NoticePeriodTests(unittest.TestCase):
    def test_general_notice_selects_next_fifteenth(self) -> None:
        data = valid_input()
        data["dismissal_received_date"] = "2026-01-04"
        data["employment_start_date"] = "2025-06-01"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertEqual(
            result["notice_period_baseline"]["earliest_baseline_end_date"],
            "2026-02-15",
        )

    def test_probation_notice_uses_two_week_baseline(self) -> None:
        data = valid_input()
        data["dismissal_received_date"] = "2026-01-31"
        data["probation_clause_active"] = "yes"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        notice = result["notice_period_baseline"]
        self.assertEqual(notice["length"], 2)
        self.assertEqual(notice["earliest_baseline_end_date"], "2026-02-14")

    def test_ten_year_employer_baseline(self) -> None:
        data = valid_input()
        data["employment_start_date"] = "2015-01-01"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        notice = result["notice_period_baseline"]
        self.assertEqual(notice["length"], 4)
        self.assertEqual(notice["unit"], "months")
        self.assertEqual(notice["termination_point"], "calendar_month_end")
        self.assertEqual(notice["earliest_baseline_end_date"], "2026-11-30")
        self.assertTrue(notice["proposed_end_precedes_baseline"])

    def test_extraordinary_dismissal_has_no_ordinary_baseline(self) -> None:
        data = valid_input()
        data["dismissal_mode"] = "extraordinary"
        result = CALCULATOR.build_result(CALCULATOR.parse_case(data))
        self.assertFalse(result["notice_period_baseline"]["available"])


class ValidationTests(unittest.TestCase):
    def test_invalid_enum_is_rejected(self) -> None:
        data = valid_input()
        data["matter_stage"] = "dismissal"
        with self.assertRaises(ValueError):
            CALCULATOR.parse_case(data)

    def test_extraordinary_is_a_mode_not_a_reason(self) -> None:
        data = valid_input()
        data["dismissal_reason"] = "extraordinary"
        with self.assertRaises(ValueError):
            CALCULATOR.parse_case(data)

    def test_end_before_start_is_rejected(self) -> None:
        data = valid_input()
        data["employment_end_date"] = "2017-12-31"
        with self.assertRaises(ValueError):
            CALCULATOR.parse_case(data)

    def test_decimal_output_is_stable(self) -> None:
        case = CALCULATOR.parse_case(valid_input())
        self.assertEqual(case.gross_monthly_pay, Decimal("5000.00"))


if __name__ == "__main__":
    unittest.main()
