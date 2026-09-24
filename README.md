### What This Script Does:
1. Physical Footprint Verification: It evaluates each piece using its exact code array dimensions (e.g., Body Armor as 2x3, Colossus Blade as 2x4, Runes as 1x1).
2. Volumetric Boundaries: If a combination takes up more than 12 slots total, or includes an item profile that exceeds 4 grid squares tall, the script flags it as a physical impossibility and drops it.
3. Strict Profile Exclusions: It runs a filtration block that identifies known core profiles—such as 3 matching items, or known socketing blueprints—and cleanly slices them out of the final document array.

You can copy this into any local Python environment (like PyCharm, VS Code, or a Jupyter Notebook) to generate the complete .csv system matrix.
