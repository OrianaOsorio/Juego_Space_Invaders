import pygame
import random
from pygame.locals import *

# Inicializar PyGame
pygame.init()


# Configuración de la pantalla
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Space Invaders")


# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Clase para la nave espacial
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2 + 230)  # Posición inicial centrada, bajada 230 píxeles
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

# Clase para los proyectiles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear enemigos
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Reloj del juego
clock = pygame.time.Clock()

# Puntuación
score = 0

# Estado del juego
game_over = False
paused = False

# Game loop
running = True
while running:
    # Actualizar
    clock.tick(60)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                paused = not paused
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speed_x = 0

    # Si el juego está en pausa, no se actualizan los sprites ni se realizan las colisiones
    if not paused:
        # Actualizar sprites
        all_sprites.update()

        # Colisiones entre proyectiles y enemigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Colisiones entre jugador y enemigos
        if pygame.sprite.spritecollide(player, enemies, False):
            game_over = True

    # Renderizar
    screen.fill(black)
    all_sprites.draw(screen)

    # Mostrar puntuación
    font = pygame.font.Font(None, 36)
    text = font.render("Puntuación: " + str(score), True, white)
    screen.blit(text, (10, 10))

    # Si el juego está en pausa, mostrar el mensaje correspondiente
    if paused:
        pause_text = font.render("Pausa", True, white)
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2))

    # Actualizar pantalla
    pygame.display.flip()

    # Si el juego ha terminado, mostrar la pantalla de Game Over y esperar antes de cerrar
    if game_over:
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, white)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2)
        screen.fill(black)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

# Finalizar PyGame
pygame.quit()
