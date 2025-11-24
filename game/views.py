from django.shortcuts import render, redirect
from .zt_poker import ZTDeck, ZTHandEvaluator
from .models import Game


def _pretty(cards):
    pretty = []
    for c in cards:
        rank = c[0]
        suit = c[1]
        is_red = suit in ["♥", "♦"]
        pretty.append({
            "raw": c,
            "text": f"{rank}{suit}",
            "is_red": is_red,
        })
    return pretty

def play(request):
    request.session.flush()

    deck = ZTDeck()

    request.session["deck"] = deck.cards
    request.session["player_cards"] = deck.zt_deal_preflop()
    request.session["opponent_cards"] = deck.zt_deal_preflop()

    request.session["flop"] = []
    request.session["turn"] = []
    request.session["river"] = []

    request.session["phase"] = "preflop"

    return redirect("step")

def step(request):
    phase = request.session.get("phase", "preflop")

    deck = ZTDeck()
    deck.cards = request.session["deck"]

    player = request.session["player_cards"]
    opponent = request.session["opponent_cards"]

    flop = request.session["flop"]
    turn = request.session["turn"]
    river = request.session["river"]

    if phase == "showdown":

        full_player = player + flop + turn + river
        full_opponent = opponent + flop + turn + river

        p_score, p_desc, p_best = ZTHandEvaluator(full_player).evaluate()
        o_score, o_desc, o_best = ZTHandEvaluator(full_opponent).evaluate()

        player_best = list(p_best)
        opponent_best = list(o_best)

        if p_score > o_score:
            outcome = "Nyertél! 🎉"
        elif o_score > p_score:
            outcome = "A gép nyert 😔"
        else:
            outcome = "Döntetlen 🤝"

        Game.objects.create(
            player_cards=",".join(player),
            opponent_cards=",".join(opponent),
            flop=",".join(flop),
            turn=",".join(turn),
            river=",".join(river),
            best_hand=p_desc,
            hand_rank=p_score,
            outcome=outcome,
        )

        return render(request, "game/result.html", {
            "player_cards": _pretty(player),
            "opponent_cards": _pretty(opponent),
            "table_cards": _pretty(flop + turn + river),

            "player_desc": p_desc,
            "opponent_desc": o_desc,

            "player_best": player_best,
            "opponent_best": opponent_best,

            "winner": ("player" if p_score > o_score else
                       "opponent" if o_score > p_score else "tie"),

            "outcome": outcome,
        })

    if phase == "preflop":
        phase_title = "Preflop – kezdőlapok"
        request.session["phase"] = "flop"

    elif phase == "flop":
        flop = deck.zt_deal_flop()
        request.session["flop"] = flop
        request.session["deck"] = deck.cards
        phase_title = "Flop – három lap az asztalon"
        request.session["phase"] = "turn"

    elif phase == "turn":
        turn = deck.zt_deal_turn()
        request.session["turn"] = turn
        request.session["deck"] = deck.cards
        phase_title = "Turn – negyedik lap"
        request.session["phase"] = "river"

    elif phase == "river":
        river = deck.zt_deal_river()
        request.session["river"] = river
        request.session["deck"] = deck.cards
        phase_title = "River – ötödik lap"
        request.session["phase"] = "showdown"

    else:
        phase_title = "Preflop"
        request.session["phase"] = "flop"

    return render(request, "game/step.html", {
        "phase_title": phase_title,
        "player_cards": _pretty(player),
        "opponent_back": ["X", "X"],
        "table_cards": _pretty(flop + turn + river),
    })


def history(request):
    games = Game.objects.all().order_by("-created_at")
    return render(request, "game/history.html", {"games": games})


def home(request):
    return render(request, "game/home.html")


def rules(request):
    return render(request, "game/rules.html")
