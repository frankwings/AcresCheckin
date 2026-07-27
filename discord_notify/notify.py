"""Discord notification connector.

Sends check-in results to a Discord channel via an incoming webhook.
Create a webhook: Discord channel -> Settings -> Integrations -> Webhooks -> New Webhook.
Set the env var DISCORD_WEBHOOK_URL to the webhook URL.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '').strip()

BEIJING_TIMEZONE = timezone(timedelta(hours=8))


def format_source_notification(source, messages, now=None):
    """Format one compact Discord notification for a platform run."""
    if isinstance(messages, str):
        messages = [messages]

    body = "\n".join(
        str(message).strip()
        for message in messages
        if message is not None and str(message).strip()
    )
    if not body:
        body = "No result was reported."

    timestamp = now or datetime.now(BEIJING_TIMEZONE)
    return f"**{source.upper()}** · {timestamp.strftime('%Y/%m/%d %H:%M:%S')}\n{body}"


def send_source_notification(source, messages):
    """Send exactly one formatted notification for a platform run."""
    send_discord_notification(format_source_notification(source, messages))


def send_discord_notification(message):
    """Send a message to Discord via webhook.

    Args:
        message: The message to send (supports Discord markdown).
    """
    if not DISCORD_WEBHOOK_URL:
        print("Discord configuration is incomplete, cannot send notification", flush=True)
        sys.exit(1)

    payload = json.dumps({"content": message[:2000]}).encode("utf-8")
    request = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "AcresCheckin/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            # Discord webhook returns 204 No Content on success
            if response.status in (200, 204):
                print("Notification sent successfully", flush=True)
            else:
                body = response.read().decode("utf-8", errors="replace")
                raise Exception(f"Notification sent failed: {response.status} - {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Notification sending process error: {e.code} - {body}", flush=True)
        sys.exit(1)
    except Exception as e:
        print(f"Notification sending process error: {str(e)}", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    send_source_notification("DISCORD", "Action test")
