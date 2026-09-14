# reversedraw

A small Django app for running a live reverse-raffle "Loser Board": type in
each ticket number as it's called, and it appears on a big number grid you
can project. Type it on your laptop and hit fullscreen for the projector, or
open the same URL on a second screen — either way it stays in sync.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`. No login is required — anyone with the
URL can use it, so keep it off the public internet if that's a concern.

## Usage

1. Create an event (a name, and optionally a "prize interval" — every Nth
   call, starting with the first, auto-highlights green as a bonus winner).
2. Open the event's board (`/<slug>/`). Type each ticket number and hit
   **ADD** (or Enter) as it's called; **UNDO** removes the most recent entry
   for typos, **CLEAR** wipes the board, and clicking any tile toggles its
   green "winner" highlight manually.
3. Hit **FULLSCREEN** to hide the controls and just show the grid for the
   projector — or open the same page on a second device, which polls for
   updates every few seconds so it always mirrors the current state.
