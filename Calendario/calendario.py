#!/usr/bin/env python3
"""
generador_calendario.py

Genera un calendario tipo "fase suizo" con 8 jornadas para los equipos
proporcionados (lista adaptada según petición del usuario: temporada 2025/26).
- Cada equipo juega 8 partidos (1 por jornada, 4 casa / 4 fuera intentado).
- Evita (si es posible) enfrentamientos entre equipos del mismo país.
- Heurístico con reintentos para resolver restricciones.
"""

import random
import itertools
import csv
from collections import defaultdict, Counter
from typing import List, Tuple, Dict, Optional, Set

Round = int
Team = str
Country = str
Match = Tuple[Team, Team]  # (home, away)
MAX_RETRIES = 3000  # reintentos globales para intentar generar calendario válido

def all_allowed_pairs(teams: List[Team], country_of: Dict[Team, Country], avoid_same_country: bool = False) -> Set[frozenset]:
    pairs = set()
    for a, b in itertools.combinations(teams, 2):
        if avoid_same_country and country_of.get(a) == country_of.get(b):
            continue
        pairs.add(frozenset((a, b)))
    return pairs

def pick_round_matching(available_pairs: Set[frozenset],
                        teams_remaining_this_round: Set[Team],
                        played_pairs: Set[frozenset],
                        matches_needed_per_team: Dict[Team, int],
                        rng: random.Random) -> Optional[List[frozenset]]:
    teams = list(teams_remaining_this_round)
    rng.shuffle(teams)
    matching: List[frozenset] = []
    used = set()

    teams_sorted = sorted(teams, key=lambda t: -matches_needed_per_team[t])
    for t in teams_sorted:
        if t in used:
            continue
        candidates = []
        for u in teams_sorted:
            if u == t or u in used:
                continue
            pair = frozenset((t, u))
            if pair in available_pairs and pair not in played_pairs:
                candidates.append(u)
        if not candidates:
            continue
        opponent = rng.choice(candidates)
        pair = frozenset((t, opponent))
        matching.append(pair)
        used.add(t)
        used.add(opponent)

    if len(used) != len(teams_remaining_this_round):
        return None
    return matching

def assign_home_away_for_round(matching: List[frozenset],
                               home_counts: Dict[Team, int],
                               target_home: int,
                               rng: random.Random) -> List[Tuple[Team, Team]]:
    oriented: List[Tuple[Team, Team]] = []
    for pair in matching:
        a, b = tuple(pair)
        if home_counts[a] < home_counts[b]:
            oriented.append((a, b))
            home_counts[a] += 1
        elif home_counts[b] < home_counts[a]:
            oriented.append((b, a))
            home_counts[b] += 1
        else:
            if home_counts[a] >= target_home and home_counts[b] < target_home:
                oriented.append((b, a))
                home_counts[b] += 1
            elif home_counts[b] >= target_home and home_counts[a] < target_home:
                oriented.append((a, b))
                home_counts[a] += 1
            else:
                if rng.random() < 0.5:
                    oriented.append((a, b))
                    home_counts[a] += 1
                else:
                    oriented.append((b, a))
                    home_counts[b] += 1
    return oriented

def validate_schedule(schedule: Dict[Round, List[Tuple[Team, Team]]],
                      teams: List[Team],
                      country_of: Dict[Team, Country],
                      rounds_expected: int = 8) -> Tuple[bool, str]:
    n = len(teams)
    if n % 2 == 1:
        return False, "Número de equipos debe ser par."
    if len(schedule) != rounds_expected:
        return False, f"Debe haber {rounds_expected} jornadas, hay {len(schedule)}."

    played_pairs = set()
    counts = Counter()
    home_counts = Counter()
    for r, matches in schedule.items():
        teams_in_round = set()
        for h, a in matches:
            if h == a:
                return False, f"Emparejamiento inválido en jornada {r}: {h} vs {a}"
            teams_in_round.add(h)
            teams_in_round.add(a)
            counts[h] += 1
            counts[a] += 1
            home_counts[h] += 1
            pair = frozenset((h, a))
            if pair in played_pairs:
                return False, f"Par {pair} repetido."
            played_pairs.add(pair)
            if country_of.get(h) == country_of.get(a):
                return False, f"Enfrentamiento entre mismo país detectado: {h} - {a} (pais {country_of.get(h)})"
        if teams_in_round != set(teams):
            missing = set(teams) - teams_in_round
            extra = teams_in_round - set(teams)
            return False, f"En jornada {r} no todos los equipos juegan. Faltan: {missing}, extra: {extra}"
    for t in teams:
        if counts[t] != rounds_expected:
            return False, f"Equipo {t} tiene {counts[t]} partidos (debería {rounds_expected})"
        if home_counts[t] not in (rounds_expected//2, rounds_expected//2 + 1):
            return False, f"Equipo {t} tiene {home_counts[t]} partidos en casa (esperado {rounds_expected//2})."
    return True, "OK"

def generate_schedule(teams: List[Team],
                      country_of: Dict[Team, Country],
                      rounds: int = 8,
                      avoid_same_country: bool = True,
                      max_global_retries: int = MAX_RETRIES,
                      seed: Optional[int] = None) -> Dict[Round, List[Tuple[Team, Team]]]:
    if len(teams) % 2 == 1:
        raise ValueError("El número de equipos debe ser par.")
    n = len(teams)
    if n < rounds + 1:
        raise ValueError(f"Con {n} equipos no es posible que cada uno juegue {rounds} rivales distintos (se necesitan >= {rounds+1}).")

    rng = random.Random(seed)
    all_pairs = all_allowed_pairs(teams, country_of, avoid_same_country)
    required_total_pairs = n * rounds // 2
    if len(all_pairs) < required_total_pairs:
        if avoid_same_country:
            raise ValueError(f"No hay suficientes pares disponibles evitando mismo país. Pairs available: {len(all_pairs)}, pairs needed: {required_total_pairs}. Prueba desactivar avoid_same_country o añade más equipos.")
        else:
            raise ValueError("No hay suficientes pares posibles en el conjunto de equipos (revisa número de equipos).")

    for attempt in range(1, max_global_retries + 1):
        played_pairs: Set[frozenset] = set()
        matches_per_team = {t: 0 for t in teams}
        home_counts = {t: 0 for t in teams}
        schedule: Dict[int, List[Tuple[Team, Team]]] = {}
        available_pairs = set(all_pairs)

        failed = False
        for r in range(1, rounds + 1):
            teams_this_round = set(teams)
            success_round = False
            inner_retries = 0
            while not success_round and inner_retries < 800:
                inner_retries += 1
                matching_pairs = pick_round_matching(available_pairs, teams_this_round, played_pairs, {t: rounds - matches_per_team[t] for t in teams}, rng)
                if matching_pairs is None:
                    rng.shuffle(list(teams_this_round))
                    continue
                trial_home_counts = dict(home_counts)
                oriented = assign_home_away_for_round(matching_pairs, trial_home_counts, target_home=rounds//2, rng=rng)
                bad = False
                if bad:
                    continue
                schedule[r] = oriented
                for pair in matching_pairs:
                    played_pairs.add(pair)
                    if pair in available_pairs:
                        available_pairs.remove(pair)
                for h, a in oriented:
                    matches_per_team[h] += 1
                    matches_per_team[a] += 1
                home_counts = trial_home_counts
                success_round = True

            if not success_round:
                failed = True
                break

        try:
            valid, msg = validate_schedule(schedule, teams, country_of, rounds_expected=rounds)
        except Exception as e:
            valid, msg = False, f"Excepción validación: {e}"

        if valid:
            return schedule
    raise RuntimeError(f"No fue posible generar un calendario válido tras {max_global_retries} intentos. Prueba ajustar equipos, desactivar avoid_same_country, o incrementar MAX_RETRIES.")

def print_schedule(schedule: Dict[Round, List[Tuple[Team, Team]]]) -> None:
    for r in sorted(schedule.keys()):
        print(f"Jornada {r}:")
        for h, a in schedule[r]:
            print(f"  {h}  vs  {a}")
        print()

def export_schedule_csv(schedule: Dict[Round, List[Tuple[Team, Team]]], path: str) -> None:
    rows = []
    for r in sorted(schedule.keys()):
        for h, a in schedule[r]:
            rows.append({"round": r, "home": h, "away": a})
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["round", "home", "away"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Exportado CSV a {path}")

# -------------------------
# Lista de equipos (según tu mensaje) — 36 equipos
# Los equipos marcados con * son ganadores de play-offs en tu lista original.
# -------------------------
if __name__ == "__main__":
    TEAMS_EXAMPLE = [
        # Inglaterra (6)
        "Liverpool", "Arsenal", "Manchester City", "Chelsea", "Tottenham", "Newcastle",
        # España (5)
        "Barcelona", "Real Madrid", "Atlético de Madrid", "Athletic Club", "Villarreal",
        # Italia (4)
        "Napoli", "Inter", "Atalanta", "Juventus",
        # Alemania (4)
        "Bayern München", "Bayer Leverkusen", "Eintracht Frankfurt", "Borussia Dortmund",
        # Francia (3)
        "Paris Saint-Germain", "Marseille", "Monaco",
        # Países Bajos (2)
        "PSV", "Ajax",
        # Portugal (2) - Benfica* = ganador play-off en tu nota
        "Benfica", "Sporting CP",
        # Bélgica (2) - Club Brugge* = ganador play-off en tu nota
        "Club Brugge", "Union Saint-Gilloise",
        # Turquía (1)
        "Galatasaray",
        # Chequia (1)
        "Slavia Praha",
        # Grecia (1)
        "Olympiacos",
        # Dinamarca (1) - Copenhagen* (play-off)
        "Copenhagen",
        # Noruega (1) - Bodø/Glimt* (play-off)
        "Bodo/Glimt",
        # Chipre (1) - Pafos* (play-off)
        "Pafos",
        # Kazajstán (1) - Kairat Almaty* (play-off)
        "Kairat Almaty",
        # Azerbaiyán (1) - Qarabağ* (play-off)
        "Qarabag"
    ]

    COUNTRY_OF_EXAMPLE = {
        # Inglaterra
        "Liverpool": "ENG", "Arsenal": "ENG", "Manchester City": "ENG",
        "Chelsea": "ENG", "Tottenham": "ENG", "Newcastle": "ENG",

        # España
        "Barcelona": "ESP", "Real Madrid": "ESP", "Atlético de Madrid": "ESP",
        "Athletic Club": "ESP", "Villarreal": "ESP",

        # Italia
        "Napoli": "ITA", "Inter": "ITA", "Atalanta": "ITA", "Juventus": "ITA",

        # Alemania
        "Bayern München": "GER", "Bayer Leverkusen": "GER",
        "Eintracht Frankfurt": "GER", "Borussia Dortmund": "GER",

        # Francia
        "Paris Saint-Germain": "FRA", "Marseille": "FRA", "Monaco": "FRA",

        # Países Bajos
        "PSV": "NED", "Ajax": "NED",

        # Portugal
        "Benfica": "POR", "Sporting CP": "POR",

        # Bélgica
        "Club Brugge": "BEL", "Union Saint-Gilloise": "BEL",

        # Turquía
        "Galatasaray": "TUR",

        # Chequia
        "Slavia Praha": "CZE",

        # Grecia
        "Olympiacos": "GRE",

        # Dinamarca
        "Copenhagen": "DEN",

        # Noruega
        "Bodo/Glimt": "NOR",

        # Chipre
        "Pafos": "CYP",

        # Kazajstán
        "Kairat Almaty": "KAZ",

        # Azerbaiyán
        "Qarabag": "AZE"
    }

    # Generar calendario
    try:
        TEAMS_DICT = {team: {"country": COUNTRY_OF_EXAMPLE[team]} for team in TEAMS_EXAMPLE}
        schedule = generate_schedule(TEAMS_DICT, rounds=8, avoid_same_country=True, seed=12345)
        print_schedule(schedule)
        export_schedule_csv(schedule, "calendario_generado_2025_26.csv")
    except Exception as e:
        print("Error generando calendario:", e)
