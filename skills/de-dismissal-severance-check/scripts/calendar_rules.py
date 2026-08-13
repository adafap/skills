"""Provide deterministic calendar helpers for the case calculator."""

from __future__ import annotations

import calendar
from datetime import date, timedelta


def add_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 + months
    year, month_zero = divmod(month_index, 12)
    month = month_zero + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def add_years(value: date, years: int) -> date:
    return add_months(value, years * 12)


def completed_service_years(start: date, end: date) -> int:
    years = end.year - start.year
    if add_years(start, years) > end:
        years -= 1
    return max(years, 0)


def rounded_section_1a_years(start: date, end: date) -> int:
    years = completed_service_years(start, end)
    anniversary = add_years(start, years)
    # 六个月整不进位，只有超过六个月才进位。
    return years + 1 if end > add_months(anniversary, 6) else years


def adjusted_workday(value: date, holidays: frozenset[date]) -> date:
    adjusted = value
    while adjusted.weekday() >= 5 or adjusted in holidays:
        adjusted += timedelta(days=1)
    return adjusted


def urgency(days_remaining: int) -> str:
    if days_remaining < 0:
        return "nominal_deadline_passed"
    if days_remaining <= 3:
        return "critical"
    if days_remaining <= 7:
        return "urgent"
    return "active"


def probation_notice_end(receipt: date) -> date:
    return receipt + timedelta(weeks=2)


def month_end_notice_end(receipt: date, months: int) -> date:
    period_end = add_months(receipt, months)
    last_day = calendar.monthrange(period_end.year, period_end.month)[1]
    return date(period_end.year, period_end.month, last_day)


def general_notice_end(receipt: date) -> date:
    period_end = receipt + timedelta(weeks=4)
    month_end = date(
        period_end.year,
        period_end.month,
        calendar.monthrange(period_end.year, period_end.month)[1],
    )
    if period_end.day <= 15:
        return date(period_end.year, period_end.month, 15)
    return month_end
