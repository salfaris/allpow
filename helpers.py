def float_to_money(val: float):
    return f"{val:.2f}"

def float_to_gbp(val: float):
    return f"£ {float_to_money(val)}"

def compute_rating(
    source,
    cost,
    savings,
    entertainment_cost,
    leftover,
):
    levered_bonus = source - (cost + savings) + 0.6 * savings

    if savings > 0:
        levered_bonus_w_punishment = levered_bonus - \
            (savings / source) * entertainment_cost
    else:
        levered_bonus_w_punishment = levered_bonus - 0.6 * entertainment_cost

    bi_ratio = levered_bonus_w_punishment / source

    rating = None
    color = None
    if bi_ratio < 0 or leftover < 0:
        rating = "F"
        color = "color_F"
    elif bi_ratio > 0 and bi_ratio <= 0.047847:
        rating = "D"
        color = "color_D"
    elif bi_ratio > 0.047847 and bi_ratio <= 0.076555:
        rating = "C"
        color = "color_C"
    elif bi_ratio > 0.076555 and bi_ratio <= 0.105263:
        rating = "B"
        color = "color_B"
    elif bi_ratio > 0.105263 and bi_ratio <= 0.153111:
        rating = "A"
        color = "color_A"
    else:
        rating = "A+"
        color = "color_Aplus"

    return rating, color