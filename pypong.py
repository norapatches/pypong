import pygame, random, sys

"""
pyPong
made by Norbert Kovács-Wilczyński in March, 2024
v 0.2
"""

BLK = (0, 0, 0)
WHT = (255, 255, 255)
WINDOWSIZE = (800, 600)
FPS = 60
BALLSIZE = 10
BLIP = './blip.wav'

# CLASSES
# BALL
class Ball:
    def __init__(self, x, y) -> None:
        random_x = random.randint(-1, 1)
        while random_x == 0:
            random_x = random.randint(-1, 1)
        random_y = random.randint(-1, 1)
        while random_y == 0:
            random_y = random.randint(-1, 1)
        self.x = x
        self.y = y
        self.dir_x = random_x
        self.dir_y = random_y
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, BALLSIZE, BALLSIZE)
    
    # DRAW THE BALL
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, WHT, self.rect)
    
    # MOVE THE BALL
    def move(self) -> None:
        self.rect.move_ip(self.dir_x * self.speed, self.dir_y * self.speed)
    
    # BOUNCE IF HIT SOMETHING
    def bounce(self, axis, sound) -> None:
        if axis == 'x':
            sound.play()
            self.dir_x *= -1
        elif axis == 'y':
            sound.play()
            self.dir_y *= -1
    
    # ADJUST SPEED
    def ball_speed(self, total) -> None:
        if total != 0 and total % 5 == 0:
            self.speed *= 1.1

# PLAYER 1/2
class Player:
    def __init__(self, x ,y, id) -> None:
        self.id = id
        self.score = 0
        self.x = x
        self.y = y
        self.speed = 4
        self.psize = WINDOWSIZE[1] / 6
        self.rect = pygame.Rect(self.x, self.y, BALLSIZE, self.psize)
    
    # DRAW THE PADDLE
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, WHT, self.rect)
    
    # MOVE THE PADDLE
    def move(self) -> None:
        # 1P CONTROLS
        if self.id == 'p1':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.rect.move_ip(0, -self.speed)
            if keys[pygame.K_s]:
                self.rect.move_ip(0, self.speed)
        # 2P CONTROLS
        elif self.id == 'p2':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.rect.move_ip(0, -self.speed)
            if keys[pygame.K_DOWN]:
                self.rect.move_ip(0, self.speed)
    
    # COLLIDE WITH WALLS
    def check_bounds(self, screen_height) -> None:
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
    
    # UPDATE SCORE
    def bonus(self, score, x, y) -> None:
        self.score = score
        if self.score != 0 and self.score % 10 == 0:
            self.psize *= 1.1
            self.rect = pygame.Rect(x, y, BALLSIZE, self.psize)

# CPU OPPONENT
class CPU:
    def __init__(self, x, y) -> None:
        self.score = 0
        self.x = x
        self.y = y
        self.speed = 4
        self.psize = WINDOWSIZE[1] / 6
        self.rect = pygame.Rect(self.x, self.y, BALLSIZE, self.psize)
    
    # DRAW THE PADDLE
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, WHT, self.rect)
    
    # MOVE PADDLE BASED ON BALL POSITION
    def cpu_move(self, ball) -> None:
        if ball.rect.bottom > self.rect.bottom:
            self.rect.move_ip(0, self.speed)
        elif ball.rect.top < self.rect.top:
            self.rect.move_ip(0, -self.speed)
    
    # COLLIDE WITH WALLS
    def check_bounds(self, screen_height) -> None:
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
    
    # UPDATE SCORE
    def bonus(self, score, x, y) -> None:
        self.score = score
        if self.score != 0 and self.score % 10 == 0:
            self.psize *= 1.1
            self.rect = pygame.Rect(x, y, BALLSIZE, self.psize)

# THE GAME CLASS
class TheGame:
    # GAME SETUP
    def __init__(self, width=WINDOWSIZE[0], height=WINDOWSIZE[1]) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # FONTS AND SIZES
        self.title_font = pygame.font.SysFont('Ubuntu', 36)
        self.text_font = pygame.font.SysFont('Ubuntu', 32)
        self.score_font = pygame.font.SysFont('Ubuntu', 24)
        self.help_font = pygame.font.SysFont('Ubuntu', 16)
        
        # SCREEN
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('pyPong')
        
        # PLAYFIELD
        # TODO
        
        # AUDIO SETUP
        pygame.mixer.init()
        self.sfx_blip = pygame.mixer.Sound(BLIP)
        
    # MAIN MENU
    def menu(self) -> str:
        """
        returns chosen game mode (str)
        """
        # BUTTONS
        button_width = WINDOWSIZE[1] / 2
        button_height = WINDOWSIZE[0] / 8
        
        but_1PvsCPU = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  self.screen.get_height() / 3 - button_height / 2,
                                  button_width, button_height)
        
        but_1Pvs2P = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  self.screen.get_height() / 3 + button_height / 2 + BALLSIZE,
                                  button_width, button_height)
        
        but_about = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  self.screen.get_height() / 3 + (button_height * 1.5) + 2 * BALLSIZE,
                                  button_width, button_height)
        
        but_quit = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  self.screen.get_height() / 3 + (button_height * 3) - 2 * BALLSIZE,
                                  button_width, button_height)
        
        buttons = [(but_1PvsCPU, '1P vs CPU'), (but_1Pvs2P, '1P vs 2P'), (but_about, 'ABOUT'), (but_quit, 'QUIT')]
        # RUN THE SCREEN
        while True:
            for event in pygame.event.get():
                # CHECK FOR EXIT GAME  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # CHECK FOR MOUSE CLICKS
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if but_1PvsCPU.collidepoint(mouse_pos):
                        return '1PvsCPU'
                    if but_1Pvs2P.collidepoint(mouse_pos):
                        return '1Pvs2P'
                    if but_about.collidepoint(mouse_pos):
                        self.about()
                    if but_quit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            # FILL WITH COLOUR
            self.screen.fill(BLK)
            # DISPLAY THE TITLE
            game_title = self.title_font.render('pyPONG', True, WHT)
            self.screen.blit(game_title, (self.screen.get_width() / 2 - game_title.get_width() / 2, 30))
            
            # DRAW ALL THE BUTTONS
            for button, label in buttons:
                pygame.draw.rect(self.screen, WHT, button, 1)
                text = self.text_font.render(label, True, WHT)
                text_rect = text.get_rect(center=button.center)
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    # ABOUT SCREEN
    def about(self) -> None:
        # BACK BUTTON
        button_width = WINDOWSIZE[1] / 4
        button_height = WINDOWSIZE[0] / 8
        
        but_back = pygame.Rect(self.screen.get_width() - (button_width + 2 * BALLSIZE),
                               self.screen.get_height() - (button_height + 2 * BALLSIZE),
                               button_width, button_height)
        
        # GAME DESCRIPTION
        game_description = '''
        pyPONG
        
        Player 1 controls:
            up: W    down: S
        Player 2 controls:
            up: UP   down: DOWN
        Press SPACE to pause the game
        Press ESC to quit
        
        The ball speed increases after successful hits
        The paddles grow after each personal 10th hit
        '''
        
        # THE LOOP
        while True:
            for event in pygame.event.get():
                # CHECK FOR EXIT GAME  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # CHECK FOR MOUSE CLICKS
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if but_back.collidepoint(mouse_pos):
                        return
            
            # FILL WITH COLOUR
            self.screen.fill(BLK)
            
            # DRAW THE TEXT DESCRIPTION
            game_text = self.text_font.render(game_description, True, WHT)
            game_text_rect = game_text.get_rect()
            self.screen.blit(game_text, game_text_rect)
            
            # DRAW BACK BUTTON
            pygame.draw.rect(self.screen, WHT, but_back, 1)
            text = self.text_font.render('BACK', True, WHT)
            text_rect = text.get_rect(center=but_back.center)
            self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
    
    # GAME OVER SCREEN
    def game_over(self, mode) -> None:
        # BUTTONS
        button_width = WINDOWSIZE[1] / 3
        button_height = WINDOWSIZE[0] / 8
        
        but_restart = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  self.screen.get_height() / 3 - (button_height / 2 + 2 * BALLSIZE),
                                  button_width, button_height)
        
        but_menu = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  self.screen.get_height() / 3 + (button_height / 2),
                                  button_width, button_height)
        
        but_quit = pygame.Rect(self.screen.get_width() / 2 - button_width / 2,
                                  (self.screen.get_height() / 3 * 2) + (button_height / 2),
                                  button_width, button_height)
        
        buttons = [(but_restart, 'RESTART'), (but_menu, 'MENU'), (but_quit, 'QUIT')]
        
        while True:
            for event in pygame.event.get():
                # CHECK FOR EXIT GAME  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # CHECK FOR MOUSE CLICKS
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if but_restart.collidepoint(mouse_pos):
                        self.game_start(mode)
                    if but_menu.collidepoint(mouse_pos):
                        new_round = self.menu()
                        self.game_start(new_round)
                    if but_quit.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            # FILL WITH COLOUR
            self.screen.fill(BLK)
            # DISPLAY THE TITLE
            game_over_txt = self.title_font.render('GAME OVER', True, WHT)
            self.screen.blit(game_over_txt, (self.screen.get_width() / 2 - game_over_txt.get_width() / 2, 30))
            
            # DRAW ALL THE BUTTONS
            for button, label in buttons:
                pygame.draw.rect(self.screen, WHT, button, 1)
                text = self.text_font.render(label, True, WHT)
                text_rect = text.get_rect(center=button.center)
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    # RESTART ROUND
    def restart(self, mode) -> None:
        if mode == '1PvsCPU':
            self.scores = [0, 0]
            self.ball = Ball(self.screen.get_width() / 2, self.screen.get_height() / 2)
            self.player = Player(0, self.screen.get_height() / 2, 'p1')
            self.opponent = CPU(self.screen.get_width() - 10, self.screen.get_height() / 2)
        elif mode == '1Pvs2P':
            self.scores = [0, 0]
            self.ball = Ball(self.screen.get_width() / 2, self.screen.get_height() / 2)
            self.player = Player(0, self.screen.get_height() / 2, 'p1')
            self.opponent = Player(self.screen.get_width() - 10, self.screen.get_height() / 2, 'p2')
    
    # THE GAME LOOP
    def game_start(self, mode) -> None:
        paused = False
        self.restart(mode)
        while True:
            for event in pygame.event.get():
                # CHECK FOR EXIT GAME  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # CHECK FOR KEYS PRESSED
                elif event.type == pygame.KEYDOWN:
                    # SPACEBAR PAUSES THE GAME
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    # ESCAPE QUITS THE GAME
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            
            # PUASE THE GAME
            if paused == True:
                # DISPLAY PAUSED TEXT
                paused_text = self.title_font.render('P A U S E D', False, WHT)
                self.screen.blit(paused_text, (self.screen.get_width() / 2 - paused_text.get_width() / 2, self.screen.get_height() / 2 - paused_text.get_height() / 2))
                
                # DISPLAY OPTIONS
                paused_text_sub = self.text_font.render('SPACE to continue, ESC to quit', False, WHT)
                self.screen.blit(paused_text_sub, (self.screen.get_width() / 2 - paused_text_sub.get_width() / 2, self.screen.get_height() / 2 - paused_text_sub.get_height() / 2 + paused_text.get_height()))
                pygame.display.flip()
                continue
            
            # FUNCTIONS TO MOVE PADDLES
            self.player.move()
            self.player.check_bounds(self.screen.get_height())
            if mode == '1PvsCPU':
                self.opponent.cpu_move(self.ball)
            elif mode == '1Pvs2P':
                self.opponent.move()
            self.opponent.check_bounds(self.screen.get_height())
            
            # LOGIC FOR BALL TO MOVE AND BOUNCE OFF WALLS
            self.ball.move()
            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.screen.get_height():
                self.ball.bounce('y', self.sfx_blip)
            
            # LOGIC FOR PENALTY FOR PLAYER
            if self.ball.rect.left <= 0:
                break
            
            # LOGIC FOR PENALTY FOR CPU/2P
            if self.ball.rect.right >= self.screen.get_width():
                break
            
            # LOGIC FOR COUNTING SCORES FOR PLAYER
            if self.ball.rect.colliderect(self.player.rect):
                self.scores[0] += 1
                self.player.bonus(self.scores[0], self.player.rect.left, self.player.rect.top)
                self.ball.bounce('x', self.sfx_blip)
                # UPDATE BALL SPEED
                total_score = self.scores[0] + self.scores[1]
                self.ball.ball_speed(total_score)
            
            # LOGIC FOR COUNTING SCORES FOR CPU
            if self.ball.rect.colliderect(self.opponent.rect):
                self.scores[1] += 1
                self.opponent.bonus(self.scores[1], self.opponent.rect.left, self.opponent.rect.top)
                self.ball.bounce('x', self.sfx_blip)
                # UPDATE BALL SPEED
                total_score = self.scores[0] + self.scores[1]
                self.ball.ball_speed(total_score)
            
            # DRAW THE ELEMENTS
            self.screen.fill(BLK)
            self.ball.draw(self.screen)
            self.player.draw(self.screen)
            self.opponent.draw(self.screen)
            
            # DRAW LINE IN THE MIDDLE
            pygame.draw.aaline(self.screen, WHT,
                                (self.screen.get_width() / 2, 0),
                                (self.screen.get_width() / 2, self.screen.get_height()))
            
            # DISPLAY SCORES
            player_score = self.score_font.render(f'{self.scores[0]}', True, WHT)
            opponent_score = self.score_font.render(f'{self.scores[1]}', True, WHT)
            
            self.screen.blit(player_score, (self.screen.get_width() / 4 - player_score.get_width() / 2, 20))
            self.screen.blit(opponent_score, ((self.screen.get_width() / 4) * 3 - opponent_score.get_width() / 2, 20))
            
            
            pygame.display.flip()
            
            self.clock.tick(FPS)
        self.game_over(mode)

# RUNNING THE GAME
if __name__ == "__main__":
    pypong = TheGame()
    game_mode = pypong.menu()
    pypong.game_start(game_mode)
