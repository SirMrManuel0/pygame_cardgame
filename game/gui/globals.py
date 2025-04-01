import numpy as np
from useful_utility.algebra import Vector

PHI: float = 1.618033988749895
SIZE: tuple = (700 * PHI, 700)

FPS: int = 60

BACKGROUND_COLOR: Vector = Vector([62, 76, 84])
BRIGHT_COLOR: Vector = Vector([248, 244, 228])
HOVER_COLOR: Vector = Vector([125, 121, 242])

v: Vector = (1/5) * (2 * BACKGROUND_COLOR + 3 * BRIGHT_COLOR)
for i in range(v.get_dimension()):
    v[i] = np.round(float(v[i]))

COLOR_OF_LIGHT: Vector = v.copy()

v: Vector = (1/7) * (4 * BACKGROUND_COLOR + 3 * BRIGHT_COLOR)
for i in range(v.get_dimension()):
    v[i] = np.round(float(v[i]))

DIFFUSED_LIGHT: Vector = v.copy()
