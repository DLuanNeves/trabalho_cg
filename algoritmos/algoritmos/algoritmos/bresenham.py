"""
Algoritmo de Bresenham - Rasterização de Linhas
Pontuação: 0.5
"""
import pygame
import sys
from .base import AlgoritmoBase

class Bresenham(AlgoritmoBase):
    def __init__(self, tela, largura, altura):
        super().__init__(tela, largura, altura)
        self.pontos = []
        self.passo_atual = 0
        self.ponto1 = None
        self.ponto2 = None
        self.animando = False
        self.finalizado = False
        
    def bresenham(self, x0, y0, x1, y1):
        """Implementação do algoritmo de Bresenham"""
        self.pontos = []
        self.passo_atual = 0
        self.finalizado = False
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        passo_x = 1 if x1 > x0 else -1
        passo_y = 1 if y1 > y0 else -1
        
        erro = 2 * dy - dx
        x, y = x0, y0
        
        self.pontos.append((x, y))
        
        if dy <= dx:
            for _ in range(dx):
                x += passo_x
                if erro >= 0:
                    y += passo_y
                    erro -= 2 * dx
                erro += 2 * dy
                self.pontos.append((x, y))
        else:
            for _ in range(dy):
                y += passo_y
                if erro >= 0:
                    x += passo_x
                    erro -= 2 * dy
                erro += 2 * dx
                self.pontos.append((x, y))
        
        self.animando = True
    
    def proximo_passo(self):
        if self.passo_atual < len(self.pontos) - 1:
            self.passo_atual += 1
        else:
            self.finalizado = True
            self.animando = False
    
    def desenhar(self):
        self.desenhar_grade()
        
        for i, (x, y) in enumerate(self.pontos[:self.passo_atual + 1]):
            px, py = self.coordenada_para_tela(x, y)
            if i == self.passo_atual:
                pygame.draw.circle(self.tela, (255, 50, 50), (px, py), 8)
            else:
                pygame.draw.circle(self.tela, (50, 200, 50), (px, py), 5)
        
        if self.passo_atual > 0:
            pontos_tela = [self.coordenada_para_tela(x, y) 
                          for x, y in self.pontos[:self.passo_atual + 1]]
            if len(pontos_tela) > 1:
                pygame.draw.lines(self.tela, (200, 200, 50), False, pontos_tela, 2)
        
        if self.ponto1:
            px, py = self.coordenada_para_tela(self.ponto1[0], self.ponto1[1])
            pygame.draw.circle(self.tela, (255, 255, 0), (px, py), 10, 2)
        if self.ponto2:
            px, py = self.coordenada_para_tela(self.ponto2[0], self.ponto2[1])
            pygame.draw.circle(self.tela, (255, 255, 0), (px, py), 10, 2)

class BresenhamInterface:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Bresenham - Rasterização de Linhas")
        self.clock = pygame.time.Clock()
        self.algoritmo = Bresenham(self.tela, self.largura, self.altura)
        self.fonte = pygame.font.Font(None, 24)
        self.auto_play = False
        self.ultimo_tempo = 0
        
    def executar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        px, py = evento.pos
                        x, y = self.algoritmo.tela_para_coordenada(px, py)
                        if -11 <= x <= 11 and -11 <= y <= 11:
                            if self.algoritmo.ponto1 is None:
                                self.algoritmo.ponto1 = (x, y)
                            elif self.algoritmo.ponto2 is None:
                                self.algoritmo.ponto2 = (x, y)
                                self.algoritmo.bresenham(
                                    self.algoritmo.ponto1[0], self.algoritmo.ponto1[1],
                                    self.algoritmo.ponto2[0], self.algoritmo.ponto2[1]
                                )
                                self.auto_play = True
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.algoritmo.proximo_passo()
                    elif evento.key == pygame.K_r:
                        self.algoritmo.ponto1 = None
                        self.algoritmo.ponto2 = None
                        self.algoritmo.pontos = []
                        self.algoritmo.passo_atual = 0
                        self.algoritmo.animando = False
                        self.algoritmo.finalizado = False
                        self.auto_play = False
                    elif evento.key == pygame.K_a:
                        self.auto_play = not self.auto_play
                    elif evento.key == pygame.K_ESCAPE:
                        rodando = False
            
            if self.auto_play and not self.algoritmo.finalizado:
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - self.ultimo_tempo > 200:
                    self.algoritmo.proximo_passo()
                    self.ultimo_tempo = tempo_atual
                    if self.algoritmo.finalizado:
                        self.auto_play = False
            
            self.tela.fill((30, 30, 40))
            self.algoritmo.desenhar()
            
            info = [
                "BRESENHAM - Clique em 2 pontos (-11 a 11)",
                f"P1: {self.algoritmo.ponto1}" if self.algoritmo.ponto1 else "P1: Clique",
                f"P2: {self.algoritmo.ponto2}" if self.algoritmo.ponto2 else "P2: Clique",
                f"Passo: {self.algoritmo.passo_atual}/{len(self.algoritmo.pontos)-1}",
                f"Auto-play: {'ON' if self.auto_play else 'OFF'}",
                "ESPAÇO: próximo | A: auto-play | R: reset | ESC: voltar"
            ]
            for i, texto in enumerate(info):
                surf = self.fonte.render(texto, True, (255, 255, 255))
                self.tela.blit(surf, (10, 10 + i * 25))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
