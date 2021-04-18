from interface import *

def main():
    global SCREEN
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global map_list
    global sprite_index
    global trainer_sprites
    global aStar_struct
    #Create map 
    pandas_map = Map(input_path.joinpath("map.csv"),input_path.joinpath("cellweights.csv"))
    
    aStar_struct = Astar(pandas_map)

    WINDOW_HEIGHT  = pandas_map.xlen * blockSize # blocksize in px * tiles for map = size of window 
    WINDOW_WIDTH = pandas_map.ylen * blockSize
    map_list = pandas_map.map.values.tolist()


    #initialize visual componets
    pygame.init()
    clock = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption('Pokémon IA')
    trainer_sprites = setupTrainer()
    trainer_sprite_index = 0
    pokeball_sprites = setupPokeballPath()
    trainer_pokeball_index = 0
    #invert position because map is inverted
    player_position = (pandas_map.start_point[1],pandas_map.start_point[0])
    battle_list,trainers_list = setupBattles()
    next_step = 0 #variable to time player animation

    while running:
        checkEvents()
        drawGrid()
        drawBattles(battle_list,trainers_list)
        drawTrainer(trainer_sprites,trainer_sprite_index,player_position)
        if not aStar_struct.over:
            drawAstar(open_nodes,closed_nodes)
        drawPokeballPath(pokeball_sprites,trainer_pokeball_index,best_path)
        pygame.display.update()

        trainer_pokeball_index = (trainer_pokeball_index + 1) % 8 
        if next_step % 4 == 0: 
            trainer_sprite_index = (trainer_sprite_index + 1) % 4
        next_step += 1
        clock.tick(60) #60 FPS

main()