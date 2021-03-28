import pandas as pd
import pathlib


class Map:
    def __init__(self, map_path:str):
        self.map = pd.read_csv(map_path, header=None)
        self.xlen = len(self.map.columns)
        self.ylen = len(self.map.index)
    
    def _get_unique_point(self, cellValue:str) -> tuple[int,int]:
        loc = map.where(map == cellValue).dropna(how='all').dropna(axis=1,how='all')
        return loc.index[0], loc.columns[0]

    def get_starting_point(self) -> tuple[int,int]:
        return self._get_unique_point("I")

    def get_final_point(self) -> tuple[int,int]:
        return self._get_unique_point("F")

    def transform_str_to_values(self, cellweights_path:str):
        cellweights = pd.read_csv(cellweights_path, header=None).to_dict()

        pass






class Agent:
    def __init__(self):
        self.x = None
        self.y = None
        self.time_spent = 0
        pass

    def move_to_coordinate(self, x:int, y:int):
        pass


input_path = pathlib.Path(__file__).parents[1].joinpath('input')
m = Map(input_path.joinpath('map.csv'))

a = Agent()
a.move_to_coordinate(m.get_starting_point)