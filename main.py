# main del juego
import pygame
import sys
from menu_principal import MenuPrincipal
from menu_config import MenuConfiguracion
from menu_pausa import MenuPausa  # <-- Nueva importación
from juego import Juego

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((1280, 720))
    # Inicializar el mezclador de audio
    pygame.mixer.init()
    
    # Cargar y reproducir la música del juego
    pygame.mixer.music.load("assets/audio/musica_fondo.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("Stickman Fighters Kombat")
    
    # Inicializar sistemas
    menu_principal = MenuPrincipal(pantalla)
    menu_config = MenuConfiguracion(pantalla, menu_principal.fondo)
    menu_pausa = None  # Se inicializará cuando sea necesario
    juego = None
    
    estado = "menu_principal"  # Puede ser: menu_principal, configuracion, juego, pausa
    reloj = pygame.time.Clock()

    configuracion = {
        'volumen': 50,
        'pantalla_completa': False,
        'dificultad': 'Normal'
    }
    
    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Máquina de estados del juego
        if estado == "menu_principal":
            menu_principal.dibujar()
            opcion = menu_principal.manejar_eventos(eventos)
            
            if opcion == "JUGAR":
                # Inicia nuevo juego con la dificultad configurada
                juego = Juego(pantalla, dificultad=configuracion['dificultad'])
                estado = "juego"
            elif opcion == "CONFIGURACIÓN":
                estado = "configuracion"
            elif opcion == "SALIR":
                pygame.quit()
                sys.exit()

        # Estado: Menú de Configuración
        elif estado == "configuracion":
            menu_config.dibujar()
            resultado = menu_config.manejar_eventos(eventos)
            
            if resultado == "aplicar":
                # Guarda la nueva configuración y vuelve al menú
                configuracion = menu_config.obtener_configuracion()
                estado = "menu_principal"
            elif resultado == "cancelar":
                estado = "menu_principal"
            # Opciones de configuración
        
        elif estado == "juego":
            resultado = juego.manejar_eventos(eventos)
            
            # Solo actualiza si el juego no está en pausa
            if not juego.en_pausa:
                juego.actualizar()
            
            juego.dibujar()

            # Manejar pausa
            if resultado == "pausa":
                # Capturamos el estado actual del juego como fondo para el menú de pausa
                fondo_pausa = pygame.Surface((pantalla.get_width(), pantalla.get_height()))
                fondo_pausa.blit(pantalla, (0, 0))
                menu_pausa = MenuPausa(pantalla, fondo_pausa)
                estado = "pausa"
            elif resultado == "menu_principal":
                estado = "menu_principal"
            elif resultado == "reiniciar":
                juego = Juego(pantalla)
        
        elif estado == "pausa":
            menu_pausa.dibujar()
            opcion = menu_pausa.manejar_eventos(eventos)
            
            if opcion == "REANUDAR":
                estado = "juego"
                juego.en_pausa = False
            elif opcion == "CONFIGURACIÓN":
                estado = "configuracion"
            elif opcion == "MENÚ PRINCIPAL":
                estado = "menu_principal"
                juego.en_pausa = False
        
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()