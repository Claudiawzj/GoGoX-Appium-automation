"""Calculate a future Hong Kong pickup each run; format observed English picker labels."""

from dataclasses import dataclass
from datetime import datetime, timedelta
import re
from zoneinfo import ZoneInfo

HONG_KONG = ZoneInfo("Asia/Hong_Kong")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def normalize_label(text):
    """iOS uses a narrow nonbreaking space before am/pm; keep comparisons semantic."""
    return " ".join((text or "").split())


@dataclass(frozen=True)
class PickupPlan:
    scheduled_at: datetime
    date_label: str
    time_label: str

    @property
    def summary_label(self):
        return f"{self.date_label}, {self.time_label}"


def build_pickup_plan(days_ahead, time_24h, now=None):
    if type(days_ahead) is not int or days_ahead < 1:
        raise ValueError("Pickup days_ahead must be a positive integer.")
    if not isinstance(time_24h, str) or not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", time_24h):
        raise ValueError("Pickup time_24h must use HH:MM, for example 14:00.")
    hour, minute = map(int, time_24h.split(":"))
    if minute % 10:
        raise ValueError("The observed pickup picker requires a ten-minute time slot.")
    current = now if now is not None else datetime.now(HONG_KONG)
    if current.tzinfo is None:
        raise ValueError("Pickup calculation requires a timezone-aware current time.")
    current = current.astimezone(HONG_KONG)
    target = (current + timedelta(days=days_ahead)).replace(
        hour=hour, minute=minute, second=0, microsecond=0)
    prefix = "Tomorrow" if days_ahead == 1 else WEEKDAYS[target.weekday()]
    date_label = f"{prefix} {target.day} {MONTHS[target.month - 1]}"
    time_label = f"{hour % 12 or 12}:{minute:02d} {'am' if hour < 12 else 'pm'} HKT"
    return PickupPlan(target, date_label, time_label)
