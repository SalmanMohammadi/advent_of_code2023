from typing import List

CARD_VALUES = {
    "A": 13,
    "K" : 12,
    "Q": 11,
    "J": 0,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

class Hand:
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.card_strengths = [CARD_VALUES[card] for card in self.cards]
        d = dict.fromkeys(self.cards, 0)
        for card in self.cards:
            d[card] += 1
        self.hand_value = self.get_hand_type(list(d.values()))

        if "J" in self.cards and len(d.keys()) > 1:
            wild_value = d.pop("J")
            max_key = max(d, key=d.get)
            d[max_key] += wild_value
        
        self.hand_value_j_wild = self.get_hand_type(list(d.values()))
        self.rank = -1
    
    def get_hand_type(self, hand_counts: List[int]) -> int:
        hand_set = set(hand_counts)
        if hand_set == {5}:
            return 5
        elif hand_set == {4, 1}:
            return 4
        elif hand_set == {3, 2}:
            return 3
        elif hand_set == {3, 1}:
            return 2
        elif hand_set == {2, 1}:
            if hand_counts.count(2) == 2:
                return 1
            else:
                return 0
        else:
            return -1

    def __repr__(self) -> str:
        return f"{self.cards}: value: {self.hand_value}, wild_value: {self.hand_value_j_wild}, bid {self.bid} card strengths {self.card_strengths}, rank: {self.rank}\n"

if __name__ == "__main__":
    with open("input") as f:
        inpt = f.read().split('\n')
        hands, bids = zip(*[x.split(" ") for x in inpt])
        bids = list(map(int, bids))
        hands = [Hand(cards, bid) for cards, bid in zip(hands, bids)]
        hands = sorted(hands, reverse=True, key=lambda x: (x.hand_value, *x.card_strengths))
        rank = len(hands)
        for hand in hands:
            hand.rank = rank
            rank -= 1
        print(f"Part one: {sum(x.rank * x.bid for x in hands)}")

        hands = sorted(hands, reverse=True, key=lambda x: (x.hand_value_j_wild, *x.card_strengths))
        rank = len(hands)
        for hand in hands:
            hand.rank = rank
            rank -= 1
        print(f"Part two: {sum(x.rank * x.bid for x in hands)}")
