import pygame
import random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (100, 100, 100)
ROJO_SALIR = (200, 0, 0)
VERDE_CONTINUAR = (0, 200, 0)
COLOR_PLUS_PUNTO = (100, 255, 100)
COLOR_MENOS_PUNTO = (255, 100, 100)
COLOR_FADE = NEGRO

FPS = 60

TIPO_ALUMINIO = "aluminio"
TIPO_PLASTICO = "plastico"

IMAGENES_BASURA_ALUMINIO = ["Cocacola.png", "Pepsi.png", "ComidaEnlatada.png", "PapelAluminio.png"]
IMAGENES_BASURA_PLASTICO = ["BotellaPlastico.png", "VasoPlastico.png", "BotellaShampoo.png"]
IMAGEN_BOTE_ALUMINIO = "BoteAluminio.png"
IMAGEN_BOTE_PLASTICO = "BotePlastico.png"

VELOCIDAD_BOTE = 10
TAMANO_BOTE = (100, 100)
TAMANO_BOTE_INSTRUCCIONES = (50, 50)
OFFSET_NOMBRE_JUGADOR = 30

VELOCIDAD_BASURA_INICIAL = 3
TAMANO_BASURA = (50, 50)
TAMANO_BASURA_INSTRUCCIONES = (35, 35)
NUM_OBJETOS_BASURA_PANTALLA = 4

TIEMPO_JUEGO_S = 120
TIEMPO_PARPADEO_ERROR_MS = 200
DURACION_FADE_MS = 500
VOLUMEN_MUSICA_DEFAULT = 0.5
VOLUMEN_INCREMENTO = 0.1

TEXTO_CONTINUAR = "Continuar"
TEXTO_SALIR_JUEGO = "Salir del Juego"
OPCIONES_PAUSA = [TEXTO_CONTINUAR, TEXTO_SALIR_JUEGO]

VELOCIDAD_TEXTO_FLOTANTE_Y = -1.5
DURACION_VIDA_TEXTO_FLOTANTE_MS = 700
FONT_SIZE_TEXTO_FLOTANTE = 30

class ObjetoBasura(pygame.sprite.Sprite):
    def __init__(self, tipo_basura, velocidad_caida, screen_width, screen_height):
        super().__init__()
        self.tipo_basura = tipo_basura
        self.original_image_path = self._get_original_image_path(tipo_basura)
        self.original_image = pygame.image.load(resource_path(os.path.join("assets", self.original_image_path))).convert_alpha()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocidad_caida = velocidad_caida
        self._reescalar_y_actualizar_rect()
        self.reiniciar_posicion()

    def _get_original_image_path(self, tipo_basura):
        if tipo_basura == TIPO_ALUMINIO:
            return random.choice(IMAGENES_BASURA_ALUMINIO)
        elif tipo_basura == TIPO_PLASTICO:
            return random.choice(IMAGENES_BASURA_PLASTICO)
        return "Cocacola.png"

    def _reescalar_y_actualizar_rect(self):
        self.image = pygame.transform.scale(self.original_image, TAMANO_BASURA)
        current_center = None
        if hasattr(self, 'rect') and self.rect is not None:
            current_center = self.rect.center
        self.rect = self.image.get_rect()
        if current_center:
            self.rect.center = current_center

    def reiniciar_posicion(self):
        self.rect.x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.y = random.randint(-self.screen_height // 2, -self.rect.height - 20)

    def update(self):
        self.rect.y += self.velocidad_caida
        if self.rect.top > self.screen_height:
            self.original_image_path = self._get_original_image_path(self.tipo_basura)
            self.original_image = pygame.image.load(resource_path(os.path.join("assets", self.original_image_path))).convert_alpha()
            self._reescalar_y_actualizar_rect()
            self.reiniciar_posicion()
    
    def update_screen_size(self, new_width, new_height):
        self.screen_width = new_width
        self.screen_height = new_height
        self._reescalar_y_actualizar_rect()
        self.rect.clamp_ip(pygame.Rect(0, 0, new_width, new_height))
        if self.rect.bottom > new_height or self.rect.top > new_height :
             self.reiniciar_posicion()

class Jugador(pygame.sprite.Sprite):
    def __init__(self, nombre, imagen_bote_nombre, pos_x_inicial, pos_y, teclas_movimiento, tipo_bote_que_recoge, screen_width):
        super().__init__()
        self.nombre = nombre
        self.tipo_bote_que_recoge = tipo_bote_que_recoge
        self.screen_width = screen_width

        self.original_image = pygame.image.load(resource_path(os.path.join("assets", imagen_bote_nombre))).convert_alpha()
        self._reescalar_y_actualizar_rect()
        
        self.rect.centerx = pos_x_inicial
        self.rect.bottom = pos_y

        self.tecla_izquierda = teclas_movimiento[0]
        self.tecla_derecha = teclas_movimiento[1]
        self.velocidad = VELOCIDAD_BOTE
        self.font = pygame.font.Font(None, 36)

    def _reescalar_y_actualizar_rect(self):
        self.image = pygame.transform.scale(self.original_image, TAMANO_BOTE)
        current_center = None
        if hasattr(self, 'rect') and self.rect is not None:
            current_center = self.rect.center
        self.rect = self.image.get_rect()
        if current_center:
            self.rect.center = current_center

    def update(self, teclas_presionadas):
        if teclas_presionadas[self.tecla_izquierda]:
            self.rect.x -= self.velocidad
        if teclas_presionadas[self.tecla_derecha]:
            self.rect.x += self.velocidad

        if self.rect.right < 0:
            self.rect.left = self.screen_width
        elif self.rect.left > self.screen_width:
            self.rect.right = 0

    def dibujar_nombre(self, screen):
        nombre_render = self.font.render(self.nombre, True, BLANCO)
        pos_nombre_x = self.rect.centerx - nombre_render.get_width() // 2
        pos_nombre_y = self.rect.top - OFFSET_NOMBRE_JUGADOR
        screen.blit(nombre_render, (pos_nombre_x, pos_nombre_y))

    def update_screen_size(self, new_width):
        current_centerx_ratio = self.rect.centerx / self.screen_width
        self.screen_width = new_width
        self._reescalar_y_actualizar_rect()
        self.rect.centerx = int(current_centerx_ratio * new_width)
        self.rect.bottom = pygame.display.get_surface().get_height() - 20
        self.rect.clamp_ip(pygame.Rect(0, 0, new_width, pygame.display.get_surface().get_height()))

class TextoFlotante(pygame.sprite.Sprite):
    def __init__(self, texto, center_x, center_y, color, font_size, velocidad_y, duracion_vida_ms):
        super().__init__()
        self.font = pygame.font.Font(None, font_size)
        self.texto_original = texto
        self.color = color
        self.velocidad_y = velocidad_y
        self.tiempo_creacion = pygame.time.get_ticks()
        self.duracion_vida_ms = duracion_vida_ms
        self.alpha = 255

        self.image = self.font.render(self.texto_original, True, (*self.color, self.alpha))
        self.rect = self.image.get_rect(center=(center_x, center_y))

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_creacion

        if tiempo_transcurrido >= self.duracion_vida_ms:
            self.kill()
            return

        self.rect.y += self.velocidad_y
        
        if tiempo_transcurrido > self.duracion_vida_ms / 2:
            self.alpha = max(0, 255 - int(((tiempo_transcurrido - (self.duracion_vida_ms / 2)) / (self.duracion_vida_ms / 2)) * 255))
        
        self.image = self.font.render(self.texto_original, True, self.color).convert_alpha()
        self.image.set_alpha(self.alpha)

def pantalla_instrucciones(screen, font_titulo, font_texto, clock, musica_path, is_fullscreen, dev_width, dev_height, volumen_actual):
    current_width, current_height = screen.get_size()
    
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(resource_path(musica_path))
        pygame.mixer.music.set_volume(volumen_actual)
        pygame.mixer.music.play(-1)

    try:
        bote_aluminio_img_orig = pygame.image.load(resource_path(os.path.join("assets", IMAGEN_BOTE_ALUMINIO))).convert_alpha()
        bote_aluminio_img = pygame.transform.scale(bote_aluminio_img_orig, TAMANO_BOTE_INSTRUCCIONES)
        
        bote_plastico_img_orig = pygame.image.load(resource_path(os.path.join("assets", IMAGEN_BOTE_PLASTICO))).convert_alpha()
        bote_plastico_img = pygame.transform.scale(bote_plastico_img_orig, TAMANO_BOTE_INSTRUCCIONES)

        basura_aluminio_imgs_orig = [pygame.image.load(resource_path(os.path.join("assets", img_nombre))).convert_alpha() for img_nombre in IMAGENES_BASURA_ALUMINIO]
        basura_aluminio_imgs = [pygame.transform.scale(img, TAMANO_BASURA_INSTRUCCIONES) for img in basura_aluminio_imgs_orig]

        basura_plastico_imgs_orig = [pygame.image.load(resource_path(os.path.join("assets", img_nombre))).convert_alpha() for img_nombre in IMAGENES_BASURA_PLASTICO]
        basura_plastico_imgs = [pygame.transform.scale(img, TAMANO_BASURA_INSTRUCCIONES) for img in basura_plastico_imgs_orig]
            
    except pygame.error as e:
        print(f"Error cargando imágenes para instrucciones: {e}")
        bote_aluminio_img, bote_plastico_img = None, None
        basura_aluminio_imgs, basura_plastico_imgs = [], []

    titulo_render = font_titulo.render("Instrucciones y Controles", True, BLANCO)
    line_height_titulo = font_titulo.get_linesize()
    line_height_texto = font_texto.get_linesize()
    margen_vertical_entre_secciones = 30
    y_offset = 40

    activo = True
    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    activo = False
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((dev_width, dev_height))
                    current_width, current_height = screen.get_size()
        
        screen.fill(NEGRO)
        current_width, current_height = screen.get_size()
        
        screen.blit(titulo_render, (current_width // 2 - titulo_render.get_width() // 2, y_offset))
        current_y_offset = y_offset + line_height_titulo + margen_vertical_entre_secciones

        def dibujar_seccion_jugador(start_y_param, titulo_str, controles_str, bote_img_param, basuras_imgs_list_param):
            temp_y_local = start_y_param

            titulo_jug_render = font_texto.render(titulo_str, True, BLANCO)
            screen.blit(titulo_jug_render, (current_width // 2 - titulo_jug_render.get_width() // 2, temp_y_local))
            temp_y_local += line_height_texto

            controles_render = font_texto.render(controles_str, True, GRIS_CLARO)
            screen.blit(controles_render, (current_width // 2 - controles_render.get_width() // 2, temp_y_local))
            temp_y_local += line_height_texto + 5 

            recoge_texto_render = font_texto.render("Recoge:", True, GRIS_CLARO)
            
            linea_recoge_contenido_width = recoge_texto_render.get_width()
            espacio_entre_elementos = 10
            
            if bote_img_param:
                linea_recoge_contenido_width += espacio_entre_elementos + TAMANO_BOTE_INSTRUCCIONES[0]
            
            if basuras_imgs_list_param:
                num_basuras = len(basuras_imgs_list_param)
                if num_basuras > 0:
                    linea_recoge_contenido_width += espacio_entre_elementos
                    linea_recoge_contenido_width += num_basuras * TAMANO_BASURA_INSTRUCCIONES[0]
                    linea_recoge_contenido_width += (num_basuras - 1) * 5

            start_x_linea_recoge = current_width // 2 - linea_recoge_contenido_width // 2
            current_x_cursor = start_x_linea_recoge
            
            screen.blit(recoge_texto_render, (current_x_cursor, temp_y_local))
            current_x_cursor += recoge_texto_render.get_width() + espacio_entre_elementos

            if bote_img_param:
                screen.blit(bote_img_param, (current_x_cursor, temp_y_local + (line_height_texto - TAMANO_BOTE_INSTRUCCIONES[1])//2 ))
                current_x_cursor += TAMANO_BOTE_INSTRUCCIONES[0] + espacio_entre_elementos
            
            if basuras_imgs_list_param:
                for i, img_basura in enumerate(basuras_imgs_list_param):
                    screen.blit(img_basura, (current_x_cursor, temp_y_local + (line_height_texto - TAMANO_BASURA_INSTRUCCIONES[1])//2 ))
                    current_x_cursor += TAMANO_BASURA_INSTRUCCIONES[0]
                    if i < len(basuras_imgs_list_param) - 1:
                        current_x_cursor += 5 
            
            altura_max_linea_recoge = line_height_texto 
            if bote_img_param:
                altura_max_linea_recoge = max(altura_max_linea_recoge, TAMANO_BOTE_INSTRUCCIONES[1])
            if basuras_imgs_list_param and len(basuras_imgs_list_param) > 0:
                altura_max_linea_recoge = max(altura_max_linea_recoge, TAMANO_BASURA_INSTRUCCIONES[1])
            temp_y_local += altura_max_linea_recoge
            return temp_y_local

        current_y_offset = dibujar_seccion_jugador(current_y_offset, "Jugador 1 (Bote Aluminio):", 
                                           "  Controles: Flecha Izquierda / Flecha Derecha", 
                                           bote_aluminio_img, basura_aluminio_imgs)
        current_y_offset += margen_vertical_entre_secciones

        current_y_offset = dibujar_seccion_jugador(current_y_offset, "Jugador 2 (Bote Plástico):", 
                                           "  Controles: Tecla A (Izquierda) / Tecla D (Derecha)", 
                                           bote_plastico_img, basura_plastico_imgs)
        current_y_offset += margen_vertical_entre_secciones

        texto_pausa_f11_font = font_texto
        line_height_pausa_f11 = texto_pausa_f11_font.get_linesize()

        texto_pausa_render = texto_pausa_f11_font.render("Presiona 'P' para Pausar/Continuar el juego", True, GRIS_CLARO)
        screen.blit(texto_pausa_render, (current_width // 2 - texto_pausa_render.get_width() // 2, current_y_offset))
        current_y_offset += line_height_pausa_f11

        texto_f11_render = texto_pausa_f11_font.render("Presiona 'F11' para Pantalla Completa / Ventana", True, GRIS_CLARO)
        screen.blit(texto_f11_render, (current_width // 2 - texto_f11_render.get_width() // 2, current_y_offset))

        continuar_texto_render = font_texto.render("Presiona ENTER o ESPACIO para continuar...", True, VERDE_CONTINUAR)
        screen.blit(continuar_texto_render, (current_width // 2 - continuar_texto_render.get_width() // 2, current_height - 60 - continuar_texto_render.get_height()))

        pygame.display.flip()
        clock.tick(FPS)
    return screen, is_fullscreen

def pantalla_inicio(screen, font, clock, texto_prompt, música_path, is_fullscreen, dev_width, dev_height, volumen_actual):
    current_width, current_height = screen.get_size()
    nombre_jugador = ""
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(resource_path(música_path))
        pygame.mixer.music.set_volume(volumen_actual)
        pygame.mixer.music.play(-1)

    activo = True
    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if nombre_jugador: activo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif len(nombre_jugador) < 16 and event.unicode.isalnum():
                    nombre_jugador += event.unicode
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((dev_width, dev_height))
                    current_width, current_height = screen.get_size()
        
        screen.fill(NEGRO)
        prompt_render = font.render(texto_prompt, True, BLANCO)
        prompt_rect = prompt_render.get_rect(center=(current_width // 2, current_height // 2 - 40))
        screen.blit(prompt_render, prompt_rect)

        input_render = font.render(nombre_jugador, True, BLANCO)
        input_rect = input_render.get_rect(center=(current_width // 2, prompt_rect.centery + font.get_linesize() + 10))
        screen.blit(input_render, input_rect)

        pygame.display.flip()
        clock.tick(FPS)
    return screen, is_fullscreen, nombre_jugador

def pantalla_final(screen, font, clock, score_final, nombre_jugador1, nombre_jugador2, is_fullscreen, dev_width, dev_height):
    current_width, current_height = screen.get_size()
    texto = f"¡Puntaje final: {score_final}!"
    texto_nombres = f"Jugadores: {nombre_jugador1} y {nombre_jugador2}"
    activo = True
    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((dev_width, dev_height))
                    current_width, current_height = screen.get_size()
                else:
                    activo = False
        screen.fill(NEGRO)
        final_render = font.render(texto, True, BLANCO)
        nombres_render = font.render(texto_nombres, True, BLANCO)
        screen.blit(final_render, (current_width // 2 - final_render.get_width() // 2, current_height // 2 - 50))
        screen.blit(nombres_render, (current_width // 2 - nombres_render.get_width() // 2, current_height // 2))
        pygame.display.flip()
        clock.tick(FPS)
    return screen, is_fullscreen

def pantalla_pausa(screen, font, clock, is_fullscreen, dev_width, dev_height, volumen_actual_musica):
    current_width, current_height = screen.get_size()
    opcion_seleccionada = 0
    overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    activo = True
    resultado_continuar = True
    volumen_modificado_local = volumen_actual_musica

    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen: screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else: screen = pygame.display.set_mode((dev_width, dev_height))
                    current_width, current_height = screen.get_size()
                    overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA); overlay.fill((0,0,0,180))
                elif event.key == pygame.K_UP: opcion_seleccionada = (opcion_seleccionada - 1) % len(OPCIONES_PAUSA)
                elif event.key == pygame.K_DOWN: opcion_seleccionada = (opcion_seleccionada + 1) % len(OPCIONES_PAUSA)
                elif event.key == pygame.K_RETURN:
                    resultado_continuar = (OPCIONES_PAUSA[opcion_seleccionada] == TEXTO_CONTINUAR)
                    activo = False
                elif event.key == pygame.K_p: 
                    resultado_continuar = True; activo = False 
                elif event.key == pygame.K_LEFT:
                    volumen_modificado_local = max(0.0, volumen_modificado_local - VOLUMEN_INCREMENTO)
                    pygame.mixer.music.set_volume(volumen_modificado_local)
                elif event.key == pygame.K_RIGHT:
                    volumen_modificado_local = min(1.0, volumen_modificado_local + VOLUMEN_INCREMENTO)
                    pygame.mixer.music.set_volume(volumen_modificado_local)
        
        screen.blit(overlay, (0,0))
        y_offset_pausa = current_height // 3
        for i, opcion_texto in enumerate(OPCIONES_PAUSA):
            color = BLANCO
            if i == opcion_seleccionada: color = VERDE_CONTINUAR if opcion_texto == TEXTO_CONTINUAR else ROJO_SALIR
            texto_render = font.render(opcion_texto, True, color)
            screen.blit(texto_render, (current_width // 2 - texto_render.get_width() // 2, y_offset_pausa + i * (font.get_linesize() + 20)))
        
        vol_font_size = font.get_height() - 4
        vol_font = pygame.font.Font(None, vol_font_size if vol_font_size > 0 else 24)
        texto_volumen_str = f"Volumen: < {int(volumen_modificado_local * 100)}% >"
        texto_volumen = vol_font.render(texto_volumen_str, True, GRIS_CLARO)
        
        pos_y_volumen = y_offset_pausa + len(OPCIONES_PAUSA) * (font.get_linesize() + 20) + 20
        screen.blit(texto_volumen, (current_width // 2 - texto_volumen.get_width() // 2, pos_y_volumen))

        pygame.display.flip()
        clock.tick(FPS)
    return screen, is_fullscreen, resultado_continuar, volumen_modificado_local

def realizar_fade(screen, clock, duracion_ms, color, fade_in=True):
    """Realiza un efecto de fade in o fade out."""
    width, height = screen.get_size()
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill(color)
    
    num_pasos = FPS * duracion_ms // 1000
    if num_pasos == 0: num_pasos = 1

    for i in range(num_pasos + 1):
        alpha = 0
        if fade_in:
            alpha = int(255 * (1 - (i / num_pasos)))
        else:
            alpha = int(255 * (i / num_pasos))
        
        alpha = max(0, min(255, alpha))
        fade_surface.set_alpha(alpha)
        
        screen.blit(fade_surface, (0,0))
        pygame.display.flip()
        clock.tick(FPS)

def juego_principal(screen, font, clock, nombre_jugador1, nombre_jugador2, is_fullscreen, dev_width, dev_height, volumen_actual_musica):
    current_WIDTH, current_HEIGHT = screen.get_size()
    score = 0
    tiempo_restante_s = TIEMPO_JUEGO_S
    tiempo_parpadeo_actual_ms = 0
    textos_flotantes_sprites = pygame.sprite.Group()
    volumen_juego = volumen_actual_musica

    try:
        original_fondo_img = pygame.image.load(resource_path(os.path.join("assets", "Fondo.jpg"))).convert()
        fondo_img = pygame.transform.scale(original_fondo_img, (current_WIDTH, current_HEIGHT))
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        original_fondo_img = None
        fondo_img = pygame.Surface(screen.get_size()); fondo_img.fill(NEGRO)

    jugador1 = Jugador(nombre_jugador1, IMAGEN_BOTE_ALUMINIO, current_WIDTH // 4, current_HEIGHT - 20, 
                       (pygame.K_LEFT, pygame.K_RIGHT), TIPO_ALUMINIO, current_WIDTH)
    jugador2 = Jugador(nombre_jugador2, IMAGEN_BOTE_PLASTICO, 3 * current_WIDTH // 4, current_HEIGHT - 20, 
                       (pygame.K_a, pygame.K_d), TIPO_PLASTICO, current_WIDTH)
    jugadores_sprites = pygame.sprite.Group(jugador1, jugador2)

    basura_sprites = pygame.sprite.Group()
    tipos_disponibles = [TIPO_ALUMINIO, TIPO_PLASTICO]
    for _ in range(NUM_OBJETOS_BASURA_PANTALLA):
        tipo_azar = random.choice(tipos_disponibles)
        basura = ObjetoBasura(tipo_azar, VELOCIDAD_BASURA_INICIAL, current_WIDTH, current_HEIGHT)
        basura_sprites.add(basura)

    if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
        try:
            pygame.mixer.music.load(resource_path(os.path.join("assets", "chiptune-grooving-142242.mp3")))
            pygame.mixer.music.set_volume(volumen_juego)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar la música del juego: {e}")

    jugando = True
    pausado = False
    while jugando:
        dt_raw = clock.tick(FPS)
        dt = dt_raw / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen: screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else: screen = pygame.display.set_mode((dev_width, dev_height))
                    current_WIDTH, current_HEIGHT = screen.get_size()
                    if original_fondo_img: fondo_img = pygame.transform.scale(original_fondo_img, (current_WIDTH, current_HEIGHT))
                    else: fondo_img = pygame.Surface(screen.get_size()); fondo_img.fill(NEGRO)
                    for j_sprite in jugadores_sprites: j_sprite.update_screen_size(current_WIDTH)
                    for b_sprite in basura_sprites: b_sprite.update_screen_size(current_WIDTH, current_HEIGHT)
                        
                elif event.key == pygame.K_p:
                    pausado = not pausado
                    if pausado: pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()
        
        if pausado:
            screen, is_fullscreen, resultado_pausa, volumen_juego_actualizado = pantalla_pausa(screen, font, clock, is_fullscreen, dev_width, dev_height, volumen_juego)
            volumen_juego = volumen_juego_actualizado
            current_WIDTH, current_HEIGHT = screen.get_size()
            if resultado_pausa: 
                pausado = False; pygame.mixer.music.unpause()
            else: 
                jugando = False
            if not jugando: continue

        if not pausado:
            teclas_presionadas = pygame.key.get_pressed()
            jugadores_sprites.update(teclas_presionadas)
            
            if jugador1.rect.colliderect(jugador2.rect):
                offset_x_centers = jugador2.rect.centerx - jugador1.rect.centerx
                overlap = 0
                if offset_x_centers > 0: overlap = jugador1.rect.right - jugador2.rect.left
                else: overlap = jugador2.rect.right - jugador1.rect.left
                if overlap > 0:
                    ajuste = (overlap // 2) + 1
                    if offset_x_centers > 0: jugador1.rect.x -= ajuste; jugador2.rect.x += ajuste
                    elif offset_x_centers < 0: jugador1.rect.x += ajuste; jugador2.rect.x -= ajuste
                    else: jugador1.rect.x -= ajuste; jugador2.rect.x += ajuste
                    for j_sprite in [jugador1, jugador2]:
                        if j_sprite.rect.right < 0: j_sprite.rect.left = j_sprite.screen_width
                        elif j_sprite.rect.left > j_sprite.screen_width: j_sprite.rect.right = 0

            basura_sprites.update()
            textos_flotantes_sprites.update()

            for jugador_actual in jugadores_sprites:
                basura_atrapada_lista = pygame.sprite.spritecollide(jugador_actual, basura_sprites, False)
                for basura_item in basura_atrapada_lista:
                    if basura_item.tipo_basura == jugador_actual.tipo_bote_que_recoge:
                        score += 1
                        texto_mas_uno = TextoFlotante("+1", basura_item.rect.centerx, basura_item.rect.centery, 
                                                      COLOR_PLUS_PUNTO, FONT_SIZE_TEXTO_FLOTANTE, 
                                                      VELOCIDAD_TEXTO_FLOTANTE_Y, DURACION_VIDA_TEXTO_FLOTANTE_MS)
                        textos_flotantes_sprites.add(texto_mas_uno)
                    else:
                        score = max(0, score - 1)
                        tiempo_parpadeo_actual_ms = TIEMPO_PARPADEO_ERROR_MS
                        texto_menos_uno = TextoFlotante("-1", basura_item.rect.centerx, basura_item.rect.centery, 
                                                      COLOR_MENOS_PUNTO, FONT_SIZE_TEXTO_FLOTANTE, 
                                                      VELOCIDAD_TEXTO_FLOTANTE_Y, DURACION_VIDA_TEXTO_FLOTANTE_MS)
                        textos_flotantes_sprites.add(texto_menos_uno)

                    basura_item.original_image_path = basura_item._get_original_image_path(basura_item.tipo_basura)
                    basura_item.original_image = pygame.image.load(resource_path(os.path.join("assets", basura_item.original_image_path))).convert_alpha()
                    basura_item._reescalar_y_actualizar_rect()
                    basura_item.reiniciar_posicion()

            for basura_item in basura_sprites:
                if basura_item.rect.top > current_HEIGHT:
                    score = max(0, score - 1)
                    tiempo_parpadeo_actual_ms = TIEMPO_PARPADEO_ERROR_MS
                    texto_perdido = TextoFlotante("-1", basura_item.rect.centerx, current_HEIGHT - 30,
                                                  COLOR_MENOS_PUNTO, FONT_SIZE_TEXTO_FLOTANTE, 
                                                  VELOCIDAD_TEXTO_FLOTANTE_Y, DURACION_VIDA_TEXTO_FLOTANTE_MS)
                    textos_flotantes_sprites.add(texto_perdido)

                    basura_item.original_image_path = basura_item._get_original_image_path(basura_item.tipo_basura)
                    basura_item.original_image = pygame.image.load(resource_path(os.path.join("assets", basura_item.original_image_path))).convert_alpha()
                    basura_item._reescalar_y_actualizar_rect()
                    basura_item.reiniciar_posicion()
                    
            tiempo_restante_s -= dt
            if tiempo_restante_s <= 0:
                jugando = False
                tiempo_restante_s = 0
            
            if tiempo_parpadeo_actual_ms > 0:
                tiempo_parpadeo_actual_ms -= dt_raw
                if tiempo_parpadeo_actual_ms < 0: tiempo_parpadeo_actual_ms = 0

            screen.blit(fondo_img, (0,0))
            jugadores_sprites.draw(screen)
            for j in jugadores_sprites: j.dibujar_nombre(screen)
            basura_sprites.draw(screen)
            textos_flotantes_sprites.draw(screen)

            score_texto = font.render(f"Puntaje: {score}", True, BLANCO)
            tiempo_texto = font.render(f"Tiempo: {int(tiempo_restante_s)}", True, BLANCO)
            screen.blit(score_texto, (10, 10))
            screen.blit(tiempo_texto, (current_WIDTH - tiempo_texto.get_width() - 10, 10))

            if tiempo_parpadeo_actual_ms > 0:
                if int(tiempo_parpadeo_actual_ms / (TIEMPO_PARPADEO_ERROR_MS / 4)) % 2 == 0:
                    s = pygame.Surface((current_WIDTH,current_HEIGHT), pygame.SRCALPHA)
                    s.fill((255,0,0,80))
                    screen.blit(s, (0,0))

        pygame.display.flip()

    pygame.mixer.music.stop()
    return screen, is_fullscreen, score, volumen_juego

def main():
    pygame.init()
    pygame.mixer.init()

    is_fullscreen = False
    dev_width, dev_height = 1000, 750
    volumen_musica = VOLUMEN_MUSICA_DEFAULT
    
    if is_fullscreen: screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else: screen = pygame.display.set_mode((dev_width, dev_height))
    
    pygame.display.set_caption("Catching Trash Remastered - Deluxe")
    
    font_titulo_grande = pygame.font.Font(None, 56)
    font_principal = pygame.font.Font(None, 48)
    font_juego = pygame.font.Font(None, 36)
    clock_principal = pygame.time.Clock()

    musica_inicio_path = os.path.join("assets", "game-background-music-169723.mp3")

    screen, is_fullscreen = pantalla_instrucciones(screen, font_titulo_grande, font_juego, clock_principal, musica_inicio_path, is_fullscreen, dev_width, dev_height, volumen_musica)
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=False)
    
    screen_negra = pygame.Surface(screen.get_size()); screen_negra.fill(NEGRO); screen.blit(screen_negra, (0,0)); pygame.display.flip()
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=True)
    screen, is_fullscreen, nombre_j1 = pantalla_inicio(screen, font_principal, clock_principal, 
                                "Inserta el nombre del Jugador 1:", musica_inicio_path, is_fullscreen, dev_width, dev_height, volumen_musica)
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=False)

    screen_negra.fill(NEGRO); screen.blit(screen_negra, (0,0)); pygame.display.flip()
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=True)
    screen, is_fullscreen, nombre_j2 = pantalla_inicio(screen, font_principal, clock_principal, 
                                "Inserta el nombre del Jugador 2:", musica_inicio_path, is_fullscreen, dev_width, dev_height, volumen_musica)
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=False)

    pygame.mixer.music.stop()

    screen_negra.fill(NEGRO); screen.blit(screen_negra, (0,0)); pygame.display.flip()
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=True)
    screen, is_fullscreen, score_final_juego, volumen_musica = juego_principal(screen, font_juego, clock_principal, nombre_j1, nombre_j2, is_fullscreen, dev_width, dev_height, volumen_musica)
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=False)

    screen_negra.fill(NEGRO); screen.blit(screen_negra, (0,0)); pygame.display.flip()
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=True)
    screen, is_fullscreen = pantalla_final(screen, font_principal, clock_principal, score_final_juego, nombre_j1, nombre_j2, is_fullscreen, dev_width, dev_height)
    realizar_fade(screen, clock_principal, DURACION_FADE_MS, COLOR_FADE, fade_in=False)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()