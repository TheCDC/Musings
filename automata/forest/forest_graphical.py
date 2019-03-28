import arcade
import forest
import time
import copy
import random
SIMULATION_DIMENSIONS = (200, 200)
CELL_HEIGHT = 3


state_to_color = {
    forest.CellStates.ash: arcade.color.WHITE,
    forest.CellStates.fire: arcade.color.BARN_RED,
    forest.CellStates.tree: arcade.color.APPLE_GREEN,
    forest.CellStates.pond: arcade.color.BLUEBERRY,
}


def generate_cell_shape(x, y, color):
    xx = x*CELL_HEIGHT + CELL_HEIGHT/2
    yy = y*CELL_HEIGHT+CELL_HEIGHT/2
    sprite = arcade.Sprite(
        filename='pixel.png',
        center_x=xx,
        center_y=yy,
        scale=CELL_HEIGHT,
    )
    sprite.color = color
    return sprite
    return arcade.create_rectangle_filled(xx, yy, CELL_HEIGHT, CELL_HEIGHT, color)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(
            SIMULATION_DIMENSIONS[0]*CELL_HEIGHT, SIMULATION_DIMENSIONS[1]*CELL_HEIGHT, 'Forest Fire')

    def setup(self):
        self.density = random.random()/2 + 1/2
        self.state = forest.generate_forest(
            *SIMULATION_DIMENSIONS, tree_density=self.density)
        self.state = forest.set_fire(self.state)
        self.previous_state = self.state

        self.shapes_grid = list()
        self.spread_chance = random.random()/2 + 1/2
        self.sprites_list = arcade.SpriteList()
        self.last_finished_time = time.time()
        arcade.set_background_color(arcade.color.WHITE)

        start_time = int(round(time.time() * 1000))

        for y, row in enumerate(self.state):
            newrow = list()
            for x, cell in enumerate(row):
                shape = generate_cell_shape(x, y, state_to_color[cell])
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


def main():
    g = Game()
    g.setup()
    arcade.run()


if __name__ == '__main__':
    main()
