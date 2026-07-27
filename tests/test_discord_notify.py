import unittest
from datetime import datetime, timedelta, timezone

from discord_notify.notify import format_source_notification


class FormatSourceNotificationTest(unittest.TestCase):
    def test_formats_single_message(self):
        now = datetime(2026, 7, 22, 10, 1, 9, tzinfo=timezone(timedelta(hours=8)))

        result = format_source_notification("1point3acres", "Check-in successful", now=now)

        self.assertEqual(
            result,
            "**1POINT3ACRES** · 2026/07/22 10:01:09\nCheck-in successful",
        )

    def test_combines_multiple_messages(self):
        now = datetime(2026, 7, 22, 10, 1, 9, tzinfo=timezone(timedelta(hours=8)))

        result = format_source_notification(
            "1point3acres",
            ["Check-in successful", "Question answered"],
            now=now,
        )

        self.assertEqual(
            result,
            "**1POINT3ACRES** · 2026/07/22 10:01:09\n"
            "Check-in successful\nQuestion answered",
        )

    def test_empty_messages_fallback(self):
        now = datetime(2026, 7, 22, 10, 1, 9, tzinfo=timezone(timedelta(hours=8)))

        result = format_source_notification("1point3acres", [], now=now)

        self.assertEqual(
            result,
            "**1POINT3ACRES** · 2026/07/22 10:01:09\nNo result was reported.",
        )


if __name__ == "__main__":
    unittest.main()
