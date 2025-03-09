import random
"""
strategy.py

This module contains the Strategy class responsible for:
 - Tracking the known state of the enemy board.
 - Deciding which (x, y) cell to attack next.
 - Registering the result of each attack (hit/miss, sunk).
 - Keeping track of remaining enemy ships in a ships_dict.
"""

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
        self.hit_list = []

    def get_next_attack(self) -> tuple[int, int]:
        if self.hit_list:
            return self.hit_list.pop(0)
        while True:
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            if self.enemy_board[y][x] == '?':
                return x, y

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        self.enemy_board[y][x] = 'H' if is_hit else 'M'
        if is_hit and not is_sunk:
            self.hit_list.extend(self.get_neighbors(x, y))
        if is_sunk:
            self.mark_sunk_ship(x, y)

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows and self.enemy_board[ny][nx] == '?':
                neighbors.append((nx, ny))
        return neighbors

    def mark_sunk_ship(self, x: int, y: int) -> None:
        for ship_id in self.ships_dict:
            if self.ships_dict[ship_id] > 0:
                self.ships_dict[ship_id] -= 1
                break

    def get_enemy_board(self) -> list[list[str]]:
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        return self.ships_dict

    def all_ships_sunk(self) -> bool:
        return all(count == 0 for count in self.ships_dict.values())
