# Menú principal del juego

import pygame

class MenuPrincipal:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.ancho, self.alto = pantalla.get_size()
        
        # Carga TU FONDO
        try:
            self.fondo = pygame.image.load("fondos/Menú.png").convert()
            self.fondo = pygame.transform.scale(self.fondo, (self.ancho, self.alto))
        except:
            print("ERROR: Coloca 'Menú.png' en la carpeta 'fondos'")
            self.fondo = pygame.Surface((self.ancho, self.alto))
            self.fondo.fill((0, 0, 0))
        
        self.fuente = pygame.font.Font(None, 48)
        self.opciones = ["JUGAR", "CONFIGURACIÓN", "SALIR"]
        self.seleccionado = 0
    
    
    def dibujar(self):  # Dibuja el menú principal
        self.pantalla.blit(self.fondo, (0, 0))  # Carga el fondo
        
        titulo = pygame.font.Font(None, 72).render("Stickman Fighters Kombat", True, (255, 255, 255)) # Crea el título
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, 100)) # Dibuja el título
        
        for i, opcion in enumerate(self.opciones): # Dibuja cada opción
            color = (255, 215, 0) if i == self.seleccionado else (200, 200, 200)
            texto = self.fuente.render(opcion, True, color)
            self.pantalla.blit(texto, (self.ancho//2 - texto.get_width()//2, 300 + i * 80))
    
    def manejar_eventos(self, eventos):  # Maneja los eventos del menú principal
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccionado = max(0, self.seleccionado - 1)
                elif evento.key == pygame.K_DOWN:
                    self.seleccionado = min(len(self.opciones) - 1, self.seleccionado + 1)
                elif evento.key == pygame.K_RETURN:
                    return self.opciones[self.seleccionado]
        return None
