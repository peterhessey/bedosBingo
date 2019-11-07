import random
import time
import pygame
import argparse



BINGO_DATA_FILEPATH = './bingo_data.txt'

def bingoTime(bingo_data, wait_time):
    pygame.init()

    bingo_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    window_width = bingo_window.get_width()
    window_height = bingo_window.get_height()

    font = pygame.font.SysFont('Cambria', 100, True)
    


    new_number = True
    start_time = time.time()
    game_quit = False

    while bool(bingo_data) and not game_quit:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_quit = True
        
        if new_number:
            #selecting random song
            numbers_left = list(bingo_data.keys())
            index_selected = random.randint(0, len(numbers_left) - 1)
            number_to_display = numbers_left[index_selected]
            text_to_display, song_to_play = bingo_data[number_to_display]
            bingo_data.pop(number_to_display)

            bingo_window.fill((140, 26, 255))
            
            number_text = font.render(str(number_to_display), True, (255,255,255))
            phrase_text = font.render(text_to_display, True, (255,255,255))

            number_pos = (window_width /2 - number_text.get_width() / 2, 
                          window_height/2*0.8 - number_text.get_height() / 2)

            phrase_pos = (window_width /2 - phrase_text.get_width() / 2, 
                          window_height/2*1.2 - phrase_text.get_height() / 2)

            bingo_window.blit(number_text, (number_pos))
            bingo_window.blit(phrase_text, (phrase_pos))

            pygame.display.update()

            new_number = False
            start_time = time.time()
        
        time_now = time.time()

        if (time_now - start_time) > wait_time:
            new_number = True



def playSong(song):
    return 0

def readBingoFiles():
    bingo_data = {}
    
    with open(BINGO_DATA_FILEPATH) as bingo_file:
        song_data = [line.rstrip('\n').split('|') for line in bingo_file]
        
    for song_datum in song_data:
        
        bingo_data[song_datum[0]] = (song_datum[1], song_datum[2])

    return bingo_data

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Bongo\'s bingo!')
    parser.add_argument('-w', dest='wait', action='store',
                        nargs=1, default=['15'], help='How long to wait \
                                                       between numbers in \
                                                       seconds | Default = 15')


    args = parser.parse_args()
    wait_time = int(args.wait[0])
    bingo_data = readBingoFiles()
    print(bingo_data)

    bingoTime(bingo_data, wait_time)
    