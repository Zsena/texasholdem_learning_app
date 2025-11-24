# Texas Hold'em Poker Learning Web App - DUE University

An educational Texas Hold'em poker web application built with **Django** and **SQLite**. The app lets you play a simple heads-up hand against a computer opponent, shows the best hand evaluation, and stores each result so you can review past hands. The UI is in Hungarian.

---

## Features
- Step-by-step play flow: preflop -> flop -> turn -> river -> showdown.
- Automated 7-card hand evaluation for both player and opponent with named hand descriptions.
- Game history saved to SQLite; browse previous hands.
- Rules page for quick reference.
- Django admin available for inspecting stored games.

---

## Stack
- Python 3.14
- Django (installed via `pip`)
- SQLite (default Django database)
- Tailwind CDN for styling in templates

---

## UML (core classes)
```
+-----------------------------+
|           ZTDeck            |
+-----------------------------+
| cards: list                 |
+-----------------------------+
| _zt_generate_deck()         |
| zt_draw(n)                  |
| zt_deal_preflop()           |
| zt_deal_flop()              |
| zt_deal_turn()              |
| zt_deal_river()             |
+-----------------------------+

+-----------------------------+
|       ZTHandEvaluator       |
+-----------------------------+
| cards7: list                |
| RANK_ORDER                  |
+-----------------------------+
| _rank_val(card)             |
| _is_straight(five)          |
| _hand_rank(five)            |
| evaluate()                  |
+-----------------------------+

+-----------------------------+
|            Game             |
+-----------------------------+
| id                          |
| player_cards                |
| opponent_cards              |
| flop                        |
| turn                        |
| river                       |
| best_hand                   |
| outcome                     |
| hand_rank                   |
| evaluation_log              |
| created_at                  |
+-----------------------------+
```

---

## Use Case Diagram
```
    +-------+
    | User  |
    +---+---+
        |
        v
 +--------------+
 | Start Game   |
 +--------------+
        |
        v
 +--------------+    +---------------+
 | Deal Cards   +--> | Evaluate Hand |
 +--------------+    +---------------+
        |
        v
 +--------------+
 | Save Game    |
 +--------------+
        |
        v
 +--------------+
 | View History |
 +--------------+
```

### Use-Case Logic
- **Start Game**: create a new deck and deal two hole cards to each side.
- **Deal Cards**: reveal community cards street by street (flop, turn, river).
- **Evaluate Hand**: compute the best 5-card hand for player and opponent from 7 cards.
- **Save Game**: persist the hand, outcome, and metadata to SQLite.
- **View History**: list stored games from the `Game` table.

---

## Database Design

### Table: Game (SQLite via Django ORM)
| Field | Type | Description |
| --- | --- | --- |
| `id` | PK (auto) | Primary key |
| `player_cards` | CharField(50) | Player hole cards (e.g., `Ah,Ks`) |
| `opponent_cards` | CharField(50) | Opponent hole cards |
| `flop` | CharField(50) | Flop cards |
| `turn` | CharField(10) | Turn card |
| `river` | CharField(10) | River card |
| `best_hand` | CharField(50) | Best hand description for the player |
| `hand_rank` | IntegerField | Numeric score for ranking |
| `outcome` | CharField(50) | Result text |
| `evaluation_log` | TextField | Optional notes |
| `created_at` | DateTime | Auto timestamp |

---

## Project Layout
- `manage.py` - Django entrypoint.
- `holdem/` - project settings and URL routing.
- `game/` - domain logic (`zt_poker.py`), views, models, and templates.
- `game/templates/` - pages for home, step-by-step play, rules, history, and results.
- `db.sqlite3` - local SQLite database (created after running migrations).

---

## Game Flow
1. Home (`/`) links to start a new hand.
2. `/game/play` initializes the session, deals player/opponent hole cards, and moves to `/game/step`.
3. `/game/step` advances through phases (preflop -> flop -> turn -> river). On showdown, both 7-card sets are evaluated and the result is stored in the `Game` table.
4. `/game/history` lists stored hands; `/game/rules` shows poker rules; `/admin` exposes Django admin (after creating a superuser).

---

## Setup & Run
1. Create a virtual environment  
   `python -m venv venv`
2. Activate it  
   - Windows: `venv\Scripts\activate`  
   - macOS/Linux: `source venv/bin/activate`
3. Install Django  
   `pip install django`
4. Migrations  
   - `python manage.py makemigrations`  
   - `python manage.py migrate`
5. Superuser  
   - Create: `python manage.py createsuperuser`  
   - Or change password: `python manage.py changepassword admin`
   - Admin UI: `/admin` (example credentials: user `zsena`, password `123456`)
6. Start the dev server  
   `python manage.py runserver`
7. Open `http://127.0.0.1:8000/` to use the app; visit `/admin` for admin access.

---

## Notes
- All game text is Hungarian. Adjust copy in `game/templates/` if you need English UI.
- Hand evaluation and dealing logic live in `game/zt_poker.py`.
- Game history persists to the local `db.sqlite3`; remove the file to clear data.
- *Licence - MIT*
- **Author: Tamás Zsanett - Q4PTDR**