
# Flower Game Simulation

This project simulates the Flower game from Destiny 2. The game is played on a grid where flowers of different species compete for dominance under the influence of the Gardener and the Winnower.

## Usage

## Requirements
- Python 3.x
- h5py
- matplotlib

Install the required packages using:
```sh
pip install -r requirements.txt
```

### Simulation
To run the simulation:
```sh
python flower_game.py <width> <height> --logfile <logfile>
```
- `<width>`: Width of the grid
- `<height>`: Height of the grid
- `--logfile`: Path to the log file for game states (default: `game_log.h5`)

### Visualization
To visualize the game states:
```sh
python animate.py <logfile> --interval <interval>
```
- `<logfile>`: Path to the log file for game states
- `--interval`: Interval between frames in milliseconds (default: 200)

## Game Rules

### Grid Setup
1. **Grid Size**: The game is played on an x by y grid.
2. **Initial Seeding**:
   - The grid is seeded with "Flowers" of different species or empty cells.
   - For each cell, there is a 30% chance it will contain a new species or be empty.
   - New species have randomized stats at spawn (HP and Attack Power both range from 1 to 10).

### Flowers
3. **Flower Attributes**:
   - **Species**: Each flower belongs to a specific species.
   - **HP (Health Points)**: The health of a flower, determining how much damage it can take before being removed from the grid.
   - **Attack Power**: The power a flower has to attack other flowers.

### Gardener Actions
4. **Gardener's Goal**: The Gardener seeks to increase life across the universe.
5. **Blessing**:
   - The Gardener can bless a species to increase its HP or upgrade its attack capabilities, but only when that species is under attack by a species controlled by the Winnower.
   - Blessing a species affects all flowers of that species on the grid.
6. **Expansion**:
   - Flowers naturally want to reproduce and expand to adjacent cells.
7. **Reproduction Rules**:
   - Flowers can expand into adjacent empty spaces.
   - If a flower is adjacent to flowers of the same species, they can combine their strengths to take over new spaces.
   - The Gardener may choose to grant higher HP or attack capabilities to groups of the same species that are close together.
8. **Seeding New Life**:
   - On the Gardener's turn, there is a 50% chance they will buff an existing species and a 50% chance they will create a new species on an empty cell.
   - New species have randomized stats at spawn (HP and Attack Power both range from 1 to 10).

### Winnower Actions
9. **Winnower's Goal**: The Winnower seeks to ensure that there is only one dominant species left in the universe.
10. **Corruption**:
    - The Winnower can take over a powerful flower and spread corruption to adjacent flowers of the same species.
    - On the Winnower's turn, they can only corrupt one tile from one species.
    - The Winnower has a 75% chance to place corruption next to an already corrupted flower.
11. **Corruption Spread**:
    - Each turn, corrupted flowers have a chance to corrupt adjacent flowers of the same species.
    - Flowers corrupted by the Winnower receive additional attack power.
12. **Conversion**:
    - If a species is defeated by the Winnower, there is a chance it will be completely annihilated or join the forces of the Winnower. The closest Winnower species will absorb the remaining flowers of a defeated species.

### Conflict and Combat
13. **Combat**:
    - When flowers of different species or different corruption states are adjacent, they will engage in combat.
    - **Attack**: Flowers will use their attack power to reduce the HP of adjacent enemy flowers.
    - **Defense**: Flowers will use their HP to withstand attacks.
    - **Resolution**: After attacks, HP and attack power adjustments are resolved, and any flowers with HP reduced to zero are removed from the grid.
14. **Combat Mechanics**:
    - Each species can only act once per turn, either by expanding or attacking.
    - Damage dealt is equal to the attack power of the attacking flower.
    - Damage is subtracted from the HP of the defending flower.
    - If a flower's HP reaches zero, it is removed from the grid.

### Turn Sequence
15. **Turn Order**:
    - **Gardener Phase**: The Gardener blesses and encourages growth in specific species, but only if they are under attack by the Winnower. The Gardener can also seed new life.
    - **Expansion Phase**: Flowers attempt to reproduce and expand.
    - **Winnower Phase**: The Winnower attempts to corrupt powerful flowers and spread corruption.
    - **Combat Phase**: Flowers engage in combat with adjacent enemy flowers.
    - **Resolution Phase**: HP and attack power adjustments are resolved, and defeated flowers are removed.

### Win and Lose Conditions
16. **Win Conditions**:
    - **The Final Shape**: The game ends when only one species or only corrupted/un-corrupted flowers remain on the grid.
    - **We Make Our Own Fate**: If the Gardener manages to create a balanced ecosystem where multiple species thrive without the influence of the Winnower, this is considered a Gardener victory.

## Game States
17. **Initialization**:
    - The grid is set up, and initial flowers are seeded.
    - The Gardener and Winnower prepare their initial actions.
18. **Active Play**:
    - The game progresses through the turn sequence: Gardener Phase, Expansion Phase, Winnower Phase, Combat Phase, and Resolution Phase.
    - Players (or the AI) take actions based on the current state of the grid and the goals of the Gardener and Winnower.
19. **Endgame**:
    - The game enters the endgame phase when only one species is left, or when the Winnower has cleared the board of all Gardener-controlled flowers.
    - The final battles occur until the win conditions are met.

## Notes
- The game state is logged every 10 turns, including the final state.
- The Winnower attempts to place corruption adjacent to already corrupted flowers with a 75% chance to strengthen its forces.
