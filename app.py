import pygame

from attrib import Color, Hud, Images, Screen, Thug, Warrior


def main():
    # initiating modules
    pygame.init()
    pygame.display.set_caption('Be a warrior')
    logo = pygame.image.load('res/warrior_right_0.png')
    pygame.display.set_icon(logo)

    # reference clock
    clock = pygame.time.Clock()

    # screen
    screen = pygame.display.set_mode(Screen.get_dimensions())
    screen.fill(Color.BLACK)

    # loading required objects
    Images()
    warrior = Warrior()
    thugs = [Thug() for i in range(Thug.count)]
    hud = Hud()

    while not Screen.EXIT:
        # update time
        Screen.TIME_SEC = int(pygame.time.get_ticks()/1000)
        
        # random movement of thugs
        for thug in thugs:
            thug.move()

        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Screen.EXIT = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    warrior.move_left()
                elif event.key == pygame.K_RIGHT:
                    warrior.move_right()
                elif event.key == pygame.K_UP:
                    warrior.move_up()
                elif event.key == pygame.K_DOWN:
                    warrior.move_down()

        # screen update for each iteration
        screen.blit(Images.image_background, (0,0))
        # blitting being objects
        screen.blit(warrior.image, warrior.get_position())
        for thug in thugs:
            screen.blit(thug.image, thug.get_position())
        # blitting hud with score
        hud_surface = hud.render_surface(score=Screen.TIME_SEC)
        screen.blit(hud_surface, (0, 0))
        # controls the frame rate
        clock.tick(Screen.FRAME_RATE)

        # redraws complete screen
        pygame.display.update()

if __name__ == '__main__':
    main()
    pygame.quit()
