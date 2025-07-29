import pygame
import requests
import time

pygame.init()
screen = pygame.display.set_mode((480, 320))  # Ajuste conforme a tela
pygame.display.set_caption("Magic Mirror")

font_evento = pygame.font.SysFont("Arial", 20)
font_hora = pygame.font.SysFont("Arial", 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def get_eventos():
    try:
        response = requests.get("http://localhost:5000/eventos")
        if response.ok:
            return response.json()
    except:
        return []
    return []

def draw_mirror():
    screen.fill(BLACK)

    # Hora atual
    hora_atual = time.strftime("%H:%M:%S")
    texto_hora = font_hora.render(hora_atual, True, WHITE)
    screen.blit(texto_hora, (160, 10))

    # Eventos do dia
    eventos = get_eventos()
    y_offset = 80
    for evento, datahora in eventos:
        hora_evento = datahora.split(" ")[1][:5]  # HH:MM
        texto = f"{hora_evento} - {evento}"
        evento_text = font_evento.render(texto, True, WHITE)
        screen.blit(evento_text, (20, y_offset))
        y_offset += 30

    pygame.display.update()

# Loop principal
running = True
while running:
    draw_mirror()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    time.sleep(1)

pygame.quit()
