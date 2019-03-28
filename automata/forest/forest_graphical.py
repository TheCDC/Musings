import arcade
import forest
SIMULATION_DIMENSIONS = (30, 30)
CELL_HEIGHT = 10


state_to_color = {
    forest.CellStates.ash: arcade.color.WHITE,
    forest.CellStates.fire: arcade.color.BARN_RED,
    forest.CellStates.tree: arcade.color.APPLE_GREEN,
    forest.CellStates.pond: arcade.color.BLUEBERRY,
}

def get_cell_corners(x,y):
    return [[x,y],[x,y+CELL_HEIGHT],[x+CELL_HEIGHT,y+CELL_HEIGHT],[x+CELL_HEIGHT,y]]
class Game(arcade.Window):
    def __init__(self):
        super().__init__(
            SIMULATION_DIMENSIONS[0]*CELL_HEIGHT, SIMULATION_DIMENSIONS[1]*CELL_HEIGHT, 'Forest Fire')
        self.state = forest.generate_forest(*SIMULATION_DIMENSIONS)
        self.state = forest.set_fire(self.state)
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                arcade.draw_rectangle_filled(
                    x*CELL_HEIGHT, y*CELL_HEIGHT, CELL_HEIGHT, CELL_HEIGHT, state_to_color[cell])

    def update(self, delta_time):
        self.state = forest.next_state(self.state)

    def on_mouse_press(self, x, y, button, modifiers):
        pass


def main():
    Game()
    arcade.run()


if __name__ == '__main__':
    main()
