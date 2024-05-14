import sys
from collections import deque
import heapq

class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []  # Lista prijelaza (stanje, cijena)

class HeuristicFunction:
    def __init__(self):
        self.values = {}  # Rječnik (stanje -> vrijednost)

def load_state_space(filename):
    state_space = {}
    start_state = None
    goal_states = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#'):  # Preskoči prazne linije i komentare
                continue
            if start_state is None:
                start_state = line
                continue
            if not goal_states:
                goal_states = line.split()
                continue

            parts = line.split(':')
            state_name = parts[0].strip()
            transitions = [(transition_part.split(',')[0].strip(), float(transition_part.split(',')[1])) 
                           for transition_part in parts[1].strip().split()]
            state_space[state_name] = transitions

    return state_space, start_state, goal_states

def load_heuristic_function(filename):
    heuristic_function = HeuristicFunction()
    with open(filename, 'r',encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#'):  # Preskoči komentare
                continue
            state_name, value = line.split(':')
            heuristic_function.values[state_name.strip()] = float(value.strip())
    return heuristic_function

#pomogao sam si s pseudokodovima sa predavanja i sa stranice https://favtutor.com/blogs/breadth-first-search-python
#prilagodio sam te pseudokodove da odgovara unosu i ispisu za ovaj labos
#pronašao video koji mi je poboljšao algoritam:
#https://www.youtube.com/watch?v=yN6iRgv09mc te sam ga prilagodio sebi
def breadth_first_search(state_space, start_state, goal_states):
    #prvo bilo lista, ali zbog primjera 3x3 promijenio sam u set
    visited = set()  # Skup posjećenih stanja
    queue = deque([(start_state, [])])  # Redak čvorova za obradu (stanje, put)

    # Glavna petlja BFS algoritma
    while queue:
        current_state, path = queue.popleft()# Uzmi sljedeći čvor iz reda

        # Provjera ciljnih stanja
        if current_state in goal_states:
            return {
                "FOUND_SOLUTION": "yes",
                "STATES_VISITED": len(visited),
                "PATH_LENGTH": len(path)+1,
                "TOTAL_COST": sum(cost for _, cost in path),
                "PATH": [state for state, _ in path] + [current_state]  # Početno stanje se dodaje samo jednom
            }

        # Označi trenutno stanje kao posjećeno
        visited.add(current_state)

        # Dodavanje susjednih stanja u red za obradu
        for next_state, cost in state_space.get(current_state, []):
            if next_state not in visited:
                queue.append((next_state, path + [(current_state, cost)]))
    # Ako nema rješenja
    return {"FOUND_SOLUTION": "no"}

#uzeo sam pseudkod iz predavanje te sam si pomogao s ovim youtube videom :https://www.youtube.com/watch?v=dLXhXcG45Tg
#prilagodio svojem kodu te unosu i ispisu potrebnom
def uniform_cost_search(state_space, start_state, goal_states):
    visited = set()  # Skup posjećenih stanja
    heap = [(0, start_state, [])]  # Prioritetni red (prioritet, stanje, put)

    # Glavna petlja UCS algoritma
    while heap:
        cost, current_state, path = heapq.heappop(heap)  # Uzmi sljedeći čvor iz prioritetskog reda

        # Provjera ciljnih stanja
        if current_state in goal_states:
            return {
                "FOUND_SOLUTION": "yes",
                "STATES_VISITED": len(visited),
                "PATH_LENGTH": len(path) + 1,  # +1 jer uključujemo i početno stanje
                "TOTAL_COST": cost,
                "PATH": [state for state, _ in path] + [current_state]
            }

        # Označi trenutno stanje kao posjećeno
        visited.add(current_state)

        # Dodavanje susjednih stanja u prioriterni red
        for next_state, next_cost in state_space.get(current_state, []):
            if next_state not in visited:
                heapq.heappush(heap, (cost + next_cost, next_state, path + [(current_state, next_cost)]))

    # Ako nema rješenja
    return {"FOUND_SOLUTION": "no"}


#također pseudokod iz predavanja te još jednom pomogao sam si s videom:https://www.youtube.com/watch?v=qWbqHKzVLIw
#prilagodio svojem kodu i strukturi podataka i ispisu
def a_star(state_space, start_state, goal_states, heuristic_function):
    visited = set()  # Skup posjećenih stanja
    heap = [(0 + heuristic_function.values[start_state], 0, start_state, [])]  # Prioritetni red (f-vrijednost, cijena, stanje, put)

    # Glavna petlja A* algoritma
    while heap:
        _, cost, current_state, path = heapq.heappop(heap)  # Uzmi sljedeći čvor iz prioritetskog reda

        # Provjera ciljnih stanja
        if current_state in goal_states:
            return {
                "FOUND_SOLUTION": "yes",
                "STATES_VISITED": len(visited)+1,
                "PATH_LENGTH": len(path) + 1,  # +1 jer uključujemo i početno stanje
                "TOTAL_COST": cost,
                "PATH": [state for state, _ in path] + [current_state]
            }

        # Označi trenutno stanje kao posjećeno
        visited.add(current_state)

        # Dodavanje susjednih stanja u prioriterni red
        for next_state, next_cost in state_space.get(current_state, []):
            if next_state not in visited:
                f_value = cost + next_cost + heuristic_function.values[next_state]
                heapq.heappush(heap, (f_value, cost + next_cost, next_state, path + [(current_state, next_cost)]))

    # Ako nema rješenja
    return {"FOUND_SOLUTION": "no"}
        
#zasebni ispisi za algoritme
def print_bfs_result(result):
    print(f"# BFS")
    print(f"[FOUND_SOLUTION]: {result['FOUND_SOLUTION']}")
    print(f"[STATES_VISITED]: {result['STATES_VISITED']}")
    if result['FOUND_SOLUTION'] == 'yes':
        print(f"[PATH_LENGTH]: {result['PATH_LENGTH']}")
        print(f"[TOTAL_COST]: {result['TOTAL_COST']:.1f}")
        print(f"[PATH]:", " => ".join(result['PATH']))
def print_ucs_result(result):
    print(f"# UCS")
    print(f"[FOUND_SOLUTION]: {ucs_result['FOUND_SOLUTION']}")
    print(f"[STATES_VISITED]: {ucs_result['STATES_VISITED']}")
    if ucs_result['FOUND_SOLUTION'] == 'yes':
        print(f"[PATH_LENGTH]: {ucs_result['PATH_LENGTH']}")
        print(f"[TOTAL_COST]: {ucs_result['TOTAL_COST']:.1f}")
        print(f"[PATH]:", " => ".join(ucs_result['PATH']))
    

def print_a_star_result(result,heuristic_filename):
    print(f"# A-STAR {heuristic_filename}")
    print(f"[FOUND_SOLUTION]: {a_star_result['FOUND_SOLUTION']}")
    print(f"[STATES_VISITED]: {a_star_result['STATES_VISITED']}")
    if a_star_result['FOUND_SOLUTION'] == 'yes':
        print(f"[PATH_LENGTH]: {a_star_result['PATH_LENGTH']}")
        print(f"[TOTAL_COST]: {a_star_result['TOTAL_COST']:.1f}")
        print(f"[PATH]:", " => ".join(a_star_result['PATH']))
        
def is_optimistic_heuristic(state_space, heuristic_function_filename):
    heuristic_function = load_heuristic_function(heuristic_function_filename)
    optimistic = True  # Pretpostavljamo da je heuristika optimistična

    # Sortiranje stanja po abecednom redu
    sorted_states = sorted(state_space.keys())

    print(f"# HEURISTIC-OPTIMISTIC {heuristic_function_filename}")
    for state in sorted_states:
        #dohvat heuristike za to stanje
        heuristic_value = heuristic_function.values[state]
        #računanje stvaren udaljenosti
        ucs_result = uniform_cost_search(state_space, state, goal_states)
        real_distance = ucs_result['TOTAL_COST']

        if heuristic_value > real_distance:
            print(f"[CONDITION]: [ERR] h({state}) <= h*: {heuristic_value} <= {real_distance:.1f}")
            optimistic = False
        else:
            print(f"[CONDITION]: [OK] h({state}) <= h*: {heuristic_value} <= {real_distance:.1f}")

    if optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")
        
def is_consistent_heuristic(state_space, heuristic_function_filename):
    heuristic_function = load_heuristic_function(heuristic_function_filename)
    consistent = True  # Pretpostavljamo da je heuristika konzistentna

    
    print(f"# HEURISTIC-CONSISTENT {heuristic_function_filename}")
    
    for state in sorted(state_space.keys()):
        #određivanje slijedećeg stanja i cijene prijelaza
        for next_state, cost in sorted(state_space[state], key=lambda x: x[0]):
            #dohvat heuristike za trenutno stanje i sa slijedeće
            heuristic_value = heuristic_function.values[state]
            next_heuristic_value = heuristic_function.values[next_state]
            if heuristic_value > next_heuristic_value + cost:
                print(f"[CONDITION]: [ERR] h({state}) <= h({next_state}) + c: {heuristic_value} <= {next_heuristic_value} + {cost}")
                consistent = False
            else:
                print(f"[CONDITION]: [OK] h({state}) <= h({next_state}) + c: {heuristic_value} <= {next_heuristic_value} + {cost}")

    if consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")



# Testiranje
if __name__ == "__main__":
    heuristic = ""
    algorithm = ""
    for i in range(len(sys.argv)):
        if (sys.argv[i] == "--ss" ):
            state_space_filename = sys.argv[i+1]
        elif (sys.argv[i] == "--alg" ):
              algorithm = sys.argv[i+1]
        elif (sys.argv[i] == "--h" ):
            heuristic_function_filename = sys.argv[i+1]
            heuristic_function = load_heuristic_function(heuristic_function_filename)
        elif (sys.argv[i] == "--check-optimistic" ) :
              heuristic = "optimistic"
        elif (sys.argv[i] == "--check-consistent" ):
              heuristic = "consistent"
    #čitanje podataka s ulaza
    state_space, start_state, goal_states = load_state_space(state_space_filename)

    #za optimističnu
    if(heuristic == "optimistic"):
        is_optimistic_heuristic(state_space, heuristic_function_filename)
    #za konzistentunu
    elif(heuristic == "consistent"):
        is_consistent_heuristic(state_space,heuristic_function_filename)
    #ako nije onda provjerava algoritme
    else:
            
        #provjera koji je algoritam
        if (algorithm=="bfs"):
            # Pokretanje algoritma pretraživanja u širinu
            bfs_result = breadth_first_search(state_space, start_state, goal_states)

            # Ispis rezultata
            print_bfs_result(bfs_result)

        elif (algorithm=="ucs"):
            # Pokretanje algoritma pretraživanja s jednolikom cijenom
            ucs_result = uniform_cost_search(state_space, start_state, goal_states)

            # Ispis rezultata
            print_ucs_result(ucs_result)

        elif(algorithm=="astar"):
            # Pokretanje algoritma a*
            a_star_result = a_star(state_space, start_state, goal_states, heuristic_function)

            #ispis rezultata
            print_a_star_result(a_star_result,heuristic_function_filename)
