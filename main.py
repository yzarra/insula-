import pygame
pygame.init()
from customizer import Customizer

def main():
    customizer = Customizer()  # create instance of customizer class 

    # variables
    start_screen = True
    running = True

    # get user's screen size
    display_info = pygame.display.Info()
    screenWidth = display_info.current_w
    screenHeight = display_info.current_h

    # setup window
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()  # frame rate (fps)

    # colours
    white = (255, 255, 255)
    green = (170, 230, 185)
    orange = (240, 182, 144)
    
    # fonts
    mainFont = pygame.font.Font(None, 36)
    smallMainFont = pygame.font.Font(None, 24)

    # buttons 
    startButton = pygame.Rect(screenWidth // 2 - 100, screenHeight // 2 - 25, 200, 50)
    exitButton = pygame.Rect(screenWidth - 90, 10, 80, 30) 

    # draw main menu window
    def draw_start_screen():
        screen.fill(green)
        # start button
        pygame.draw.rect(screen, white, startButton)
        text_surface = mainFont.render("Start Game", True, orange)
        text_rect = text_surface.get_rect(center=startButton.center)
        screen.blit(text_surface, text_rect)
        # exit button
        pygame.draw.rect(screen, orange, exitButton)
        exit_text = smallMainFont.render("Exit", True, white)
        exit_text_rect = exit_text.get_rect(center=exitButton.center)
        screen.blit(exit_text, exit_text_rect)

    # draw gameplay screen
    def draw_gameplay_screen():
        screen.fill((0, 0, 0))
        # exit button
        pygame.draw.rect(screen, orange, exitButton)
        exit_text = smallMainFont.render("Exit", True, white)
        exit_text_rect = exit_text.get_rect(center=exitButton.center)
        screen.blit(exit_text, exit_text_rect)

    while running:
        for event in pygame.event.get():  # processes events (clicks, window close, etc.)
            # manage exiting game
            if event.type == pygame.QUIT:
                running = False
            # handle exit button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.collidepoint(event.pos):
                    running = False
                # handle start button
                elif start_screen and startButton.collidepoint(event.pos):
                    start_screen = False
                    customizer.overall()
            # handle resizing window        
            elif event.type == pygame.VIDEORESIZE:
                screenWidth, screenHeight = event.w, event.h
                screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
                startButton.center = (screenWidth // 2, screenHeight // 2)
                exitButton.topleft = (screenWidth - 90, 10)

        # draw starting screen
        if start_screen:
            draw_start_screen()
        # handle starting screen false
        else:
            draw_gameplay_screen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":  # call main to start the main method
    main()
