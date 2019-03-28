import arcade
import forest
import time
import copy
import random
import argparse
SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 15


state_to_color = {
    forest.CellStates.ash: arcade.color.WHITE,
    forest.CellStates.fire: arcade.color.BARN_RED,
    forest.CellStates.tree: arcade.color.APPLE_GREEN,
    forest.CellStates.pond: arcade.color.BLUEBERRY,
}


def generate_cell_shape(x, y, color, cell_height=CELL_HEIGHT):
    xx = x*cell_height + cell_height/2
    yy = y*cell_height+cell_height/2
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
            window_height*cell_height, window_height*cell_height, 'Forest Fire')
        self.simulation_height = window_height
        self.cell_height = cell_height

    def setup(self):
        self.density = random.random()
        self.state = forest.generate_forest(
            self.simulation_height, self.simulation_height, tree_density=self.density)
        self.state = forest.set_fire(self.state)
        self.previous_state = self.state

        self.shapes_grid = list()
        self.spread_chance = random.random()
        self.sprites_list = arcade.SpriteList()
        self.last_finished_time = time.time()
        arcade.set_background_color(arcade.color.WHITE)

        start_time = int(round(time.time() * 1000))

        for y, row in enumerate(self.state):
            newrow = list()
            for x, cell in enumerate(row):
                shape = generate_cell_shape(x, y, state_to_color[cell], self.cell_height)
                newrow.append(shape)
                self.sprites_list.append(shape)
            self.shapes_grid.append(newrow)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('setup', total_time)

    def on_draw(self):

        start_time = int(round(time.time() * 1000))
        shapes = arcade.ShapeElementList()
        arcade.start_render()
        self.sprites_list.draw()
        arcade.draw_text(
            f'P(spread):{self.spread_chance:.2f}, density={self.density:.2f}', 10, 20, arcade.color.BLACK, 18)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('draw', total_time)

    def update(self, delta_time):
        start_time = int(round(time.time() * 1000))
        self.previous_state = self.state
        self.state = forest.next_state(
            self.state, spread_chance=self.spread_chance)
        fire_count = 0
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                prev_val = self.previous_state[y][x]
                new_val = self.state[y][x]
                if new_val != prev_val:
                    # changing colors is expensive, so only do it when necenssary
                    self.shapes_grid[y][x].color = state_to_color[cell]
                if new_val == forest.CellStates.fire:
                    fire_count += 1
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('update', total_time)
        if fire_count == 0 and time.time() - self.last_finished_time > 3:
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        self.setup()


parser = argparse.ArgumentParser()
parser.add_argument('--height', type=int,
                    help="Simulation height (cells)", default=75,)
parser.add_argument('--cell_height', type=int,
                    help='Cell height (pixels)', default=10,)


def main():
    args = parser.parse_args()
    CELL_HEIGHT = args.cell_height
    SIMULATION_DIMENSIONS = (args.height, args.height)
    print(CELL_HEIGHT, SIMULATION_DIMENSIONS)

    g = Game(args.height, args.cell_height)
    g.setup()
    arcade.run()


if __name__ == '__main__':
    main()
