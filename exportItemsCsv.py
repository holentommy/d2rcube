import csv
import itertools

# 1. DEFINE THE ENTIRE ITEM CATALOG WITH PHYSICAL SIZES (Width x Height)
RUNES = [f"{r} Rune" for r in [
    "El", "Eld", "Tir", "Nef", "Eth", "Ith", "Tal", "Ral", "Ort", "Thul", "Amn", "Sol", "Shael", 
    "Dol", "Hel", "Io", "Lum", "Ko", "Fal", "Lem", "Pul", "Um", "Mal", "Ist", "Gul", "Vex", 
    "Ohm", "Lo", "Sur", "Ber", "Jah", "Cham", "Zod"
]] # All 33 runes take up 1x1 inventory slots

GEM_TIERS = ["Chipped", "Flawed", "Normal", "Flawless", "Perfect"]
GEM_TYPES = ["Amethyst", "Diamond", "Emerald", "Ruby", "Sapphire", "Topaz", "Skull"]
GEMS = [f"{t} {g}" for t in GEM_TIERS for g in GEM_TYPES] # All 35 gems take up 1x1 inventory slots

QUEST_ENDGAME = {
    "Standard of Heroes": (1, 1), "Horadric Staff": (1, 4), "Khalim's Will": (1, 3),
    "Wirt's Leg": (1, 3), "Hellforge Hammer": (1, 3), "Scroll of Inifuss": (2, 2),
    "Key of Terror": (1, 1), "Key of Hate": (1, 1), "Key of Destruction": (1, 1),
    "Mephisto's Brain": (1, 1), "Diablo's Horn": (1, 1), "Baal's Eye": (1, 1),
    "Twisted Essence of Suffering": (1, 1), "Charged Essence of Hatred": (1, 1),
    "Burning Essence of Terror": (1, 1), "Festering Essence of Destruction": (1, 1),
    "Token of Absolution": (1, 1)
}

# Base gear classified by size footprint (Width, Height)
GEAR_TYPES = {
    "Ring / Amulet / Jewel / Charm (Small)": (1, 1),
    "Large Charm / Boots / Gloves / Belts / Circlets": (1, 2),
    "Grand Charm / Daggers / Wands / Scepters": (1, 3),
    "1x4 Item (e.g., Phase Blade, Crystal Sword)": (1, 4),
    "Helm / Shield / Melee Weapons (Medium)": (2, 2),
    "Body Armor / Crossbows / Polearms / Spears": (2, 3),
    "2x4 Item (e.g., Colossus Blade, Pike, Grand Matron Bow)": (2, 4)
}

# 2. DEFINE KNOWN BLIZZARD RECIPES TO EXCLUDE (Signature matching profiles)
# Profiles represent structures like: 3 of same item, gear + specific runes + gems, etc.
KNOWN_RECIPE_PROFILES = [
    # Gems & Runes upgrades
    {"items": ["3 of same Rune"], "gear": None},
    {"items": ["2 of same Rune", "1 Gem"], "gear": None},
    {"items": ["3 of same Gem"], "gear": None},
    # Jewelry & Quest
    {"items": ["3 Rings"], "gear": None},
    {"items": ["3 Amulets"], "gear": None},
    {"items": ["3 Perfect Gems"], "gear": "Ring / Amulet / Jewel / Charm (Small)"},
    {"items": ["Key of Terror", "Key of Hate", "Key of Destruction"], "gear": None},
    {"items": ["Mephisto's Brain", "Diablo's Horn", "Baal's Eye"], "gear": None},
    {"items": ["Wirt's Leg", "Tome of Town Portal"], "gear": None},
    # Gear socketing/repairing/upgrading shortcuts (generalized profiles)
    {"items": ["1 Tal Rune", "1 Thul Rune", "1 Perfect Topaz"], "gear": "Body Armor / Crossbows / Polearms / Spears"},
    {"items": ["1 Ral Rune", "1 Amn Rune", "1 Perfect Amethyst"], "gear": "Helm / Shield / Melee Weapons (Medium)"},
    {"items": ["1 Ort Rune", "1 Amn Rune", "1 Perfect Sapphire"], "gear": "1x4 Item (e.g., Phase Blade, Crystal Sword)"},
    {"items": ["1 Ral Rune", "1 Ort Rune", "1 Perfect Emerald"], "gear": "Shield"},
]

def get_size(item_name):
    """Returns total grid slot usage (area) and dimensions for any item."""
    if item_name in RUNES or item_name in GEMS:
        return 1, 1, 1
    if item_name in QUEST_ENDGAME:
        w, h = QUEST_ENDGAME[item_name]
        return w * h, w, h
    if item_name in GEAR_TYPES:
        w, h = GEAR_TYPES[item_name]
        return w * h, w, h
    return 1, 1, 1

def generate_matrix(output_filename="exhaustive_cube_permutation_matrix.csv"):
    with open(output_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "Category", "Base Gear Type", "Component 1", "Component 2", 
            "Component 3", "Component 4", "Total Grid Slots Used", "Max Item Height Used"
        ])
        
        print("Processing permutations... Enforcing 12-slot physical layout boundary.")
        
        # Track total entries processed
        recipe_counter = 0

        # --- LOOP 1: SYSTEMATIC RUNE COMBINATIONS ---
        # Theoretical combinations of runes mixing together up to 4 ingredients
        for r_count in range(2, 5):
            for combo in itertools.combinations_with_replacement(RUNES, r_count):
                # Filter out standard 3-of-the-same rune upgrades
                if len(combo) == 3 and len(set(combo)) == 1:
                    continue
                # Physical validation (each rune is 1 slot, fits within 12 max)
                slots = len(combo)
                row = ["Rune Intersection Matrix", "None"] + list(combo) + [""] * (4 - len(combo)) + [slots, 1]
                writer.writerow(row)
                recipe_counter += 1

        # --- LOOP 2: SYSTEMATIC GEM COMBINATIONS ---
        # Non-functional variations mixing different tiers and types
        for g_count in range(2, 5):
            for combo in itertools.combinations_with_replacement(GEMS, g_count):
                if len(combo) == 3 and len(set(combo)) == 1: # Exclude standard gem upgrades
                    continue
                slots = len(combo)
                row = ["Gem Structural Permutations", "None"] + list(combo) + [""] * (4 - len(combo)) + [slots, 1]
                writer.writerow(row)
                recipe_counter += 1

        # --- LOOP 3: GEAR + MODIFIER MATRIX ---
        # Evaluates all physical base shapes alongside runes/gems/quest objects
        modifier_pool = RUNES[:10] + GEMS[:10] + ["Standard of Heroes", "Token of Absolution"] # Curated pool for validation
        
        for gear_name, (g_w, g_h) in GEAR_TYPES.items():
            gear_slots = g_w * g_h
            
            # Look at adding 1 to 3 modifiers alongside the gear piece
            for mod_count in range(1, 4):
                for mods in itertools.combinations_with_replacement(modifier_pool, mod_count):
                    # Check physical cube capacity constraints (Total Area <= 12 slots, Max Height <= 4)
                    total_mod_slots = sum(get_size(m)[0] for m in mods)
                    total_slots = gear_slots + total_mod_slots
                    
                    max_height = max([g_h] + [get_size(m)[2] for m in mods])
                    
                    if total_slots <= 12 and max_height <= 4:
                        # Ensure it's not a known Horadric Socket/Upgrade recipe
                        # Simple match check to eliminate standard crafting patterns
                        if "Perfect" in str(mods) and gear_name.startswith("Body Armor") and "Tal Rune" in str(mods):
                            continue # Skips known socket recipes
                            
                        row = [
                            "Theoretical Item Crafting Matrix", 
                            gear_name
                        ] + list(mods) + [""] * (4 - len(mods)) + [total_slots, max_height]
                        
                        writer.writerow(row)
                        recipe_counter += 1

        print(f"Done! Generated {recipe_counter} mathematically valid theoretical recipe nodes.")
        print(f"Matrix saved successfully to: {output_filename}")

if __name__ == "__main__":
    generate_matrix()
