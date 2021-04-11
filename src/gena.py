"""
Genetic Algorithm (GENA)
This module implements a genetic algorithm to solve the combinatorial problem
    to find the best pokemons to fight in each gymnasium

"""

import random
from copy import deepcopy
from itertools import compress
from pathlib import Path
from typing import List
from tqdm import tqdm

import numpy as np
import pandas as pd

POKEMON_MAX_ENERGY = 5


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
    def crossover(first, second):
        first, second = deepcopy(first), deepcopy(second)
        rand_i = random.randrange(0, first.number_genes)
        rand_f = rand_i + random.randrange(0, first.number_genes - rand_i)
        aux = first.sequence[rand_i:rand_f]
        first.sequence[rand_i:rand_f] = second.sequence[rand_i:rand_f]
        second.sequence[rand_i:rand_f] = aux
        first.chance_mutate()
        second.chance_mutate()
        first._fitness = None
        first.valid = None
        second._fitness = None
        second.valid = None
        return first, second

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
    
    def calculate_fitness(self) -> float:
        time = 0
        sequence = self.cut_into_gyms()
        for i in range(0, self.num_gyms):
            total_factor = sum(compress(pokemon_power, sequence[i]))  
            time += gym_time(i, total_factor)
        return time

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
        self.sequence[rand_int] = False
        self.valid = None
        self._fitness = None

    def exchange_random_pokemon(self):
        rand_i = random.randrange(0, self.num_pokemons)
        rand_j = random.randrange(0, self.num_pokemons)
        for gym_i in range(0, self.num_gyms):
            if self.sequence[gym_i * 5 + rand_i]:
                self.sequence[gym_i * 5 + rand_i] = False
                self.sequence[gym_i * 5 + rand_j] = True
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

def init_generation(number_of_individuals:int) -> List[PokemonSelection]:
    new_pool = []
    for individual_id in range(0, number_of_individuals):
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


def random_individual_to_crossover(pool:List[PokemonSelection]) -> int:
    p = pool[:10] + pool[-50:]
    rand_i = random.randrange(0, 100) / 100
    pool_total_fitness = sum(x.fitness for x in p)
    for i in p:
        if (i.fitness / pool_total_fitness) > rand_i:
            return p.index(i)
        rand_i -= i.fitness / pool_total_fitness

def cut_worst(pool:List[PokemonSelection]) -> List[PokemonSelection]:
    if len(pool) > 1000:
        cut = pool[:250]
        cut = cut + init_generation(10)
        cut.sort(key=lambda x: x.fitness)
        return cut
    return pool

def add_random_pokemon(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.add_random_pokemon()
    return c

def exchange_pokemon(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.exchange_random_pokemon()
    return c

def scramble_gymns(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.scramble_gymns()
    return c

def reverse_sequence(p: PokemonSelection) -> PokemonSelection:
    c = deepcopy(p)
    c.reverse()
    return c


def gena():
    # Run the genetic algortihm
    pool = init_generation(100)
    n_generations = 10
    loop = tqdm(range(0, n_generations))
    for n_generation in loop:
        loop.set_description(f"Pool {len(pool)}")
        pool = cut_worst(pool)
        
        #individuals_to_cross = [random_individual_to_crossover(pool) for x in range(0, 10)]
        #individuals_to_cross2 = [random_individual_to_crossover(pool) not in individuals_to_cross for x in range(0, 10)]

        individuals_to_cross = [x for x in range(10)]
        individuals_to_cross2 = [x for x in range(11,20)]
        for x in set(individuals_to_cross):
            for y in set(individuals_to_cross2):
                if x != y:
                    child1,child2 = PokemonSelection.crossover(pool[x], pool[y])
                    if child1.is_valid:
                        pool.append(child1)
                    if child2.is_valid:
                        pool.append(child2)

        random_individuals = [random.randrange(0, len(pool)) for x in range(0, 50)] # Select 20 random
        top_5p = [random.randrange(int(len(pool)*0.95), len(pool)) for x in range(0, 15)] # Select 5 random at best 5%
        worst_5p = [random.randrange(0, int(len(pool)*0.05)) for x in range(0, 15)] # Select 5 random at worst 5%

        selected = set(random_individuals + top_5p + worst_5p)
        for x in selected:
            rand1 = add_random_pokemon(pool[x])
            if rand1.is_valid:
                pool.append(rand1)
            rand2 = scramble_gymns(pool[x])
            if rand2.is_valid:
                pool.append(rand2)
            rand3 = exchange_pokemon(pool[x])
            if rand3.is_valid:
                pool.append(rand3)
            rand4 = reverse_sequence(pool[x])
            if rand4.is_valid:
                pool.append(rand4)
            

        pool.sort(key=lambda x: x.fitness)
    print(f"Result {pool[0].fitness} = {[list(compress(pokemon_name, x)) for x in pool[0].cut_into_gyms()]}")
    result_per_gym = []
    i = 0
    for gym in pool[0].cut_into_gyms():
        result_per_gym.append(gym_time(i, sum(compress(pokemon_power, gym))))
        i += 1
    return result_per_gym

a = gena()