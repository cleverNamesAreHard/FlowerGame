import argparse
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def load_game_states(logfile):
    with h5py.File(logfile, 'r') as f:
        states = {}
        for key in f.keys():
            group = f[key]
            state = []
            for cell_key, dataset in group.items():
                y, x = map(int, cell_key.split('_')[1:])
                species, hp, attack_power, corrupted = dataset[:]
                state.append((y, x, species, hp, attack_power, corrupted))
            states[int(key.split('_')[1])] = state
    return states

def get_grid_dimensions(states):
    max_y = max(cell[0] for state in states.values() for cell in state)
    max_x = max(cell[1] for state in states.values() for cell in state)
    return max_x + 1, max_y + 1

def create_color_map(states, width, height):
    species_colors = {}
    winnower_color = np.array([1.0, 0.5, 0.0])
    empty_color = np.array([1.0, 1.0, 1.0])

    for state in states.values():
        for y, x, species, hp, attack_power, corrupted in state:
            if species not in species_colors:
                species_colors[species] = np.random.rand(3)
    
    return species_colors, winnower_color, empty_color

def update_frame(frame, img, states, width, height, species_colors, winnower_color, empty_color):
    turn = sorted(states.keys())[frame]
    state = np.full((height, width, 3), empty_color)
    for y, x, species, hp, attack_power, corrupted in states[turn]:
        color = winnower_color if corrupted else species_colors[species]
        state[y, x] = color
    img.set_array(state)
    return [img]

def animate_game(logfile, interval, output):
    states = load_game_states(logfile)
    width, height = get_grid_dimensions(states)
    species_colors, winnower_color, empty_color = create_color_map(states, width, height)

    fig, ax = plt.subplots()
    img = ax.imshow(np.zeros((height, width, 3)), interpolation='nearest')
    ax.axis('off')

    ani = animation.FuncAnimation(
        fig, update_frame, frames=len(states), fargs=(img, states, width, height, species_colors, winnower_color, empty_color), blit=True, interval=interval
    )

    if output:
        ani.save(output, writer='pillow')
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Animate the Flower game from Destiny 2.")
    parser.add_argument("logfile", type=str, help="Log file for game states")
    parser.add_argument("--interval", type=int, default=200, help="Interval between frames in milliseconds")
    parser.add_argument("--output", type=str, help="Output file for the animation (e.g., animation.gif)")
    args = parser.parse_args()

    animate_game(args.logfile, args.interval, args.output)

if __name__ == "__main__":
    main()
