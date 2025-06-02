# Configuración del menú
import pygame

class MenuConfiguracion:
    def __init__(self, pantalla, fondo_principal):
        self.pantalla = pantalla
        self.fondo_principal = fondo_principal
        self.ancho, self.alto = pantalla.get_size()
        self.mixer = pygame.mixer
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 60)
        self.fuente_opciones = pygame.font.Font(None, 36)
        self.fuente_botones = pygame.font.Font(None, 32)
        
        # Configuración
        self.config = {
            'volumen': 70,
            'pantalla_completa': False,
            'dificultad': 'Normal'
        }
        
        # Estado
        self.seleccionado = 0
        self.opciones = [
            {"nombre": "Volumen", "valor": self.config['volumen']},
            {"nombre": "Pantalla Completa", "valor": self.config['pantalla_completa']},
            {"nombre": "Dificultad", "valor": self.config['dificultad'], "opciones": ["Fácil", "Normal", "Difícil"]}
        ]
    
    def dibujar(self):
        # Fondo principal
        self.pantalla.blit(self.fondo_principal, (0, 0))
        
        # Capa semitransparente
        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.pantalla.blit(overlay, (0, 0))
        
        # Panel
        panel_rect = pygame.Rect(self.ancho//4, self.alto//6, self.ancho//2, self.alto//1.8)
        pygame.draw.rect(self.pantalla, (40, 40, 60), panel_rect, border_radius=10)
        pygame.draw.rect(self.pantalla, (80, 80, 120), panel_rect, 2, border_radius=10)
        
        # Título
        titulo = self.fuente_titulo.render("CONFIGURACIÓN", True, (255, 215, 0))
        self.pantalla.blit(titulo, (self.ancho//2 - titulo.get_width()//2, self.alto//5))
        
        # Opciones
        for i, opcion in enumerate(self.opciones):
            y = self.alto//3 + i * 60
            color = (100, 200, 255) if i == self.seleccionado else (220, 220, 220)
            
            # Nombre opción
            texto = self.fuente_opciones.render(opcion["nombre"], True, color)
            self.pantalla.blit(texto, (self.ancho//2 - 200, y))
            
            # Valor
            if opcion["nombre"] == "Volumen":
                valor_text = self.fuente_opciones.render(f"{opcion['valor']}%", True, (255, 255, 255))
                bar_width = 150 * (opcion['valor'] / 100)
                pygame.draw.rect(self.pantalla, (80, 80, 80), (self.ancho//2 + 50, y + 5, 150, 10))
                pygame.draw.rect(self.pantalla, (100, 200, 255), (self.ancho//2 + 50, y + 5, bar_width, 10))
                self.pantalla.blit(valor_text, (self.ancho//2 + 210, y))
            
            elif opcion["nombre"] == "Pantalla Completa":
                estado = "ON" if opcion['valor'] else "OFF"
                color_estado = (0, 180, 0) if opcion['valor'] else (180, 0, 0)
                estado_text = self.fuente_opciones.render(estado, True, color_estado)
                self.pantalla.blit(estado_text, (self.ancho//2 + 150, y))
            
            elif opcion["nombre"] == "Dificultad":
                dificultad_text = self.fuente_opciones.render(opcion['valor'], True, (255, 255, 255))
                self.pantalla.blit(dificultad_text, (self.ancho//2 + 150, y))
        
        # Botones
        pygame.draw.rect(self.pantalla, (70, 130, 180) if self.seleccionado == 3 else (50, 90, 130), 
                         (self.ancho//2 - 220, self.alto - 150, 180, 50), border_radius=5)
        aplicar_text = self.fuente_botones.render("APLICAR", True, (255, 255, 255))
        self.pantalla.blit(aplicar_text, (self.ancho//2 - 220 + 90 - aplicar_text.get_width()//2, self.alto - 135))
        
        pygame.draw.rect(self.pantalla, (70, 130, 180) if self.seleccionado == 4 else (50, 90, 130), 
                         (self.ancho//2 + 40, self.alto - 150, 180, 50), border_radius=5)
        cancelar_text = self.fuente_botones.render("CANCELAR", True, (255, 255, 255))
        self.pantalla.blit(cancelar_text, (self.ancho//2 + 40 + 90 - cancelar_text.get_width()//2, self.alto - 135))
    
    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccionado = max(0, self.seleccionado - 1)
                elif evento.key == pygame.K_DOWN:
                    self.seleccionado = min(4, self.seleccionado + 1)
                elif evento.key == pygame.K_LEFT:
                    if self.seleccionado == 0:  # Volumen
                        self.opciones[0]['valor'] = max(0, self.opciones[0]['valor'] - 5)
                    elif self.seleccionado == 1:  # Pantalla completa
                        self.opciones[1]['valor'] = not self.opciones[1]['valor']
                    elif self.seleccionado == 2:  # Dificultad
                        current = self.opciones[2]['opciones'].index(self.opciones[2]['valor'])
                        self.opciones[2]['valor'] = self.opciones[2]['opciones'][max(0, current - 1)]
                elif evento.key == pygame.K_RIGHT:
                    if self.seleccionado == 0:  # Volumen
                        self.opciones[0]['valor'] = min(100, self.opciones[0]['valor'] + 5)
                    elif self.seleccionado == 1:  # Pantalla completa
                        self.opciones[1]['valor'] = not self.opciones[1]['valor']
                    elif self.seleccionado == 2:  # Dificultad
                        current = self.opciones[2]['opciones'].index(self.opciones[2]['valor'])
                        self.opciones[2]['valor'] = self.opciones[2]['opciones'][min(2, current + 1)]
                elif evento.key == pygame.K_RETURN:
                    if self.seleccionado == 3:  # Aplicar
                        self._aplicar_configuracion()
                        return "aplicar"
                    elif self.seleccionado == 4:  # Cancelar
                        return "cancelar"
        return None
    
    def obtener_configuracion(self): # Obtiene la configuración actual
        """Devuelve la configuración actual"""
        return {
            'volumen': self.opciones[0]['valor'],
            'pantalla_completa': self.opciones[1]['valor'],
            'dificultad': self.opciones[2]['valor']
        }  # Devuelve la configuración actual
    
    def _aplicar_configuracion(self): # Aplica la configuración actual
        """Aplica los cambios de configuración"""
        self.config = {
            'volumen': self.opciones[0]['valor'],
            'pantalla_completa': self.opciones[1]['valor'],
            'dificultad': self.opciones[2]['valor']
        } # Aplica los cambios de configuración
        
        # Aplicar volumen a la música de fondo
        volumen = self.config['volumen'] / 100  # Convertir a rango 0.0-1.0
        self.mixer.music.set_volume(volumen)
        
        # Aplicar pantalla completa
        if self.config['pantalla_completa']:
            pygame.display.set_mode((self.ancho, self.alto), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((self.ancho, self.alto))
        
        print(f"Configuración aplicada - Volumen: {self.config['volumen']}%")
        
        # Aplicar pantalla completa
        if self.config['pantalla_completa']:
            pygame.display.set_mode((self.ancho, self.alto), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((self.ancho, self.alto))
        
        print("Configuración aplicada:", self.config)