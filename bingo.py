import random
import time
import pygame
import argparse



BINGO_DATA_FILEPATH = './bingo_data.txt'

def bingoTime(bingo_data, wait_time):
    """Main function, runs the bingo program using pygame.
    
    Arguments:
        bingo_data {int: (string, string)} -- The data from the bingo_data.txt
        file
        wait_time {int} -- How long to wait in seconds between displaying each
        number
    """

    #pygame set up
    pygame.init()

    bingo_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    window_width = bingo_window.get_width()
    window_height = bingo_window.get_height()
    number_font = pygame.font.SysFont('Cambria', 250, True)
    text_font = pygame.font.SysFont('Cambria', 100, True)

    #loop variables
    new_number = True
    start_time = time.time()
    game_quit = False

    #loops while there is still data in the dictionary
    while bool(bingo_data) and not game_quit:

        #check if user has tried to quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_quit = True
        
        #select next number if enough time has passed
        if new_number:
            #selecting random song
            numbers_left = list(bingo_data.keys())
            index_selected = random.randint(0, len(numbers_left) - 1)
            number_to_display = numbers_left[index_selected]
            text_to_display, song_to_play = bingo_data[number_to_display]
            bingo_data.pop(number_to_display)

            #prepare text surfaces
            bingo_window.fill((140, 26, 255))            
            number_text = number_font.render(str(number_to_display), True,
                                            (255,255,255))
            phrase_text = text_font.render(text_to_display, True,
                                          (255,255,255))

            #text position on the game window
            number_pos = (window_width /2 - number_text.get_width() / 2, 
                          window_height/2*0.7 - number_text.get_height() / 2)

            phrase_pos = (window_width /2 - phrase_text.get_width() / 2, 
                          window_height/2*1.3 - phrase_text.get_height() / 2)

            #draw and display the text
            bingo_window.blit(number_text, (number_pos))
            bingo_window.blit(phrase_text, (phrase_pos))
            pygame.display.update()

            #reset variables
            new_number = False
            start_time = time.time()
        
        #monitor passing of time
        time_now = time.time()
        if (time_now - start_time) > wait_time:
            new_number = True


def playSong(song):
    return 0

def readBingoFiles():
    """Reads the data from bingo_data.txt
    
    Returns:
        {int:(string,string)} -- The data stored in dictionary format
    """
    bingo_data = {}
    
    with open(BINGO_DATA_FILEPATH) as bingo_file:
        song_data = [line.rstrip('\n').split('|') for line in bingo_file]
        
    for song_datum in song_data:
        
        bingo_data[song_datum[0]] = (song_datum[1], song_datum[2])

    return bingo_data

if __name__=='__main__':
    #argument parsing from command line
    parser = argparse.ArgumentParser(description='Bongo\'s bingo!')
    parser.add_argument('-w', dest='wait', action='store',
                        nargs=1, default=['15'], help='How long to wait \
                                                       between numbers in \
                                                       seconds | Default = 15')


    args = parser.parse_args()
    wait_time = float(args.wait[0])
    bingo_data = readBingoFiles()

    bingoTime(bingo_data, wait_time)
    