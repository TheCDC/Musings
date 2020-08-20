import arcade
import forest
import time
import copy
import random
import argparse
from collections import Counter
from typing import Dict, List, Tuple,Generic
SIMULATION_DIMENSIONS = (50, 50)
CELL_HEIGHT = 15

state_to_color = {
    forest.CellStates.ash.value: arcade.color.ASH_GREY,
    forest.CellStates.fire.value: arcade.color.RED_ORANGE,
    forest.CellStates.tree.value: arcade.color.GUPPIE_GREEN,
    forest.CellStates.pond.value: (40, 122, 255),
    0: arcade.color.YELLOW,
}
class Point:
    def __init__(self, coords: Tuple[float]):
        self.coordinates = list(coords)
        lc = len(self.coordinates)
    def __mul__(self,other):
        return Point([c * other for c in self.coordinates])
    def __hash__(self):
        return hash(tuple(self.coordinates))
    def __repr__(self):
       return f"Point({self.coordinates})"
class Tile:
    def __init__(self,logical_corners:List[Point],actual_corners:List[Point],color:Tuple[int]):
        self.logical_corners = logical_corners
        self.actual_corners = actual_corners
        self._color = color
        self.shape :arcade.Shape = self.get_shape()
    def __str__(self):
        return "Tile({},{},{})".format(len(self.logical_corners,self.actual_corners,self.color))
    def get_shape(self):
        return arcade.create_polygon([p.coordinates for p in self.actual_corners] ,self.color)
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,value):
        if value != self._color:
            self._color = value
            self.shape = self.get_shape()


class Board:
    def __init__(self,width:int,height:int,cell_side_length:float,simulation_state:List[List[int]]):
        self.width :int = width
        self.height :int = height
        self.unit_coordinates :List[List[Point]] = [[Point([x,y]) for x in range(self.width + 1)] for y in range(self.height + 1)]
        self.cell_side_length :float = cell_side_length
        self.actual_coordinates :List[List[Point]] = [
            [perturb_point(p * cell_side_length,cell_side_length,0.2) for p in row]
           for row in self.unit_coordinates]
        self.tiles :List[Tile] = list()
        self.logical_coords_to_tiles :Dict[Point,Tile] = dict()
        for coord in ((x,y) for x in range(self.width) for y in range(self.height)):
            corners_logical = [Point(cs) for cs in get_cell_corners(coord)]
            corners_actual = [self.actual_coordinates[c.coordinates[0]][c.coordinates[1]] for c in corners_logical]
            t = Tile(corners_logical,corners_actual,state_to_color[simulation_state[coord[1]][coord[0]]])
            self.logical_coords_to_tiles.update({coord:t})
            self.tiles.append(t)
        
    def update(self,simulation_state):
        for y,row in enumerate(simulation_state):
            for x, cell_state in enumerate(row):
                old = self.logical_coords_to_tiles[(x,y)].color 
                new_color = state_to_color[cell_state]
                self.logical_coords_to_tiles[(x,y)].color = new_color
    def draw(self):
        shapes = arcade.ShapeElementList()
        for t in self.tiles:
            shapes.append(t.shape)
        shapes.draw()

    
def perturb_point(p:Point,side_length:float,tolerance=0.1):
    return Point([
        c + side_length * randrange(-tolerance,tolerance) for c in p.coordinates
        ])

def randrange(start,stop):
    return random.random() * (start - stop) + start

def perturb_corner(coords,side_length,tolerance=0.1) -> Tuple[float]:
    return tuple(c + side_length * randrange(-tolerance,tolerance) for c in coords)
def get_cell_corners(coords):
    offsets = ((0,0),
               (1,0),
               (1,1),
               (0,1),)
    return tuple((coords[0] + o[0],coords[1] + o[1]) for o in offsets)

def get_corners(x, y, cell_height=CELL_HEIGHT) -> Tuple[Tuple]:
    xx = x * cell_height 
    yy = y * cell_height 
    offsets = ((xx,yy),
               (xx + cell_height,yy),
               (xx + cell_height,yy + cell_height),
               (xx,yy + cell_height),)
    tolerance = 0.1
    t = tolerance * cell_height
   
    #corners = tuple([(a + randrange(-t,t),b + randrange(-t,t)) for a,b in
    #offsets])
    corners = ((xx ,yy),
               (xx + cell_height,yy),
               (xx + cell_height ,yy + cell_height),
               (xx,yy + cell_height),)
    return corners

def generate_cell_shape(x, y, color, cell_height=CELL_HEIGHT):
    xx = x * cell_height + cell_height / 2
    yy = y * cell_height + cell_height / 2
    sprite = arcade.Sprite(filename='pixel.png',
        center_x=xx,
        center_y=yy,
        scale=cell_height,)
    sprite.color = color
    return sprite


class Game ( arcade.Window ):
    def __init__(self, window_height:int, cell_height:int):
        super().__init__(width=window_height * cell_height,
            height=window_height * cell_height,
            title=f'Forest Fire {window_height}x{window_height}',
            resizable=False,
            antialiasing=False,)
        self.set_update_rate(1 / 16)
        self.simulation_height :int = window_height
        self.cell_height = cell_height
        self.simulation_parameters = None
        self.simulation = None
        self.previous_state = None
        self.irregular_corners :Dict[Tuple,Tuple[Tuple]] = dict()

    def setup(self):
        self.simulation_parameters = dict(tree_density=random.random(),
            chance_spread_fire_to_tree=random.random() * 0.9,
            chance_fire_sustain=random.random() / 2,
            chance_spread_fire_to_ash=random.random() / 5)
        self.simulation : forest.SimulationState = forest.SimulationState(self.simulation_height, self.simulation_height)
        self.previous_state = self.simulation

        self.shapes_grid = list()
        self.sprites_list = arcade.SpriteList()
        arcade.set_background_color(arcade.color.WHITE)

        start_time = int(round(time.time() * 1000))
        self.board = Board(self.simulation_height,self.simulation_height,self.cell_height,self.simulation.state)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('setup', total_time)

    def on_draw(self):

        start_time = int(round(time.time() * 1000))
        self.board.draw()

        self.sprites_list.draw()
        status_str = '\n'.join([f'density={self.simulation_parameters["tree_density"]:.2f}',
            f'P(spread)={self.simulation_parameters["chance_spread_fire_to_tree"]:.2f}',
            f'P(sustain)={self.simulation_parameters["chance_fire_sustain"]:.2f}',
            f'P(reignite)={self.simulation_parameters["chance_spread_fire_to_ash"]:.2f}',])
        arcade.draw_text(status_str,
            10,
            20,
            arcade.color.BLACK,
            18,
            bold=False,)
        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('draw', total_time)

    def update(self, delta_time):
        start_time = int(round(time.time() * 1000))
        self.previous_state = self.simulation.state
        self.simulation.step(**self.simulation_parameters)
        self.state = self.simulation.state
        self.board.update(self.state)
        counts = Counter()

        for y, row in enumerate(self.simulation.state):
            counts.update(row)
        

        end_time = int(round(time.time() * 1000))
        total_time = end_time - start_time
        # print('update', total_time)
        if 0 in [counts[forest.CellStates.fire.value],
                counts[forest.CellStates.tree.value]]:
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        self.setup()


parser = argparse.ArgumentParser()
parser.add_argument('--height',
    type=int,
    help="Simulation height (cells)",
    default=50,)
parser.add_argument('--cell_height',
    type=int,
    help='Cell height (pixels)',
    default=10,)


def main():
    args = parser.parse_args()
    CELL_HEIGHT = args.cell_height
    SIMULATION_DIMENSIONS = (args.height, args.height)
    
    g = Game(args.height, args.cell_height)
    
    g.setup()
    arcade.run()


if __name__ == '__main__':
    main()
