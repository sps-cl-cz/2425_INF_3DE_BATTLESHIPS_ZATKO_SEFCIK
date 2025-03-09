import random

class BoardSetup:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]

        self.ship_shapes = {
            1: [(0, 0), (1, 0)],  
            2: [(0, 0), (1, 0), (2, 0)],  
            3: [(0, 0), (1, 0), (2, 0), (3, 0)],  
            4: [(0, 0), (1, 0), (2, 0), (1, 1)],  
            5: [(0, 0), (1, 0), (2, 0), (2, 1)],  
            6: [(0, 1), (1, 1), (1, 0), (2, 0)],  
            7: [(1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1)] 
        }

    def get_board(self) -> list[list[int]]:
        return self.board

    def get_tile(self, x: int, y: int) -> int:
        if y < 0 or y >= self.rows or x < 0 or x >= self.cols:
            raise IndexError("Coordinates out of bounds")
        return self.board[y][x]

    def is_adjacent_to_ship(self, shape, start_x, start_y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in shape:
            x, y = start_x + dx, start_y + dy
            for dir_x, dir_y in directions:
                adj_x, adj_y = x + dir_x, y + dir_y
                if 0 <= adj_x < self.cols and 0 <= adj_y < self.rows:
                    if self.board[adj_y][adj_x] != 0:
                        return True
        return False

    def can_place_ship(self, shape, start_x, start_y):
        for dx, dy in shape:
            x, y = start_x + dx, start_y + dy
            if x < 0 or x >= self.cols or y < 0 or y >= self.rows or self.board[y][x] != 0:
                return False
        return not self.is_adjacent_to_ship(shape, start_x, start_y)

    def place_ship(self, ship_id, shape, start_x, start_y):
        for dx, dy in shape:
            x, y = start_x + dx, start_y + dy
            self.board[y][x] = ship_id

    def place_ships(self) -> None:
        for ship_id, count in self.ships_dict.items():
            shape = self.ship_shapes.get(ship_id)
            if not shape:
                raise ValueError(f"Invalid ship ID: {ship_id}")
            
            for _ in range(count):
                placed = False
                attempts = 0
                while not placed and attempts < 100:
                    start_x = random.randint(0, self.cols - 1)
                    start_y = random.randint(0, self.rows - 1)
                    if self.can_place_ship(shape, start_x, start_y):
                        self.place_ship(ship_id, shape, start_x, start_y)
                        placed = True
                    attempts += 1
                
                if not placed:
                    raise ValueError("Unable to place all ships")

    def reset_board(self) -> None:
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def board_stats(self) -> dict:
        empty_spaces = sum(row.count(0) for row in self.board)
        occupied_spaces = self.rows * self.cols - empty_spaces
        return {"empty_spaces": empty_spaces, "occupied_spaces": occupied_spaces}

    def print_board(self) -> None:
        for row in self.board:
            print(" ".join(str(cell) for cell in row))

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]
        self.hit_list = []
        self.shots_fired = set()

    def get_next_attack(self) -> tuple[int, int]:
        if self.hit_list:
            return self.hit_list.pop(0)
        while True:
            x, y = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            if (x, y) not in self.shots_fired:
                self.shots_fired.add((x, y))
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

if __name__ == "__main__":
    rows, cols = 10, 10
    ships_dict = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}
    board = BoardSetup(rows, cols, ships_dict)
    board.place_ships()
    board.print_board()
    print(board.board_stats())

    strategy = Strategy(rows, cols, ships_dict)
    for _ in range(100):  # Maximum 100 shots
        x, y = strategy.get_next_attack()
        is_hit = board.get_tile(x, y) != 0
        is_sunk = all(board.get_tile(nx, ny) == 0 for nx, ny in strategy.get_neighbors(x, y))
        strategy.register_attack(x, y, is_hit, is_sunk)
        print(f"Attack on ({x}, {y}) - {'HIT' if is_hit else 'MISS'}")
        
        if strategy.all_ships_sunk():
            print("All enemy ships have been sunk!")
            break
