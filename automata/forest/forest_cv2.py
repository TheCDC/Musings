#!/usr/bin/python3
from cv2_utils import numpy_to_cv2
import time
import arcade
import forest
import random
import argparse
import cv2
from scipy.ndimage import convolve, zoom
import numpy as np
from time import strftime

SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 15
WHITE = np.array(arcade.color.WHITE)
DRY_BROWN = np.array((176, 135, 3))
state_to_color = {
    forest.CellStates.ash.value: np.array(arcade.color.LIGHT_GRAY),
    forest.CellStates.fire.value: np.array(arcade.color.RED_ORANGE),
    forest.CellStates.tree.value: np.array(arcade.color.GREEN),
    forest.CellStates.pond.value: np.array((40, 122, 255)),
    0: arcade.color.YELLOW,
}

KERNEL_WATER_DEPTH = np.ones((7, 7))


def generate_cell_shape(x, y, color, cell_height=CELL_HEIGHT):
    xx = x * cell_height + cell_height / 2
    yy = y * cell_height + cell_height / 2
    sprite = arcade.Sprite(
        filename="pixel.png",
        center_x=xx,
        center_y=yy,
        scale=cell_height,
    )
    sprite.color = color
    return sprite


def color_point_mean(colors: np.array, weights: np.array = None):
    if weights is None:
        weights = np.ones(colors.shape)
    else:
        weights = weights.reshape((weights.shape[0], 1))

    return sum(colors * weights) / len(colors)


class Game:
    def __init__(self, window_height, cell_height):
        self.window_name = None
        self.simulation_height = window_height
        self.cell_height = cell_height
        self.simulation_parameters = None
        self.simulation = None
        self.previous_state = None
        self.paused: bool = True
        self.color_buffer = np.zeros(
            (self.simulation_height, self.simulation_height, 3)
        )
        self.is_lit = False
        self.window_id_unique = "Forest Fire"
        cv2.namedWindow(self.window_id_unique, cv2.WINDOW_AUTOSIZE)
        cv2.createButton("Reset",self.setup,None,cv2.QT_PUSH_BUTTON,1)


    def setup(self,*args):
        start_time: float = time.time()
        self.paused: bool = True
        self.is_lit = False
        self.simulation_parameters = dict(
            tree_density=random.random() * 0.7,
            chance_spread_fire_to_tree=random.random() / 2 + 0.1,
            chance_fire_sustain=random.random(),
            chance_spread_fire_to_ash=random.random() * 0.9,
        )
        self.simulation: forest.SimulationState = forest.SimulationState(
            self.simulation_height, self.simulation_height
        )
        self.previous_state: forest.SimulationState = self.simulation
        self.state: np.array = self.simulation.state
        name_old = self.window_name
        self.window_name = (
            f"Forest Fire {self.simulation_height}x{self.simulation_height}"
            + strftime("%Y-%m-%d %H%M%S")
        )
        cv2.setWindowTitle(self.window_id_unique, self.window_name)
        cv2.setMouseCallback(self.window_id_unique, self.mouse_click)

        end_time = time.time()
        total_time = end_time - start_time
        print(
            f"setup {total_time:.2f}",
        )

    def on_draw(self):

        start_time = time.time()
        status_str = "\n".join(
            [
                f'density={self.simulation_parameters["tree_density"]:.2f}',
                f'P(spread)={self.simulation_parameters["chance_spread_fire_to_tree"]:.2f}',
                f'P(sustain)={self.simulation_parameters["chance_fire_sustain"]:.2f}',
                f'P(reignite)={self.simulation_parameters["chance_spread_fire_to_ash"]:.2f}',
            ]
        )

        color_map_scalar_shape = self.state.shape + (1,)

        self.color_buffer = np.zeros((self.state.shape) + (3,))

        trees = self.state == forest.CellStates.tree.value
        fire = self.state == forest.CellStates.fire.value
        ash = self.state == forest.CellStates.ash.value
        pond = self.state == forest.CellStates.pond.value

        num_tree_neighbors = convolve(
            trees.astype(int), KERNEL_WATER_DEPTH, mode="constant"
        )
        num_pond_neighbors = convolve(
            pond.astype(int), KERNEL_WATER_DEPTH, mode="constant"
        )

        altitude_color_map = self.simulation.altitude_map.reshape(
            color_map_scalar_shape
        )
        snow_color_layer = altitude_color_map * np.full(self.color_buffer.shape, WHITE)
        dry_tree_color_layer = self.simulation.temperature_map.reshape(
            color_map_scalar_shape
        ) * np.full(self.color_buffer.shape, DRY_BROWN)
        tree_color_layer = np.full(
            self.color_buffer.shape, state_to_color[forest.CellStates.tree.value]
        )
        water_color_layer = np.full(
            self.color_buffer.shape, state_to_color[forest.CellStates.pond.value]
        )
        ash_color_layer = np.full(
            self.color_buffer.shape, state_to_color[forest.CellStates.ash.value]
        )

        self.color_buffer[trees] = (
            (
                (
                    snow_color_layer * 0.6
                    + tree_color_layer * 0.2
                    + dry_tree_color_layer * 0.2
                )
            )
        )[trees]
        self.color_buffer[pond] = (
            water_color_layer
            * (0.98 ** num_pond_neighbors.reshape(color_map_scalar_shape))
        )[pond]
        self.color_buffer[fire] = state_to_color[forest.CellStates.fire.value]
        self.color_buffer[ash] = (
            ash_color_layer
            * (0.90 ** self.simulation.times_burned.reshape(color_map_scalar_shape))
        )[ash]

        img = (
            zoom(self.color_buffer, (self.cell_height, self.cell_height, 1), order=0)
            / 255
        )
        img = cv2.cvtColor(img.astype("float32"), cv2.COLOR_RGB2BGR)
        s = img.shape

        # =========== Set up mouse click event handler ==========
        cv2.imshow(self.window_id_unique, img)
        cv2.setWindowTitle(self.window_id_unique, self.window_name)
        cv2.waitKey(1)

        cv2.imshow(
            "times_burned", (self.simulation.times_burned >= 1).astype("float32")
        )
        cv2.waitKey(1)
        end_time = time.time()
        total_time = end_time - start_time
        # print(f"draw {total_time:.2f}")

    def update(self, delta_time, force=False):
        if self.paused and not force:
            return
        if not self.is_lit:
            self.simulation.set_fire()
            self.is_lit = True
        self.previous_state = self.simulation.state
        self.simulation.step(**self.simulation_parameters)
        self.state = self.simulation.state

    def mouse_click(self, event, x, y, flags, param):
        # to check if left mouse
        # button was clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            self.paused = not self.paused
            pass
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.setup()


parser = argparse.ArgumentParser()
parser.add_argument(
    "--height",
    type=int,
    help="Simulation height (cells)",
    default=200,
)
parser.add_argument(
    "--cell_height",
    type=int,
    help="Cell height (pixels)",
    default=2,
)


def main():
    args = parser.parse_args()
    CELL_HEIGHT = args.cell_height
    SIMULATION_DIMENSIONS = (args.height, args.height)

    g = Game(args.height, args.cell_height)
    g.setup()
    while True:
        g.update(0)
        g.on_draw()


if __name__ == "__main__":
    main()
