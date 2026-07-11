def recommend(quality):

    if quality == 0:
        return "High → Suitable for Animal Feed / Paper"

    elif quality == 1:
        return "Medium → Paper / Biodegradable Products"

    else:
        return "Low → Biomass Energy"


# Explainable AI feature
def explain_prediction(moisture, fiber, impurity, odor):

    reasons = []

    if moisture > 45:
        reasons.append("High moisture reduces bagasse quality")

    if fiber < 5:
        reasons.append("Low fiber strength detected")

    if impurity == "High":
        reasons.append("High impurity level affects usability")

    if odor == "Bad":
        reasons.append("Strong odor indicates decomposition")

    if len(reasons) == 0:
        reasons.append("All parameters indicate good bagasse quality")

    return reasons