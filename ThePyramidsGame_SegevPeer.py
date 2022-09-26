# Made by Segev Peer
import random
import pygame

# Some reference variables
WIDTH = 600
HEIGHT = 600
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

def add_text(where, label, pos):  # This function adds text to the window
    font = pygame.font.Font(None, 36)  # Uses default font and defines font size
    text = font.render(label, True, (10, 10, 10))  # Draw text on new surface
    where.blit(text, pos)  # Adds the new surface to where it should go


def start_button(mouse, screen, posx, posy, sizex, sizey):  # Creates a start button on the main menu
    if posx <= mouse[0] <= posx + sizex and posy <= mouse[1] <= posy + sizey:  # changes the color of button
        pygame.draw.rect(screen, color_light, [posx, posy, sizex, sizey])

    else:
        pygame.draw.rect(screen, color_dark, [posx, posy, sizex, sizey])  # changes the color of button
    add_text(screen, 'Start', (220, 210))


def quit_button(mouse, screen, posx, posy, sizex, sizey):  # Creates a quit button on the main menu

    if posx <= mouse[0] <= posx + sizex and posy <= mouse[1] <= posy + sizey:  # changes the color of button
        pygame.draw.rect(screen, color_light, [posx, posy, sizex, sizey])

    else:
        pygame.draw.rect(screen, color_dark, [posx, posy, sizex, sizey])  # changes the color of button
    add_text(screen, 'Quit', (220, 360))


def check_yellow(pyr, i):  # Checks for illegal yellow bricks
    count = 0  # Counts how many bricks the Program found
    for j in range(4 - i, 5 + i):  # Check the whole row
        if pyr[i][j] == 'y':
            count = count + 1
            if count == 4:
                return True  # The whole row needs to be replaced
    return False  # Less than 4 yellow bricks


def swap(pyr, i, j, screen):  # Swaps the illegal brick with a random one
    pygame.event.get() # Clears the event log so the program will not get stuck
    clock = pygame.time.Clock()  # Clock definition
    a = ['b', 'p', 'y']  # b is for blue, p is for pink and y is for Yellow
    pyr[i][j] = random.choice(a)
    draw_cube(screen, pyr[i][j], i, j)  # Adds the new brick to the screen
    clock.tick(60)  # Defines the speed everything moves around
    return pyr


def switch_illegal(pyr, screen):  # Flags illegal bricks and switch them
    keep_play = False  # If no illegal were found we will return false
    for i in range(0, 5):
        for j in range(4 - i, 5 + i):
            if pyr[i][j] == 'b':  # Checks for illegal blue bricks
                if i == 0 or i == 4:
                    pyr = swap(pyr, i, j, screen)
                    keep_play = True
                if 0 < i < 4:
                    if pyr[i][j - 1] == 'e' or pyr[i][j + 1] == 'e':
                        pyr = swap(pyr, i, j, screen)
                        keep_play = True
            if pyr[i][j] == 'p':  # Checks for illegal pink bricks
                if i == 0:
                    if pyr[i + 1][j] == 'b':
                        pyr = swap(pyr, i, j, screen)
                        keep_play = True
                if i == 4:
                    if j == 0:
                        if pyr[i][j + 1] == 'b':
                            pyr = swap(pyr, i, j, screen)
                            keep_play = True
                    if j == 8:
                        if pyr[i][j - 1] == 'b':
                            pyr = swap(pyr, i, j, screen)
                            keep_play = True
                    if 0 < j < 8:
                        if pyr[i][j - 1] == 'b' or pyr[i - 1][j] == 'b' or pyr[i][j + 1] == 'b':
                            pyr = swap(pyr, i, j, screen)
                            keep_play = True
                if 0 < i < 4:
                    if pyr[i][j - 1] == 'b' or pyr[i + 1][j] == 'b' or pyr[i - 1][j] == 'b' or pyr[i][j + 1] == 'b':
                        pyr = swap(pyr, i, j, screen)
                        keep_play = True
            if pyr[i][j] == 'y':  # Checks for illegal yellow bricks
                if 2 <= i <= 4:
                    if check_yellow(pyr, i):
                        for e in range(4 - i, 5 + i):
                            pyr = swap(pyr, i, e, screen)
                        keep_play = True
    return keep_play


def draw_cube(screen, color, i, j):  # Draw a brick on the screen based on the given color
    if color == 'b':
        r = pygame.draw.rect(screen, (0, 0, 255), [25 + j * 50, 50 + i * 50, 50, 50])
        pygame.display.update(r)
        return
    if color == 'p':
        r = pygame.draw.rect(screen, (255, 192, 203), [25 + j * 50, 50 + i * 50, 50, 50])
        pygame.display.update(r)
        return
    if color == 'y':
        r = pygame.draw.rect(screen, (255, 234, 0), [25 + j * 50, 50 + i * 50, 50, 50])
        pygame.display.update(r)
        return


def start_game(screen):  # Creates the initial pyramid
    rounds = 0
    pyr = [['e' for i in range(9)] for j in range(5)]
    a = ['b', 'p', 'y']
    for i in range(0, 5):
        for j in range(4 - i, 5 + i):
            pyr[i][j] = random.choice(a)
            draw_cube(screen, pyr[i][j], i, j)
    while switch_illegal(pyr, screen):  # This loop will run until the pyramid is solved
        rounds = rounds + 1
    return rounds


def main():  # Creates the main menu
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('The Pyramids Game by Segev Peer')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background.fill((230, 230, 230))

    # Display some text
    add_text(background, "The Pyramids game", (140, 0))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    st = 0  # if 0 the start button will be added otherwise it will not
    rounds=0
    while True:
        mouse = pygame.mouse.get_pos()
        if st == 0:
            start_button(mouse, screen, 180, 200, 140, 40)
            quit_button(mouse, screen, 180, 350, 140, 40)
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:  # Checks if a button was clicked

                if 180 <= mouse[0] <= 180 + 140 and 350 <= mouse[1] <= 350 + 40:
                    pygame.quit()
                if st == 0:
                    if 180 <= mouse[0] <= 180 + 140 and 200 <= mouse[1] <= 200 + 40:
                        screen.fill((230, 230, 230))
                        st = 1
                        rounds=start_game(screen)
                        add_text(screen, "You Won in " + str(rounds) + " rounds!", (140, 240))
        pygame.display.update()


main()
