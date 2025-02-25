PHI: float = 1.618033988749895

class Dimension:
    def __init__(self, sizes: tuple = (0, 0), dimension: int = 2, base_ratios: float = (PHI)) -> None:
        self._sizes: list = [*sizes]
        self._dimension: int = dimension
        if dimension > 2 and base_ratios != 0:
            ...
