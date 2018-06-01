# Imports
import pygame
import random
import xbox360_controller

# Initialize game engine
pygame.init()



# Window
WIDTH = 1000
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# make a controller
my_controller = xbox360_controller.Controller(0)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font('assets/Fonts/SPACEBAR.ttf', 64)
FONT_XL = pygame.font.Font('assets/Fonts/SPACEBAR.ttf', 96)

''' Make stars '''
stars = []
for i in range(800):
    x = random.randrange(-100, 1102)
    y = random.randrange(-200, 620)
    r = random.randrange(1,5)
    s = [x, y, r, r]
    stars.append(s)

# Images
ship_img = pygame.image.load('assets/images/playerShip3_blue.png')
laser_img = pygame.image.load('assets/images/laserBlue03.png')
mob_img = pygame.image.load('assets/images/enemyRed3.png')
mob2_img = pygame.image.load('assets/images/shipBlue.png')
bomb_img = pygame.image.load('assets/images/laserRed13.png')
SPLASH = pygame.image.load('assets/images/splash')


# Sounds
START_BACKGROUND = pygame.mixer.Sound('assets/sounds/background.ogg')
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
END_BACKGROUND = pygame.mixer.Sound('assets/sounds/end.ogg')
PLAYING_BACKGROUND = pygame.mixer.Sound('assets/sounds/playing.ogg')



# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 10
        self.shield = 2
        
    def move(self, left_x):
        self.rect.x += self.speed * left_x
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, shield):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.shield = shield

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            self.shield -= 1

        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += 1
            self.shield -= 1

            if self.shield < 0:
                self.kill()


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

def setup():
    global ship, player, lasers, mobs, bombs, fleet, stage
    # Make game objects
    ship = Ship(384, 536, ship_img)
    mob1 = Mob(128, 64, mob2_img, 5)
    mob2 = Mob(256, 64, mob2_img, 5)
    mob3 = Mob(384, 64, mob2_img, 5)
    mob4 = Mob(128, 150, mob_img, 5)
    mob5 = Mob(256, 150, mob_img, 5)
    mob6 = Mob(384, 150, mob_img, 5)
    mob7 = Mob(128, 50, mob_img, 5)


    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    
    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)

    stage = START
    pygame.mixer.music.load('assets/sounds/background.ogg')
    pygame.mixer.music.play(2)

# stages
START = 0
PLAYING = 1
END = 2
  
# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    t_rect = title_text.get_rect()
    t_rect.centerx = WIDTH /2
    t_rect.bottom = HEIGHT / 2
    screen.blit(title_text, t_rect)
    screen.blit(SPLASH, [50, 200])

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    shield_text = FONT_MD.render(str(ship.shield), 1, WHITE)
    screen.blit(score_text, [32, 32])
    screen.blit(shield_text, [32, 50])

    if ship.shield == 2:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100,100,18])
    elif ship.shield == 1:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, GREEN, [20,100, 50, 18])
    else:
        pygame.draw.rect(screen, WHITE, [20,100,100,18])
        pygame.draw.rect(screen, RED, [20,100,0,18])

# Game loop
setup()
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYBUTTONDOWN:
            print("button")
            if stage == START:
                if event.button == xbox360_controller.START:
                    stage = PLAYING
                    print("start")
            elif stage == PLAYING:
                if event.button ==xbox360_controller.A :
                    ship.shoot()
                    pygame.mixer.music.load('assets/Sounds/playing.ogg')
                    pygame.mixer.music.play(2)
            elif stage == END:
                restart_text = FONT_LG.render("Press tab to restart.", 1, WHITE)
                r_rect = restart_text.get_rect()
                r_rect.centerx = WIDTH / 2
                r_rect.bottom = HEIGHT / 2
                
                screen.blit(restart_text, r_rect)

                if event.button == xbox360_controller.START:
                    setup()

    if stage == PLAYING:
        left_x, _ = my_controller.get_left_stick()

        ship.move(left_x)     
            
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
        if len(player) == 0:
            stage = END
            pygame.mixer.music.load('assets/Sounds/end.ogg')
            pygame.mixer.music.play(2)
        if len(mobs) == 0:
            stage = END
            pygame.mixer.music.load('assets/Sounds/end.ogg')
            pygame.mixer.music.play(2)
            

    for r in stars:
        r[1]+=2

        if r[1] >620:
            r[1] = random.randrange(-800, -200)
            r[0] = random.randrange(-500,1102)
     
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)

    ''' stars '''
    for s in stars:
        pygame.draw.ellipse(screen, WHITE, s)

        
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
