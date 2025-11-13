import random

def fitness(rivales, equipos_dict, bombos, max_mismo_pais=2):

    score = 0
    for eq, rs in rivales.items():
        score += max(0, 8 - abs(len(rs) - 8))  # penaliza si no son 8
        pais_counts = {}
        for r in rs:
            pais = equipos_dict[r]['country']
            pais_counts[pais] = pais_counts.get(pais, 0) + 1
            if pais_counts[pais] > max_mismo_pais:  # ahora parametrizable
                score -= 1
        # Revisar rivales por bombo
        eq_bombo = next(i for i, b in enumerate(bombos) if eq in b)
        for b_idx, bombo in enumerate(bombos):
            if b_idx == eq_bombo:
                continue
            count_bombo = sum(1 for r in rs if r in bombo)
            score += min(count_bombo, 2)
    return score


def generar_rivales_metaheuristica(equipos, equipos_dict, bombos, iteraciones=100000, max_mismo_pais=2):
    """
    Esta metaheuristica genera rivales usando metaheurística asegurando 8 rivales por equipo
    y respetando un máximo de rivales del mismo país parametrizable.
    """
    rivales_deseados = 8
    mejor_rivales = None
    mejor_score = -float('inf')
    
    for _ in range(iteraciones):
        rivales = {eq: set() for eq in equipos}
        for eq in equipos:
            eq_bombo = next(i for i, b in enumerate(bombos) if eq in b)
            bombos_restantes = [b for i, b in enumerate(bombos) if i != eq_bombo]
            
            rivales_por_bombo = rivales_deseados // len(bombos_restantes)
            extra = rivales_deseados % len(bombos_restantes)
            
            for b in bombos_restantes:
                candidatos = [r for r in b if r != eq]
                n = rivales_por_bombo
                if extra > 0:
                    n += 1
                    extra -= 1
                n = min(n, len(candidatos))
                rivales[eq].update(random.sample(candidatos, n))
        
        score = fitness(rivales, equipos_dict, bombos, max_mismo_pais=max_mismo_pais)
        if score > mejor_score:
            mejor_score = score
            mejor_rivales = rivales
            print(f"Iteracion n: {_} -")
            print(f"Nuevo mejor score: {score}")
    
    return mejor_rivales
