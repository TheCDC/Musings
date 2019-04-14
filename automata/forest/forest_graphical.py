import arcade
import forest
import time
import copy
import random
import argparse
from collections import Counter
SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 15

state_to_color = {
    forest.CellStates.ash.value: arcade.color.ASH_GREY,
    forest.CellStates.fire.value: arcade.color.RED_ORANGE,
    forest.CellStates.tree.value: arcade.color.GUPPIE_GREEN,
    forest.CellStates.pond.value: arcade.color.BLUE_YONDER,
}


def generate_cell_shape(x, y, color, cell_height=CELL_HEIGHT):
    xx = x * cell_height + cell_height / 2
    yy = y * cell_height + cell_height / 2
    sprite = arcade.Sprite(
        filename='pixel.png',
        center_x=xx,
        center_y=yy,
        scale=cell_height,
    )
    sprite.color = color
    return sprite


class Game(arcade.Window):
    def __init__(self, window_height, cell_height):
        super().__init__(
            width=window_height * cell_height,
            height=window_height * cell_height,
            title='Forest Fire',
            update_rate=1 / 60,
            resizable=False,
            antialiasing=False,
        )
        self.simulation_height = window_height
        self.cell_height = cell_height
        self.simulation_parameters = None
        self.simulation = None
        self.previous_state = None

    def setup(self):
        self.simulation_parameters = dict(
            tree_density=random.random() * 0.5 + 0.5,
            spread_chance=random.random() * 0.9,
            sustain_chance=random.random(),
            reignite_chance=random.random() / 5)
        self.simulation: forest.SimulationState = forest.SimulationState(
            self.simulation_height, self.simulation_height,
            **self.simulation_parameters)
        self.previous_state = self.simulation

        self.shapes_grid = list()
        self.sprites_list = arcade.SpriteList()
        self.last_finished_time = time.time()
        arcade.set_background_color(arcade.color.WHITE)

        start_time = int(round(time.time() * 1000))

        for y, row in enumerate(self.simulation.state):
            newrow = list()
            for x, cell in enumerate(row):
                shape = generate_cell_shape(x, y, state_to_color[cell],
                                            self.cell_height)
                newrow.append(shape)
                self.sprites_list.append(shape)
            self.shapes_grid.append(newrow)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('setup', total_time)

    def on_draw(self):

        start_time = int(round(time.time() * 1000))
        arcade.start_render()
        self.sprites_list.draw()
        status_str = '\n'.join([
            f'density={self.simulation_parameters["tree_density"]:.2f}',
            f'P(spread)={self.simulation_parameters["spread_chance"]:.2f}',
            f'P(sustain)={self.simulation_parameters["sustain_chance"]:.2f}',
            f'P(reignite)={self.simulation_parameters["reignite_chance"]:.2f}',
        ])
        arcade.draw_text(
            status_str,
            10,
            20,
            arcade.color.BLACK,
            25,
            bold=True,
        )
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('draw', total_time)

    def update(self, delta_time):
        start_time = int(round(time.time() * 1000))
        self.previous_state = self.simulation.state
        self.simulation.step(**self.simulation_parameters)
        self.state = self.simulation.state

        counts = Counter()
        for y, row in enumerate(self.simulation.state):
            counts.update(row)
            for x, cell in enumerate(row):
                prev_val = self.previous_state[y][x]
                new_val = self.simulation.state[y][x]
                if new_val != prev_val:
                    # changing colors is expensive, so only do it when necessary
                    self.shapes_grid[y][x].color = state_to_color[cell]
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('update', total_time)
        if 0 in [
                counts[forest.CellStates.fire.value],
                counts[forest.CellStates.tree.value]
        ] and time.time() - self.last_finished_time > 3:
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        self.setup()


parser = argparse.ArgumentParser()
parser.add_argument(
    '--height',
    type=int,
    help="Simulation height (cells)",
    default=75,
)
parser.add_argument(
    '--cell_height',
    type=int,
    help='Cell height (pixels)',
    default=10,
)


def main():
    args = parser.parse_args()
    CELL_HEIGHT = args.cell_height
    SIMULATION_DIMENSIONS = (args.height, args.height)

    g = Game(args.height, args.cell_height)
    g.setup()
    arcade.run()


if __name__ == '__main__':
    main()
