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
        ["Baclaran", "Redemptorist-Aseana"],
        ["Redemptorist-Aseana", "MIA Road"],
        ["MIA Road", "PITX"],
        ["PITX", "Ninoy Acquino Ave."],
        ["Ninoy Acquino Ave.", "Dr. Santos"],
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
    if start == goal:
        return [start]

    explored = set()
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            for neighbour in graph[node]:
                new_path = path + [neighbour]

                if neighbour == goal:
                    return new_path  

                queue.append(new_path)

            explored.add(node)

    return None

if __name__ == "__main__":

    graph = build_graph()
    
    bfs_sp(graph, "Roosevelt", "Bambang")
    print()
    bfs_sp(graph, "Anonas", "United Nations")
    print()
    bfs_sp(graph, "Balintawak", "Santolan-Anapolis")
