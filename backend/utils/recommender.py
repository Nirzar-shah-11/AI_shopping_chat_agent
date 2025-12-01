import json
import os

# Path to your dataset (adjust if needed)
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../dataset/phones.json")

def load_phones():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def recommend_phones(brand=None, budget=None, features=None, limit=5):
    """
    Recommend phones based on brand, budget, and key features.
    Features can include: 'camera', 'battery', 'fast charging', 'display', 'performance'.
    """
    phones = load_phones()
    results = []

    for phone in phones:
        phone_brand = phone.get("brand", "").lower()
        price = phone.get("price_inr", 0)
        notes = phone.get("notes", "").lower()
        camera = phone.get("camera", {})
        battery = phone.get("battery_mah", 0)
        fast_charge = phone.get("fast_charge_w", 0)
        ram = phone.get("ram_gb", 0)
        display_type = phone.get("display", {}).get("type", "").lower()

        # ---- Brand Filter ----
        if brand and brand.lower() not in phone_brand:
            continue

        # ---- Budget Filter ----
        if budget and price > budget:
            continue

        # ---- Feature Matching ----
        if features:
            feature_match = True
            for f in features:
                f = f.lower()
                if "camera" in f:
                    if camera.get("main_mp", 0) < 48:
                        feature_match = False
                elif "battery" in f:
                    if battery < 4500:
                        feature_match = False
                elif "fast" in f or "charging" in f:
                    if fast_charge < 33:
                        feature_match = False
                elif "display" in f:
                    if "amoled" not in display_type:
                        feature_match = False
                elif "performance" in f or "speed" in f:
                    if ram < 6:
                        feature_match = False
            if not feature_match:
                continue

        results.append(phone)

    # Sort results by price ascending
    results = sorted(results, key=lambda x: x.get("price_inr", 0))

    return results[:limit]


def compare_phones(phone_names):
    """
    Compare multiple phones side by side based on their IDs or model names.
    """
    phones = load_phones()
    comparisons = []
    normalized_names = [name.lower() for name in phone_names]

    for phone in phones:
        if phone.get("id", "").lower() in normalized_names or phone.get("model", "").lower() in normalized_names:
            comparisons.append(phone)

    return comparisons


# --- Example Test ---
if __name__ == "__main__":
    test = recommend_phones(brand="Realme", budget=25000, features=["camera", "fast charging"])
    print(json.dumps(test, indent=2))

    comp = compare_phones(["12+ 5G", "Pixel 8a"])
    print(json.dumps(comp, indent=2))