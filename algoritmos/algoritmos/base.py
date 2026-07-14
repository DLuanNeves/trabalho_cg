"""
Classe base para todos os algoritmos - Contém funções comuns
"""
import pygame

class AlgoritmoBase:
    def __init__(self, tela, largura, altura):
        self.tela = tela
        self.largura = largura
        self.altura = altura
        self.limite = 11
        
    def coordenada_para_tela(self, x, y):
        """Converte coordenada do sistema (-11..11) para pixel da tela"""
        cx = int((x + self.limite) / (2 * self.limite) * self.largura)
        cy = int((self.limite - y) / (2 * self.limite) * self.altura)
        return cx, cy
    
    def tela_para_coordenada(self, px, py):
        """Converte pixel da tela para coordenada do sistema"""
        x = (px / self.largura) * (2 * self.limite) - self.limite
        y = self.limite - (py / self.altura) * (2 * self.limite)
        return round(x), round(y)
    
    def desenhar_grade(self):
        """Desenha a grade de coordenadas"""
        # Eixos X e Y
        pygame.draw.line(self.tela, (80, 80, 80), 
                        (0, self.altura//2), (self.largura, self.altura//2), 1)
        pygame.draw.line(self.tela, (80, 80, 80), 
                        (self.largura//2, 0), (self.largura//2, self.altura), 1)
        
        # Marcadores
        fonte = pygame.font.Font(None, 16)
        for i in range(-self.limite, self.limite + 1):
            if i == 0: continue
            x, y = self.coordenada_para_tela(i, 0)
            pygame.draw.circle(self.tela, (100, 100, 100), (x, self.altura//2), 2)
            pygame.draw.circle(self.tela, (100, 100, 100), (self.largura//2, y), 2)
            
            if i % 2 == 0:
                texto = fonte.render(str(i), True, (100, 100, 100))
                self.tela.blit(texto, (x - 8, self.altura//2 + 8))
                self.tela.blit(texto, (self.largura//2 + 8, y - 8))
    
    def desenhar_informacoes(self, info_list):
        """Desenha informações na tela"""
        fonte = pygame.font.Font(None, 20)
        for i, texto in enumerate(info_list):
            if texto:
                surf = fonte.render(texto, True, (200, 200, 200))
                self.tela.blit(surf, (10, 10 + i * 25))
