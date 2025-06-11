import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 1000, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Movimento Uniforme - Física para Ensino Médio")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (30, 144, 255)
VERMELHO = (220, 20, 60)
VERDE = (50, 205, 50)
AMARELO = (255, 215, 0)
CINZA = (200, 200, 200)
FUNDO = (25, 25, 40)

# Parâmetros da simulação
posicao_inicial = 100
velocidade = 50  # pixels por segundo
tempo = 0
pausado = False
mostrar_formulas = True
mostrar_grafico = True

# Objeto em movimento
carro_img = pygame.Surface((80, 40), pygame.SRCALPHA)
pygame.draw.rect(carro_img, AZUL, (0, 10, 70, 30), border_radius=8)
pygame.draw.rect(carro_img, (180, 220, 255), (10, 15, 20, 20))
pygame.draw.rect(carro_img, (180, 220, 255), (40, 15, 20, 20))
pygame.draw.rect(carro_img, (200, 230, 255), (60, 15, 10, 10))

# Fonte
fonte = pygame.font.SysFont(None, 32)
fonte_pequena = pygame.font.SysFont(None, 28)
fonte_titulo = pygame.font.SysFont(None, 48, bold=True)

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor=VERDE, cor_texto=BRANCO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.clicado = False
        
    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect, border_radius=8)
        pygame.draw.rect(superficie, BRANCO, self.rect, 2, border_radius=8)
        
        texto_surf = fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def verificar_clique(self, pos):
        if self.rect.collidepoint(pos):
            self.clicado = True
            return True
        return False

# Criar botões
botao_pausar = Botao(50, 500, 120, 50, "PAUSAR" if not pausado else "CONTINUAR", AMARELO)
botao_reset = Botao(190, 500, 120, 50, "REINICIAR", VERMELHO)
botao_formulas = Botao(330, 500, 180, 50, "FÓRMULAS: ON" if mostrar_formulas else "FÓRMULAS: OFF")
botao_grafico = Botao(530, 500, 180, 50, "GRÁFICO: ON" if mostrar_grafico else "GRÁFICO: OFF")

# Lista para armazenar pontos do gráfico
pontos_posicao = []
pontos_velocidade = []

# Relógio para controle de FPS
clock = pygame.time.Clock()
tempo_inicial = pygame.time.get_ticks()

def desenhar_seta(superficie, inicio, fim, cor=BRANCO, largura=2, tamanho_cabeca=10):
    dx = fim[0] - inicio[0]
    dy = fim[1] - inicio[1]
    angulo = math.atan2(dy, dx)
    
    # Desenha a linha principal
    pygame.draw.line(superficie, cor, inicio, fim, largura)
    
    # Desenha a cabeça da seta
    pygame.draw.polygon(superficie, cor, [
        fim,
        (fim[0] - tamanho_cabeca * math.cos(angulo - math.pi/6), 
         fim[1] - tamanho_cabeca * math.sin(angulo - math.pi/6)),
        (fim[0] - tamanho_cabeca * math.cos(angulo + math.pi/6), 
         fim[1] - tamanho_cabeca * math.sin(angulo + math.pi/6))
    ])

# Loop principal
executando = True
while executando:
    tempo_atual = pygame.time.get_ticks()
    dt = (tempo_atual - tempo_inicial) / 1000.0  # Delta time em segundos
    tempo_inicial = tempo_atual
    
    if not pausado:
        tempo += dt
    
    # Calcular nova posição usando S = S0 + v * t
    posicao_atual = posicao_inicial + velocidade * tempo
    
    # Adicionar pontos para gráficos
    if not pausado and tempo > 0:
        pontos_posicao.append((tempo, posicao_atual))
        pontos_velocidade.append((tempo, velocidade))
    
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_pausar.verificar_clique(evento.pos):
                pausado = not pausado
                botao_pausar.texto = "CONTINUAR" if pausado else "PAUSAR"
                botao_pausar.cor = AMARELO
                
            elif botao_reset.verificar_clique(evento.pos):
                tempo = 0
                pontos_posicao = []
                pontos_velocidade = []
                
            elif botao_formulas.verificar_clique(evento.pos):
                mostrar_formulas = not mostrar_formulas
                botao_formulas.texto = "FÓRMULAS: ON" if mostrar_formulas else "FÓRMULAS: OFF"
                
            elif botao_grafico.verificar_clique(evento.pos):
                mostrar_grafico = not mostrar_grafico
                botao_grafico.texto = "GRÁFICO: ON" if mostrar_grafico else "GRÁFICO: OFF"
    
    # Atualizar interface
    tela.fill(FUNDO)
    
    # Desenhar eixo e pista
    pygame.draw.line(tela, CINZA, (50, 300), (LARGURA - 50, 300), 3)
    for x in range(50, LARGURA - 40, 30):
        pygame.draw.line(tela, BRANCO, (x, 290), (x, 310), 2)
    
    # Desenhar carro
    carro_rect = carro_img.get_rect(midleft=(posicao_atual, 300))
    tela.blit(carro_img, carro_rect)
    
    # Desenhar vetor velocidade
    desenhar_seta(tela, 
                 (posicao_atual + 70, 280), 
                 (posicao_atual + 70 + velocidade, 280), 
                 VERDE, 3)
    
    # Desenhar informações
    pygame.draw.rect(tela, (40, 40, 60), (20, 20, LARGURA - 40, 150), border_radius=10)
    pygame.draw.rect(tela, AZUL, (20, 20, LARGURA - 40, 150), 2, border_radius=10)
    
    titulo = fonte_titulo.render("Movimento Uniforme (MU)", True, AMARELO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 30))
    
    texto = fonte.render("Características do MU: Velocidade constante, aceleração nula", True, BRANCO)
    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, 80))
    
    # Fórmulas
    if mostrar_formulas:
        formulas = [
            "Fórmulas:",
            f"Posição: S = S₀ + v * t",
            f"Velocidade: v = ΔS / Δt",
            f"Aceleração: a = 0"
        ]
        
        for i, formula in enumerate(formulas):
            texto_formula = fonte_pequena.render(formula, True, VERDE)
            tela.blit(texto_formula, (LARGURA//2 - 200, 110 + i * 30))
    
    # Valores atuais
    info_textos = [
        f"Tempo: {tempo:.1f}s",
        f"Posição Inicial (S₀): {posicao_inicial}m",
        f"Velocidade (v): {velocidade}m/s",
        f"Posição Atual (S): {posicao_atual:.1f}m"
    ]
    
    for i, texto_info in enumerate(info_textos):
        texto_surf = fonte.render(texto_info, True, BRANCO)
        tela.blit(texto_surf, (LARGURA - 350, 200 + i * 40))
    
    # Gráficos
    if mostrar_grafico and pontos_posicao:
        # Gráfico Posição x Tempo
        pygame.draw.rect(tela, (40, 40, 60), (50, 350, 400, 200), border_radius=10)
        pygame.draw.rect(tela, AZUL, (50, 350, 400, 200), 2, border_radius=10)
        
        titulo_grafico = fonte_pequena.render("Gráfico: Posição x Tempo", True, AMARELO)
        tela.blit(titulo_grafico, (250 - titulo_grafico.get_width()//2, 360))
        
        # Eixos
        pygame.draw.line(tela, BRANCO, (100, 500), (420, 500), 2)  # Eixo x
        pygame.draw.line(tela, BRANCO, (100, 500), (100, 370), 2)   # Eixo y
        
        # Desenhar setas
        desenhar_seta(tela, (100, 370), (100, 360), BRANCO, 2)
        desenhar_seta(tela, (420, 500), (430, 500), BRANCO, 2)
        
        # Legendas
        texto_x = fonte_pequena.render("Tempo (s)", True, BRANCO)
        tela.blit(texto_x, (420, 510))
        
        texto_y = fonte_pequena.render("Posição (m)", True, BRANCO)
        tela.blit(texto_y, (70, 350))
        
        # Desenhar curva
        if len(pontos_posicao) > 1:
            pontos_plot = []
            max_tempo = max(1, max(t for t, _ in pontos_posicao))
            max_pos = max(1, max(p for _, p in pontos_posicao))
            
            for t, p in pontos_posicao:
                x = 100 + (t / max_tempo) * 300
                y = 500 - (p / max_pos) * 120
                pontos_plot.append((x, y))
            
            pygame.draw.lines(tela, VERDE, False, pontos_plot, 3)
        
        # Gráfico Velocidade x Tempo
        pygame.draw.rect(tela, (40, 40, 60), (550, 350, 400, 200), border_radius=10)
        pygame.draw.rect(tela, AZUL, (550, 350, 400, 200), 2, border_radius=10)
        
        titulo_grafico = fonte_pequena.render("Gráfico: Velocidade x Tempo", True, AMARELO)
        tela.blit(titulo_grafico, (750 - titulo_grafico.get_width()//2, 360))
        
        # Eixos
        pygame.draw.line(tela, BRANCO, (600, 500), (920, 500), 2)  # Eixo x
        pygame.draw.line(tela, BRANCO, (600, 500), (600, 370), 2)   # Eixo y
        
        # Desenhar setas
        desenhar_seta(tela, (600, 370), (600, 360), BRANCO, 2)
        desenhar_seta(tela, (920, 500), (930, 500), BRANCO, 2)
        
        # Legendas
        texto_x = fonte_pequena.render("Tempo (s)", True, BRANCO)
        tela.blit(texto_x, (900, 510))
        
        texto_y = fonte_pequena.render("Velocidade (m/s)", True, BRANCO)
        tela.blit(texto_y, (570, 350))
        
        # Linha de velocidade constante
        pygame.draw.line(tela, VERMELHO, (600, 440), (920, 440), 3)
    
    # Desenhar botões
    botao_pausar.desenhar(tela)
    botao_reset.desenhar(tela)
    botao_formulas.desenhar(tela)
    botao_grafico.desenhar(tela)
    
    # Atualizar tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()