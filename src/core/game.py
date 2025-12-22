from src.core.game_engine import KrestikNolikEngine


class Krestik_nolik(KrestikNolikEngine):
    def __init__(self, size: int = 3) -> None:
        if not isinstance(size, int):
            raise TypeError("Размер\
 должен быть целым числом")
        if size < 1:
            raise ValueError("Размер\
 поля должен быть положительным")
        if size > 5:
            raise ValueError("Размер поля слишком большой")

        super().__init__(size)
