"""
TRABALHO DE COMPUTAÇÃO GRÁFICA - 2026
Síntese de Imagem - Todos os Algoritmos

Autores: [Seu Nome] e [Nome do Colega]
Professor: Dr. Bianchi Serique Meiguins
"""

import pygame
import sys
from algoritmos.bresenham import BresenhamInterface
from algoritmos.circulo_elipse import CirculoElipseInterface
from algoritmos.bezier import BezierInterface

class MenuPrincipal:
    def __init__(self):
        pygame.init()
        self.largura = 900
        self.altura = 700
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Trabalho CG 2026 - Síntese de Imagem")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 32)
        self.fonte_pequena = pygame.font.Font(None, 24)
        self.opcoes = [
            "1. Bresenham (Linhas)",
            "2. Círculos e Elipses",
            "3. Curvas de Bézier (Grau 2 e 3)",
            "4. Sair"
        ]
        self.opcao_selecionada = 0
        
    def desenhar_menu(self):
        self.tela.fill((20, 20, 30))
        
        titulo = self.fonte.render("TRABALHO DE COMPUTAÇÃO GRÁFICA - 2026", True, (255, 200, 50))
        self.tela.blit(titulo, (self.largura//2 - titulo.get_width()//2, 30))
        
        subtitulo = self.fonte_pequena.render("Síntese de Imagem - Algoritmos Rasterização", True, (200, 200, 200))
        self.tela.blit(subtitulo, (self.largura//2 - subtitulo.get_width()//2, 70))
        
        pygame.draw.line(self.tela, (100, 100, 100), (50, 100), (self.largura-50, 100), 1)
        
        for i, opcao in enumerate(self.opcoes):
            cor = (255, 255, 0) if i == self.opcao_selecionada else (255, 255, 255)
            cor_fundo = (60, 60, 80) if i == self.opcao_selecionada else (30, 30, 40)
            
            rect = pygame.Rect(100, 130 + i * 55, self.largura - 200, 45)
            pygame.draw.rect(self.tela, cor_fundo, rect)
            pygame.draw.rect(self.tela, cor, rect, 2 if i == self.opcao_selecionada else 1)
            
            texto = self.fonte_pequena.render(opcao, True, cor)
            self.tela.blit(texto, (120, 140 + i * 55))
        
        rodape = self.fonte_pequena.render("↑↓: Navegar | ENTER: Selecionar | ESC: Sair", True, (150, 150, 150))
        self.tela.blit(rodape, (self.largura//2 - rodape.get_width()//2, self.altura - 40))
        
        pygame.display.flip()
    
    def executar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
                    elif evento.key == pygame.K_DOWN:
                        self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
                    elif evento.key == pygame.K_RETURN:
                        self.executar_opcao(self.opcao_selecionada)
                    elif evento.key == pygame.K_ESCAPE:
                        rodando = False
            
            self.desenhar_menu()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def executar_opcao(self, indice):
        if indice == 0:
            BresenhamInterface().executar()
        elif indice == 1:
            CirculoElipseInterface().executar()
        elif indice == 2:
            BezierInterface().executar()
        elif indice == 3:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    MenuPrincipal().executar()
