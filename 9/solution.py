
from typing import List

class History():
    def __init__(self, values: List[int]):
        self.sequences = [values]
        i = 0
        while not all([x == 0 for x in self.sequences[-1]]):
            differences = []
            for a, b in zip(self.sequences[i], self.sequences[i][1:]):
                differences.append(b - a)
            self.sequences.append(differences)
            i +=1
    
    def extend_sequence_forward(self) -> int:
        self.sequences[-1].append(0)
        for i in range(len(self.sequences) - 2 , -1, -1):
            self.sequences[i].append(self.sequences[i][-1] + self.sequences[i+1][-1])
        return self.sequences[0][-1]

    def extend_sequence_backward(self) -> int:
        self.sequences[-1].insert(0, 0)
        for i in range(len(self.sequences) - 2 , -1, -1):
            self.sequences[i].insert(0, self.sequences[i][0] - self.sequences[i + 1][0])
        return self.sequences[0][0]
    
    def __repr__(self) -> str:
        history_str = ""
        for i, sequence in enumerate(self.sequences):
            history_str += (" " * (i * 2)) + str.join("   " ,[ str(x) for x in sequence]) + "\n"
        return history_str

if __name__ == "__main__":
    with open("input") as f:
        inpt = f.read().split('\n')
        histories_part_one = []
        histories_part_two = []
        for h in inpt:
            history = History(list(map(int, h.strip().split())))
            histories_part_one.append(history.extend_sequence_forward())
            histories_part_two.append(history.extend_sequence_backward())
        print(f"Part one: {sum(histories_part_one)}")
        print(f"Part two: {sum(histories_part_two)}")