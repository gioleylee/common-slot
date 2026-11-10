"""Find shared availability from lists of timestamp intervals."""

import argparse
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamps must be strings")
    moment = datetime.fromisoformat(value)
    if moment.utcoffset() is None:
        raise ValueError(f"{value!r}: include a UTC offset")
    return moment.astimezone(UTC)


def merge(windows):
    if not isinstance(windows, list):
        raise ValueError("each participant's availability must be a list")
    intervals = []
    for pair in windows:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("each interval must contain a start and an end")
        start, end = map(timestamp, pair)
        if start >= end:
            raise ValueError("an interval must end after it starts")
        intervals.append((start, end))
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            previous_start, previous_end = merged[-1]
            merged[-1] = previous_start, max(previous_end, end)
        else:
            merged.append((start, end))
    return merged


def intersect(left, right):
    shared = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_start, left_end = left[i]
        right_start, right_end = right[j]
        start, end = max(left_start, right_start), min(left_end, right_end)
        if start < end:
            shared.append((start, end))
        if left_end <= right_end:
            i += 1
        if right_end <= left_end:
            j += 1
    return shared


def find_slots(participants, minutes):
    if not isinstance(participants, dict) or not participants:
        raise ValueError("expected a nonempty object mapping participants to intervals")
    if minutes <= 0:
        raise ValueError("minimum duration must be positive")
    duration = timedelta(minutes=minutes)
    calendars = iter(participants.values())
    shared = merge(next(calendars))
    for calendar in calendars:
        shared = intersect(shared, merge(calendar))
    return [
        {"start": start.isoformat(), "end": end.isoformat()}
        for start, end in shared
        if end - start >= duration
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("availability", type=Path)
    parser.add_argument("--minutes", type=int, required=True)
    args = parser.parse_args()
    try:
        with args.availability.open(encoding="utf-8-sig") as stream:
            slots = find_slots(json.load(stream), args.minutes)
    except (OSError, ValueError, OverflowError) as error:
        parser.error(str(error))
    print(json.dumps(slots, indent=2))


if __name__ == "__main__":
    main()
