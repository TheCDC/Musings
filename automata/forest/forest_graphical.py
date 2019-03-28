import arcade
import forest
import time
import copy
SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 10


state_to_color = {
    forest.CellStates.ash: arcade.color.WHITE,
    forest.CellStates.fire: arcade.color.BARN_RED,
    forest.CellStates.tree: arcade.color.APPLE_GREEN,
    forest.CellStates.pond: arcade.color.BLUEBERRY,
}


def generate_cell_shape(x, y, color):
    return arcade.create_rectangle_filled(
        x*CELL_HEIGHT + CELL_HEIGHT/2, y*CELL_HEIGHT+CELL_HEIGHT/2, CELL_HEIGHT, CELL_HEIGHT, color)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(
            SIMULATION_DIMENSIONS[0]*CELL_HEIGHT, SIMULATION_DIMENSIONS[1]*CELL_HEIGHT, 'Forest Fire')
        self.set_simulation()

    def setup(self):
        self.shapes_grid = list()

        arcade.set_background_color(arcade.color.WHITE)

        start_time = int(round(time.time() * 1000))

        for y, row in enumerate(self.state):
            newrow = list()
            for x, cell in enumerate(row):
                shape = generate_cell_shape(x, y, state_to_color[cell])
                newrow.append(shape)
            self.shapes_grid.append(newrow)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        print('setup', total_time)

    def set_simulation(self):
        self.state = forest.generate_forest(
            *SIMULATION_DIMENSIONS, density=0.65)
        self.state = forest.set_fire(self.state)
        self.previous_state = copy.deepcopy(self.state)
        self.finished_simulation = False

    def get_rectangles(self):
        shapes = arcade.ShapeElementList()
        for row in self.shapes_grid:
            for item in row:
                shapes.append(item)

        return shapes

    def on_draw(self):

        start_time = int(round(time.time() * 1000))
        shapes = arcade.ShapeElementList()
        arcade.start_render()
        self.get_rectangles().draw()
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        print('draw', total_time)

    def update(self, delta_time):
        start_time = int(round(time.time() * 1000))
        self.previous_state = self.state
        self.state = forest.next_state(self.state)
        fire_count = 0
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                prev_val = self.previous_state[y][x]
                new_val = self.state[y][x]
                if new_val != prev_val:
                    shape = generate_cell_shape(x, y, state_to_color[cell])

                    self.shapes_grid[y][x] = shape
                if new_val == forest.CellStates.fire:
                    fire_count += 1
        if fire_count == 0:
            self.finished_simulation = True
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        print('update', total_time)

    def on_mouse_press(self, x, y, button, modifiers):
        self.set_simulation()
        self.setup()


def main():
    g = Game()
    g.setup()
    arcade.run()


if __name__ == '__main__':
    main()
