from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    M_IN_HR = 60
    LEN_STEP = 0.65
    """Расстояние за один шаг."""
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * self.M_IN_HR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_KOEF = 0.035
    WEIGHT_KOEF_2 = 0.029
    S_IN_HR = 3600
    M_IN_KM = 1000
    CM_IN_M = 100
    SPEED_M_S = round(M_IN_KM / S_IN_HR, 3)

    def get_spent_calories(self) -> float:
        return (
            (self.WEIGHT_KOEF * self.weight
             + ((self.get_mean_speed() * self.SPEED_M_S) ** 2
                / (self.height / self.CM_IN_M))
             * self.WEIGHT_KOEF_2 * self.weight)
            * (self.duration * self.M_IN_HR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_KOEF = 1.1
    WEIGHT_KOEF = 2
    """Расстояние за один гребок."""
    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        return (
            (self.length_pool * self.count_pool) / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SPEED_KOEF) * self.WEIGHT_KOEF
            * self.weight * self.duration
        )


TRAINING_TYPES = {
    'RUN': Running,
    'SWM': Swimming,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type in TRAINING_TYPES:
        return TRAINING_TYPES[workout_type](*data)
    else:
        raise ValueError('Несуществующий код тренировки')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
