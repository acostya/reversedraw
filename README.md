# reversedraw

A small Django app for running a live reverse-raffle "Loser Board": an operator
types in each ticket number as it's called out, and a public, auto-refreshing
board page displays the numbers in order for projection on a screen.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/` and log in.

## Usage

1. Create an event (gives it a name and a URL slug).
2. Open its **call panel** (`/<slug>/admin/`, login required) and type each
   ticket number as it's called — it's appended to that event's board.
   "Undo last" removes the most recently entered number in case of a typo.
3. Open the **loser board** (`/<slug>/loser-board/`) on the projector — it's a
   public page that polls for updates every couple of seconds, so it stays in
   sync with the call panel automatically.
