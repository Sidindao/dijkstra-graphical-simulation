import heapq
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.animation import FuncAnimation

# Initialisation des variables ar
graph = {
    'A': {'B': 5, 'C': 2,'D':6},
    'B': { 'C': 2, 'E': 5},
    'C': { 'D': 3, 'E': 9, 'F':6},
    'D': { 'F': 1},
    'E': {'G':2},
    'F': {'E': 1,'G':6},
    'G':{}
}

# Positions des nœuds pour la figure fixe
fixed_pos = {
    'A': (0, 0),
    'B': (2, 2),  # Ajuster la position de B pour former un triangle équilatéral avec A et D
    'C': (2, 0),   # Hauteur de ABC
    'D': (2, -2),   # Ajuster la position de D pour former un triangle équilatéral avec A et B
    'E': (3, 1.5), # Ajuster la position de E pour former un triangle parallèle à BCD
    'F': (3, -1.5),  # Ajuster la position de F pour former un triangle parallèle à BCD
    'G': (4, 0)   # Ajuster la position de G pour former un triangle isoéles en G
}

# Création du graphique NetworkX
G = nx.DiGraph()
for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)
pos = fixed_pos  # Utilisation des positions fixes

def show_initial_graph():
    global ax, text, steps,step_index
    step_index = -1
    ax.clear()
    ax.set_title("Graphe de départ", fontsize=18)
    ax.set_aspect('auto')

    # Dessiner le graphe initial avec les poids des arêtes
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=18, ax=ax)
    for u, v, weight in G.edges(data=True):
        label = weight['weight']
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label}, ax=ax, font_size=14)  

    text.set("Graphe de départ affiché. Cliquez sur 'Suivant' pour démarrer la simulation de l'algorithme de Dijkstra.")


# Initialisation de l'itérateur pour l'algorithme de Dijkstra
def dijkstra_iter(graph, start):
    distances = {node: float('inf') for node in graph}
    print(distances)
    distances[start] = 0
    queue = [(0, start)]
    visited = set()
    steps = []

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        step = {'distances': distances.copy(), 'current_node': current_node, 'visited': visited.copy()}
        steps.append(step)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

                step = {'distances': distances.copy(), 'current_node': current_node, 'visited': visited.copy()}
                steps.append(step)

    return steps

# Fonction pour afficher une étape
# Fonction pour afficher une étape
def show_step(step_index):
    global ax, text, steps
    step = steps[step_index]
    distances = step['distances']
    current_node = step['current_node']
    visited = step['visited']

    ax.clear()
    ax.set_title("Simulation de l'algorithme de Dijkstra", fontsize=18)
    ax.set_xlabel("Cliquez sur 'Suivant' ou 'Précédent' pour continuer...", fontsize=14)
    ax.set_aspect('auto')

    # Dessiner le graphe avec les distances actuelles
    nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=1000, font_size=18, ax=ax)
    for node in G.nodes():
        if node in visited:
            nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='yellow', node_size=1000, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=[], width=2, arrows=True, ax=ax)
    for u, v, weight in G.edges(data=True):
        label = weight['weight']
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): label}, ax=ax, font_size=14)  # Augmenter la taille de la police des étiquettes d'arête

    # Ajouter les étiquettes de texte pour afficher les noms des nœuds et leurs distances actuelles
    labels = {node: f"{node} ({dist})" for node, dist in distances.items()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_color='black', ax=ax)  # Augmenter la taille de la police des étiquettes de nœud
    
    start_node = node_combobox.get()
    text.set(f"Étape {step_index + 1}/{len(steps)}:\n"
             f"Distances les plus courtes depuis le nœud de départ {start_node} :\n" +
             "\n".join([f"Distance jusqu'au nœud {node}: {dist}" for node, dist in distances.items()]))

# Fonction pour afficher l'étape suivante
def next_step(event):
    global step_index,steps
    if(step_index<=-1):
        start_node = node_combobox.get()
        steps = dijkstra_iter(graph, start_node)
        step_index=0
        show_step(0)
        return
    if step_index < len(steps) - 1:
        step_index += 1
        show_step(step_index)
        canvas.draw_idle()

# Fonction pour afficher l'étape précédente
def prev_step(event):
    global step_index
    if(step_index<=0):
        step_index=-1
        show_initial_graph()
    if step_index > 0:
        step_index -= 1
        show_step(step_index)
        canvas.draw_idle()

# Fonction pour lancer la simulation automatique avec un intervalle de temps
def start_auto_simulation():
    global auto_simulation_running
    auto_simulation_running = True
    auto_simulate_step()

# Fonction pour arrêter la simulation automatique
def stop_auto_simulation():
    global auto_simulation_running
    auto_simulation_running = False
    
# Fonction pour simuler automatiquement les étapes avec un intervalle de temps
def auto_simulate_step():
    global step_index,steps
    if(step_index==-1):
        start_node = node_combobox.get()
        steps = dijkstra_iter(graph, start_node)
    if auto_simulation_running and step_index < len(steps) - 1:
        step_index += 1
        show_step(step_index)
        canvas.draw_idle()
        # Définir l'intervalle de temps pour la simulation automatique (en millisecondes)
        root.after(1000, auto_simulate_step)


# Création de la fenêtre Tkinter
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

taille=str(screen_width)+"x"+str(screen_height)
root.geometry(taille)
print(screen_width)
root.title("Simulation de l'algorithme de Dijkstra")

# Création du graphique Matplotlib
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=1)

# Création du texte pour afficher les distances
text = StringVar()
text.set("Cliquez sur 'Suivant' pour démarrer la simulation")
label = Label(root, textvariable=text)
label.pack(side=BOTTOM)

# Liaison des événements de clic des boutons à leurs fonctions respectives
prev_button = Button(root, text="Précédent")
prev_button.pack(side=LEFT)
prev_button.bind("<Button-1>", prev_step)

next_button = Button(root, text="Suivant")
next_button.pack(side=RIGHT)
next_button.bind("<Button-1>", next_step)


# Création du bouton pour lancer la simulation automatique
auto_button = Button(root, text="Lancer la simulation automatique", command=start_auto_simulation)
auto_button.pack(side=LEFT)

# Création du bouton pour arrêter la simulation automatique
stop_auto_button = Button(root, text="Arrêter la simulation automatique", command=stop_auto_simulation)
stop_auto_button.pack(side=LEFT)

# Création de la combobox pour sélectionner le nœud de départ
node_combobox = ttk.Combobox(root, values=list(graph.keys()))
node_combobox.pack(side=TOP)
node_combobox.set("A")  # Sélectionner le premier nœud par défaut

# Création du bouton pour démarrer l'algorithme avec le nœud sélectionné
start_button = Button(root, text="Démarrer Dijkstra", command=show_initial_graph)
start_button.pack(side=TOP)


# Calcul des étapes de l'algorithme de Dijkstra
#steps = dijkstra_iter(graph, 'A')
step_index = -1
steps=None
show_initial_graph()
#show_step(step_index)

root.mainloop(n=0)
