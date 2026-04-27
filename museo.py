import pygame
import sys
import json

pygame.init()
pygame.mixer.init()

# =========================
# PANTALLA
# =========================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Museo Digital")

clock = pygame.time.Clock()

# TIPOGRAFÍA MEJORADA
font_title = pygame.font.SysFont("georgia", 64, bold=True)
font = pygame.font.SysFont("georgia", 28)

# =========================
# FADE TRANSITION
# =========================
fade = 0
fade_dir = 0
next_state = None

def iniciar_fade(nuevo_estado):
    global fade, fade_dir, next_state
    fade = 0
    fade_dir = 1
    next_state = nuevo_estado

# =========================
# MAPA
# =========================
mapa = pygame.image.load("imagenes/mexico mapa.png")
mapa = pygame.transform.scale(mapa, (WIDTH, HEIGHT))

# =========================
# CIUDADES (FULLSCREEN + SMOOTH)
# =========================
ciudades_img = {
    "punto_0": pygame.transform.smoothscale(
        pygame.image.load("imagenes/teotihuacan.webp"), (WIDTH, HEIGHT)
    ),
    "punto_1": pygame.transform.smoothscale(
        pygame.image.load("imagenes/chichenitza.webp"), (WIDTH, HEIGHT)
    ),
    "punto_2": pygame.transform.smoothscale(
        pygame.image.load("imagenes/palenque.webp"), (WIDTH, HEIGHT)
    ),
    "punto_3": pygame.transform.smoothscale(
        pygame.image.load("imagenes/Monte-Alban.webp"), (WIDTH, HEIGHT)
    ),
}

ciudades_texto = {
    "punto_0": """Teotihuacan: Teotihuacán fue una de las ciudades más grandes y influyentes de Mesoamérica. 
    Destacan la Pirámide del Sol y la Pirámide de la Luna, alineadas con un complejo urbano planificado. 
    Su apogeo fue entre los siglos I y VII d.C., y su cultura sigue siendo en gran parte un misterio.""",

    "punto_1": """Chichén Itzá: Chichén Itzá es un importante centro político y religioso. 
    Su estructura más icónica es la pirámide de Kukulkán, que refleja conocimientos astronómicos avanzados. 
    Fue declarada Patrimonio de la Humanidad y una de las Nuevas Siete Maravillas del Mundo.""",

    "punto_2": """Palenque: Palenque es una ciudad maya rodeada de selva, conocida por la calidad de su arquitectura y esculturas. 
    El Templo de las Inscripciones alberga la tumba del rey Pakal. 
    Es uno de los sitios más importantes para entender la historia y escritura maya.""",

    "punto_3": """Monte Albán: Monte Albán fue la capital de los zapotecas y una de las primeras ciudades de Mesoamérica. 
    Está construida sobre una montaña con vistas al valle de Oaxaca. 
    Destaca por sus plazas ceremoniales, tumbas y el sistema de escritura zapoteca."""
}

# =========================
# PUNTOS
# =========================
with open("puntos.json", "r") as f:
    puntos = json.load(f)

# =========================
# SONIDO
# =========================
sonidos = {
    "punto_0": pygame.mixer.Sound("audio/teotihuacan.ogg"),
    "punto_1": pygame.mixer.Sound("audio/chichenitza.ogg"),
    "punto_2": pygame.mixer.Sound("audio/palenque.ogg"),
    "punto_3": pygame.mixer.Sound("audio/montealban.ogg"),
}

sonido_actual = None

def cambiar_sonido(nombre):
    global sonido_actual
    if sonido_actual:
        sonido_actual.stop()
    sonido_actual = sonidos[nombre]
    sonido_actual.play(-1)

def detener_sonido():
    global sonido_actual
    if sonido_actual:
        sonido_actual.stop()
        sonido_actual = None

# =========================
# ESTADOS
# =========================
STATE_INTRO = "intro"
STATE_MAPA = "mapa"
STATE_CIUDAD = "ciudad"

state = STATE_INTRO
actual = None

# =========================
# BOTONES
# =========================
boton_iniciar = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
boton_volver = pygame.Rect(20, 20, 120, 50)

# =========================
# TYPEWRITER
# =========================
texto_intro_mapa = "PRINCIPALES CIUDADES. ARQUEOLÓGICAS. HAZ CLICK EN EL MAPA."
texto_mostrado = ""
indice_texto = 0
timer_texto = 0
velocidad_texto = 2

def actualizar_texto():
    global texto_mostrado, indice_texto, timer_texto

    if indice_texto < len(texto_intro_mapa):
        timer_texto += 1
        if timer_texto >= velocidad_texto:
            texto_mostrado += texto_intro_mapa[indice_texto]
            indice_texto += 1
            timer_texto = 0

# =========================
# WRAP TEXT
# =========================
def dibujar_texto(texto, x, y, ancho=860):
    palabras = texto.split(" ")
    linea = []
    lineas = []

    for p in palabras:
        test = " ".join(linea + [p])
        if font.size(test)[0] < ancho:
            linea.append(p)
        else:
            lineas.append(" ".join(linea))
            linea = [p]
    lineas.append(" ".join(linea))

    for i, l in enumerate(lineas):
        img = font.render(l, True, (255,255,255))
        screen.blit(img, (x, y + i * 28))

# =========================
# LOOP
# =========================
while True:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            detener_sonido()
            pygame.quit()
            sys.exit()

        if state == STATE_INTRO and event.type == pygame.MOUSEBUTTONDOWN:
            if boton_iniciar.collidepoint(event.pos):
                state = STATE_MAPA

        if state == STATE_MAPA and event.type == pygame.MOUSEBUTTONDOWN:
            for nombre, pos in puntos.items():
                x, y = pos
                rect = pygame.Rect(x-12, y-12, 24, 24)

                if rect.collidepoint(event.pos):
                    actual = nombre
                    cambiar_sonido(nombre)
                    iniciar_fade(STATE_CIUDAD)

        if state == STATE_CIUDAD and event.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver.collidepoint(event.pos):
                detener_sonido()
                iniciar_fade(STATE_MAPA)

    # =========================
    # INTRO
    # =========================
    if state == STATE_INTRO:
        screen.fill((10,10,20))

        title = font_title.render("Museo Digital de México", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        pygame.draw.rect(screen, (50,50,50), boton_iniciar, border_radius=12)
        pygame.draw.rect(screen, (255,255,255), boton_iniciar, 2, border_radius=12)

        btn = font.render("Iniciar", True, (255,255,255))
        screen.blit(btn, (boton_iniciar.x + 60, boton_iniciar.y + 15))

    # =========================
    # MAPA
    # =========================
    elif state == STATE_MAPA:
        screen.blit(mapa, (0,0))
        actualizar_texto()

        # puntos
        for nombre, pos in puntos.items():
            x, y = pos
            color = (255,255,120) if pygame.Rect(x-12,y-12,24,24).collidepoint(mouse) else (0,180,255)
            pygame.draw.circle(screen, color, (x,y), 10)

        # PANEL GLASS
        panel = pygame.Surface((520, 220), pygame.SRCALPHA)
        panel.fill((0,0,0,160))
        screen.blit(panel, (20,20))
        pygame.draw.rect(screen, (255,255,255), (20,20,520,220), 1, border_radius=12)

        lineas = texto_mostrado.split(". ")

        for i, l in enumerate(lineas):
            img = font.render(l, True, (255,255,255))
            screen.blit(img, (40, 40 + i * 30))

    # =========================
    # CIUDAD
    # =========================
    elif state == STATE_CIUDAD:
        screen.blit(ciudades_img[actual], (0,0))

        # panel inferior glass
        panel = pygame.Surface((WIDTH, 150), pygame.SRCALPHA)
        panel.fill((0,0,0,170))
        screen.blit(panel, (0,450))
        pygame.draw.rect(screen, (255,255,255), (0,450,WIDTH,150), 1, border_radius=12)

        dibujar_texto(ciudades_texto[actual], 20, 470)

        pygame.draw.rect(screen, (50,50,50), boton_volver, border_radius=12)
        pygame.draw.rect(screen, (255,255,255), boton_volver, 2, border_radius=12)

        txt = font.render("Volver", True, (255,255,255))
        screen.blit(txt, (boton_volver.x + 25, boton_volver.y + 15))

    # =========================
    # FADE
    # =========================
    if fade_dir != 0:
        fade += 10 * fade_dir

        if fade >= 255:
            fade = 255
            fade_dir = -1
            state = next_state

            if state == STATE_MAPA:
                texto_mostrado = ""
                indice_texto = 0
                timer_texto = 0

        elif fade <= 0:
            fade = 0
            fade_dir = 0

    if fade > 0:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(fade)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

    pygame.display.flip()