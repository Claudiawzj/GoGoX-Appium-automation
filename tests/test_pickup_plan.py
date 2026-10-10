"""Calendar/timezone cases that must stay correct when the demo runs later."""

from datetime import datetime, timezone

import pytest

from utils.pickup_plan import HONG_KONG, build_pickup_plan, normalize_label


@pytest.mark.parametrize("now, expected", [
    (datetime(2026, 10, 10, 20, 30, tzinfo=HONG_KONG), "Mon 12 Oct"),
    (datetime(2026, 12, 31, 23, 50, tzinfo=HONG_KONG), "Sat 2 Jan"),
    (datetime(2028, 2, 28, 20, 0, tzinfo=HONG_KONG), "Wed 1 Mar"),
    (datetime(2026, 10, 10, 20, 0, tzinfo=timezone.utc), "Tue 13 Oct"),
])
def test_future_pickup_calendar_and_timezone(now, expected):
    plan = build_pickup_plan(2, "14:00", now)
    assert plan.scheduled_at > now
    assert plan.date_label == expected
    assert plan.time_label == "2:00 pm HKT"
    assert plan.summary_label == f"{expected}, 2:00 pm HKT"
    assert plan.scheduled_at.hour == 14 and plan.scheduled_at.minute == 0


@pytest.mark.parametrize("days, slot", [(0, "14:00"), (True, "14:00"),
                                         (2, "24:00"), (2, "14:05"), (2, "2:00")])
def test_invalid_pickup_configuration_is_rejected(days, slot):
    with pytest.raises(ValueError):
        build_pickup_plan(days, slot)


def test_ios_time_spacing_is_normalized():
    assert normalize_label("2:00\u202fpm HKT") == "2:00 pm HKT"
