import random
from collections import Counter
from itertools import combinations

class ZTDeck:

    def __init__(self):
        self.cards = self._zt_generate_deck()
        random.shuffle(self.cards)

    def _zt_generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        suits = ["♥", "♦", "♣", "♠"]
        return [r + s for r in ranks for s in suits]

    def zt_draw(self, n=1):
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

    def zt_deal_preflop(self):
        return self.zt_draw(2)

    def zt_deal_flop(self):
        return self.zt_draw(3)

    def zt_deal_turn(self):
        return self.zt_draw(1)

    def zt_deal_river(self):
        return self.zt_draw(1)


class ZTHandEvaluator:
    
    RANK_ORDER = "23456789TJQKA"

    def __init__(self, cards7):
        self.cards7 = cards7

    def _rank_val(self, card):
        return ZTHandEvaluator.RANK_ORDER.index(card[0])

    def _is_straight(self, five):
        ranks = sorted(set([c[0] for c in five]),
                       key=lambda r: self._rank_val(r))

        if set(["A", "2", "3", "4", "5"]).issubset(ranks):
            return True, 3 

        vals = [self._rank_val(r) for r in ranks]
        return (vals == list(range(vals[0], vals[0] + 5)),
                vals[-1])

    def _hand_rank(self, five):
        ranks = [c[0] for c in five]
        suits = [c[1] for c in five]
        counts = Counter(ranks)

        is_flush = len(set(suits)) == 1
        is_straight, straight_hi = self._is_straight(five)

        ranks_sorted = sorted(five,
                              key=lambda c: self._rank_val(c[0]))

        if is_flush and is_straight and ranks_sorted[-1][0] == "A":
            return (10_000, "Royal Flush")

        if is_flush and is_straight:
            return (9_000 + straight_hi, "Straight Flush")

        if 4 in counts.values():
            quad = [r for r in counts if counts[r] == 4][0]
            kicker = max([r for r in counts if r != quad],
                         key=lambda x: self._rank_val(x))
            score = 8_000 + self._rank_val(quad) * 20 + self._rank_val(kicker)
            return (score, f"Four of a Kind ({quad})")

        trips = sorted([r for r in counts if counts[r] == 3],
                       key=lambda x: self._rank_val(x))
        pairs = sorted([r for r in counts if counts[r] == 2],
                       key=lambda x: self._rank_val(x))

        if trips and pairs:
            best_trip = trips[-1]
            best_pair = pairs[-1]
            score = 7_000 + self._rank_val(best_trip) * 20 + self._rank_val(best_pair)
            return (score, f"Full House ({best_trip}-{best_pair})")

        if is_flush:
            hi_cards = sorted([self._rank_val(r) for r in ranks], reverse=True)
            score = 6_000 + hi_cards[0]
            return (score, "Flush")

        if is_straight:
            return (5_000 + straight_hi, "Straight")

        if trips:
            trip = trips[-1]
            score = 4_000 + self._rank_val(trip)
            return (score, f"Three of a Kind ({trip})")

        if len(pairs) == 2:
            highp, lowp = pairs[-1], pairs[-2]
            score = 3_000 + self._rank_val(highp) * 20 + self._rank_val(lowp)
            return (score, f"Two Pair ({highp} és {lowp})")

        if len(pairs) == 1:
            score = 2_000 + self._rank_val(pairs[0])
            return (score, f"One Pair ({pairs[0]})")

        high = max(five, key=lambda c: self._rank_val(c[0]))
        return (1_000 + self._rank_val(high[0]), f"High Card ({high})")

    def evaluate(self):
        best_score = -1
        best_desc = ""
        best_five = None

        for five in combinations(self.cards7, 5):
            score, desc = self._hand_rank(list(five))
            if score > best_score:
                best_score = score
                best_desc = desc
                best_five = list(five)

        return best_score, best_desc, best_five
