from constantes import *
from Onca import Onca
from Crocodilo import Crocodilo
from Formiga import Formiga
from Planta import Planta
from Adaga import Adaga
from Pistola import Pistola
from Espada import Espada
from AreiaMovediça import AreiaMovedica
from GasVenenoso import GasVenenoso
from PVenenosa import PVenenosa
from Vertice import Vertice
import random


class Grafo:

        def __init__(self):
            self.qtd_vertices = LINHAS * COLUNAS
            self.vertices = [Vertice(i) for i in range(self.qtd_vertices)] #Cria todas as instâncias de vértices
            self.qtd_inimigos = 0
            self.qtd_plantas = 0
            self.qtd_armas = 0
            self.qtd_perigos = 0
            self.grafo = {self.vertices[i]: [] for i in range(self.qtd_vertices)} # Cria o grafo utilizando as instâncias de vértices, colocando em cada chave um vértice e criando uma lista para cada chave/vértice
            self.preencher_grafo()

        #Funções para  o Grafo
        def adicionar_aresta(self, u, v):
            if v not in self.grafo[u]:
                self.grafo[u].append(v)
            if u not in self.grafo[v]:
                self.grafo[v].append(u)

        def preencher_grafo(self):
            for i in range(self.qtd_vertices):
                linha = i // COLUNAS
                coluna = i % COLUNAS
                vizinhos = []
                if linha > 0:
                    vizinhos.append(self.vertices[i - COLUNAS])
                if linha < LINHAS - 1:
                    vizinhos.append(self.vertices[i + COLUNAS])
                if coluna > 0:
                    vizinhos.append(self.vertices[i - 1])
                if coluna < COLUNAS - 1:
                    vizinhos.append(self.vertices[i + 1])
                for vizinho in vizinhos:
                    self.adicionar_aresta(self.vertices[i], vizinho)

        def imprimir_indices_vertices(self):
            for vertice in self.vertices:
                print(f"Índice do vértice: {vertice.indice}")

        def imprimir_lista_adjacencias(self):
            print("Grafo representado por lista de adjacências:")
            for vertice, vizinhos in self.grafo.items():
                vizinhos_indices = [vizinho.indice for vizinho in vizinhos]
                print(f"{vertice.indice}: {vizinhos_indices}")

        def imprimir_matriz_adjacencias(self):
            matriz_adjacencias = [[0] * self.qtd_vertices for _ in range(self.qtd_vertices)]

            for vertice, vizinhos in self.grafo.items():
                for vizinho in vizinhos:
                    matriz_adjacencias[vertice.indice][vizinho.indice] = 1

            for linha in matriz_adjacencias:
                print(linha)

        def acessar_vertice_por_indice(self, indice):
            for lista_vertices in self.grafo.values():
                for vertice in lista_vertices:
                    if vertice.indice == indice:
                        return vertice
            return None

        #Funções para o Pygame:
        def associar_posicoes_aos_vertices(self):
            posicao_vertices = []  # conjunto de posicoes (x,y) dos vértices

            espacamento_x = TELA_MENU_LARGURA // (COLUNAS + 1)
            espacamento_y = 100

            for linha in range(LINHAS):
                for coluna in range(COLUNAS):
                    x = (coluna * espacamento_x) + 200
                    y = (linha * espacamento_y) + 100
                    posicao_vertices.append((x, y))

            for i, vertice in enumerate(self.vertices):  # de 0 a 24
                vertice.posicao = posicao_vertices[i]

        def desenhar_ilha(self, tela):
            for vertice in self.vertices:
                # Desenha vértices
                pygame.draw.circle(tela, MARROM, vertice.posicao, 10)

            for vertice, vizinhos in self.grafo.items():
                for vizinho in vizinhos:
                    # Desenha uma linha entre o vértice atual e seu vizinho
                    pygame.draw.line(tela, MARROM, vertice.posicao, vizinho.posicao, 2)

        def imprimir_objetos_dos_vertices(self):
            for vertice in self.vertices:
                print(f"Índice do vértice: {vertice.indice}")
                print(f"Lista de objetos: {vertice.objetos}")

        def distribuir_plantas(self):
            vertices_indices = list(range(1, self.qtd_vertices))
            random.shuffle(vertices_indices)
            for i in range(min(self.qtd_plantas, len(vertices_indices))): #o número total de plantas distribuídas é o menor entre o número de plantas especificado e o número total de vértices disponíveis
                vertice_index = vertices_indices[i]
                planta = Planta()
                self.vertices[vertice_index].objetos.append(planta)

        def distribuir_inimigos(self):
            vertices_indices = list(range(1, self.qtd_vertices))
            random.shuffle(vertices_indices)

            for i in range(min(self.qtd_inimigos, len(vertices_indices))):
                vertice_index = vertices_indices[i]
                inimigo = random.choice([Onca(), Crocodilo(), Formiga()])
                while any(isinstance(objeto, Planta) for objeto in self.vertices[vertice_index].objetos): # verificamos se o vértice escolhido aleatoriamente já contém uma planta. Se sim, escolhemos um novo vértice aleatório
                    vertice_index = random.choice(vertices_indices)
                self.vertices[vertice_index].objetos.append(inimigo)

        def distribuir_armas(self):
            vertices_indices = list(range(1, self.qtd_vertices))
            random.shuffle(vertices_indices)

            for i in range(min(self.qtd_armas, len(vertices_indices))):
                vertice_index = vertices_indices[i]
                arma = random.choice([Adaga(), Pistola(), Espada()])
                while any(isinstance(objeto, (Crocodilo, Onca, Formiga)) for objeto in
                          self.vertices[vertice_index].objetos):
                    vertice_index = random.choice(vertices_indices)
                self.vertices[vertice_index].objetos.append(arma)

        def distribuir_perigos(self):
            vertices_indices = list(range(1, self.qtd_vertices))
            random.shuffle(vertices_indices)

            for i in range(min(self.qtd_perigos, len(vertices_indices))):
                vertice_index = vertices_indices[i]
                perigo = random.choice([AreiaMovedica(), GasVenenoso(),PVenenosa()])
                while any(isinstance(objeto, Planta) for objeto in self.vertices[vertice_index].objetos) or \
                        any(isinstance(objeto, (Crocodilo, Onca, Formiga)) for objeto in
                            self.vertices[vertice_index].objetos):
                    vertice_index = random.choice(vertices_indices)
                self.vertices[vertice_index].objetos.append(perigo)

        def obter_descricao_vertice(self, jogador):
            indice_vertice_posicao_jogador = jogador.posicao
            vertice_que_o_jogador_esta = self.vertices[indice_vertice_posicao_jogador]

            #Se tiver algum objeto no vértice:
            if vertice_que_o_jogador_esta.objetos:
                # Se a lista de objetos do vértice não estiver vazia, retorna a descrição de cada objeto
                descricoes = [objeto.descricao for objeto in vertice_que_o_jogador_esta.objetos]

                return descricoes

            else:
                # Se a lista de objetos do vértice estiver vazia, retorna que o vértice está vazio
                return ["Vertice sem nenhum objeto"]