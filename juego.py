# juego.py - Codigo del juego
import pygame
import os

class Juego:
    def __init__(self, pantalla, dificultad="Normal"):
        self.pantalla = pantalla
        self.ancho, self.alto = pantalla.get_size()
        self.estado = "jugando" # Puede ser: "jugando", "pausa", "fin_ronda", "fin_juego"
        self.reloj = pygame.time.Clock()
        self.en_pausa = False  # ← indica si el juego está en pausa
        self.dificultad = dificultad # Almacena la dificultad seleccionada
        self.sonido_salto = pygame.mixer.Sound("assets/audio/salto.wav")
        self.sonido_golpe = pygame.mixer.Sound("assets/audio/golpe.wav")
        self.cargar_sonidos(0.5)  # 0.5 es el volumen por defecto (50%)

        # Configuración según dificultad
        if self.dificultad == "Fácil":
            self.factor_velocidad = 0.8  # Más lento el movimiento
            self.danio_golpe = 8        # Menos daño por golpe
            self.vida_base = 150        # Más vida inicial
        elif self.dificultad == "Difícil":
            self.factor_velocidad = 1.2  # Más rápido
            self.danio_golpe = 16       # Más daño
            self.vida_base = 80         # Menos vida
        else:  # Normal
            self.factor_velocidad = 1.0
            self.danio_golpe = 12
            self.vida_base = 100
            
        self.sonido_salto = pygame.mixer.Sound("assets/audio/salto.wav")
        self.sonido_golpe = pygame.mixer.Sound("assets/audio/golpe.wav")
        self.cargar_sonidos(0.5)  # Configura volumen al 50%
        
        # Inicialización de componentes del juego
        self.cargar_recursos() # Carga imágenes y sprites
        self.inicializar_jugadores() # Configura los jugadores
        self.inicializar_rondas() # Prepara el sistema de rondas
        
        # Fuentes para texto en pantalla
        self.fuente = pygame.font.Font(None, 36) # Pequeña para HUD
        self.fuente_grande = pygame.font.Font(None, 72) # Para mensajes
        self.fuente_combate = pygame.font.Font(None, 120) # Para texto grande
    
    def cargar_recursos(self):
        try:
            # Carga los fondos de los mapas para cada ronda
            self.mapas = [
                pygame.transform.scale(pygame.image.load(os.path.join("Mapas", "Dia.jpeg")).convert(), (self.ancho, self.alto)),
                pygame.transform.scale(pygame.image.load(os.path.join("Mapas", "Tarde.jpeg")).convert(), (self.ancho, self.alto)),
                pygame.transform.scale(pygame.image.load(os.path.join("Mapas", "Noche.jpeg")).convert(), (self.ancho, self.alto))
            ]
        except:
             # Si falla la carga, crea fondos alternativos
            self.mapas = [self.crear_fondo_alternativo() for _ in range(3)]
        
         # Carga los sprites de los jugadores
        base_path = "sprites"
        self.sprites = {
            "jugador1": self.cargar_sprites_jugador(os.path.join(base_path, "Derecha"), "1"),
            "jugador2": self.cargar_sprites_jugador(os.path.join(base_path, "Izquierda"), "2")
        }
        
        # carga los sonidos del juego (salto y golpe) con el volumen especificado
    def cargar_sonidos(self, volumen_base=0.5):
        try:
            self.sonido_salto = pygame.mixer.Sound("assets/audio/salto.wav") # Sonido de salto
            self.sonido_salto.set_volume(volumen_base * 0.8)  # # Golpe a volumen de base
        except:
            self.sonido_salto = None
            print("⚠️ No se pudo cargar 'salto.wav'")

        try:
            self.sonido_golpe = pygame.mixer.Sound("assets/audio/golpe.wav")
            self.sonido_golpe.set_volume(volumen_base)  # 100% del volumen base
        except:
            self.sonido_golpe = None
            print("⚠️ No se pudo cargar 'golpe.wav'")
        try:
                self.sonido_golpe = pygame.mixer.Sound("assets/audio/golpe.wav")
                self.sonido_golpe.set_volume(0.6)
        except:
                self.sonido_golpe = None
        print("⚠️ No se pudo cargar 'golpe.wav'")
    
    
    def cargar_sprites_jugador(self, path, tipo_jugador):
        # Diccionario con las animaciones disponibles
        animaciones = {
            "pose": f"pose{tipo_jugador}_1.png",
            "agacharse": f"agacharse{tipo_jugador}_1.png" if tipo_jugador == "1" else f"agacharse{tipo_jugador}_2.png",
            "caminar": [f"caminar{tipo_jugador}_{i}.png" for i in range(1, 6)] if tipo_jugador == "1" else [f"caminar{tipo_jugador}_{i}.png" for i in range(2, 6)],
            "saltar": [f"saltar{i}_{tipo_jugador}.png" for i in range(1, 7)],
            "pelear": [f"pelear{tipo_jugador}_{i}.png" for i in range(1, 7)]
        }
        # Carga cada sprite y lo escala adecuadamente
        sprites = {}
        for animacion, archivos in animaciones.items():
            if isinstance(archivos, list):
                sprites[animacion] = [self.cargar_sprite(os.path.join(path, archivo)) for archivo in archivos]
            else:
                sprites[animacion] = self.cargar_sprite(os.path.join(path, archivos))
        
        return sprites
    
     # Carga una imagen individual y la prepara para su uso
    def cargar_sprite(self, ruta_completa):
        try:
            sprite = pygame.image.load(ruta_completa).convert_alpha()
             # Escala según el tipo de sprite
            if any(x in ruta_completa for x in ["pose", "saltar", "pelear", "caminar"]):
                return pygame.transform.scale(sprite, (150, 270))
            elif "agacharse" in ruta_completa:
                return pygame.transform.scale(sprite, (150, 120))
            return sprite
        except Exception as e:
            print(f"Error cargando sprite: {e}")
            surf = pygame.Surface((150, 270), pygame.SRCALPHA)
            color = (255, 0, 0, 180) if "1" in ruta_completa else (128, 0, 128, 180)
            pygame.draw.rect(surf, color, (0, 0, 150, 270))
            return surf
    
    # Configuración base común a ambos jugadores
    def inicializar_jugadores(self):
        config_base = {
            "velocidad": 7 * self.factor_velocidad,  # Afectado por dificultad
            "saltando": False,
            "agachado": False,
            "direccion": 1,
            "animacion": 0, # Frame actual de animación
            "tiempo_animacion": 0,
            "y_base": self.alto//2 + 60, # Posición base en Y
            "moviendose": False,
            "tiempo_salto": 0,
            "golpeando": False,
            "tiempo_golpe": 0,
            "vida": self.vida_base,      # Vida actual (Afectado por dificultad)
            "vida_max": self.vida_base,   # Vida base (Afectado por dificultad)
            "golpes_recibidos": 0,
            "altura_salto": 220, # Altura máxima del salto
            "invulnerable": 0 # Tiempo de inmunidad tras golpe
        }
        
         # Jugador 1 (Rojo)
        self.jugador1 = {
            **config_base,
            "x": self.ancho//4, # Posición inicial izquierda
            "y": self.alto//2 + 60,
            "sprites": "jugador1", # Conjunto de sprites a usar
            "direccion": 1 # Mirando a la derecha
        }

        # Jugador 2 (Lila)
        self.jugador2 = {
            **config_base,
            "x": 3*self.ancho//4, # Posición inicial derecha
            "y": self.alto//2 + 60,
            "sprites": "jugador2",
            "direccion": -1 # Mirando a la izquierda
        }
    
    def inicializar_rondas(self):
        self.ronda_actual = 0
        self.max_rondas = 3
        self.ganador_ronda = None
        self.tiempo_fin_ronda = 0
        self.tiempo_espera_ronda = 3000 # 3 segundos entre rondas
        self.estado_ronda = "jugando" # cambia segun el estado de: "jugando", "fin_ronda", "fin_juego"
        self.puntuaciones = {"jugador1": 0, "jugador2": 0}
        self.tiempo_inicio_ronda = pygame.time.get_ticks()  # Para el temporizador
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Pausa/despausa el juego
                    self.en_pausa = not self.en_pausa
                    return "pausa" if self.en_pausa else None
                elif evento.key == pygame.K_e and not self.jugador1["golpeando"]:
                    self.sonido_golpe.play()
                    # Jugador 1 golpea
                    self.jugador1["golpeando"] = True
                    self.jugador1["tiempo_golpe"] = pygame.time.get_ticks()
                    self.verificar_golpe(self.jugador1, self.jugador2)
                elif evento.key == pygame.K_1 and not self.jugador2["golpeando"]:
                    self.sonido_golpe.play()
                     # Jugador 2 golpea
                    self.jugador2["golpeando"] = True
                    self.jugador2["tiempo_golpe"] = pygame.time.get_ticks()
                    self.verificar_golpe(self.jugador2, self.jugador1)
                elif evento.key == pygame.K_SPACE and self.estado_ronda == "fin_juego":
                    return "reiniciar"
                # Reinicia el juego al finalizar

        # Movimiento continuo con teclas presionadas
        teclas = pygame.key.get_pressed()
        self.procesar_controles(self.jugador1, teclas[pygame.K_a], teclas[pygame.K_d], teclas[pygame.K_w], teclas[pygame.K_s])
        self.procesar_controles(self.jugador2, teclas[pygame.K_LEFT], teclas[pygame.K_RIGHT], teclas[pygame.K_UP], teclas[pygame.K_DOWN])
        
        return None
    
    def verificar_golpe(self, atacante, defensor): # verifica si un jugador golpea al otro y actualiza el daño al jugador recibido
        if defensor["invulnerable"] > pygame.time.get_ticks():
            return # Todavía es invulnerable
            
        distancia = abs(atacante["x"] - defensor["x"])
        if distancia < 180:  # Rango de golpe
            defensor["vida"] = max(0, defensor["vida"] - self.danio_golpe)  # Usa el daño configurado
            defensor["invulnerable"] = pygame.time.get_ticks() + 500 # 0.5s de inmunidad
            
            if defensor["vida"] <= 0:
                self.finalizar_ronda(atacante)
    
    def finalizar_ronda(self, ganador):
        self.ganador_ronda = ganador
        self.estado_ronda = "fin_ronda"
        self.tiempo_fin_ronda = pygame.time.get_ticks()
        # Actualiza puntuación
        if ganador["sprites"] == "jugador1":
            self.puntuaciones["jugador1"] += 1
        else:
            self.puntuaciones["jugador2"] += 1

        # Verifica si el juego terminó (mejor de 3)
        if max(self.puntuaciones.values()) >= 2:
            self.estado_ronda = "fin_juego"
        elif self.ronda_actual < self.max_rondas - 1:
            self.ronda_actual += 1
    
    def reiniciar_ronda(self):
        self.inicializar_jugadores() # Restaura vidas y posiciones
        if self.estado_ronda == "fin_juego":
            self.inicializar_rondas()  # Reinicia todo el juego
        else:
            # Solo prepara la siguiente ronda
            self.estado_ronda = "jugando"
            self.ganador_ronda = None
            self.tiempo_inicio_ronda = pygame.time.get_ticks() 
    
    def procesar_controles(self, jugador, izquierda, derecha, arriba, abajo):
        if self.estado_ronda != "jugando":
            return # No procesar controles si no estamos jugando
            
        jugador["moviendose"] = izquierda or derecha

         # Movimiento horizontal
        if izquierda:
            jugador["x"] = max(75, jugador["x"] - jugador["velocidad"])
            jugador["direccion"] = -1 # Mirando izquierda
        
        if derecha:
            jugador["x"] = min(self.ancho - 75, jugador["x"] + jugador["velocidad"])
            jugador["direccion"] = 1 # Mirando derecha

         # Salto
        if arriba and not jugador["saltando"] and not jugador["golpeando"]:
            jugador["saltando"] = True
            jugador["tiempo_salto"] = pygame.time.get_ticks()
            self.sonido_salto.play()

        # Agacharse
        jugador["agachado"] = abajo and not jugador["saltando"] and not jugador["golpeando"]

        # Animación de caminar
        if jugador["moviendose"] and not jugador["golpeando"]:
            jugador["animacion"] = (jugador["animacion"] + 1) % len(self.sprites[jugador["sprites"]]["caminar"])
        
        # Física del salto (movimiento parabólico)
        if jugador["saltando"]:
            progreso = (pygame.time.get_ticks() - jugador["tiempo_salto"]) / 500 # 0.5s duración
            if progreso >= 1.0:
                jugador["saltando"] = False 
                jugador["y"] = jugador["y_base"] # Vuelve al suelo
            else:
                # Calcula altura con curva parabólica
                altura = jugador["altura_salto"] * progreso * (1 - progreso)
                jugador["y"] = jugador["y_base"] - altura
        # Temporizador de golpe
        if jugador["golpeando"]:
            if pygame.time.get_ticks() - jugador["tiempo_golpe"] > 600:
                jugador["golpeando"] = False
    
    def actualizar(self):
        if self.en_pausa:
             return  # Si está pausado, no hace nada

        # Temporizador entre rondas
        if self.estado_ronda == "fin_ronda":
            if pygame.time.get_ticks() - self.tiempo_fin_ronda > self.tiempo_espera_ronda:
                self.reiniciar_ronda() # Pasa a la siguiente ronda
    
    def dibujar(self):
        # Fondo del nivel actual
        self.pantalla.blit(self.mapas[self.ronda_actual], (0, 0))

         # Interfaz y elementos del juego
        self.dibujar_hud() # Barras de vida, marcador
        
        self.dibujar_jugador(self.jugador1) # Sprite Jugador 1
        self.dibujar_jugador(self.jugador2) # Sprite Jugador 2

        # Mensajes de estado del juego
        if self.estado_ronda == "fin_ronda":
            self.dibujar_mensaje_ronda() # Muestra un mensaje del ganador de la ronda
        elif self.estado_ronda == "fin_juego":
            self.dibujar_mensaje_final() # Muestra un mensaje final del jugado 
        self.dibujar_controles() # Teclas de control

        # Mensaje de pausa
        if self.en_pausa:
            fuente = pygame.font.SysFont(None, 80)
            texto = fuente.render("PAUSA", True, (255, 255, 255))
            rect = texto.get_rect(center=(640, 360))  # Centro de la pantalla
            self.pantalla.blit(texto, rect)

    # Hud del juego: barras de vidas, textos de rondas, tiempo
    def dibujar_hud(self):
        self.dibujar_barra_vida(self.jugador1, 50, 30, 400, 25, (220, 40, 40))
        self.dibujar_barra_vida(self.jugador2, self.ancho - 450, 30, 400, 25, (160, 40, 220))
        
        texto_ronda = self.fuente.render(f"Ronda {self.ronda_actual + 1}/{self.max_rondas}", True, (255, 255, 0))
        self.pantalla.blit(texto_ronda, (self.ancho//2 - texto_ronda.get_width()//2, 20))
        
        score_text = self.fuente.render(f"{self.puntuaciones['jugador1']}   -   {self.puntuaciones['jugador2']}", True, (255, 255, 255))
        self.pantalla.blit(score_text, (self.ancho//2 - score_text.get_width()//2, 60))
        
        tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio_ronda) // 1000
        tiempo_text = self.fuente.render(f"{30 - tiempo_transcurrido}", True, (255, 255, 255))
        self.pantalla.blit(tiempo_text, (self.ancho//2 - tiempo_text.get_width()//2, 100))
    
    def dibujar_barra_vida(self, jugador, x, y, ancho, alto, color):
        pygame.draw.rect(self.pantalla, (40, 40, 40), (x, y, ancho, alto), border_radius=3)
        vida_ancho = max(0, (jugador["vida"] / jugador["vida_max"]) * ancho)
        pygame.draw.rect(self.pantalla, color, (x, y, vida_ancho, alto), border_radius=3)
        pygame.draw.rect(self.pantalla, (220, 220, 220), (x, y, ancho, alto), 2, border_radius=3)
        texto = self.fuente.render(f"{jugador['vida']}/{jugador['vida_max']}", True, (255, 255, 255))
        self.pantalla.blit(texto, (x + ancho//2 - texto.get_width()//2, y + alto//2 - texto.get_height()//2))
    
    # Sprites de acciones de los jugadores o mecanicas
    def dibujar_jugador(self, jugador):
        sprites = self.sprites[jugador["sprites"]]
        
        if jugador["golpeando"]:
            frame = min(5, int((pygame.time.get_ticks() - jugador["tiempo_golpe"]) / 100))
            sprite = sprites["pelear"][frame]
        elif jugador["saltando"]:
            frame = min(5, int((pygame.time.get_ticks() - jugador["tiempo_salto"]) / 500 * 6))
            sprite = sprites["saltar"][frame]
        elif jugador["agachado"]:
            sprite = sprites["agacharse"]
            jugador["y"] = jugador["y_base"] + 75
        else:
            jugador["y"] = jugador["y_base"]
            if jugador["moviendose"]:
                sprite = sprites["caminar"][jugador["animacion"] % len(sprites["caminar"])]
            else:
                sprite = sprites["pose"]
        
        if (jugador["direccion"] == -1 and jugador["sprites"] == "jugador1") or \
           (jugador["direccion"] == 1 and jugador["sprites"] == "jugador2"):
            sprite = pygame.transform.flip(sprite, True, False)
        
        if not jugador["saltando"]:
            sombra_width = int(120 * (1 - (jugador["y"] - jugador["y_base"]) / 300))
            sombra = pygame.Surface((sombra_width, 12), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 70 - abs(jugador["y"] - jugador["y_base"]) // 4))
            self.pantalla.blit(sombra, (jugador["x"] - sombra_width//2, jugador["y_base"] + 100))
        
        self.pantalla.blit(sprite, (jugador["x"] - sprite.get_width()//2, jugador["y"] - sprite.get_height()//2))
    
    # Mensaje de victoria del jugador ganador
    def dibujar_mensaje_ronda(self):
        mensaje = self.fuente_grande.render(
            "¡Red Gana!" if self.ganador_ronda["sprites"] == "jugador1" else "¡Lila Gana!", 
            True, 
            (255, 215, 0)
        )
        self.pantalla.blit(mensaje, (self.ancho//2 - mensaje.get_width()//2, self.alto//2 - 100))
        
        texto_siguiente = self.fuente.render("Siguiente ronda...", True, (255, 255, 255))
        self.pantalla.blit(texto_siguiente, (self.ancho//2 - texto_siguiente.get_width()//2, self.alto//2))
    
    # Mensajes de victoria
    def dibujar_mensaje_final(self):
        mensaje = self.fuente_grande.render(
            "¡RED VICTORIA!" if self.puntuaciones["jugador1"] > self.puntuaciones["jugador2"] else "¡LILA VICTORIA!", 
            True, 
            (255, 215, 0)
        )
        self.pantalla.blit(mensaje, (self.ancho//2 - mensaje.get_width()//2, self.alto//2 - 120))
        
        texto_puntuacion = self.fuente.render(
            f"Final: {self.puntuaciones['jugador1']} - {self.puntuaciones['jugador2']}", 
            True, 
            (255, 255, 255)
        )
        self.pantalla.blit(texto_puntuacion, (self.ancho//2 - texto_puntuacion.get_width()//2, self.alto//2 - 50))
        
        texto_reinicio = self.fuente.render("Presiona ESPACIO para reiniciar", True, (255, 255, 255))
        self.pantalla.blit(texto_reinicio, (self.ancho//2 - texto_reinicio.get_width()//2, self.alto//2 + 20))
    
    # Mensaje en la esquina inferior del juego
    def dibujar_controles(self):
        texto = self.fuente.render(
            "ESC: Menú | WASD: Jugador Rojo | FLECHAS: Jugador Lila | E/1: Golpear", 
            True, 
            (200, 200, 200)
        )
        self.pantalla.blit(texto, (self.ancho//2 - texto.get_width()//2, self.alto - 30))