# First assignment for the Artificial Intelligence Course
Best pokemon set for the battles: 379.54278050230073 units of time

The path cost: 293 units of time

Both: 672.54278050230073 units of time
<p align="center">
  
<img src="./docs/video_rota.gif" style="text-align:center" width="450" height="450">

</p>

A better video representing the interface is avaliable <a href="./docs/video_rota.mp4"> here </a>
  
To execute, run the code at <a href="./src/interface.py"> interface.py </a>

## The assignment
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

For the combinatorial problem, we decided to go with a genetic algorithm that we called [GENA](./src/gena.py). It consists on creating random initial choices to battle all gyms, that we call individuals or chromossomes. Then, the algorithm crosses the best individuals and make random modifications in order to create better children, which are measured by the total time spent on gyms.

## Performance
We were able to find the time mentioned result for the battles in less than 12 seconds. But it usually takes a little more and we can not garantee it will ever find the best solution.


## Explanation (pt-BR)

[![EXPLANATION_PT_BR_YOUTUBE](https://img.youtube.com/vi/FeiCFcLdaTI/0.jpg)](https://www.youtube.com/watch?v=FeiCFcLdaTI)

