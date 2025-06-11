class Edge:
    def __init__(self, target, weight):
        self.target = target
        self.weight = weight


class Vertex:
    def __init__(self, name, description, boss=None):
        self.name = name
        self.description = description
        self.adjacents = [None] * 10  # até 10 conexões
        self.adj_count = 0
        self.items = [None] * 5       # até 5 itens no local
        self.item_count = 0
        self.boss = boss

    def addEdge(self, target, weight):
        if self.adj_count < 10:
            self.adjacents[self.adj_count] = Edge(target, weight)
            self.adj_count += 1

    def addItem(self, item):
        if self.item_count < 5:
            self.items[self.item_count] = item
            self.item_count += 1

    def removeItem(self, index):
        if 0 <= index < self.item_count:
            for i in range(index, self.item_count - 1):
                self.items[i] = self.items[i + 1]
            self.items[self.item_count - 1] = None
            self.item_count -= 1


class Graph:
    def __init__(self):
        self.vertices = [None] * 10  # até 10 locais
        self.vertex_count = 0

    def addVertex(self, name, description, boss=None):
        if self.vertex_count < 10:
            if self.getVertex(name) is None:
                self.vertices[self.vertex_count] = Vertex(name, description, boss)
                self.vertex_count += 1

    def addEdge(self, source, target, weight):
        src = self.getVertex(source)
        tgt = self.getVertex(target)
        if src and tgt:
            src.addEdge(target, weight)

    def getVertex(self, name):
        for i in range(self.vertex_count):
            if self.vertices[i].name == name:
                return self.vertices[i]
        return None
class Game:
    def __init__(self):
        self.graph = Graph()
        self.inventory = [None] * 10
        self.inv_count = 0
        self.current = None

    def setup(self):
        self.graph.addVertex("Vila", "Você está na vila central com casas de pedra.")
        self.graph.addVertex("Floresta", "Uma floresta escura cheia de ruídos...", boss="Lobisomem")
        self.graph.addVertex("Caverna", "Uma caverna fria e úmida.", boss="Troll")
        self.graph.addVertex("Castelo", "Um castelo abandonado e assombrado.", boss="Cavaleiro Negro")

        self.graph.addEdge("Vila", "Floresta", 1)
        self.graph.addEdge("Vila", "Caverna", 1)
        self.graph.addEdge("Floresta", "Castelo", 1)
        self.graph.addEdge("Caverna", "Castelo", 1)
        self.graph.addEdge("Castelo", "Vila", 1)

        self.graph.getVertex("Floresta").addItem("Espada")
        self.graph.getVertex("Caverna").addItem("Poção")
        self.graph.getVertex("Castelo").addItem("Chave")

        self.current = self.graph.getVertex("Vila")

    def run(self):
        while True:
            print(f"\n📍 Local: {self.current.name}")
            print(self.current.description)

            # Combate com boss
            if self.current.boss:
                print(f"⚔️ Um inimigo aparece: {self.current.boss}")
                if self.hasItem("Espada"):
                    print("✅ Você derrotou o boss com sua espada!")
                    self.current.boss = None
                
                else:
                   print("❌ Você precisa de uma espada. Escolha outro caminho ou pegue um item.")


            # Mostrar itens
            print("🎁 Itens disponíveis:")
            for i in range(self.current.item_count):
                print(f"{i+1}. {self.current.items[i]}")

            # Mostrar caminhos
            print("\n🧭 Caminhos disponíveis:")
            for i in range(self.current.adj_count):
                print(f"{i+1}. {self.current.adjacents[i].target}")

            print("\n1. Mover")
            print("2. Coletar item")
            print("3. Ver inventário")
            print("4. Sair")

            op = input("Escolha uma opção: ")

            if op == "1":
                destino = int(input("Digite o número do destino: ")) - 1
                if 0 <= destino < self.current.adj_count:
                    nome_destino = self.current.adjacents[destino].target
                    self.current = self.graph.getVertex(nome_destino)
                else:
                    print("❌ Caminho inválido.")
            elif op == "2":
                if self.current.item_count > 0:
                    item = self.current.items[0]
                    if self.inv_count < 10:
                        self.inventory[self.inv_count] = item
                        self.inv_count += 1
                        self.current.removeItem(0)
                        print(f"✅ Você coletou: {item}")
                    else:
                        print("❌ Inventário cheio!")
                else:
                    print("❌ Nenhum item aqui.")
            elif op == "3":
                print("🎒 Inventário:")
                if self.inv_count == 0:
                    print("- vazio -")
                for i in range(self.inv_count):
                    print(f"- {self.inventory[i]}")
            elif op == "4":
                print("👋 Você saiu do jogo.")
                break
            else:
                print("❌ Opção inválida.")

    def hasItem(self, name):
        for i in range(self.inv_count):
            if self.inventory[i] == name:
                return True
        return False
jogo = Game()
jogo.setup()
jogo.run()
