import pandas as pd
import numpy as np
import pathlib


class Map:
    def __init__(self, map_path:str, cellweights_path:str):
        self.map = pd.read_csv(map_path, header=None)
        self.map_values = self._transform_str_to_values(cellweights_path)
        self.start_point = self._get_unique_point("I")
        self.final_point = self._get_unique_point("F")
        self.xlen = len(self.map.index)
        self.ylen = len(self.map.columns)
        self.heuristic_map = pd.DataFrame(0, index=np.arange(self.xlen), columns=np.arange(self.ylen)).apply(lambda row: abs(row.index - self.final_point[0]) + abs(int(row.name) - self.final_point[1]))
    
    def _get_unique_point(self, cellValue:str):
        loc = self.map.where(self.map == cellValue).dropna(how='all').dropna(axis=1,how='all')
        return loc.index[0], loc.columns[0]

    def get_node_weight(self, coordinates) -> int:
        value = self.map_values.loc[coordinates[0], coordinates[1]]
        return value

    def get_node_label(self, coordinates) -> str:
        return self.map.loc[coordinates[0], coordinates[1]]

    def get_heuristic_weight(self, coordinates):
        return self.heuristic_map.loc[coordinates[0], coordinates[1]]

    def _transform_str_to_values(self, cellweights_path:str) -> pd.DataFrame:
        #cellweights = pd.read_csv(cellweights_path, header=None, index_col=0, squeeze=True).to_dict()
        cellweights = {'F': 1, 'I': 1, 'B': 3, 'M': 200, 'R': 5, '.': 1}

        return self.map.replace(cellweights)
        

class Agent:
    def __init__(self):
        self.x = None
        self.y = None
        self.time_spent = 0
        pass

    def move_to_coordinate(self, x:int, y:int):
        pass