import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burnie: Code Jumper")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Clase para Burnie
class Burnie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("burnie.png")  # Rectángulo simple (luego reemplaza con sprite)
        self.image = pygame.transform.scale(self.image, (40, 60))  # Pelo en llamas (rojo)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 100
        self.velocity_y = 0
        self.jump_power = -15
        self.gravity = 0.8

    def update(self):
        # Aplicar gravedad
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # No caer por debajo del suelo
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0

    def jump(self):
        if self.rect.bottom == HEIGHT:  # Solo salta si está en el suelo
            self.velocity_y = self.jump_power

# Clase para plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Clase para íconos de código
class CodeIcon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
code_icons = pygame.sprite.Group()

# Crear a Burnie
burnie = Burnie()
all_sprites.add(burnie)

# Crear plataformas
ground = Platform(0, HEIGHT - 40, WIDTH, 40)
platform1 = Platform(200, 400, 200, 20)
platform2 = Platform(500, 300, 200, 20)
platforms.add(ground, platform1, platform2)
all_sprites.add(ground, platform1, platform2)

# Crear íconos de código
code1 = CodeIcon(300, 360)
code2 = CodeIcon(600, 260)
code_icons.add(code1, code2)
all_sprites.add(code1, code2)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Puntuación
score = 0
font = pygame.font.SysFont(None, 36)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                burnie.jump()

    # Movimiento de Burnie
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        burnie.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        burnie.rect.x += 5

    # Mantener a Burnie en la pantalla
    if burnie.rect.left < 0:
        burnie.rect.left = 0
    if burnie.rect.right > WIDTH:
        burnie.rect.right = WIDTH

    # Actualizar
    all_sprites.update()

    # Colisiones con plataformas
    hits = pygame.sprite.spritecollide(burnie, platforms, False)
    for platform in hits:
        if burnie.velocity_y > 0:  # Cayendo
            burnie.rect.bottom = platform.rect.top
            burnie.velocity_y = 0
        elif burnie.velocity_y < 0:  # Subiendo
            burnie.rect.top = platform.rect.bottom
            burnie.velocity_y = 0

    # Colisiones con íconos de código
    collected = pygame.sprite.spritecollide(burnie, code_icons, True)
    score += len(collected)

    # Dibujar
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Mostrar puntuación
    score_text = font.render(f"Code Points: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

# Salir
pygame.quit()
sys.exit()