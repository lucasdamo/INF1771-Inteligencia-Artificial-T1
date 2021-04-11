# First assignment for the Artificial Intelligence Course
As the first assignment we have the problem to solve described on [enunciado.pdf (portuguese-BR)](./docs/enunciado.pdf) or as follows:
>   A promising pokemon trainer of Viridian's city was invited to continue his training on Neon's city. To achieve his most desired training, he must go through Kanto's region. On this mission, our hero is taking his 5 pokemon and must go through several cities - 12 of which have gyminasiums
>
> Great dangers await him on this adventure! Beside the gymns there are rough paths and easier ones. He must get to his destination with at least one pokemon still with energy, so he can make its training.

The assingment states that we have to solve the path problem with A* algortihm. And gives [the cost of passing through each type of tile](./input/cellweights.csv) as follows

| Tile Representation   | Time cost (in minutes) | 
| -------------         |:-----------------------| 
| M                     | + 200                  | 
| R                     | + 5                    | 
| .                     | + 1                    |  

It alsos gives [each pokemon power](./input/pokemons.csv), [each gymnasium difficulty](./input/gymnasiums.csv) and the equation that determines how much time the trainer will spend on each gymn based on the pokemons chosen to fight. So we can determine the best combination to minimize the time spent in all gyms.

| Gymn order            | Difficulty             | 
| -------------         |:-----------------------| 
| 1                     | 55                     | 
| 2                     | 60                     | 
| 3                     | 65                     | 
| 4                     | 70                     | 
| 5                     | 75                     | 
| 6                     | 80                     | 
| 7                     | 85                     | 
| 8                     | 90                     | 
| 9                     | 95                     | 
| 10                    | 100                    | 
| 11                    | 110                    | 
| 12                    | 120                    | 

| Pokemon               | Power factor           | 
| -------------         |:-----------------------| 
| Pikachu               | 1.5                    | 
| Bulbasaur             | 1.4                    | 
| Rattata               | 1.3                    | 
| Catterpie             | 1.2                    |
| Weedle                | 1.1                    |

Gym's time spent equation:
Time = Gym's Difficulty / Sum of pokemon power factors

All of those variables can be edited on /input/ except for the time equation.

## The solution
As stated before, the path problem is solved by the [A* algortihm](./src/astar.py). It uses the manhattan distance to the final destination as its heuristic.

For the combinatorial problem, we