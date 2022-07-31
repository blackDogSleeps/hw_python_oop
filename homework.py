from dataclasses import dataclass
from string import Template


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = Template('Тип тренировки: $training_type; '
                       + 'Длительность: $duration ч.; '
                       + 'Дистанция: $distance км; '
                       + 'Ср. скорость: $speed км/ч; '
                       + 'Потрачено ккал: $calories.')

    def get_message(self) -> str:
        return self.message.substitute(training_type=self.training_type,
                                       duration=format(self.duration, '.3f'),
                                       distance=format(self.distance, '.3f'),
                                       speed=format(self.speed, '.3f'),
                                       calories=format(self.calories, '.3f'))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(str(type(self).__name__),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: float = 18
    coeff_calorie_2: float = 20
    minutes_in_hour: float = 60

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        duration = self.duration * self.minutes_in_hour
        return ((self.coeff_calorie_1
                * self.get_mean_speed()
                - self.coeff_calorie_2)
                * self.weight
                / self.M_IN_KM
                * duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029
    minutes_in_hour: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        duration = self.duration * self.minutes_in_hour
        return ((self.coeff_calorie_1
                * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.coeff_calorie_2
                * self.weight)
                * duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.coeff_calorie_1)
                * self.coeff_calorie_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    table: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    return table[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
