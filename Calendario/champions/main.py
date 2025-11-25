# main.py
"""Punto de entrada: ejecuta el sorteo y muestra el resultado por pantalla."""

from solver import search, calls
from state import teams, adj, deg, pot_count
from config import N_MATCHES, PER_POT, MAX_SAME_COUNTRY
from state import teams
from data import generar_bombos_aleatorios
from fixtures import generar_partidos_unicos_ida_vuelta, print_partidos_bonitos
from league_calendar import generate_league_calendar, print_calendar

from verificar_calendario import verificar_calendario


def mostrar_bombos():
    print("\n==============================")
    print("       BOMBOS GENERADOS")
    print("==============================")

    # reconstruir los bombos a partir del atributo pot
    bombos = {1: [], 2: [], 3: [], 4: []}
    for t in teams:
        bombos[t.pot].append(t.name)

    for p in range(1, 5):
        print(f"\nBOMBO {p}:")
        for eq in bombos[p]:
            print(" -", eq)


def check_constraints() -> bool:
    """Verifica que todos los equipos cumplen las restricciones."""
    ok = True
    for i, t in enumerate(teams):
        if deg[i] != N_MATCHES:
            print("❌ Grado incorrecto en", t.name, "->", deg[i])
            ok = False

        # Comprobar que tiene exactamente PER_POT rivales de cada bombo
        for p in range(1, 5):
            if pot_count[i][p] != PER_POT:
                print(f"❌ Error bombo {p} en {t.name}: {pot_count[i][p]}")
                ok = False

    return ok


def print_diagnostics():
    print("\n==============================")
    print("     DIAGNÓSTICO DETALLADO")
    print("==============================\n")

    for i, t in enumerate(teams):
        name = t.name
        pot = t.pot
        country = t.country

        rivals_idx = adj[i]
        rivals = sorted([teams[j].name for j in rivals_idx])
        rival_countries = [teams[j].country for j in rivals_idx]
        rival_pots = [teams[j].pot for j in rivals_idx]

        # Límite del mismo país (si no hay caso especial, usa default)
        country_limit = MAX_SAME_COUNTRY.get(country, MAX_SAME_COUNTRY["default"])

        # Número de rivales del mismo país
        same_country_count = sum(1 for c in rival_countries if c == country)

        # Conteo por país
        country_count_map = {}
        for c in rival_countries:
            country_count_map[c] = country_count_map.get(c, 0) + 1

        # Conteo por bombo
        pot_count_map = {}
        for p in rival_pots:
            pot_count_map[p] = pot_count_map.get(p, 0) + 1

        # Comprobaciones
        ok_same_country = same_country_count <= country_limit
        ok_by_pot = all(pot_count_map.get(p, 0) == PER_POT for p in range(1, 5))
        ok_deg = len(rivals) == N_MATCHES

        print(f"🔵 {name} ({country}, B{pot})")
        print(f"   Rivales ({len(rivals)}): {rivals}")

        print(
            f"   ➤ Rivales del mismo país: {same_country_count}/{country_limit} "
            f"{'✔' if ok_same_country else '❌'}"
        )
        print(f"   ➤ Rivales por país: {country_count_map}")
        print(f"   ➤ Rivales por bombo: {pot_count_map}")

        print(f"   ➤ {N_MATCHES} rivales obligatorios: {'✔' if ok_deg else '❌'}")
        print(f"   ➤ {PER_POT} por bombo: {'✔' if ok_by_pot else '❌'}")

        print("----------------------------------------------------")





def main():
    print("Generando sorteo determinista con bombos aleatorios...")
    mostrar_bombos()
    found = search()
    print("¿Solución encontrada?:", found, "| Llamadas recursivas:", calls)

    if not found:
        print("❌ No se encontró solución para estos bombos.")
        return

    ok = check_constraints()
    print("¿Restricciones correctas?:", ok)

    print("\nRESULTADO FINAL:\n")
    for i, t in enumerate(teams):
        rivals = sorted([teams[j].name for j in adj[i]])
        print(f"{t.name:22s} ({t.country}, B{t.pot}) -> {rivals}")
    print_diagnostics()

    # 🆕 AQUI generamos ida+vuelta
    partidos = generar_partidos_unicos_ida_vuelta()

    print_partidos_bonitos(partidos)

if __name__ == "__main__":
    main()
