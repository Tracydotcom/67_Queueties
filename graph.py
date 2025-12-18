import math
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
STATION_DATA = {
    # --- LRT 1 (Green Line) ---
    "Baclaran": ("LRT1", 0.0), 
    "EDSA": ("LRT1", 0.6), 
    "Libertad": ("LRT1", 1.6),
    "Gil Puyat": ("LRT1", 2.3), 
    "Vito Cruz": ("LRT1", 3.4), 
    "Quirino": ("LRT1", 4.2),
    "Pedro Gil": ("LRT1", 5.0), 
    "United Nations": ("LRT1", 5.9), 
    "Central Terminal": ("LRT1", 7.1),
    "Carriedo": ("LRT1", 7.8), 
    "Doroteo Jose": ("LRT1", 8.5), 
    "Bambang": ("LRT1", 9.1),
    "Tayuman": ("LRT1", 9.7), 
    "Blumentritt": ("LRT1", 10.3), 
    "Abad Santos": ("LRT1", 11.2),
    "R. Papa": ("LRT1", 11.8), 
    "5th Avenue": ("LRT1", 12.7), 
    "Monumento": ("LRT1", 13.8),
    "Balintawak": ("LRT1", 16.0), 
    "Roosevelt": ("LRT1", 18.2),
    
    # NEW EXTENSION STATIONS (Approximate distances from Baclaran)
    # Note: These use negative numbers or we extend the base. 
    # For simplicity, we just extend distance relative to Baclaran (0.0).
    # Since Baclaran is 0.0, we treat these as "South" extension.
    # To keep math simple (abs(dist1 - dist2)), we can assign them negative distance
    # OR shift Baclaran. But the easiest way for your current logic is:
    "Redemptorist-Aseana": ("LRT1", -1.0),
    "MIA Road": ("LRT1", -2.2),
    "PITX": ("LRT1", -3.6),
    "Ninoy Acquino Ave.": ("LRT1", -5.0),
    "Dr. Santos": ("LRT1", -7.0),

    # --- LRT 2 (Blue Line) ---
    "Recto": ("LRT2", 0.0), 
    "Legarda": ("LRT2", 1.1), 
    "Pureza": ("LRT2", 2.4),
    "V. Mapa": ("LRT2", 3.7), 
    "J. Ruiz": ("LRT2", 4.8), 
    "Gilmore": ("LRT2", 5.8),
    "Betty-Go Belmonte": ("LRT2", 6.9), 
    "LRT Araneta-Center Cubao": ("LRT2", 8.0),
    "Anonas": ("LRT2", 9.4), 
    "Katipunan": ("LRT2", 10.3), 
    "Santolan": ("LRT2", 12.2),
    "Marikina": ("LRT2", 14.8), 
    "Antipolo": ("LRT2", 16.8),

    # --- MRT 3 (Yellow Line) ---
    "North Avenue": ("MRT3", 0.0), 
    "Quezon Avenue": ("MRT3", 1.2), 
    "GMA Kamuning": ("MRT3", 2.2),
    "MRT Araneta-Cubao": ("MRT3", 4.0), 
    "Santolan-Anapolis": ("MRT3", 5.5), 
    "Ortigas Avenue": ("MRT3", 7.8),
    "Shaw Boulevard": ("MRT3", 8.6), 
    "Boni": ("MRT3", 9.6), 
    "Guadalupa": ("MRT3", 10.4),
    "Buendia": ("MRT3", 12.3), 
    "Ayala": ("MRT3", 13.5), 
    "Magallanes": ("MRT3", 14.7),
    "Taft Avenue": ("MRT3", 16.9)
}
def calculate_fare(path, passenger_type):
    if not path:
        return 0

    total_fare = 0
    
    # Track the start of the current train ride
    segment_start_station = path[0]
    segment_line = STATION_DATA[path[0]][0] # e.g., 'LRT1'

    # Iterate through the path to find transfers
    for i in range(1, len(path)):
        current_station = path[i]
        current_line = STATION_DATA[current_station][0]

        # If the line changes, the previous segment is finished
        if current_line != segment_line:
            # Calculate fare for the finished segment (e.g., Start -> Transfer Point)
            segment_end_station = path[i-1]
            
            # Only calculate if we actually moved (avoids calculating fare for the walk between lines)
            if segment_start_station != segment_end_station:
                total_fare += compute_segment_cost(segment_start_station, segment_end_station, passenger_type)
            
            # Reset for the new line
            segment_start_station = current_station
            segment_line = current_line

    # Calculate the final segment (from last transfer point to destination)
    if segment_start_station != path[-1]:
        total_fare += compute_segment_cost(segment_start_station, path[-1], passenger_type)

    return total_fare

def compute_segment_cost(start, end, passenger_type):
    # 1. Get Distance
    dist1 = STATION_DATA[start][1]
    dist2 = STATION_DATA[end][1]
    km_travelled = abs(dist1 - dist2)

    # 2. Base Rates (Approximation of Metro Manila Fares)
    base_fare = 13.00
    per_km = 1.00

    if passenger_type == "Beep":
        base_fare = 11.00 # Beep is often slightly cheaper on base
    
    fare = base_fare + (km_travelled * per_km)

    # 3. Apply Discounts
    # Senior, PWD, Student usually get 20% discount
    if passenger_type in ["Student", "Senior", "PWD"]:
        fare = fare * 0.80

    # 4. Rounding (Standard tickets round to nearest integer)
    return math.ceil(fare)

# ==========================================
# 3. MAIN EXECUTION
# ==========================================

if __name__ == "__main__":
    graph = build_graph()
    
    # Define test cases
    trips = [
        ("Roosevelt", "Bambang", "Student"),
        ("Anonas", "United Nations", "Regular"), # Regular = Single Journey Ticket
        ("Balintawak", "Santolan-Anapolis", "PWD"),
        ("North Avenue", "Taft Avenue", "Beep")
    ]

    print(f"{'START':<25} {'DESTINATION':<25} {'TYPE':<10} {'FARE':<5} {'ROUTE'}")
    print("-" * 110)

    for start, end, p_type in trips:
        path = bfs_sp(graph, start, end)
        if path:
            cost = calculate_fare(path, p_type)
            route_str = " -> ".join(path)
            print(f"{start:<25} {end:<25} {p_type:<10} ₱{cost:<5} {route_str}")
        else:
            print(f"No path found between {start} and {end}")