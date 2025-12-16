from collections import defaultdict
from pprint import pprint

def build_graph():
    edges = [
        ["Roosevelt", "Balintawak"],        ## START OF LRT-1
        ["Balintawak", "Monumento"],
        ["Monumento", "5th Avenue"],
        ["5th Avenue", "R. Papa"],
        ["R. Papa", "Abad Santos"],
        ["Abad Santos", "Blumentritt"],
        ["Blumentritt", "Tayuman"],
        ["Tayuman", "Bambang"],
        ["Bambang", "Doroteo Jose"],
        ["Doroteo Jose", "Carriedo"],
        ["Carriedo", "Central Terminal"],
        ["Central Terminal", "United Nations"],
        ["United Nations", "Pedro Gil"],
        ["Pedro Gil", "Quirino"],
        ["Quirino", "Vito Cruz"],
        ["Vito Cruz", "Gil Puyat"],
        ["Gil Puyat", "Libertad"],
        ["Libertad", "EDSA"],
        ["EDSA", "Baclaran"],
        ["Antipolo", "Marikina"],          ## START OF LRT-2
        ["Marikina", "Santolan"],
        ["Santolan", "Katipunan"],
        ["Katipunan", "Anonas"],
        ["Anonas", "LRT Araneta-Center Cubao"],
        ["LRT Araneta-Center Cubao", "Betty-Go Belmonte"],
        ["Betty-Go Belmonte", "Gilmore"],
        ["Gilmore", "J. Ruiz"],
        ["J. Ruiz", "V. Mapa"],
        ["V. Mapa", "Pureza"],
        ["Pureza", "Legarda"],
        ["Legarda", "Recto"],
        ["North Avenue", "Quezon Avenue"],     ## START OF MRT-3
        ["Quezon Avenue", "GMA Kamuning"],
        ["GMA Kamuning", "MRT Araneta-Cubao"],
        ["MRT Araneta-Cubao", "Santolan-Anapolis"],
        ["Santolan-Anapolis", "Ortigas Avenue"],
        ["Ortigas Avenue", "Shaw Boulevard"],
        ["Shaw Boulevard", "Boni"],
        ["Boni", "Guadalupa"],
        ["Guadalupa", "Buendia"],
        ["Buendia", "Ayala"],
        ["Ayala", "Magallanes"],
        ["Magallanes", "Taft Avenue"],
        ["Doroteo Jose", "Recto"],                         ## LRT-1 TO LRT-2
        ["EDSA", "Taft Avenue"],                           ## LRT-1 TO MRT-3
        ["LRT Araneta-Center Cubao", "MRT Araneta-Cubao"]  ## LRT-2 TO MRT-3
    ]
    graph = defaultdict(list)

    for edge in edges: ## LIST EVERY CONNETION
        a, b = edge[0], edge[1]
        graph[a].append(b)
        graph[b].append(a)
    return graph

def bfs_sp(graph, start, goal):
    explored = []

    queue = [[start]]

    if start == goal:
        print("Its the Same Station")
        return
    
    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            neighbours = graph[node]

            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour == goal:
                    print("The Shortest Route you can take is: ", *new_path, sep=" -> ")
                    return
            explored.append(node)

    print("So Sorry but the Stations you have selected dont have a connecting path")
    return

if __name__ == "__main__":

    graph = build_graph()
    
    bfs_sp(graph, "Roosevelt", "Bambang")
    print()
    bfs_sp(graph, "Anonas", "United Nations")
    print()
    bfs_sp(graph, "Balintawak", "Santolan-Anapolis")
