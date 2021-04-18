"""
Genetic Algorithm (GENA)
This module implements a genetic algorithm to solve the combinatorial problem
    of finding the best pokemons to fight in each gymnasium

"""

import random
import time
from collections import deque
from copy import deepcopy
from itertools import compress
from os import stat
from pathlib import Path
from typing import Callable, List

from math import floor
import pandas as pd
from tqdm import tqdm

POKEMON_MAX_ENERGY = 5
INIT_GENERATION = 25
MAX_POP = 250
MAX_GENERATION_WITHOUT_IMPROVMENT = 300


input_path_dir = Path(__file__).parents[1].joinpath('input')
gym_level = pd.read_csv(input_path_dir.joinpath('gymnasiums.csv')).sort_values('id')['level'].values
pokemon = pd.read_csv(input_path_dir.joinpath('pokemons.csv')).sort_values('power')
pokemon_name = pokemon['name'].values
pokemon_power = pokemon['power'].values

n_pokemons = len(pokemon_name)
n_gyms = len(gym_level)


def gym_time(gym_id:int, total_factor:int) -> float:
    return gym_level[gym_id] / total_factor

class Chromosome:
    """
        Each gene is a boolean
        The Chromosome is a list of genes
    """
    def __init__(self, number_genes:int):
        self.sequence = [False] * number_genes
        self.number_genes = number_genes
        self.valid = None
        self._fitness = None
        
    def __repr__(self) -> str:
        return str(self.sequence)

    def __eq__(self, other) -> bool:
        return self.sequence == other.sequence
    
    def __hash__(self):
        # Hash chromossome as a binary sequence
        exp = 0
        rHash = 0
        for b in self.sequence[::-1]:
            if b:
                rHash += 2 ** exp
            exp += 1
        return rHash

    def check_if_valid(self):
        return True
    
    @property
    def is_valid(self):
        if self.valid is None:
            self.valid = self.check_if_valid()
        return self.valid

    def calculate_fitness(self):
        return 0

    @property
    def fitness(self):
        # Returns the fitness score of this chromossome. The higher the better
        if self._fitness is None:
            self._fitness = self.calculate_fitness()
        return self._fitness

    @staticmethod
    def _cross_over_middle(first, second):
        first, second = deepcopy(first), deepcopy(second)
        aux = first.sequence[0:first.number_genes//2]
        first.sequence[0:first.number_genes//2] = second.sequence[first.number_genes//2:]
        second.sequence[first.number_genes//2:] = aux
        first._fitness = None
        first.valid = None
        second._fitness = None
        second.valid = None
        return first, second

    @staticmethod
    def _cross_over_random(first, second):
        first, second = deepcopy(first), deepcopy(second)
        rand_i = random.randrange(0, first.number_genes)
        rand_f = rand_i + random.randrange(0, first.number_genes - rand_i)
        aux = first.sequence[rand_i:rand_f]
        first.sequence[rand_i:rand_f] = second.sequence[rand_i:rand_f]
        second.sequence[rand_i:rand_f] = aux
        first._fitness = None
        first.valid = None
        second._fitness = None
        second.valid = None
        return first, second

    @staticmethod
    def crossover(first, second):
        rand_i = random.randrange(0,100)
        if rand_i > 85:
            c1, c2 = PokemonSelection._cross_over_middle(first, second)
        else:
            c1, c2 = PokemonSelection._cross_over_random(first, second)
        c1.chance_mutate()
        c2.chance_mutate()
        return c1,c2

    def mutate(self):
        rand_pos = random.randrange(0, self.number_genes)
        self.sequence[rand_pos] = not self.sequence[rand_pos]
        self.valid = None
        self._fitness = None

    def chance_mutate(self):
        prob = 0.01     # 1 porcent of chance of suffering a mutation
        rand = random.randint(0, 100)
        if rand <= (prob * 100):
            self.mutate()

    def reverse(self):
        self.sequence = self.sequence[::-1]
        self.valid = None
        self._fitness = None

    def shift_left(self, n):
        for _ in range(0, n):
            self.sequence.append(self.sequence.pop(0))
        self.valid = None
        self._fitness = None

    def shift_right(self, n):
        for _ in range(0, n):
            self.sequence.insert(0, self.sequence.pop())
        self.valid = None
        self._fitness = None


class PokemonSelection(Chromosome):
    """
        Using the concept of a chromosome and adapting for this problem
        Each gene is a list where true=pokemon at its index used
        Each chromossome is the chosen pokemon for each and all gymnasiums
        The gyms are ordered by its id, and the pokemon by its value. Both ascending
    """
    def __init__(self, num_gyms, num_pokemons):
        super().__init__(num_gyms * num_pokemons)
        self.num_gyms = num_gyms
        self.num_pokemons = num_pokemons
        self.time = float('inf')
    
    def __repr__(self) -> str:
        return str([list(compress(pokemon_name, x)) for x in self.cut_into_gyms()])

    def check_if_valid(self) -> bool:
        count = [0] * self.number_genes
        for gene in self.cut_into_gyms():
            count = list(map(lambda x,y: x + 1 if y else x, count, gene))
            if True not in gene:
                # There is a gym setup with no fighting pokemon
                return False
        if max(count) > POKEMON_MAX_ENERGY:
            # There is a pokemon exceeding its energy limits
            return False
        if min(count) == POKEMON_MAX_ENERGY:
            # At least one must have energy at the end
            return False
        return True

    def cut_into_gyms(self) -> list:
        # Return the sequence in the format of a list of lists
        return [self.sequence[x:x+self.num_pokemons] for x in range(0, self.num_gyms*self.num_pokemons, self.num_pokemons)]
    
    def calculate_time(self) -> float:
        time = 0
        sequence = self.cut_into_gyms()
        for i in range(0, self.num_gyms):
            total_factor = sum(compress(pokemon_power, sequence[i]))  
            time += gym_time(i, total_factor)
        return time

    def calculate_fitness(self) -> float:
        return (( 1 / self.calculate_time() ) * 10000)

    def add_random_pokemon(self):
        rand_int = random.randrange(0, self.num_gyms * self.num_pokemons)
        self.sequence[rand_int] = True
        if not self.check_if_valid():
            for x in range(5):
                if self.sequence[rand_int // 12 + x]:
                    self.sequence[rand_int // 12 + x] = False
        self.valid = None
        self._fitness = None

    def remove_random_pokemon(self):
        rand_int = random.randrange(0, self.num_gyms * self.num_pokemons)
        while(not self.sequence[rand_int]):
            rand_int = random.randrange(0, self.num_gyms * self.num_pokemons)
        self.sequence[rand_int] = False
        self.valid = None
        self._fitness = None

    def exchange_random_pokemon(self):
        rand_gym_i = random.randrange(self.num_gyms) * self.num_pokemons
        rand_gym_j = random.randrange(self.num_gyms) * self.num_pokemons
        all_i = []
        all_j = []
        for x in range(self.num_pokemons):
            if self.sequence[rand_gym_i + x]:
                all_i.append(x)
            if self.sequence[rand_gym_j + x]:
                all_j.append(x)
        if len(all_i) == 0 or len(all_j) == 0:
            return
        rand_i = random.choice(all_i)
        rand_j = random.choice(all_j)
        self.sequence[rand_gym_i + rand_i] = False
        self.sequence[rand_gym_i + rand_j] = True
        self.sequence[rand_gym_j + rand_j] = False
        self.sequence[rand_gym_j + rand_i] = True
        self.valid = None
        self._fitness = None
        

    def scramble_gymns(self):
        rand_gym_i = random.randrange(0, self.num_gyms)
        rand_gym_j = random.randrange(0, self.num_gyms)
        aux = self.sequence[rand_gym_i*self.num_pokemons:(rand_gym_i + 1)*self.num_pokemons]
        self.sequence[rand_gym_i*self.num_pokemons:(rand_gym_i + 1)*self.num_pokemons] = self.sequence[rand_gym_j*self.num_pokemons:(rand_gym_j + 1)*self.num_pokemons]
        self.sequence[rand_gym_j*self.num_pokemons:(rand_gym_j + 1)*self.num_pokemons] = aux
        self.valid = None
        self._fitness = None

    def reverse_random_gym(self):
        rand_gym_i = random.randrange(0, self.num_gyms)
        self.sequence[rand_gym_i*self.num_pokemons:(rand_gym_i + 1)*self.num_pokemons] = self.sequence[rand_gym_i*self.num_pokemons:(rand_gym_i + 1)*self.num_pokemons][::-1]
        self.valid = None
        self._fitness = None

def init_generation(number_of_individuals:int) -> List[PokemonSelection]:
    new_pool = []
    for _ in range(0, number_of_individuals):
        new_individual = PokemonSelection(n_gyms, n_pokemons)
        while(not new_individual.is_valid):
            new_individual = PokemonSelection(n_gyms, n_pokemons)
            for gym_id in range(0, new_individual.num_gyms):
                rand_pokemon = random.randrange(0, n_pokemons)
                new_individual.sequence[gym_id * n_pokemons + rand_pokemon] = True
                extra_pokemon = random.randrange(0, n_pokemons * 3)
                if extra_pokemon < n_pokemons:
                    new_individual.sequence[gym_id * n_pokemons + extra_pokemon] = True
        new_pool.append(new_individual)
    return sorted(new_pool, key=lambda x: x.fitness)


def random_individual_to_crossover(pool:List[PokemonSelection], modifier:int=1) -> int:
    p = pool
    if modifier > 10:
        modifier = 10
    rand_i = random.randrange(0, 100) / 100
    pool_total_fitness = sum((x.fitness ** modifier) for x in p)
    for i in p:
        i_fitness_modified = i.fitness ** modifier
        if (i_fitness_modified / pool_total_fitness) > rand_i:
            return p.index(i)
        rand_i -= i_fitness_modified / pool_total_fitness

def cut_worst(pool:List[PokemonSelection], n) -> List[PokemonSelection]:
    cut = pool[-n:]
    cut = cut + init_generation(int(INIT_GENERATION / 2))
    cut = list(set(cut))
    return cut

def add_random_pokemon(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.add_random_pokemon()
    return c

def remove_random_pokemon(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.remove_random_pokemon()
    return c

def exchange_pokemon(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.exchange_random_pokemon()
    return c

def exchange_multiple_pokemon(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    for _ in range(0,3):
        c.exchange_random_pokemon()
    return c

def scramble_gymns(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    for _ in range(0,5):
        c.scramble_gymns()
    return c

def reverse_sequence(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.reverse()
    return c
    
def random_shift(p:PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    rand_int = random.randrange(0, 3 * p.number_genes // 4)
    rand_choice = random.choice([False, True])
    if rand_choice:
        c.shift_left(rand_int)
    else:
        c.shift_right(rand_int)
    return c

def mutate(p:PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.mutate()
    while(not c.is_valid):
        c.mutate()
    return c

def reverse_random_gym(p:PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.reverse_random_gym()
    return c

def cross_individuals(p1:List[PokemonSelection], p2:List[PokemonSelection]) -> List[PokemonSelection]:
    cross_childs = []
    for x in range(0, len(p1)):
        if p1[x] != p2[x]:
            child1,child2 = PokemonSelection.crossover(p1[x], p2[x])
            if child1.is_valid:
                cross_childs.append(child1)
            if child2.is_valid:
                cross_childs.append(child2)
    return cross_childs

def apply_disturbances(selected:List[PokemonSelection], func:List[Callable]) -> List[PokemonSelection]:
    childs = []
    for x in selected:
        prev = x
        for f in func:
            prev = f(prev)
            c = f(x)
            if c.is_valid:
                childs.append(c)
        if prev.is_valid:
            childs.append(prev)
    return childs


def gena():
    # Run the genetic algortihm
    pool = init_generation(INIT_GENERATION)
    previous_best = pool[0]
    generations_without_improvement = 0
    total_generations = 0
    ini_time = time.time()
    loop = tqdm(total=MAX_GENERATION_WITHOUT_IMPROVMENT)
    while generations_without_improvement < MAX_GENERATION_WITHOUT_IMPROVMENT:
        loop.set_description(f"Pool {len(pool)} Best {previous_best.calculate_time()}")
        if len(pool) > MAX_POP:
            pool = cut_worst(pool, int(INIT_GENERATION / 2))
        #pool = pool + init_generation(5)
        
        cross_childs = cross_individuals([pool[random_individual_to_crossover(pool, generations_without_improvement)] for _ in range(0, 10)], [pool[random_individual_to_crossover(pool, generations_without_improvement)] for _ in range(0, 10)])
        
        w_random_individuals = [pool[random_individual_to_crossover(pool)] for _ in range(0, 5)] + cross_childs
        
        pool.extend(apply_disturbances(w_random_individuals, [scramble_gymns, exchange_pokemon, reverse_sequence, random_shift, remove_random_pokemon, add_random_pokemon, reverse_random_gym, exchange_multiple_pokemon]))
        

        # Sort and update running info
        total_generations += 1
        pool.sort(key=lambda x: x.fitness)
        best = pool[-1]
        if best.calculate_time() >= previous_best.calculate_time():
            generations_without_improvement += 1
            loop.update(1)
        else:
            previous_best = best
            generations_without_improvement = 0
            loop.reset(MAX_GENERATION_WITHOUT_IMPROVMENT)

    print(f"\nTotal generations {total_generations}.\tExecution Time {time.time() - ini_time} seconds.\nResult {pool[-1].calculate_time()} = {[list(compress(pokemon_name, x)) for x in pool[-1].cut_into_gyms()]}")
    return pool[-1].calculate_time()
    result_per_gym = []
    i = 0
    for gym in pool[-1].cut_into_gyms():
        result_per_gym.append(gym_time(i, sum(compress(pokemon_power, gym))))
        i += 1
    return result_per_gym

#a = gena()
'''
i = 0
best = 0
for i in range(100):
    a = gena()
    if '379.54' in str(sum(a)) :
        print('BEST!')
        best = best + 1
print('succes rate ' + str(best) + '%')
'''

a = gena()
