def get_plant_stage(xp: float) -> str:
    if xp < 50:
        return "seed"
    elif xp < 150:
        return "sprout"
    return "flower"
