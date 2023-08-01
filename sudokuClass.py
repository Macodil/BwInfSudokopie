from typing import Optional, Callable
import copy
from dataclasses import dataclass, field


@dataclass
class Sudoku:
    zeilen: list[list[int]]

    def get_zeile(self, zeile: int) -> list[int]:
        return self.zeilen[zeile]

    def get_spalte(self, spalte: int) -> list[int]:
        return [x[spalte] for x in self.zeilen]

    def get_zeilen_block(self, pos: int) -> list[list[int]]:
        return self.zeilen[pos * 3: pos * 3 + 3]

    def get_spalten_block(self, pos: int) -> list[list[int]]:
        my_array = []
        for i in range(pos * 3, pos * 3 + 3):
            my_array += [self.get_spalte(i)]
        return my_array

    def turn_90_degree(self) -> list[list[int]]:
        return list(reversed([self.get_spalte(i) for i in range(9)]))

    def print(self):
        for i in self.zeilen:
            print("| ", end='')
            for a in i:
                print(a, end=" | ")
            print("")
        print("")

    def switch_zeilen(self, pos_1, pos_2) -> list[list[int]]:
        my_new_zeilen = self.zeilen[:]
        my_new_zeilen[pos_1], my_new_zeilen[pos_2] = my_new_zeilen[pos_2], my_new_zeilen[pos_1]
        return my_new_zeilen

    def switch_spalten(self, pos_1, pos_2) -> list[list[int]]:
        my_new_zeilen = copy.deepcopy(self.zeilen)  # deepcopy
        for i in range(9):
            my_new_zeilen[i][pos_1], my_new_zeilen[i][pos_2] = my_new_zeilen[i][pos_2], my_new_zeilen[i][pos_1]
        return my_new_zeilen

    def switch_zeilen_block(self, pos_1, pos_2) -> list[list[int]]:
        my_new_zeilen = Sudoku(self.zeilen[:])
        for i in range(3):
            my_new_zeilen = Sudoku(my_new_zeilen.switch_zeilen(pos_1 * 3 + i, pos_2 * 3 + i))
        return my_new_zeilen.zeilen

    def switch_spalten_block(self, pos_1, pos_2) -> list[list[int]]:
        my_new_zeilen = Sudoku(self.zeilen[:])
        for i in range(3):
            my_new_zeilen = Sudoku(my_new_zeilen.switch_spalten(pos_1 * 3 + i, pos_2 * 3 + i))
        return my_new_zeilen.zeilen


def get_amount_numbers(zeile_or_spalte: list[int]) -> int:
    return len([x for x in zeile_or_spalte if x != 0])


def get_position_numbers(zeile_or_spalte: list[int]) -> list[int]:
    return [i for i in range(9) if zeile_or_spalte[i] != 0]


def get_amount_numbers_in_block(block: list[list[int]]) -> list[int]:
    return [get_amount_numbers(block[i]) for i in range(3)]