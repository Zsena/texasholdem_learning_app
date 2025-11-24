# Texas Hold’em WebApp – DUE UNIVERSITY

A simple educational Texas Hold’em application built with **Python**, **SQLite**, and a minimal **web interface**.  
The goal of this project is to demonstrate **database usage**, **object-oriented design**, **UML modeling**, and **basic hand evaluation logic**.

---

## 📘 1. UML Class Diagram
```
+-----------------------+
| ZTDeck |
+-----------------------+
| cards: list |
+-----------------------+
| _zt_generate_deck() |
| shuffle() |
| draw_card() |
+-----------------------+

+-----------------------+
| ZTHandEvaluator |
+-----------------------+
| - ranks |
| - suits |
+-----------------------+
| evaluate_hand() |
| detect_pairs() |
| detect_flush() |
| detect_straight() |
+-----------------------+

+-----------------------+
| Game |
+-----------------------+
| id |
| player_cards |
| flop |
| turn |
| river |
| best_hand |
| hand_rank |
| created_at |
| evaluation_log |
+-----------------------+
```

### **Diagram Explanation**

- **ZTDeck** → Generates a 52-card deck and handles drawing cards  
- **ZTHandEvaluator** → Evaluates the player’s best Texas Hold’em hand  
- **Game** → Stores the round result in the SQLite database  

---

## 2. Database Design

The application stores every played game round in a single table:

### **Table: Game**

| Field            | Type       | Description                               |
|------------------|------------|-------------------------------------------|
| `id`             | PK         | Auto-incremented ID                       |
| `player_cards`   | Text       | Example: `"Ah, Ks"`                       |
| `flop`           | Text       | Example: `"2c, 7h, 9d"`                   |
| `turn`           | Text       | Example: `"Jh"`                            |
| `river`          | Text       | Example: `"5s"`                            |
| `best_hand`      | Text       | Example: `"Pair of Aces"`                 |
| `hand_rank`      | Integer    | Numerical strength of the hand            |
| `created_at`     | DateTime   | Automatic timestamp                       |
| `evaluation_log` | Text       | Optional calculation log                  |

---

## 🎮 3. USE CASE Diagram
```
    +-----------------------+
    |        User           |
    +-----------------------+
             / \
              |
      ----------------
      |   Use Cases  |
      ----------------
        | Start Game
        | Deal Cards
        | Show Flop
        | Show Turn
        | Show River
        | Evaluate Hand
        | Save Game
        | View History
```

### **Use-Case Logic**

- **Start Game** → Creates a new deck and deals two cards  
- **Deal Cards** → Flop → Turn → River  
- **Evaluate Hand** → Determines the best 5-card hand  
- **Save Game** → Writes the record to the DB  
- **View History** → Loads game history from SQLite  

---

## 🚀 4. Installation & Running

### 1. Create virtual environment

```
python -m venv venv 
```
### 2. Activate:

- Windows:

```venv\Scripts\activate```


- Linux/Mac:

```source venv/bin/activate```

### 3. Install dependencies

SQLite comes built-in with Python.

### 4. Run the app
```python manage.py runserver```

Starting development server at ```http://127.0.0.1:8000/```

### 5. Superuser 

```python manage.py createsuperuser```

or 

```python manage.py changepassword admin```


admin: 

 /admin

 - user: zsena
 - password: 123456


### 5. migrations

- ```python manage.py makemigrations```
- ```python manage.py migrate```


