# fixtures.py
from state import teams, adj


def generar_partidos_unicos():
    """
    Genera los 144 partidos (local, visitante) a partir del grafo adj.

    Usa un recorrido de Euler en cada componente del grafo para orientar
    las aristas de forma que cada equipo tenga el mismo número de partidos
    en casa y fuera (4/4 porque el grado es 8).
    """
    n = len(teams)

    # Construimos lista de aristas (cada arista solo una vez, i < j)
    edges = []  # cada elemento: {"u": i, "v": j, "local": None, "visitante": None}
    graph = [[] for _ in range(n)]  # graph[v] = lista de ids de arista incidentes

    for i in range(n):
        for j in adj[i]:
            if i < j:
                eid = len(edges)
                edges.append({"u": i, "v": j, "local": None, "visitante": None})
                graph[i].append(eid)
                graph[j].append(eid)

    used = [False] * len(edges)

    # Recorremos cada componente que tenga aristas
    for start in range(n):
        if not graph[start]:
            continue  # sin aristas

        stack = [start]

        while stack:
            v = stack[-1]

            # Saltar aristas ya usadas en la lista de v
            while graph[v] and used[graph[v][-1]]:
                graph[v].pop()

            if not graph[v]:
                # No quedan aristas desde v, retrocedemos
                stack.pop()
                continue

            eid = graph[v].pop()
            if used[eid]:
                continue

            used[eid] = True
            u = edges[eid]["u"]
            w = edges[eid]["v"]
            other = w if v == u else u

            # Orientamos la arista en la dirección v -> other
            edges[eid]["local"] = v
            edges[eid]["visitante"] = other

            stack.append(other)

    # Convertimos a lista (local_name, visitante_name)
    partidos = []
    for e in edges:
        local_name = teams[e["local"]].name
        visitante_name = teams[e["visitante"]].name
        partidos.append((local_name, visitante_name))

    return partidos


def print_fixtures(lista):
    print("\n==============================")
    print("     PARTIDOS (LOCAL/VISITANTE)")
    print("==============================\n")

    for local, visitante in lista:
        print(f"{local:22s} (LOCAL)  vs  {visitante}")
