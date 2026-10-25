# Illustrative approximate values per serving for an offline demo.
# Replace with verified food composition data before research/production use.
FOODS = {
    "Idli (2 pieces)": {"serving":"2 pieces","calories":140,"protein_g":4,"carbs_g":28,"fat_g":1,"fibre_g":2,"sugar_g":2,"sodium_mg":300},
    "Plain dosa (1 medium)": {"serving":"1 medium","calories":170,"protein_g":4,"carbs_g":27,"fat_g":5,"fibre_g":2,"sugar_g":2,"sodium_mg":350},
    "Vegetable upma (1 cup)": {"serving":"1 cup","calories":220,"protein_g":6,"carbs_g":35,"fat_g":7,"fibre_g":4,"sugar_g":4,"sodium_mg":450},
    "Cooked rice (1 cup)": {"serving":"1 cup","calories":205,"protein_g":4,"carbs_g":45,"fat_g":0.4,"fibre_g":1,"sugar_g":0.1,"sodium_mg":5},
    "Chicken biryani (1 plate)": {"serving":"1 plate","calories":520,"protein_g":25,"carbs_g":62,"fat_g":18,"fibre_g":3,"sugar_g":4,"sodium_mg":950},
    "Sambar (1 cup)": {"serving":"1 cup","calories":130,"protein_g":7,"carbs_g":20,"fat_g":3,"fibre_g":5,"sugar_g":4,"sodium_mg":500},
    "Apple (1 medium)": {"serving":"1 medium","calories":95,"protein_g":0.5,"carbs_g":25,"fat_g":0.3,"fibre_g":4.4,"sugar_g":19,"sodium_mg":2},
    "Boiled egg (1)": {"serving":"1 egg","calories":78,"protein_g":6,"carbs_g":0.6,"fat_g":5,"fibre_g":0,"sugar_g":0.6,"sodium_mg":62},
    "French fries (1 medium serving)": {"serving":"1 serving","calories":365,"protein_g":4,"carbs_g":48,"fat_g":17,"fibre_g":4,"sugar_g":0.5,"sodium_mg":250},
    "Curd (1 cup)": {"serving":"1 cup","calories":150,"protein_g":8,"carbs_g":11,"fat_g":8,"fibre_g":0,"sugar_g":10,"sodium_mg":120}
}
def lookup_food(name):
    return FOODS.get(name)
def list_foods():
    return [{"name": n, **v} for n, v in FOODS.items()]
