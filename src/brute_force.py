from copy import deepcopy
from pathlib import Path

from tqdm import tqdm

import pandas as pd

from collections import Counter

class Node:

    def __init__(self, pokemonList, time):
        self.pokemonList = pokemonList
        self.time = time #time used in battles

    def __eq__(self,another):
        return self.time == another.time

    def __lt__(self, another):
        return self.time < another.time
    
    def __repr__(self):
        return ('{0} Time: {1}'.format(self.pokemonList,self.time))

POKEMON_MAX_ENERGY = 5

input_path_dir = Path(__file__).parents[1].joinpath('input')
gym_level = pd.read_csv(input_path_dir.joinpath('gymnasiums.csv')).sort_values('id')['level'].values
pokemon = pd.read_csv(input_path_dir.joinpath('pokemons.csv')).sort_values('power')
pokemon_name = pokemon['name'].values
pokemon_power_list = pokemon['power'].values

n_pokemons = len(pokemon_name)
n_gyms = len(gym_level)

n_pokemons = len(pokemon_name)
n_gyms = len(gym_level)


def birthChildren(current_node:Node,pokemon_power:dict):    
    breed_children = []

    battle_list = current_node.pokemonList
    # for each pokemon, for each battle create children node with new pokemon on every possible position
    for (name,_) in pokemon_power.items():
        for i in range(n_gyms):
            j = 0
            while  j < n_pokemons:
                if battle_list[i][j] == None:
                    child = deepcopy(current_node)
                    #print(child.pokemonList[i][j])
                    child.pokemonList[i][j] = name
                    child.time = getTotalTime (child.pokemonList,pokemon_power,gym_level)
                    #print('child after ' + str(child.pokemonList))
                    if NodeIsValid(child):
                        breed_children.append(child)
                    j = n_pokemons
                j = j + 1
                    #read about pyhton memory managment if is possible to delete child from memory if not valid
    return breed_children

def bruteForce(pokemon_name,pokemon_power,gym_level):
    empty_battles = []
    for _ in range(len(gym_level)):
        empty_battles.append([None,None,None,None,None])

    working_node = Node(empty_battles, getTotalTime(empty_battles,pokemon_power,gym_level))
    best_node = deepcopy(working_node)
    open_nodes = []
    open_nodes.append(working_node)
    children = []
    t = tqdm(total=59604644775390625000000000000000000000000)
    while open_nodes:
        t.set_description(f"Best {best_node.time}")
        t.update(1)
        working_node = open_nodes.pop(0)
        if working_node.time < best_node.time:
            best_node = working_node
        children = birthChildren(working_node,pokemon_power)
        for _ in children:
            open_nodes.append(children.pop(0))
    return best_node


def NodeIsValid(current_node):
    battle_list = current_node.pokemonList
    all_fighters = []
    for battle in battle_list:
        for pokemon in battle:
            if pokemon != None:
                all_fighters.append(pokemon)
    pokemon_count = list(Counter(all_fighters).values())
    if max(pokemon_count) > POKEMON_MAX_ENERGY or sum(pokemon_count) >= POKEMON_MAX_ENERGY * POKEMON_MAX_ENERGY:
        return False # if pokemon is used more than max lives or no pokemon is alive at the end 
    return True


def getTotalTime (battles,pokemon_power,gym_level):
    totalTime = 0
    for i in range(len(battles)):
        battlePower = 0
        for j in range(len(battles[i])):
            if battles[i][j] != None:
                battlePower = battlePower + pokemon_power[battles[i][j]]
        if battlePower == 0:
            battlePower = 1
        battleTime = gym_level[i]/battlePower
        totalTime = totalTime + battleTime
    return totalTime


empty_battles = []
for _ in range(len(gym_level)):
    empty_battles.append([None,None,None,None,None])

pokemon_power = {}
for i in range(n_pokemons):
    pokemon_power[pokemon_name[i]] = pokemon_power_list[i]

#test birthChildren
'''
children = birthChildren(Node(empty_battles, getTotalTime(empty_battles,pokemon_power,gym_level)),pokemon_power)
print(children[0])
'''

#DON'T RUN THIS CODE
best = bruteForce(pokemon_name,pokemon_power,gym_level)
print(best.time)
