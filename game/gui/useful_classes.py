PHI: float = 1.618033988749895


class Dimension:
    def __init__(self, sizes: tuple = (0, 0), base_ratios: float = (PHI)) -> None:
        self._sizes: list = [*sizes]
        self._dimension: int = len(self._sizes)

    def get_dimensions(self):
        return tuple(self._sizes)