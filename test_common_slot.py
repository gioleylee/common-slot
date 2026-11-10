from unittest import TestCase

from common_slot import find_slots


class CommonSlotTests(TestCase):
    def test_merges_adjacent_windows_and_normalizes_offsets(self):
        calendars = {
            "Taipei": [
                ["2026-11-10T17:00+08:00", "2026-11-10T17:30+08:00"],
                ["2026-11-10T16:30+08:00", "2026-11-10T17:00+08:00"],
            ],
            "Berlin": [["2026-11-10T09:45+01:00", "2026-11-10T10:15+01:00"]],
        }
        self.assertEqual(find_slots(calendars, 30), [{
            "start": "2026-11-10T08:45:00+00:00",
            "end": "2026-11-10T09:15:00+00:00",
        }])
        self.assertEqual(find_slots(calendars, 31), [])
        self.assertEqual(find_slots({**calendars, "Unavailable": []}, 30), [])

    def test_rejects_naive_timestamps(self):
        with self.assertRaisesRegex(ValueError, "UTC offset"):
            find_slots({"Local": [["2026-11-10T09:00", "2026-11-10T10:00"]]}, 30)
