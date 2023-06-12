from dataclasses import asdict, dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.'
               )

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    M_IN_HR = 60
    LEN_STEP = 0.65
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
        raise Exception('Not usable function')

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
    CALORIES_MEAN_SPEED_MULTIPLIER_1 = 0.035
    CALORIES_MEAN_SPEED_MULTIPLIER_2 = 0.029
    S_IN_HR = 3600
    CM_IN_M = 100
    SPEED_M_S = round(Training.M_IN_KM / S_IN_HR, 3)

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER_1 * self.weight
             + ((self.get_mean_speed() * self.SPEED_M_S) ** 2
                / (self.height / self.CM_IN_M))
             * self.CALORIES_MEAN_SPEED_MULTIPLIER_2 * self.weight)
            * (self.duration * self.M_IN_HR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        return (
            (self.length_pool * self.count_pool) / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight * self.duration
        )


TRAINING_TYPES = {
    'RUN': (Running, len(fields(Running))),
    'SWM': (Swimming, len(fields(Swimming))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}

TRAINING_TYPE_ERROR = (
    'Тренировки "{workout_type}" нет в базе тренировок'
)

PACKAGE_LENGTH_ERROR = (
    'Неверное количество параметров для "{workout_type}": {package_length}, '
    'Должно быть: {normal_length} '
)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAINING_TYPES:
        raise ValueError(TRAINING_TYPE_ERROR.format(workout_type=workout_type))
    workout, length = TRAINING_TYPES[workout_type]
    if len(data) != length:
        raise ValueError(PACKAGE_LENGTH_ERROR.format(workout_type=workout_type,
                                                     package_length=len(data),
                                                     normal_length=length))
    return workout(*data)


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
