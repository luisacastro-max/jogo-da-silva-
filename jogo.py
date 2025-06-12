class Edge:
    # A classe Edge (Aresta) representa uma conexão de um sentido entre dois locais no jogo.
    # Ela armazena o local de destino, o "nome" do caminho e um possível item necessário para atravessar.
    def __init__(self, target, weight, item_required=None):
        # 'target' é o nome do vértice (local) para onde esta aresta aponta.
        self.target = target
        # 'weight' é o rótulo ou descrição do caminho (ex: "Trilha Leste", "Caminho Secreto").
        self.weight = weight
        # 'item_required' é o nome do item que o jogador precisa ter no inventário para usar este caminho.
        # Se for None, nenhum item é necessário.
        self.item_required = item_required 
        

class Vertex:
    # A classe Vertex (Vértice) representa um local ou ponto de interesse no mapa do jogo.
    # Ela contém informações sobre o local, suas conexões com outros locais e o que pode ser encontrado lá.
    def __init__(self, name, description="", item_present=None, special_message=None):
        # 'name' é o identificador único do local (ex: "Entrada da Floresta", "Templo Antigo").
        self.name = name
        # 'description' é uma breve narrativa que descreve o local ao jogador.
        self.description = description
        # 'adjacents' é uma lista de objetos Edge, representando todos os caminhos que saem deste local.
        self.adjacents = []
        # 'item_present' é o nome de um item que pode ser encontrado e coletado neste local.
        # Se for None, não há item aqui.
        self.item_present = item_present 
        # 'special_message' é uma mensagem adicional que aparece apenas ao entrar neste local,
        # usada para eventos ou encontros específicos (como um "boss").
        self.special_message = special_message 
        
    # O método addEdge adiciona uma nova conexão (aresta) que parte deste vértice.
    def addEdge(self, target, weight, item_required=None):
        self.adjacents.append(Edge(target, weight, item_required))
        

class Graph:
    # A classe Graph (Grafo) é a estrutura principal que gerencia todos os locais (vértices)
    # e suas conexões (arestas), formando o mapa completo do jogo.
    def __init__(self):
        # 'vertices' é um dicionário que armazena todos os objetos Vertex do grafo.
        # A chave do dicionário é o nome do vértice, e o valor é o objeto Vertex correspondente.
        self.vertices = {}
        
    # O método addVertex adiciona um novo local (vértice) ao grafo.
    # Ele garante que um local com o mesmo nome não seja adicionado duas vezes.
    def addVertex(self, name, description="", item_present=None, special_message=None):
        if name not in self.vertices:
            self.vertices[name] = Vertex(name, description, item_present, special_message)
            
    # O método addEdge adiciona uma nova conexão (aresta) entre dois locais no grafo.
    # Ele verifica se os locais de origem e destino já existem, criando-os se necessário.
    def addEdge(self, source, target, weight, item_required=None):
        # Primeiro, garante que o vértice de origem exista no grafo.
        if source not in self.vertices:
            self.addVertex(source)
        # Segundo, garante que o vértice de destino exista no grafo.
        if target not in self.vertices:
            self.addVertex(target)
        # Adiciona a aresta ao vértice de origem.
        self.vertices[source].addEdge(target, weight, item_required) 
    
    # O método findPath realiza uma busca em profundidade (DFS) para encontrar um caminho
    # entre um vértice de origem e um vértice de destino.
    # É um método genérico para grafos e não é diretamente usado na lógica de movimentação do jogo.
    def findPath(self, graph, source, target, visited=None, path=None):
        # Inicializa o conjunto de vértices visitados e a lista do caminho atual para a primeira chamada.
        if visited is None:
            visited = set()
        if path is None:
            path = []

        # Se o vértice de origem já foi visitado nesta busca, significa que há um ciclo
        # ou já exploramos este caminho, então retorna para evitar loops infinitos.
        if source in visited:
            return
        
        # Marca o vértice atual como visitado e o adiciona ao caminho.
        visited.add(source)
        path.append(source)
        
        # Se o vértice atual é o alvo, encontramos um caminho; retorna uma cópia deste caminho.
        if source == target:
            return path.copy()
            
        # Explora recursivamente cada vértice adjacente (vizinho).
        for edge in self.vertices[source].adjacents:
            result = self.findPath(graph, edge.target, target, visited, path)
            # Se um caminho for encontrado a partir de um vizinho, propaga o resultado.
            if result:
                return result
        
        # Se nenhum caminho for encontrado a partir do vértice atual (todos os vizinhos foram explorados
        # sem sucesso), remove-o do caminho para "retroceder" na busca.
        path.pop()

---
## Lógica Principal do Jogo

### `run_game()`: Gerencia o Fluxo e a Interação do Jogo

A função `run_game` orquestra toda a experiência do jogo. Ela cria o mapa, gerencia a posição do jogador, os itens coletados e a interação com o menu.

```python
def run_game():
    # Cria uma nova instância do grafo que será o mapa do nosso jogo.
    game_graph = Graph()

    # Define os diferentes locais do jogo (vértices do grafo).
    # Cada local tem um nome, uma descrição que o jogador lerá, e pode conter um item específico
    # ou uma mensagem especial que é exibida ao entrar no local.
    game_graph.addVertex("Entrada da Floresta", "Você está na entrada de uma floresta densa. O cheiro de terra molhada paira no ar.")
    game_graph.addVertex("Clareira Secreta", "Uma clareira iluminada pelo sol, com flores raras e um riacho murmurante.")
    game_graph.addVertex("Caverna Sombria", "A entrada de uma caverna escura e úmida. Sons estranhos ecoam lá de dentro.", item_present="Amuleto Antigo") 
    game_graph.addVertex("Montanha Nebulosa", "Um pico rochoso coberto por uma névoa espessa. A vista é limitada, mas o ar é gélido.", item_present="Chave Antiga", special_message="Você sente uma presença maligna... Um Guardião da Montanha bloqueia o caminho para o leste!") 
    game_graph.addVertex("Templo Antigo", "As ruínas de um templo esquecido, com símbolos gravados nas pedras. Parece haver algo brilhando lá dentro...", item_present="Tesouro")
    game_graph.addVertex("Lago Calmo", "Um lago de águas cristalinas, refletindo o céu. Pequenos peixes nadam tranquilamente.")

    # Estabelece as conexões (arestas) entre os locais do jogo.
    # Para cada aresta, definimos a origem, o destino, o "nome" do caminho
    # e, opcionalmente, um item que o jogador precisa ter para atravessar por ali.
    game_graph.addEdge("Entrada da Floresta", "Clareira Secreta", "Trilha Leste")
    game_graph.addEdge("Clareira Secreta", "Entrada da Floresta", "Trilha Oeste") 
    game_graph.addEdge("Entrada da Floresta", "Caverna Sombria", "Caminho Rochoso")
    game_graph.addEdge("Caverna Sombria", "Entrada da Floresta", "Voltar")
    game_graph.addEdge("Clareira Secreta", "Lago Calmo", "Atravessar Rio")
    game_graph.addEdge("Lago Calmo", "Clareira Secreta", "Voltar")
    
    game_graph.addEdge("Caverna Sombria", "Montanha Nebulosa", "Passagem Estreita")
    game_graph.addEdge("Montanha Nebulosa", "Caverna Sombria", "Descer")
    
    # Este caminho é protegido por um "Guardião" (boss) e só pode ser acessado
    # se o jogador possuir o "Amuleto Antigo".
    game_graph.addEdge("Montanha Nebulosa", "Templo Antigo", "Caminho Secreto", item_required="Amuleto Antigo") 
    game_graph.addEdge("Templo Antigo", "Montanha Nebulosa", "Voltar") 
    
    # Este é um caminho alternativo para o Templo Antigo, que exige a "Chave Antiga".
    game_graph.addEdge("Lago Calmo", "Templo Antigo", "Ponte Quebrada", item_required="Chave Antiga") 
    game_graph.addEdge("Templo Antigo", "Lago Calmo", "Voltar Pela Ponte")

    # Define o local onde o jogador começa a aventura.
    current_location = "Entrada da Floresta" 
    # Inicializa uma lista vazia para armazenar os itens que o jogador coletar.
    player_items = [] 

    # Exibe as mensagens iniciais do jogo, explicando o objetivo.
    print("Bem-vindo ao Jogo de Exploração do Grafo!")
    print("Seu objetivo é encontrar o 'Tesouro' no Templo Antigo!")
    print("Para chegar lá, você precisará ser esperto e encontrar os itens certos!")

    # Inicia o loop principal do jogo. Cada iteração representa um "turno".
    # O loop continua até o jogador encontrar o tesouro ou decidir sair.
    while True:
        # Imprime uma linha separadora para melhorar a legibilidade entre os turnos.
        print("\n" + "="*40) 
        # Mostra ao jogador o nome do local atual.
        print(f"Local: {game_graph.vertices[current_location].name}")
        # Oferece uma descrição detalhada do ambiente atual.
        print(f"Descrição: {game_graph.vertices[current_location].description}")
        
        # Se o local tiver uma mensagem especial (como um evento ou a presença do boss), ela é exibida.
        if game_graph.vertices[current_location].special_message:
            print(f"\n[EVENTO]: {game_graph.vertices[current_location].special_message}")

        # Verifica se há um item para ser coletado no local atual.
        if game_graph.vertices[current_location].item_present:
            item = game_graph.vertices[current_location].item_present
            # Se o item ainda não estiver no inventário do jogador, ele é adicionado.
            if item not in player_items: 
                player_items.append(item)
                print(f"\n*** Você encontrou: {item}! Ele foi adicionado ao seu inventário. ***")
                # O item é removido do local para que não possa ser pego novamente.
                game_graph.vertices[current_location].item_present = None 
        
        # Verifica se o jogador já possui o "Tesouro". Se sim, o jogo termina.
        if "Tesouro" in player_items:
            print("\n*** PARABÉNS! Você encontrou o TESOURO ANTIGO! ***")
            print("Sua aventura termina aqui. Obrigado por jogar!")
            break
            
        # Exibe todos os itens que o jogador coletou até o momento.
        print("\nSeus itens:", ", ".join(player_items) if player_items else "Nenhum")

        # Pergunta ao jogador para onde ele deseja ir.
        print("\nPara onde você quer ir?")
        
        # 'options' armazenará um mapeamento dos números de escolha do jogador para os objetos de aresta.
        options = {} 
        # 'available_edges' listará as arestas que o jogador pode efetivamente seguir.
        available_edges = [] 

        # Itera sobre todas as arestas (caminhos) que partem do local atual.
        for edge in game_graph.vertices[current_location].adjacents:
            # Verifica se o caminho exige um item e se o jogador não o possui.
            if edge.item_required and edge.item_required not in player_items:
                # Se o caminho estiver bloqueado, informa o jogador e qual item é necessário.
                print(f" (BLOQUEADO) '{edge.weight}' para '{edge.target}': Você precisa de '{edge.item_required}' para passar!")
            else:
                # Se o caminho estiver livre, ele é adicionado às opções disponíveis.
                available_edges.append(edge)
        
        # Numera e exibe as opções de caminhos disponíveis para o jogador.
        for i, edge in enumerate(available_edges):
            option_number = i + 1
            # Associa o número da opção ao objeto Edge correspondente.
            options[str(option_number)] = edge 
            print(f"{option_number}. Seguir '{edge.weight}' para '{edge.target}'")
        
        # Adiciona a opção para o jogador sair do jogo a qualquer momento.
        print("0. Sair do jogo") 

        # Lê a escolha do jogador.
        choice = input("Escolha uma opção: ") 

        # Processa a escolha do jogador.
        if choice == "0":
            print("Saindo do jogo. Até a próxima!")
            break
        # Se a escolha for um número válido correspondente a uma opção disponível.
        elif choice in options:
            chosen_edge = options[choice]
            # Atualiza a localização do jogador para o destino do caminho escolhido.
            current_location = chosen_edge.target
        # Se a escolha não corresponder a nenhuma opção válida.
        else:
            print("Opção inválida. Por favor, escolha um número válido.")

# Esta condição garante que a função 'run_game()' seja chamada apenas quando o script é executado diretamente,
# e não quando importado como um módulo em outro arquivo.
if __name__ == "__main__":
    run_game()
