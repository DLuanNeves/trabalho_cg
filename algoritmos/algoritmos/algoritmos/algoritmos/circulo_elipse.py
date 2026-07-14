"""
Círculos e Elipses - Algoritmo de Bresenham
Pontuação: 0.5 + 0.5
"""
import pygame
import sys
from .base import AlgoritmoBase

class CirculoElipse(AlgoritmoBase):
    def __init__(self, tela, largura, altura):
        super().__init__(tela, largura, altura)
        self.pontos = []
        self.passo_atual = 0
        self.modo = "circulo"
        self.centro = (0, 0)
        self.raio_x = 0
        self.raio_y = 0
        self.animando = False
        self.finalizado = False
        
    def desenhar_pontos_simetricos(self, cx, cy, x, y):
        pontos = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        return pontos
    
    def desenhar_pontos_elipse(self, cx, cy, x, y):
        pontos = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y)
        ]
        return pontos
    
    def circulo_bresenham(self, cx, cy, raio):
        self.pontos = []
        self.passo_atual = 0
        self.centro = (cx, cy)
        self.raio_x = raio
        self.raio_y = raio
        self.modo = "circulo"
        self.finalizado = False
        
        x = 0
        y = raio
        p = 3 - 2 * raio
        
        self.pontos.extend(self.desenhar_pontos_simetricos(cx, cy, x, y))
        
        while x < y:
            x += 1
            if p < 0:
                p += 4 * x + 6
            else:
                y -= 1
                p += 4 * (x - y) + 10
            
            novos_pontos = self.desenhar_pontos_simetricos(cx, cy, x, y)
            self.pontos.extend(novos_pontos)
        
        self.animando = True
    
    def elipse_bresenham(self, cx, cy, rx, ry):
        self.pontos = []
        self.passo_atual = 0
        self.centro = (cx, cy)
        self.raio_x = rx
        self.raio_y = ry
        self.modo = "elipse"
        self.finalizado = False
        
        x = 0
        y = ry
        
        p1 = ry * ry - rx * rx * ry + (rx * rx) // 4
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y
        
        while dx < dy:
            self.pontos.extend(self.desenhar_pontos_elipse(cx, cy, x, y))
            x += 1
            dx += 2 * ry * ry
            if p1 < 0:
                p1 += dx + ry * ry
            else:
                y -= 1
                dy -= 2 * rx * rx
                p1 += dx - dy + ry * ry
        
        p2 = ry * ry * (x + 0.5) * (x + 0.5) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry
        
        while y >= 0:
            self.pontos.extend(self.desenhar_pontos_elipse(cx, cy, x, y))
            y -= 1
            dy -= 2 * rx * rx
            if p2 > 0:
                p2 += rx * rx - dy
            else:
                x += 1
                dx += 2 * ry * ry
                p2 += dx - dy + rx * rx
        
        self.animando = True
    
    def proximo_passo(self):
        passo = 8 if self.modo == "circulo" else 4
        if self.passo_atual < len(self.pontos) - passo:
            self.passo_atual += passo
        else:
            self.passo_atual = len(self.pontos) - 1
            self.finalizado = True
            self.animando = False
    
    def desenhar(self):
        self.desenhar_grade()
        
        cx, cy = self.coordenada_para_tela(self.centro[0], self.centro[1])
        pygame.draw.circle(self.tela, (255, 255, 0), (cx, cy), 8)
        pygame.draw.circle(self.tela, (255, 255, 0), (cx, cy), 12, 2)
        
        for i, (x, y) in enumerate(self.pontos[:self.passo_atual + 1]):
            px, py = self.coordenada_para_tela(x, y)
            if i == self.passo_atual:
                pygame.draw.circle(self.tela, (255, 50, 50), (px, py), 6)
            else:
                pygame.draw.circle(self.tela, (50, 200, 255), (px, py), 3)

class CirculoElipseInterface:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Círculos e Elipses - Bresenham")
        self.clock = pygame.time.Clock()
        self.algoritmo = CirculoElipse(self.tela, self.largura, self.altura)
        self.fonte = pygame.font.Font(None, 24)
        self.cx = self.cy = self.rx = self.ry = 0
        self.parametro_atual = "cx"
        self.auto_play = False
        self.ultimo_tempo = 0
        
    def executar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_c:
                        self.algoritmo.modo = "circulo"
                        self.parametro_atual = "cx"
                    elif evento.key == pygame.K_e:
                        self.algoritmo.modo = "elipse"
                        self.parametro_atual = "cx"
                    elif evento.key == pygame.K_TAB:
                        params = ["cx", "cy", "rx", "ry"] if self.algoritmo.modo == "elipse" else ["cx", "cy", "rx"]
                        idx = (params.index(self.parametro_atual) + 1) % len(params)
                        self.parametro_atual = params[idx]
                    elif evento.key == pygame.K_RETURN:
                        if self.algoritmo.modo == "circulo":
                            self.algoritmo.circulo_bresenham(self.cx, self.cy, abs(self.rx) or 5)
                        else:
                            self.algoritmo.elipse_bresenham(self.cx, self.cy, abs(self.rx), abs(self.ry))
                        self.auto_play = True
                    elif evento.key == pygame.K_UP:
                        self.ajustar_parametro(1)
                    elif evento.key == pygame.K_DOWN:
                        self.ajustar_parametro(-1)
                    elif evento.key == pygame.K_SPACE:
                        self.algoritmo.proximo_passo()
                    elif evento.key == pygame.K_r:
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
                if tempo_atual - self.ultimo_tempo > 150:
                    self.algoritmo.proximo_passo()
                    self.ultimo_tempo = tempo_atual
                    if self.algoritmo.finalizado:
                        self.auto_play = False
            
            self.tela.fill((30, 30, 40))
            self.algoritmo.desenhar()
            
            info = [
                f"MODO: {self.algoritmo.modo.upper()}",
                f"Centro: ({self.cx}, {self.cy})",
                f"Raio X: {self.rx}",
                f"Raio Y: {self.ry}" if self.algoritmo.modo == "elipse" else "",
                f"Parâmetro: {self.parametro_atual} (↑↓ ajusta)",
                f"Auto-play: {'ON' if self.auto_play else 'OFF'}",
                "C: círculo | E: elipse | TAB: muda parâmetro",
                "ENTER: desenhar | ESPAÇO: próximo | R: reset | ESC: voltar"
            ]
            for i, texto in enumerate(info):
                if texto:
                    surf = self.fonte.render(texto, True, (255, 255, 255))
                    self.tela.blit(surf, (10, 10 + i * 25))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def ajustar_parametro(self, valor):
        if self.parametro_atual == "cx":
            self.cx += valor
        elif self.parametro_atual == "cy":
            self.cy += valor
        elif self.parametro_atual == "rx":
            self.rx += valor
        elif self.parametro_atual == "ry":
            self.ry += valor
