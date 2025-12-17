from core.game_engine import KrestikNolikEngine

class Krestik_nolik(KrestikNolikEngine):
    def __init__(self, size=3):
        if not isinstance(size, int):
            raise TypeError(f"Размер должен быть целым числом, получено: {type(size).__name__}")
        if size < 1:
            raise ValueError(f"Размер поля должен быть положительным")
        if size > 5:
            raise ValueError(f"Размер поля слишком большой")

        super().__init__(size)
