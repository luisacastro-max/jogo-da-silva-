class Edge:
    def __init__(self, target, weight, item_required=None):
        self.target = target
        self.weight = weight
        self.item_required = item_required # Item necessário para passar por esta aresta
        

class Vertex:
    def __init__(self, name, description="", item_present=None, special_message=None):
        self.name = name
        self.description = description
        self.adjacents = []
        self.item_present = item_present # Se este local tem um item para o jogador pegar
        self.special_message = special_message # Mensagem especial ao entrar neste local
        
    def addEdge(self, target, weight, item_required=None):
        self.adjacents.append(Edge(target, weight, item_required))
        

class Graph:
    def __init__(self):
        self.vertices = {}
        
    def addVertex(self, name, description="", item_present=None, special_message=None):
        if name not in self.vertices:
            self.vertices[name] = Vertex(name, description, item_present, special_message)
            
    def addEdge(self, source, target, weight, item_required=None):
        # Garante que os vértices existam antes de adicionar a aresta
        if source not in self.vertices:
            self.addVertex(source)
        if target not in self.vertices:
            self.addVertex(target)
        self.vertices[source].addEdge(target, weight, item_required) 
    
    def findPath(self, graph, source, target, visited=None, path=None):
        # Inicializa visited e path se forem None para a primeira chamada
        if visited is None:
            visited = set()
        if path is None:
            path = []

        # Evita ciclos infinitos em grafos com ciclos
        if source in visited:
            return
        
        visited.add(source)
        path.append(source)
        
        # Se encontrou o alvo, retorna uma cópia do caminho
        if source == target:
            return path.copy()
            
        # Explora os vizinhos
        for edge in self.vertices[source].adjacents:
            result = self.findPath(graph, edge.target, target, visited, path)
            if result:
                return result
        
        # Se não encontrou caminho por esta ramificação, remove o último vértice
        path.pop()

# --- Lógica do Jogo ---

def run_game():
    game_graph = Graph()

    # Criando o Cenário do Jogo (Vértices e Arestas)
    # Cada vértice representa um local no jogo, com uma descrição e, opcionalmente, um item.
    game_graph.addVertex("Entrada da Floresta", "Você está na entrada de uma floresta densa. O cheiro de terra molhada paira no ar.")
    game_graph.addVertex("Clareira Secreta", "Uma clareira iluminada pelo sol, com flores raras e um riacho murmurante.")
    game_graph.addVertex("Caverna Sombria", "A entrada de uma caverna escura e úmida. Sons estranhos ecoam lá de dentro.", item_present="Amuleto Antigo") 
    game_graph.addVertex("Montanha Nebulosa", "Um pico rochoso coberto por uma névoa espessa. A vista é limitada, mas o ar é gélido.", item_present="Chave Antiga", special_message="Você sente uma presença maligna... Um Guardião da Montanha bloqueia o caminho para o leste!") 
    game_graph.addVertex("Templo Antigo", "As ruínas de um templo esquecido, com símbolos gravados nas pedras. Parece haver algo brilhando lá dentro...", item_present="Tesouro")
    game_graph.addVertex("Lago Calmo", "Um lago de águas cristalinas, refletindo o céu. Pequenos peixes nadam tranquilamente.")

    # Definindo as conexões (arestas) entre os locais.
    # O 'weight' é o nome do caminho. 'item_required' indica um item necessário para passar.
    game_graph.addEdge("Entrada da Floresta", "Clareira Secreta", "Trilha Leste")
    game_graph.addEdge("Clareira Secreta", "Entrada da Floresta", "Trilha Oeste") 
    game_graph.addEdge("Entrada da Floresta", "Caverna Sombria", "Caminho Rochoso")
    game_graph.addEdge("Caverna Sombria", "Entrada da Floresta", "Voltar")
    game_graph.addEdge("Clareira Secreta", "Lago Calmo", "Atravessar Rio")
    game_graph.addEdge("Lago Calmo", "Clareira Secreta", "Voltar")
    
    game_graph.addEdge("Caverna Sombria", "Montanha Nebulosa", "Passagem Estreita")
    game_graph.addEdge("Montanha Nebulosa", "Caverna Sombria", "Descer")
    
    # Caminho protegido pelo "boss" que exige o "Amuleto Antigo"
    game_graph.addEdge("Montanha Nebulosa", "Templo Antigo", "Caminho Secreto", item_required="Amuleto Antigo") 
    game_graph.addEdge("Templo Antigo", "Montanha Nebulosa", "Voltar") 
    
    # Caminho alternativo que exige a "Chave Antiga"
    game_graph.addEdge("Lago Calmo", "Templo Antigo", "Ponte Quebrada", item_required="Chave Antiga") 
    game_graph.addEdge("Templo Antigo", "Lago Calmo", "Voltar Pela Ponte")


    current_location = "Entrada da Floresta" # Onde o jogador começa sua jornada
    player_items = [] # Lista para armazenar os itens que o jogador coletou

    print("Bem-vindo ao Jogo de Exploração do Grafo!")
    print("Seu objetivo é encontrar o 'Tesouro' no Templo Antigo!")
    print("Para chegar lá, você precisará ser esperto e encontrar os itens certos!")

    # Loop principal do jogo: continua até o jogador encontrar o tesouro ou sair
    while True:
        print("\n" + "="*40) # Separador visual para cada turno
        print(f"Local: {game_graph.vertices[current_location].name}")
        print(f"Descrição: {game_graph.vertices[current_location].description}")
        
        # Exibe uma mensagem especial se o local tiver uma
        if game_graph.vertices[current_location].special_message:
            print(f"\n[EVENTO]: {game_graph.vertices[current_location].special_message}")

        # Verifica se há um item para coletar no local atual
        if game_graph.vertices[current_location].item_present:
            item = game_graph.vertices[current_location].item_present
            if item not in player_items: # Só adiciona se o jogador ainda não tiver o item
                player_items.append(item)
                print(f"\n*** Você encontrou: {item}! Ele foi adicionado ao seu inventário. ***")
                game_graph.vertices[current_location].item_present = None # Remove o item do local
        
        # Verifica se o jogador já coletou o "Tesouro" para encerrar o jogo
        if "Tesouro" in player_items:
            print("\n*** PARABÉNS! Você encontrou o TESOURO ANTIGO! ***")
            print("Sua aventura termina aqui. Obrigado por jogar!")
            break
            
        # Mostra os itens que o jogador possui
        print("\nSeus itens:", ", ".join(player_items) if player_items else "Nenhum")

        print("\nPara onde você quer ir?")
        
        options = {} # Dicionário para mapear as escolhas do jogador (números) para as arestas
        available_edges = [] # Lista das arestas que o jogador pode realmente usar

        # Percorre todas as arestas adjacentes ao local atual
        for edge in game_graph.vertices[current_location].adjacents:
            # Verifica se a aresta exige um item e se o jogador tem esse item
            if edge.item_required and edge.item_required not in player_items:
                # Se o item necessário não estiver no inventário, informa que o caminho está bloqueado
                print(f" (BLOQUEADO) '{edge.weight}' para '{edge.target}': Você precisa de '{edge.item_required}' para passar!")
            else:
                # Se o caminho estiver liberado, adiciona à lista de opções disponíveis
                available_edges.append(edge)
        
        # Numera e exibe as opções de caminhos disponíveis para o jogador
        for i, edge in enumerate(available_edges):
            option_number = i + 1
            options[str(option_number)] = edge # Armazena a aresta completa para a escolha
            print(f"{option_number}. Seguir '{edge.weight}' para '{edge.target}'")
        
        print("0. Sair do jogo") # Opção para sair do jogo

        choice = input("Escolha uma opção: ") # Pede a entrada do jogador

        if choice == "0":
            print("Saindo do jogo. Até a próxima!")
            break
        elif choice in options:
            chosen_edge = options[choice]
            # Confirma a movimentação para o novo local
            current_location = chosen_edge.target
        else:
            print("Opção inválida. Por favor, escolha um número válido.")

# Esta linha garante que run_game() só será chamada quando o script for executado diretamente.
if __name__ == "__main__":
    run_game()
