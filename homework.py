class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    # Константы класса
    LEN_STEP: float = 0.65

    CONST_CALORIES_CALC_1: float = 0.0
    CONST_CALORIES_CALC_2: float = 0.0

    M_IN_KM: int = 1000
    H_TO_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
    # Тут Mypy ругается, что у нас пустое тело, а мы на вывод хотим float.
    # Как в таком случае поступают?

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CONST_CALORIES_CALC_1: float = 18.0
    CONST_CALORIES_CALC_2: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CONST_CALORIES_CALC_1
                 * self.get_mean_speed()
                 + self.CONST_CALORIES_CALC_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.H_TO_MIN
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CONST_CALORIES_CALC_1: float = 0.035
    CONST_CALORIES_CALC_2: float = 0.029
    # Локальные константы для расчетов в подклассе:
    # Я бы их в константы класса вынесла, это универсальные значения,
    # Если в будущем расширять код, они могут понадобиться
    # и для других расчетов, но pytest не пустил...
    KMH_TO_MS: float = 0.278
    M_TO_CM: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CONST_CALORIES_CALC_1
                 * self.weight
                 + ((self.get_mean_speed()
                     * self.KMH_TO_MS)**2
                    / (self.height
                       / self.M_TO_CM))
                 * self.CONST_CALORIES_CALC_2
                 * self.weight)
                * self.duration
                * self.H_TO_MIN
                )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CONST_CALORIES_CALC_1: float = 1.1
    CONST_CALORIES_CALC_2: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration
                )

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CONST_CALORIES_CALC_1)
                * self.CONST_CALORIES_CALC_2
                * self.weight
                * self.duration
                )


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""

    # Хочется проаннотировать словарь, разное пытаюсь - не выходит
    # #package_code: dict[str, Training] - самый логичный вариант,
    # который приходит в голову, но тут явно что-то не то, памагите...
    package_code = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        training_type: Training = package_code[workout_type](*data)
        return training_type
    except KeyError:
        error: str = 'Такой тренировки нет.'
        print(error)
# Mypy ругается, что нет return.
# Судя по всему он его не видит в блоке try.
# Как поступить, что делать?


def main(training: Training) -> None:
    """Главная функция."""

    try:
        info: InfoMessage = Training.show_training_info(training)
        print(info.get_message())
    except (AttributeError, TypeError):
        error: str = 'Наверное, вам это приснилось...'
        print(error)


if __name__ == '__main__':
    packages: list[tuple[str, list[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    try:
        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
    except (ValueError, TypeError):
        error: str = 'Ваше сердце не бьется, у меня для вас плохие новости...'
        print(error)
