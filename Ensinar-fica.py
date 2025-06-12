import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela Full HD
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

# Objeto em movimento - tamanho relativo
carro_largura = int(LARGURA * 0.04)  # 4% da largura da tela
carro_altura = int(ALTURA * 0.04)    # 4% da altura da tela
carro_img = pygame.Surface((carro_largura, carro_altura), pygame.SRCALPHA)
pygame.draw.rect(carro_img, AZUL, (0, carro_altura//4, carro_largura*0.875, carro_altura*0.75), border_radius=8)
pygame.draw.rect(carro_img, (180, 220, 255), (carro_largura*0.125, carro_altura*0.375, carro_largura*0.25, carro_altura*0.5))
pygame.draw.rect(carro_img, (180, 220, 255), (carro_largura*0.5, carro_altura*0.375, carro_largura*0.25, carro_altura*0.5))
pygame.draw.rect(carro_img, (200, 230, 255), (carro_largura*0.75, carro_altura*0.375, carro_largura*0.125, carro_altura*0.25))

# Fontes com tamanhos relativos
fonte_tamanho = int(ALTURA * 0.03)  # 3% da altura
fonte_pequena_tamanho = int(ALTURA * 0.025) # 2.5% da altura
fonte_titulo_tamanho = int(ALTURA * 0.045) # 4.5% da altura

fonte = pygame.font.SysFont(None, fonte_tamanho)
fonte_pequena = pygame.font.SysFont(None, fonte_pequena_tamanho)
fonte_titulo = pygame.font.SysFont(None, fonte_titulo_tamanho, bold=True)

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor=VERDE, cor_texto=BRANCO):
        # As coordenadas e dimensões são dadas em frações da tela
        self.rect = pygame.Rect(
            int(LARGURA * x),
            int(ALTURA * y),
            int(LARGURA * largura),
            int(ALTURA * altura)
        )
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

# Criar botões com posições e tamanhos relativos
botao_pausar = Botao(0.04, 0.83, 0.1, 0.05, "PAUSAR" if not pausado else "CONTINUAR", AMARELO)
botao_reset = Botao(0.15, 0.83, 0.1, 0.05, "REINICIAR", VERMELHO)
botao_formulas = Botao(0.26, 0.83, 0.12, 0.05, "FÓRMULAS: ON" if mostrar_formulas else "FÓRMULAS: OFF")
botao_grafico = Botao(0.39, 0.83, 0.12, 0.05, "GRÁFICO: ON" if mostrar_grafico else "GRÁFICO: OFF")

# Lista para armazenar pontos do gráfico
pontos_posicao = []
pontos_velocidade = []

# Relógio para controle de FPS
clock = pygame.time.Clock()
tempo_inicial = pygame.time.get_ticks()

def desenhar_seta(superficie, inicio, fim, cor=BRANCO, largura=2, tamanho_cabeca=None):
    if tamanho_cabeca is None:
        tamanho_cabeca = ALTURA * 0.015  # 1.5% da altura
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

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                pausado = not pausado
                botao_pausar.texto = "CONTINUAR" if pausado else "PAUSAR"
                botao_pausar.cor = AMARELO
            elif evento.key == pygame.K_r:
                tempo = 0
                pontos_posicao = []
                pontos_velocidade = []
    
    # Atualizar interface
    tela.fill(FUNDO)
    
    # Desenhar eixo e pista
    eixo_y = ALTURA // 2  # Centro da tela
    pygame.draw.line(tela, CINZA, (int(LARGURA * 0.05), eixo_y), (int(LARGURA * 0.95), eixo_y), 3)
    for x in range(int(LARGURA * 0.05), int(LARGURA * 0.95), int(LARGURA * 0.03)):
        pygame.draw.line(tela, BRANCO, (x, eixo_y - 10), (x, eixo_y + 10), 2)
    
    # Desenhar carro
    carro_rect = carro_img.get_rect(midleft=(posicao_atual, eixo_y))
    tela.blit(carro_img, carro_rect)
    
    # Desenhar vetor velocidade
    desenhar_seta(tela, 
                 (posicao_atual + carro_largura, eixo_y - 30), 
                 (posicao_atual + carro_largura + velocidade, eixo_y - 30), 
                 VERDE, 3)
    
    # Desenhar informações
    pygame.draw.rect(tela, (40, 40, 60), 
                    (int(LARGURA * 0.02), int(ALTURA * 0.02), 
                    int(LARGURA * 0.96), int(ALTURA * 0.15)), 
                    border_radius=10)
    pygame.draw.rect(tela, AZUL, 
                    (int(LARGURA * 0.02), int(ALTURA * 0.02), 
                    int(LARGURA * 0.96), int(ALTURA * 0.15)), 
                    2, border_radius=10)
    
    titulo = fonte_titulo.render("Movimento Uniforme (MU)", True, AMARELO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, int(ALTURA * 0.05)))
    
    texto = fonte.render("Características do MU: Velocidade constante, aceleração nula", True, BRANCO)
    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, int(ALTURA * 0.1)))
    
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
            tela.blit(texto_formula, (int(LARGURA * 0.10), int(ALTURA * 0.05) + i * int(ALTURA * 0.03)))
    
    # Valores atuais
    info_textos = [
        f"Tempo: {tempo:.1f}s",
        f"Posição Inicial (S₀): {posicao_inicial}m",
        f"Velocidade (v): {velocidade}m/s",
        f"Posição Atual (S): {posicao_atual:.1f}m"
    ]
    
    for i, texto_info in enumerate(info_textos):
        texto_surf = fonte.render(texto_info, True, BRANCO)
        tela.blit(texto_surf, (int(LARGURA * 0.7), int(ALTURA * 0.02) + i * int(ALTURA * 0.04)))
    
    # Gráficos
    if mostrar_grafico and pontos_posicao:
        # Gráfico Posição x Tempo
        pygame.draw.rect(tela, (40, 40, 60), 
                        (int(LARGURA * 0.05), int(ALTURA * 0.6), 
                        int(LARGURA * 0.4), int(ALTURA * 0.3)), 
                        border_radius=10)
        pygame.draw.rect(tela, AZUL, 
                        (int(LARGURA * 0.05), int(ALTURA * 0.6), 
                        int(LARGURA * 0.4), int(ALTURA * 0.3)), 
                        2, border_radius=10)
        
        titulo_grafico = fonte_pequena.render("Gráfico: Posição x Tempo", True, AMARELO)
        tela.blit(titulo_grafico, (int(LARGURA * 0.25) - titulo_grafico.get_width()//2, int(ALTURA * 0.61)))
        
        # Eixos
        inicio_x = int(LARGURA * 0.1)
        fim_x = int(LARGURA * 0.4)
        eixo_y_grafico = int(ALTURA * 0.85)
        pygame.draw.line(tela, BRANCO, (inicio_x, eixo_y_grafico), (fim_x, eixo_y_grafico), 2)  # Eixo x
        pygame.draw.line(tela, BRANCO, (inicio_x, eixo_y_grafico), (inicio_x, int(ALTURA * 0.65)), 2)   # Eixo y
        
        # Desenhar setas
        desenhar_seta(tela, (inicio_x, int(ALTURA * 0.65)), (inicio_x, int(ALTURA * 0.64)), BRANCO, 2)
        desenhar_seta(tela, (fim_x, eixo_y_grafico), (fim_x + 10, eixo_y_grafico), BRANCO, 2)
        
        # Legendas
        texto_x = fonte_pequena.render("Tempo (s)", True, BRANCO)
        tela.blit(texto_x, (fim_x, eixo_y_grafico + 10))
        
        texto_y = fonte_pequena.render("Posição (m)", True, BRANCO)
        tela.blit(texto_y, (inicio_x - 50, int(ALTURA * 0.63)))
        
        # Desenhar curva
        if len(pontos_posicao) > 1:
            pontos_plot = []
            max_tempo = max(1, max(t for t, _ in pontos_posicao))
            max_pos = max(1, max(p for _, p in pontos_posicao))
            
            for t, p in pontos_posicao:
                x = inicio_x + (t / max_tempo) * (fim_x - inicio_x)
                y = eixo_y_grafico - (p / max_pos) * (eixo_y_grafico - int(ALTURA * 0.65))
                pontos_plot.append((x, y))
            
            pygame.draw.lines(tela, VERDE, False, pontos_plot, 3)
        
        # Gráfico Velocidade x Tempo
        pygame.draw.rect(tela, (40, 40, 60), 
                        (int(LARGURA * 0.55), int(ALTURA * 0.6), 
                        int(LARGURA * 0.4), int(ALTURA * 0.3)), 
                        border_radius=10)
        pygame.draw.rect(tela, AZUL, 
                        (int(LARGURA * 0.55), int(ALTURA * 0.6), 
                        int(LARGURA * 0.4), int(ALTURA * 0.3)), 
                        2, border_radius=10)
        
        titulo_grafico = fonte_pequena.render("Gráfico: Velocidade x Tempo", True, AMARELO)
        tela.blit(titulo_grafico, (int(LARGURA * 0.75) - titulo_grafico.get_width()//2, int(ALTURA * 0.61)))
        
        # Eixos
        inicio_x = int(LARGURA * 0.6)
        fim_x = int(LARGURA * 0.9)
        eixo_y_grafico = int(ALTURA * 0.85)
        pygame.draw.line(tela, BRANCO, (inicio_x, eixo_y_grafico), (fim_x, eixo_y_grafico), 2)  # Eixo x
        pygame.draw.line(tela, BRANCO, (inicio_x, eixo_y_grafico), (inicio_x, int(ALTURA * 0.65)), 2)   # Eixo y
        
        # Desenhar setas
        desenhar_seta(tela, (inicio_x, int(ALTURA * 0.65)), (inicio_x, int(ALTURA * 0.64)), BRANCO, 2)
        desenhar_seta(tela, (fim_x, eixo_y_grafico), (fim_x + 10, eixo_y_grafico), BRANCO, 2)
        
        # Legendas
        texto_x = fonte_pequena.render("Tempo (s)", True, BRANCO)
        tela.blit(texto_x, (fim_x, eixo_y_grafico + 10))
        
        texto_y = fonte_pequena.render("Velocidade (m/s)", True, BRANCO)
        tela.blit(texto_y, (inicio_x - 60, int(ALTURA * 0.63)))
        
        # Linha de velocidade constante
        escala_velocidade = 100
        y_vel = eixo_y_grafico - (velocidade / escala_velocidade) * (eixo_y_grafico - int(ALTURA * 0.65))
        pygame.draw.line(tela, VERMELHO, (inicio_x, y_vel), (fim_x, y_vel), 3)
    
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
