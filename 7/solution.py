import time
import functools
import operator

CARD_VALUES = {
    "A": 13,
    "K" : 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1
}

if __name__ == "__main__":
    with open("test") as f:
        inpt = f.read().split('\n')
        hands, bids = zip(*[x.split(" ") for x in inpt])
        bids = list(map(int, bids))
        print(hands, bids)
        hands_counts = []
        hand_counts_idxs = {k: [] for k in range(1, 6)[::-1]}
        for i, hand in enumerate(hands):
            d = dict.fromkeys(hand, 0)
            for card in hand:
                d[card] += 1
            max_hand_value = max(d.values())
            hands_counts.append(max_hand_value)
            hand_counts_idxs[max_hand_value].append(i)
        print(hands_counts)
        print(hand_counts_idxs)
        # sorted_idxs = sorted(range(len(hands)), reverse=True, key = lambda i: hands_counts[i])
        # hands = [hands[i] for i in sorted_idxs]
        ranks = [0 for _ in range(len(hands))]
        rank = len(hands)
        for k, count_idx in hand_counts_idxs.items():
            if len(count_idx):
                print("i", count_idx, "n_match", k)
                for card_idx in range(5):
                    print("card_idx ", card_idx)
                    card_strengths = [CARD_VALUES[hands[idx][card_idx]] for idx in count_idx]
                    card_strength_idxs = sorted(range(len(count_idx)), reverse=True, key=lambda i: card_strengths[i])
                    card_strengths_unique = list(dict.fromkeys(card_strengths))
                    print("strenghts", card_strengths)
                    if len(set(card_strengths)) > 1:
                        removed_idxs = []
                        for j in card_strength_idxs:
                            if card_strengths[j] != card_strengths[0]:
                                break
                            ranks[count_idx[j]] = rank
                            count_idx.pop(j)
                            rank -= 1
                    else:
                        break
        winnings = [hand_rank * bid for hand_rank, bid in zip(ranks, bids)]
        print("ranks", ranks)
        print(winnings)
        total_winnings = sum(winnings)
        # print(hands, bids, hands_counts)
        start = time.time()
        # res = solve_part_one(inpt)
        end = time.time()
        print(f"Part one solution: {total_winnings} taking {(end - start):.7f}s")

        start = time.time()
        # res = solve_part_two(inpt)
        end = time.time()
        # print(f"Part two solution: {res} taking {(end - start):.7f}s")
