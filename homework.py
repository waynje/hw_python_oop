from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


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
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM * self.duration * self.M_IN_HR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float
    KOEF_SPORTS_WALKING_1: float = 0.035
    KOEF_SPORTS_WALKING_2: float = 0.029
    S_IN_HR: int = 3600
    CM_IN_M: int = 100
    KOEF_SPEED_M_S = 0.278

    def get_meter_speed(self) -> float:
        return (
            self.get_mean_speed() * self.KOEF_SPEED_M_S
        )

    def get_spent_calories(self) -> float:
        return (
            (self.KOEF_SPORTS_WALKING_1 * self.weight
             + (self.get_meter_speed() ** 2 / (self.height / self.CM_IN_M))
             * self.KOEF_SPORTS_WALKING_2 * self.weight)
            * (self.duration * self.M_IN_HR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIM_KOEF = 1.1
    SWIM_KOEF_2 = 2
    """Расстояние за один гребок."""
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    def get_mean_speed(self):
        return (
            (self.length_pool * self.count_pool) / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIM_KOEF) * self.SWIM_KOEF_2
            * self.weight * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dist_data = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking
    }

    if workout_type in dist_data:
        return dist_data[workout_type](*data)
    else:
        print('Введен неверный идентификатор тренировки')


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
        training = read_package(workout_type, data)
        main(training)
