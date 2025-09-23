from pathlib import Path
import random, re

def prepare_path(*path_parts):
    """
    Construit un chemin à partir des arguments et crée le dossier parent si nécessaire.

    Usage :
        output_path = prepare_path("data", "raw", "diabetes.csv")
    """ 
    path = Path(*path_parts).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def random_age_from_interval(interval):
    match = re.match(r'\[(\d+)-(\d+)\)', interval)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        return random.randint(start, end - 1)
    else:
        return None