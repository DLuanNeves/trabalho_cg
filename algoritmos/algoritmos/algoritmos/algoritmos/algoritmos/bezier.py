"""
Curvas de Bézier - Graus 2 e 3
Pontuação: 1.0 + 1.0
"""
import pygame
import sys
from .base import AlgoritmoBase

class Bezier(AlgoritmoBase):
    def __init__(self, tela, largura, altura):
        super().__init__(tela, largura, altura)
        self.pontos_controle = []
        self.pontos_curva = []
        self.passo_atual = 0
        self.grau = 2
        self.animando = False
        self.finalizado = False
        
    def bezier_recursivo(self, pontos, t):
        if len(pontos) == 1:
            return pontos[0]
        novos_pontos = []
        for i in range(len(pontos) - 1):
            x = (1 - t) * pontos[i][0] + t * pontos[i + 1][0]
            y = (1 - t) * pontos[i][1] + t * pontos[i + 1][1]
            novos_pontos.append((x, y))
        return self.bezier_recursivo(novos_pontos, t)
    
    def calcular_bezier(self, pontos_controle, num_pontos=100):
        self.pontos_controle = pontos_controle
        self.pontos_curva = []
        self.passo_atual = 0
        self.grau = len(pontos_controle) - 1
        
        for i in range(num_pontos + 1):
            t = i / num_pontos
            ponto = self.bezier_recursivo(pontos_controle, t)
            self.pontos_curva.append(ponto)
        
        self.animando = True
        self.finalizado = False
    
    def proximo_passo(self):
        if self.passo_atual < len(self.pontos_curva) - 1:
            self.passo_atual += 1
        else:
            self.finalizado = True
            self.animando = False
    
    def desenhar(self):
        self.desenhar_grade()
        
        for i, (x, y) in enumerate(self.pontos_controle):
            px, py = self.coordenada_para_tela(x, y)
            cor = (255, 200, 50) if i == 0 or i == len(self.pontos_controle)-1 else (255, 150, 50)
            pygame.draw.circle(self.tela, cor, (px, py), 8)
            fonte = pygame.font.Font(None, 18)
            texto = fonte.render(f"P{i}", True, (255, 255, 255))
            self.tela.blit(texto, (px + 10, py - 8))
        
        if len(self.pontos_controle) > 1:
            pontos_tela = [self.coordenada_para_tela(x, y) for x, y in self.pontos_controle]
            pygame.draw.lines(self.tela, (100, 100, 150), False, pontos_tela, 1)
        
        if self.passo_atual > 0:
            pontos_tela = [self.coordenada_para_tela(x, y) 
                          for x, y in self.pontos_curva[:self.passo_atual + 1]]
            if len(pontos_tela) > 1:
                pygame.draw.lines(self.tela, (50, 255, 100), False, pontos_tela, 3)
        
        if self.passo_atual > 0 and self.passo_atual < len(self.pontos_curva):
            x, y = self.pontos_curva[self.passo_atual]
            px, py = self.coordenada_para_tela(x, y)
            pygame.draw.circle(self.tela, (255, 50, 50), (px, py), 6)

class BezierInterface:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Curvas de Bézier")
        self.clock = pygame.time.Clock()
        self.algoritmo = Bezier(self.tela, self.largura, self.altura)
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
                            if len(self.algoritmo.pontos_controle) < 4:
                                self.algoritmo.pontos_controle.append((x, y))
                                if len(self.algoritmo.pontos_controle) >= 3:
                                    self.algoritmo.calcular_bezier(self.algoritmo.pontos_controle)
                                    self.auto_play = True
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.algoritmo.proximo_passo()
                    elif evento.key == pygame.K_r:
                        self.algoritmo.pontos_controle = []
                        self.algoritmo.pontos_curva = []
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
                if tempo_atual - self.ultimo_tempo > 50:
                    self.algoritmo.proximo_passo()
                    self.ultimo_tempo = tempo_atual
                    if self.algoritmo.finalizado:
                        self.auto_play = False
            
            self.tela.fill((30, 30, 40))
            self.algoritmo.desenhar()
            
            info = [
                f"BÉZIER - Grau {self.algoritmo.grau}",
                f"Pontos: {len(self.algoritmo.pontos_controle)}/{self.algoritmo.grau + 1}",
                f"Passo: {self.algoritmo.passo_atual}/{len(self.algoritmo.pontos_curva)-1}",
                f"Auto-play: {'ON' if self.auto_play else 'OFF'}",
                "Clique para adicionar pontos de controle (mínimo 3)",
                "ESPAÇO: próximo | A: auto-play | R: reset | ESC: voltar"
            ]
            for i, texto in enumerate(info):
                if texto:
                    surf = self.fonte.render(texto, True, (255, 255, 255))
                    self.tela.blit(surf, (10, 10 + i * 25))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
