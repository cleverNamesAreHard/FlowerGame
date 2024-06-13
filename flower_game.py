import argparse
import random
import h5py

# Define the Flower class
class Flower:
    def __init__(self, species, hp, attack_power):
        self.species = species
        self.hp = hp
        self.attack_power = attack_power
        self.corrupted = False

    def __repr__(self):
        return f"{self.species}(HP:{self.hp}, AP:{self.attack_power}, Corrupted:{self.corrupted})"

# Define the Grid class
class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.species_counter = 0

    def seed_initial_flowers(self):
        print("Initial Seeding....")
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < 0.3:  # 30% chance to place a flower
                    species = f"Species_{self.species_counter}"
                    hp = random.randint(1, 10)
                    attack_power = random.randint(1, 10)
                    self.grid[y][x] = Flower(species, hp, attack_power)
                    self.species_counter += 1

    def display(self):
        for row in self.grid:
            print(" | ".join(str(cell) if cell else "Empty" for cell in row))

    def get_adjacent_cells(self, x, y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent_cells = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                adjacent_cells.append((nx, ny))
        return adjacent_cells

    def expand_flowers(self, acted_species):
        for y in range(self.height):
            for x in range(self.width):
                flower = self.grid[y][x]
                if flower and flower.species not in acted_species:
                    for nx, ny in self.get_adjacent_cells(x, y):
                        if not self.grid[ny][nx] and random.random() < 0.5:
                            self.grid[ny][nx] = Flower(flower.species, flower.hp, flower.attack_power)
                            acted_species.add(flower.species)
                            break

    def gardener_bless(self):
        for y in range(self.height):
            for x in range(self.width):
                flower = self.grid[y][x]
                if flower and random.random() < 0.5:
                    flower.hp += random.randint(1, 5)
                    flower.attack_power += random.randint(1, 5)

    def winnower_corrupt(self):
        corrupted_flowers = [(y, x) for y in range(self.height) for x in range(self.width) if self.grid[y][x] and self.grid[y][x].corrupted]
        if corrupted_flowers and random.random() < 0.75:
            y, x = random.choice(corrupted_flowers)
            adjacent_cells = self.get_adjacent_cells(x, y)
            non_corrupted_adjacent = [(ny, nx) for nx, ny in adjacent_cells if self.grid[ny][nx] and not self.grid[ny][nx].corrupted]
            if non_corrupted_adjacent:
                ny, nx = random.choice(non_corrupted_adjacent)
                self.grid[ny][nx].corrupted = True
                return

        all_flowers = [(y, x, self.grid[y][x]) for y in range(self.height) for x in range(self.width) if self.grid[y][x] and not self.grid[y][x].corrupted]
        if not all_flowers:
            return
        y, x, flower = random.choice(all_flowers)
        flower.corrupted = True

    def combat_phase(self, acted_species):
        for y in range(self.height):
            for x in range(self.width):
                flower = self.grid[y][x]
                if flower and flower.species not in acted_species:
                    for nx, ny in self.get_adjacent_cells(x, y):
                        neighbor = self.grid[ny][nx]
                        if neighbor and (neighbor.species != flower.species or neighbor.corrupted != flower.corrupted):
                            self.resolve_combat(flower, neighbor)
                            acted_species.add(flower.species)
                            break

    def resolve_combat(self, flower1, flower2):
        flower1.hp -= flower2.attack_power
        flower2.hp -= flower1.attack_power
        if flower1.hp <= 0:
            self.remove_flower(flower1)
        if flower2.hp <= 0:
            self.remove_flower(flower2)

    def remove_flower(self, flower):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == flower:
                    self.grid[y][x] = None

    def check_victory_conditions(self):
        species_present = set()
        corrupted_present = False
        non_corrupted_present = False

        for row in self.grid:
            for cell in row:
                if cell:
                    species_present.add(cell.species)
                    if cell.corrupted:
                        corrupted_present = True
                    else:
                        non_corrupted_present = True

        if len(species_present) == 1 and (corrupted_present != non_corrupted_present):
            print(f"The Final Shape is achieved by {species_present.pop()}")
            return True
        return False

    def count_flowers(self):
        return sum(cell is not None for row in self.grid for cell in row)

def log_game_state(grid, turn, file):
    with h5py.File(file, 'a') as f:
        group = f.create_group(f"turn_{turn}")
        for y in range(grid.height):
            for x in range(grid.width):
                flower = grid.grid[y][x]
                if flower:
                    dataset = group.create_dataset(f"cell_{y}_{x}", (4,), dtype='i')
                    dataset[0] = int(flower.species.split('_')[1])
                    dataset[1] = flower.hp
                    dataset[2] = flower.attack_power
                    dataset[3] = 1 if flower.corrupted else 0

def game_loop(grid, logfile):
    turn = 0
    winnower_defeated = False

    while not grid.check_victory_conditions():
        if turn % 100 == 0 and turn >= 0:
            print(f"Turn {turn}-{turn+100}")
        
        if turn % 10 == 0:
            log_game_state(grid, turn, logfile)

        if grid.count_flowers() == 0:
            winnower_defeated = True
            print(f"Approaching the Final Shape at turn {turn}")
            break

        acted_species = set()
        grid.gardener_bless()
        grid.expand_flowers(acted_species)
        grid.winnower_corrupt()
        grid.combat_phase(acted_species)
        turn += 1

    # Log the final state
    log_game_state(grid, turn, logfile)

    if winnower_defeated:
        print("The Winnower has defeated the Gardener. Approaching the Final Shape.")
    else:
        print(f"Victory achieved on turn {turn}")

def main():
    parser = argparse.ArgumentParser(description="Simulate the Flower game from Destiny 2.")
    parser.add_argument("width", type=int, help="Width of the grid")
    parser.add_argument("height", type=int, help="Height of the grid")
    parser.add_argument("--logfile", type=str, default="game_log.h5", help="Log file for game states")
    args = parser.parse_args()

    grid = Grid(args.width, args.height)
    grid.seed_initial_flowers()

    game_loop(grid, args.logfile)

if __name__ == "__main__":
    main()
