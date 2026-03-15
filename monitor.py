from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from leipz_pars import FlatListing, LeipzigParser
from telegram import TelegramNotifier


INTERVAL_SECONDS = 600
STATE_FILE = Path("seen_flats.json")


def load_state(path: Path) -> set[str]:
    if not path.exists():
        return set()

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        logging.warning("State-Datei ist ungueltig, starte mit leerem Zustand.")
        return set()

    if not isinstance(raw, list):
        logging.warning("State-Datei hat falsches Format, starte mit leerem Zustand.")
        return set()

    return {str(item) for item in raw if isinstance(item, str)}


def save_state(path: Path, seen_urls: set[str]) -> None:
    data = sorted(seen_urls)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")


def format_new_flats_message(new_flats: list[FlatListing]) -> str:
    header = "Neue Sozialwohnung gefunden:" if len(new_flats) == 1 else "Neue Sozialwohnungen gefunden:"
    lines = [header]
    for flat in new_flats:
        lines.append(f"- {flat.title}")
        lines.append(flat.url)
    return "\n".join(lines)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    parser = LeipzigParser()
    notifier = TelegramNotifier()
    seen_urls = load_state(STATE_FILE)
    initialize_only = not STATE_FILE.exists()

    logging.info("Monitor gestartet, Intervall: %s Sekunden.", INTERVAL_SECONDS)

    while True:
        try:
            listings = parser.fetch_listings()
            current_urls = {listing.url for listing in listings}

            if initialize_only:
                seen_urls = current_urls
                save_state(STATE_FILE, seen_urls)
                initialize_only = False
                logging.info("Initialer Stand gespeichert: %s Eintraege.", len(seen_urls))
            else:
                new_flats = [listing for listing in listings if listing.url not in seen_urls]

                if new_flats:
                    notifier.send_message(format_new_flats_message(new_flats))
                    seen_urls.update(flat.url for flat in new_flats)
                    save_state(STATE_FILE, seen_urls)
                    logging.info("Neue Wohnungen gemeldet: %s", len(new_flats))
                else:
                    logging.info("Keine neuen Wohnungen gefunden.")
        except Exception:
            logging.exception("Fehler beim Monitoring-Durchlauf.")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
