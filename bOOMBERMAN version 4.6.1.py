import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SPRITE_SIZE = 50
MOVEMENT_SPEED = 2

# Colores
GRAY = (170, 170, 170)

# Crear la ventana
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BoomBerMan")

# Crear el buffer (superficie)
buffer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

# Cargar las imágenes
try:
    fondo = pygame.image.load("fondo.bmp").convert()
    hitler_sprite = pygame.image.load("Personaje.bmp").convert()
    hitler_sprite.set_colorkey((255, 0, 255))  # Hacer transparente el color rosa
    solido_sprite = pygame.image.load("Solido.bmp").convert()
    bomba_sprite = pygame.image.load("BOMBA 2.0.png").convert()  # Cargar la imagen de la bomba
    bomba_sprite.set_colorkey((255, 0, 255))  # Hacer transparente el color rosa en la bomba
except pygame.error as e:
    print(f"No se pudo cargar la imagen: {e}")
    sys.exit(-1)

# Configuración de la animación
animations = {
    'down': [hitler_sprite.subsurface(pygame.Rect(col * SPRITE_SIZE, 0 * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
             for col in range(11)],
    'up': [hitler_sprite.subsurface(pygame.Rect(col * SPRITE_SIZE, 1 * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
           for col in range(11)],
    'right': [hitler_sprite.subsurface(pygame.Rect(col * SPRITE_SIZE, 2 * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
              for col in range(1, 4)],
    'left': [hitler_sprite.subsurface(pygame.Rect(col * SPRITE_SIZE, 3 * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
             for col in range(1, 4)],
    'static': [hitler_sprite.subsurface(pygame.Rect(col * SPRITE_SIZE, 6 * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
               for col in range(44)],
}

# Animación de la bomba
bomba_animation = [bomba_sprite.subsurface(pygame.Rect(0, row * SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))
                   for row in range(4)]  # Extraer la primera columna de la bomba

def load_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip().split(',')
            row = [int(num) for num in line if num.isdigit()]
            matrix.append(row)
    return matrix

def main():
    matrix = load_matrix("ASDC.txt")

    # Variables de posición y dirección
    x = 0
    y = 50
    direction = 'down'
    frame_index = 0  # Inicializar en 0
    animation_tick = 0  # Contador para controlar la velocidad de animación
    ANIMATION_SPEED = 8  # Controla la velocidad de la animación (mayor número = más lento)
    
    bomba_index = -1
    bomba_position = None
    clock = pygame.time.Clock()
    frame_counter = 0

    running = True
    while running:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_q and bomba_index == -1:
                    bomba_index = 0
                    bomba_position = (x, y)

        # Obtener estado del teclado
        keys = pygame.key.get_pressed()
        
        # Incrementar el contador de animación
        animation_tick += 1
        
        # Movimiento y dirección del personaje
        old_direction = direction  # Guardar la dirección anterior
        if keys[pygame.K_UP]:
            y -= MOVEMENT_SPEED
            direction = 'up'
        elif keys[pygame.K_DOWN]:
            y += MOVEMENT_SPEED
            direction = 'down'
        elif keys[pygame.K_LEFT]:
            x -= MOVEMENT_SPEED
            direction = 'left'
        elif keys[pygame.K_RIGHT]:
            x += MOVEMENT_SPEED
            direction = 'right'
        else:
            direction = 'static'

        # Actualizar el frame_index solo cuando corresponda
        if animation_tick >= ANIMATION_SPEED:
            animation_tick = 0  # Reiniciar el contador
            
            # Si cambió la dirección, reiniciar el frame_index
            if old_direction != direction:
                frame_index = 0
            else:
                frame_index = (frame_index + 1) % len(animations[direction])

        # Asegurar que frame_index esté dentro de los límites
        frame_index = frame_index % len(animations[direction])

        # Límites de pantalla
        x = max(0, min(x, WINDOW_WIDTH - SPRITE_SIZE))
        y = max(0, min(y, WINDOW_HEIGHT - SPRITE_SIZE))

        # Limpiar buffer
        buffer.fill(GRAY)

        # Dibujar el fondo
        buffer.blit(fondo, (0, 0))

        # Dibujar la matriz
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == 1:
                    buffer.blit(solido_sprite, (col * SPRITE_SIZE, row * SPRITE_SIZE))

        # Dibujar el personaje en el buffer
        current_frame = animations[direction][frame_index]
        buffer.blit(current_frame, (x, y))

        # Dibujar la animación de la bomba si está activa
        if bomba_index != -1:
            if bomba_position:
                buffer.blit(bomba_animation[bomba_index], bomba_position)
                frame_counter += 1
                if frame_counter >= 60:
                    frame_counter = 0
                    bomba_index += 1
                    if bomba_index >= len(bomba_animation):
                        bomba_index = -1

        # Dibujar el buffer en la pantalla
        screen.blit(buffer, (0, 0))
        pygame.display.flip()

        # Control de velocidad
        clock.tick(60)

    # Limpiar y salir
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()