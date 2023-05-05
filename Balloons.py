import pygame
import random
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
MORADO = (255, 0, 255)
colores = [ROJO, VERDE, AZUL, AMARILLO, MORADO]

# Definir un título
pygame.display.set_caption("Math balloons")

# Definir dimensiones de la pantalla
dimensiones = (1300, 760)
pantalla = pygame.display.set_mode(dimensiones)

# Crear una fuente
fuente = pygame.font.SysFont('Comic Sans MS', 20)
fuente2 = pygame.font.SysFont('Comic Sans MS', 40)

# Función para generar operación
def operacion_aleatoria(resultado):
    operadores = ['+', '-', '*', '//']
    num1 = random.randint(0, resultado)
    operador = random.choice(operadores)

    if operador == '+':
        num2 = resultado - num1
        return f"{num1} + {num2} = ?"
    elif operador == '-':
        num2 = resultado + num1
        return f"{num2} - {num1} = ?"
    elif operador == '*':
        num2 = resultado // num1
        return f"{num1} * {num2} = ?"
    else:
        num2 = resultado * num1
        return f"{num2} / {num1} = ?"

# Definir imagen de fondo
fondo = pygame.image.load("sky.jpg").convert()

# Definir el rectángulo del contenedor
rectangulo_contenedor = pygame.Rect(0, 0, dimensiones[0], 100)

# Definir una lista de pelotas
pelotas = []
for i in range(100):
    # Crear una pelota con posición y velocidad aleatorias
    pelota = {
        'x': random.randint(30, dimensiones[0] - 30),
        'y': random.randint(130, dimensiones[1] - 30),
        'dx': random.uniform(-0.5, 0.5),
        'dy': random.uniform(-0.5, 0.5),
        'color': random.choice(colores),
        'radio': 30,
        'numero': random.randint(1, 100)
    }
    pelotas.append(pelota)

# Función para obtener un número aleatorio de los globos
def getNumber(index):
    return pelotas[index]['numero']

# Función para generar operación
def operacion_aleatoria(operacion):
    operadores = ['+', '-', '*', '//']
    num1 = random.randint(0, operacion)
    operador = random.choice(operadores)

    if operador == '+':
        num2 = operacion - num1
        return f"{num1} + {num2} = ?"
    elif operador == '-':
        num2 = operacion + num1
        return f"{num2} - {num1} = ?"
    elif operador == '*':
        if num1 == 0:
            return operacion_aleatoria(operacion)
        num2 = operacion // num1
        return f"{num1} * {num2} = ?"
    else:
        num2 = operacion * num1
        return f"{num2} / {num1} = ?"
    
# Generar el resultado
resultado = getNumber(random.randint(0, 59))
operacion = operacion_aleatoria(resultado)

# Loop principal del juego
jugando = True
while jugando:
    # Procesar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si el clic del mouse está dentro del área de alguna pelota
            x, y = evento.pos
            for pelota in pelotas:
                if (x - pelota['x']) ** 2 + (y - pelota['y']) ** 2 <= pelota['radio'] ** 2:
                    # Eliminar la pelota y agregar una nueva
                    pelotas.remove(pelota)
                    nueva_pelota = {
                        'x': random.randint(30, dimensiones[0] - 30),
                        'y': random.randint(130, dimensiones[1] - 30),
                        'dx': random.uniform(-0.5, 0.5),
                        'dy': random.uniform(-0.5, 0.5),
                        'color': random.choice(colores),
                        'radio': 30,
                        'numero': random.randint(1, 99),
                    }
                    pelotas.append(nueva_pelota)
                    
                    if pelota['numero'] == resultado:
                        resultado = getNumber(random.randint(0, 59))
                        operacion = operacion_aleatoria(resultado)

                        # Crear una superficie de texto con el resultado de la operación aleatoria
                        text_surface = fuente2.render(operacion, True, NEGRO)

                        # Renderizar la superficie de texto en la ventana de Pygame
                        pantalla.blit(text_surface, (dimensiones[0] // 2 - text_surface.get_width() // 2,
                                        dimensiones[1] // 16 - text_surface.get_height() // 2))
                    break

    # Mover las pelotas
    for pelota in pelotas:
        pelota['x'] += pelota['dx']
        pelota['y'] += pelota['dy']
        
        # Si la pelota sale de la pantalla, rebotarla
        if pelota['x'] < pelota['radio'] or pelota['x'] > dimensiones[0] - pelota['radio']:
            pelota['dx'] = -pelota['dx']
        # Si la pelota sale del contenedor en la parte superior, mantenerla dentro del contenedor
        if pelota['y'] < pelota['radio'] + rectangulo_contenedor.height or pelota['y'] > dimensiones[1] - pelota['radio']:
            #pelota['y'] = pelota['radio'] + rectangulo_contenedor.height
            pelota['dy'] = -pelota['dy']
            
    # Dibujar el fondo
    pantalla.blit(fondo, [0, 0])
    #pantalla.fill(BLANCO)

    # Dibujar el contenedor
    pygame.draw.rect(pantalla, BLANCO, rectangulo_contenedor)

    # Dibujar las pelotas
    for pelota in pelotas:
        pygame.draw.circle(pantalla, pelota['color'], (int(pelota['x']), int(pelota['y'])), pelota['radio'])
        texto = fuente.render(str(pelota['numero']), True, NEGRO)
        texto_rect = texto.get_rect()
        texto_rect.center = (int(pelota['x']), int(pelota['y']))
        pantalla.blit(texto, texto_rect)

    # Crear una superficie de texto con el resultado de la operación aleatoria
    text_surface = fuente2.render(operacion, True, NEGRO)

    # Renderizar la superficie de texto en la ventana de Pygame
    pantalla.blit(text_surface, (dimensiones[0] // 2 - text_surface.get_width() // 2,
                            dimensiones[1] // 16 - text_surface.get_height() // 2))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de pygame
pygame.quit()