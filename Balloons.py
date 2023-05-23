import pygame
import random
import pygame_menu

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

# Definir dimensiones de la pantalla
dimensiones = (1300, 760)
pantalla = pygame.display.set_mode(dimensiones)

# Crear una fuente
fuente = pygame.font.SysFont('Comic Sans MS', 20)
fuente2 = pygame.font.SysFont('Comic Sans MS', 40)

# Definir imagen de fondo
fondo = pygame.image.load(f"assets/sky.jpg").convert()
fondo = pygame.transform.scale(fondo, dimensiones)
fondo2 = pygame.image.load(f"assets/fondo2.jpg").convert()
fondo2 = pygame.transform.scale(fondo2, dimensiones)


# Definir el rectángulo del contenedor
rectangulo_contenedor = pygame.Rect(0, 0, dimensiones[0], 100)

# Definir una lista de pelotas
pelotas = []
for i in range(80):
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

# Función para obtener un número aleatorio de las pelotas
def getNumber(index):
    return pelotas[index]['numero']

# Función para generar operación
def operacion_aleatoria(resultado):
    operadores = ['+', '-', '*', '/']
    num1 = random.randint(1, resultado)
    operador = random.choice(operadores)

    if operador == '+':
        num2 = resultado - num1
        return f"{num1} + {num2} = ?"
    elif operador == '-':
        num2 = resultado + num1
        return f"{num2} - {num1} = ?"
    elif operador == '*':
        num2 = resultado // num1
        if num1 * num2 != resultado:
            return operacion_aleatoria(resultado)
        else:
            return f"{num1} * {num2} = ?"
    else:
        num2 = resultado * num1
        if num2 / num1 != resultado:
            return operacion_aleatoria(resultado)
        else:
            return f"{num2} / {num1} = ?"

# Función para iniciar el juego principal
def iniciar_juego():
    # Generar el resultado
    resultado = getNumber(random.randint(0, 59))
    operacion = operacion_aleatoria(resultado)

    # Puntuación inicial
    puntos = 0

    # Tiempo restante
    duracion = 180  # 3 minutos → 180 segundos
    tiempo = pygame.time.get_ticks()
    reloj = pygame.time.Clock()

    # Factor de escala para la velocidad de las pelotas
    factor_escala = 3

    # Loop principal del juego
    jugando = True
    while jugando:
        # Regular los frames
        reloj.tick(60)

        # Calcular el tiempo transcurrido en segundos desde el inicio del juego
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo) / 1000

        # Calcular el tiempo restante en segundos
        tiempo_restante = duracion - tiempo_transcurrido

        if tiempo_restante <= 0:
            jugando = False
            menu_principal()
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
                            puntos += 1
                        break

        # Mover las pelotas
        for pelota in pelotas:
            pelota['x'] += pelota['dx'] * factor_escala
            pelota['y'] += pelota['dy'] * factor_escala

            # Si la pelota sale de la pantalla, rebotarla
            if pelota['x'] < pelota['radio'] or pelota['x'] > dimensiones[0] - pelota['radio']:
                pelota['dx'] = -pelota['dx']
            # Si la pelota sale del contenedor en la parte superior, mantenerla dentro del contenedor
            if pelota['y'] < pelota['radio'] + rectangulo_contenedor.height or pelota['y'] > dimensiones[
                1] - pelota['radio']:
                # pelota['y'] = pelota['radio'] + rectangulo_contenedor.height
                pelota['dy'] = -pelota['dy']

        # Dibujar el fondo
        pantalla.blit(fondo, [0, 0])
        # pantalla.fill(BLANCO)

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

        # Crear una superficie de texto con la puntuación
        puntuacion = fuente.render(f"Puntuación: {puntos}", True, NEGRO)

        # Renderizar la superficie de texto de la puntuación en la ventana de Pygame
        pantalla.blit(puntuacion, (20, 20))

        # Crear una superficie de texto con el tiempo restante
        tiempo_restante_str = f"Tiempo restante: {int(tiempo_restante)} s"
        tiempo_restante_surface = fuente.render(tiempo_restante_str, True, NEGRO)

        # Renderizar la superficie de texto del tiempo restante en la ventana de Pygame
        pantalla.blit(tiempo_restante_surface, (dimensiones[0] - tiempo_restante_surface.get_width() - 20, 20))

        # Actualizar la pantalla
        pygame.display.flip()

    # Salir de pygame
    pygame.quit()


def menu_principal():
    pygame.init()

    # Definir dimensiones de la pantalla
    dimensiones = (1300, 760)
    pantalla = pygame.display.set_mode(dimensiones)

    # Crear una fuente
    fuente = pygame.font.SysFont('Comic Sans MS', 50)

    # Definir colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)

    # Definir texto del menú principal
    titulo = fuente.render("Number Pop", True, NEGRO)
    jugar_texto = fuente.render("Jugar", True, NEGRO)
    instrucciones_texto = fuente.render("Instrucciones", True, NEGRO)
    salir_texto = fuente.render("Salir", True, NEGRO)

    # Definir rectángulos de los botones
    jugar_rect = jugar_texto.get_rect(center=(dimensiones[0] // 2, dimensiones[1] // 2 - 50))
    instrucciones_rect = instrucciones_texto.get_rect(center=(dimensiones[0] // 2, dimensiones[1] // 2))
    salir_rect = salir_texto.get_rect(center=(dimensiones[0] // 2, dimensiones[1] // 2 + 50))

    # Loop principal del menú
    menu = True
    while menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if jugar_rect.collidepoint(evento.pos):
                    iniciar_juego()
                    menu = False
                elif instrucciones_rect.collidepoint(evento.pos):
                    mostrar_instrucciones()
                elif salir_rect.collidepoint(evento.pos):
                    pygame.quit()
                    return

        # Dibujar el fondo
        pantalla.blit(fondo2,[0, 0])

        # Renderizar los textos en la pantalla
        pantalla.blit(titulo, (dimensiones[0] // 2 - titulo.get_width() // 2, 100))
        pantalla.blit(jugar_texto, jugar_rect)
        pantalla.blit(instrucciones_texto, instrucciones_rect)
        pantalla.blit(salir_texto, salir_rect)

        # Actualizar la pantalla
        pygame.display.flip()

def mostrar_instrucciones():
    pygame.init()

    # Definir dimensiones de la pantalla
    dimensiones = (1300, 760)
    pantalla = pygame.display.set_mode(dimensiones)

    # Crear una fuente
    fuente = pygame.font.SysFont('Comic Sans MS', 25)

    # Definir colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)

    # Definir texto de las instrucciones
    instrucciones = [
        "Instrucciones:",
        "",
        "- Haz clic sobre los globos para poncharlos.",
        "- Cada globo tiene un número y debes ponchar",
        "  el globo cuyo número coincide con el resultado de",
        "  una operación matemática que aparecerá en la parte",
        "  superior de la pantalla.",
        "- Por cada acierto, recibirás 1 punto.",
        "- El juego dura 3 minutos. Trata de obtener la mayor",
        "  puntuación posible antes de que se acabe el tiempo.",
        "",
        "¡Buena suerte!"
    ]

    # Calcular la altura total de las instrucciones
    altura_instrucciones = len(instrucciones) * 40

    # Loop principal de las instrucciones
    instrucciones_menu = True
    while instrucciones_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                instrucciones_menu = False

        # Dibujar el fondo
        pantalla.blit(fondo2, [0, 0])

        # Dibujar el rectángulo del área de las instrucciones
        # pygame.draw.rect(pantalla, NEGRO, area_instrucciones)

        # Renderizar los textos de las instrucciones en la pantalla
        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, NEGRO)
            pantalla.blit(texto, (
                dimensiones[0] // 2 - texto.get_width() // 2,
                dimensiones[1] // 2 - altura_instrucciones // 2 + i * 40
            ))

        # Actualizar la pantalla
        pygame.display.flip()


# Llamar al menú principal
menu_principal()
