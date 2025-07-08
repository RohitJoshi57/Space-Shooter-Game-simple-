import pygame

from random import randint, uniform

class star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Player(pygame.sprite.Sprite):
   

   def __init__ (self, groups):
      super().__init__(groups)
      self.image = pygame.image.load(r'C:\Users\rohit\Downloads\5games-main\5games-main\space shooter\images\player.png').convert_alpha()
      self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.5))
      self.direction = pygame.Vector2()
      self.speed = 300

      #Cooldown
      self.can_shoot = True
      self.laser_shoot_time = 0
      self.cooldown_duration = 400
    
   def laser_timer(self):
          if not self.can_shoot:
             current_time = pygame.time.get_ticks()
             if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
           
       

    
   def update(self, dt):
      keys = pygame.key.get_pressed()
      self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
      self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
      self.direction = self.direction.normalize() if self.direction else self.direction  
      self.rect.center += self.direction * self.speed * dt

      recent = pygame.key.get_just_pressed()
      if recent  [pygame.K_SPACE] and self.can_shoot:
         Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
         self.can_shoot = False
         self.laser_shoot_time = pygame.time.get_ticks()
      self.laser_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.2, 0.2 a ), 1)
        self.speed = randint (300, 400)


    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()

         

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()


#imports
star_surf = pygame.image.load(r'C:\Users\rohit\Downloads\5games-main\5games-main\space shooter\images\star.png').convert_alpha()
meteor_surf = pygame.image.load(r'C:\Users\rohit\Downloads\5games-main\5games-main\space shooter\images\meteor.png').convert_alpha()
laser_surf = pygame.image.load(r'C:\Users\rohit\Downloads\5games-main\5games-main\space shooter\images\laser.png').convert_alpha()

#sprites
all_sprites = pygame.sprite.Group()
for i in range(20):
    star(all_sprites, star_surf)
player = Player(all_sprites)

meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()


# events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    #frame rate
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200,  -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))
    #updates
    all_sprites.update(dt)
    collisions()


    # drawing the game
    display_surface.fill('black')
    all_sprites.draw(display_surface)

 
    pygame.display.update()

pygame.quit()
