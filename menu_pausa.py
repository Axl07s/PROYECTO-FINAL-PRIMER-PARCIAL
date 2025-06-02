# Menú de pausa del juego
import pygame

class MenuPausa:
    def __init__(self, pantalla, fondo_principal):
        self.pantalla = pantalla
        self.ancho, self.alto = pantalla.get_size()
        self.fondo_principal = fondo_principal
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 72)
        self.fuente_opciones = pygame.font.Font(None, 48)
        
        # Opciones del menú
        self.opciones = ["REANUDAR", "CONFIGURACIÓN", "MENÚ PRINCIPAL"]
        self.seleccionado = 0
        
        # Efecto visual
        self.alpha_surface = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self.alpha_surface.fill((0, 0, 0, 180))  # Fondo semitransparente
    
    def dibujar(self):
        # Dibujar el fondo del juego desenfocado/semitransparente
        self.pantalla.blit(self.fondo_principal, (0, 0))
        self.pantalla.blit(self.alpha_surface, (0, 0))
        
        # Título
        titulo = self.fuente_titulo.render("JUEGO EN PAUSA", True, (255, 215, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, self.alto//4))
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            color = (100, 200, 255) if i == self.seleccionado else (220, 220, 220)
            texto = self.fuente_opciones.render(opcion, True, color)
            self.pantalla.blit(texto, (self.ancho//2 - texto.get_width()//2, self.alto//2 + i * 70))
        
        # Instrucción
        instruccion = pygame.font.Font(None, 30).render("Presiona ESC para reanudar", True, (200, 200, 200))
        self.pantalla.blit(instruccion, (self.ancho//2 - instruccion.get_width()//2, self.alto - 50))
    
    def manejar_eventos(self, eventos): # Manejar eventos del menú de pausa del juego
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccionado = max(0, self.seleccionado - 1)
                elif evento.key == pygame.K_DOWN:
                    self.seleccionado = min(len(self.opciones) - 1, self.seleccionado + 1)
                elif evento.key == pygame.K_RETURN:
                    return self.opciones[self.seleccionado]
                elif evento.key == pygame.K_ESCAPE:
                    return "REANUDAR"
        return None