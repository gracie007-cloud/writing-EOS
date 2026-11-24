import json
import os
import time
import urllib.request
from pathlib import Path

JSON_PATH = Path(__file__).resolve().parent.parent / "data" / "notion_database_entries.json"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")


def main():
    if not NOTION_TOKEN or not DATABASE_ID:
        raise SystemExit("Set NOTION_TOKEN and NOTION_DATABASE_ID environment variables first.")

    entries = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    for idx, entry in enumerate(entries, start=1):
        payload = json.dumps({"parent": {"database_id": DATABASE_ID}, **entry}).encode("utf-8")
        req = urllib.request.Request("https://api.notion.com/v1/pages", data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            print(f"[{idx}/{len(entries)}] Imported (HTTP {resp.status})")
        time.sleep(0.35)


if __name__ == "__main__":
    main()
