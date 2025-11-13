import random
import time

NUM_RIVALES = 8
RIVALES_POR_BOMBO = 2


# ===========================================
# Verifica compatibilidad
# ===========================================
def son_compatibles(e1, e2, equipos_dict, bombos, max_mismo_pais):
    for bombo in bombos:
        if e1 in bombo and e2 in bombo:
            return False
    if equipos_dict[e1]["country"] == equipos_dict[e2]["country"]:
        return False
    return True


# ===========================================
# Genera solución inicial con 2 rivales por bombo
# ===========================================
def generar_solucion_inicial(equipos, equipos_dict, bombos, max_mismo_pais):
    solucion = {}
    for e in equipos:
        rivales = set()
        for bombo in bombos:
            posibles = [
                r
                for r in bombo
                if r != e
                and son_compatibles(e, r, equipos_dict, bombos, max_mismo_pais)
            ]
            if len(posibles) >= RIVALES_POR_BOMBO:
                seleccionados = random.sample(posibles, RIVALES_POR_BOMBO)
            else:
                seleccionados = random.sample(
                    [r for r in equipos if r != e], RIVALES_POR_BOMBO
                )
            rivales.update(seleccionados)
        solucion[e] = rivales
    return solucion


# ===========================================
# Calcula fitness
# ===========================================
def calcular_fitness(solucion, equipos_dict, bombos, max_mismo_pais):
    score = 0
    for equipo, rivales in solucion.items():
        if len(rivales) != NUM_RIVALES:
            score -= 100
        bombos_usados = set()
        for rival in rivales:
            for i, bombo in enumerate(bombos):
                if rival in bombo:
                    bombos_usados.add(i)
                    break
        score += len(bombos_usados) * 2
        paises = [equipos_dict[r]["country"] for r in rivales]
        for p in set(paises):
            count = paises.count(p)
            if count > max_mismo_pais:
                score -= (count - max_mismo_pais) * 10
        # Penaliza si no tiene 2 rivales por bombo
        for i, bombo in enumerate(bombos):
            count_bombo = len([r for r in rivales if r in bombo])
            if count_bombo != RIVALES_POR_BOMBO:
                score -= abs(RIVALES_POR_BOMBO - count_bombo) * 5
    return score


# ===========================================
# Genera vecino
# ===========================================
def generar_vecino(solucion, equipos, equipos_dict, bombos, max_mismo_pais):
    nuevo = {k: set(v) for k, v in solucion.items()}
    equipo_mutar = random.choice(equipos)
    rivales = set()
    for bombo in bombos:
        posibles = [
            r
            for r in bombo
            if r != equipo_mutar
            and son_compatibles(equipo_mutar, r, equipos_dict, bombos, max_mismo_pais)
        ]
        if len(posibles) >= RIVALES_POR_BOMBO:
            seleccionados = random.sample(posibles, RIVALES_POR_BOMBO)
        else:
            seleccionados = random.sample(
                [r for r in equipos if r != equipo_mutar], RIVALES_POR_BOMBO
            )
        rivales.update(seleccionados)
    nuevo[equipo_mutar] = rivales
    return nuevo


# ===========================================
# Metaheurística principal con progreso
# ===========================================
def generar_rivales_metaheuristica(
    equipos,
    equipos_dict,
    bombos,
    iteraciones=10000,
    max_mismo_pais=1,
    mostrar_progreso=True,
):
    print("Generando rivales...\n")
    start = time.time()
    mejor = generar_solucion_inicial(equipos, equipos_dict, bombos, max_mismo_pais)
    mejor_fitness = calcular_fitness(mejor, equipos_dict, bombos, max_mismo_pais)
    interacciones = 0

    for i in range(1, iteraciones + 1):
        interacciones += 1
        vecino = generar_vecino(mejor, equipos, equipos_dict, bombos, max_mismo_pais)
        fitness_vecino = calcular_fitness(vecino, equipos_dict, bombos, max_mismo_pais)
        if fitness_vecino > mejor_fitness:
            mejor = vecino
            mejor_fitness = fitness_vecino

        # Mostrar progreso cada 5% de iteraciones
        if mostrar_progreso and i % max(1, iteraciones // 20) == 0:
            porcentaje = (i / iteraciones) * 100
            print(f"🔄 Progreso: {porcentaje:.0f}% ({i}/{iteraciones} iteraciones)")

    end = time.time()
    print(f"\n✅ Metaheurística completada en {end - start:.2f} segundos")
    print(f"🔥 Mejor fitness final: {mejor_fitness}")
    print(f"🔹 Total de interacciones realizadas: {interacciones}\n")
    print("===== RIVALES POR EQUIPO =====\n")

    # Impresión final de rivales
    for equipo, rivales in mejor.items():
        pais_equipo = equipos_dict[equipo]["country"]
        total_rivales = len(rivales)
        # Conteo por país
        paises = {}
        for r in rivales:
            p = equipos_dict[r]["country"]
            paises[p] = paises.get(p, 0) + 1
        paises_str = ", ".join(f"{k}: {v}" for k, v in paises.items())
        # Conteo por bombo
        bombos_rivales = {}
        for i, bombo in enumerate(bombos):
            bombos_rivales[i + 1] = len([r for r in rivales if r in bombo])
        bombos_str = ", ".join(f"B{i}: {c}" for i, c in bombos_rivales.items())
        rivales_str = " • ".join(rivales)
        print(
            f"{equipo} ({pais_equipo}) | Total rivales: {total_rivales} | "
            f"[{paises_str}] | {rivales_str} | {bombos_str}"
        )
    print("\n=============================")
    return mejor
