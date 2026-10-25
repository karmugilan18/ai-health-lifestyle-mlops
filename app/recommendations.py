def make_recommendations(x):
    recs = []
    if x["fruit_servings_day"] < 2: recs.append("Consider adding whole-fruit servings gradually.")
    if x["vegetable_servings_day"] < 3: recs.append("Consider adding vegetables to meals to improve variety and fibre.")
    if x["fibre_g_day"] < 25: recs.append("Consider fibre-rich foods such as beans, lentils, vegetables, fruit and whole grains.")
    if x["fried_meals_week"] > 3: recs.append("Consider replacing some fried meals with grilled, steamed or boiled options.")
    if x["processed_meals_week"] > 3: recs.append("Consider reducing frequent highly processed meals when practical.")
    if x["sugar_g_day"] > 50: recs.append("Review sources of added sugar, such as sweetened drinks and desserts.")
    if x["sodium_mg_day"] > 2300: recs.append("Review salty packaged foods and added salt.")
    if x["exercise_min_week"] < 150: recs.append("If appropriate, gradually increase regular weekly physical activity.")
    if not 7 <= x["sleep_hours_day"] <= 9: recs.append("Review your sleep routine; adult sleep needs vary, and many adults aim for about 7–9 hours.")
    if x["water_l_day"] < 1.5: recs.append("Review fluid intake in the context of activity, climate and personal needs.")
    if x["protein_g_day"] < 50: recs.append("Check that meals include suitable protein sources.")
    if not recs: recs.append("Your recorded indicators look relatively balanced in this demo. Continue tracking and review trends.")
    return recs
