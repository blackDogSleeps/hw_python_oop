from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {training_type}; '
               + 'Длительность: {duration:.3f} ч.; '
               + 'Дистанция: {distance:.3f} км; '
               + 'Ср. скорость: {speed:.3f} км/ч; '
               + 'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(training_type=self.training_type,
                                   duration=self.duration,
                                   distance=self.distance,
                                   speed=self.speed,
                                   calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MINUTES_IN_HOUR: float = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action_in_steps: int = action
        self.duration_in_hours: float = duration
        self.weight_in_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action_in_steps * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration_in_hours)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(str(type(self).__name__),
                           self.duration_in_hours,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_FORMULA_CONST_1: float = 18
    CALORIES_FORMULA_CONST_2: float = 20

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_FORMULA_CONST_1
                * self.get_mean_speed()
                - self.CALORIES_FORMULA_CONST_2)
                * self.weight_in_kg
                / self.M_IN_KM
                * (self.duration_in_hours * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_FORMULA_CONST_1: float = 0.035
    CALORIES_FORMULA_CONST_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height_in_cm: float = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_FORMULA_CONST_1
                * self.weight_in_kg
                + (self.get_mean_speed()**2 // self.height_in_cm)
                * self.CALORIES_FORMULA_CONST_2
                * self.weight_in_kg)
                * (self.duration_in_hours * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_FORMULA_CONST_1: float = 1.1
    CALORIES_FORMULA_CONST_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool_in_meters: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool_in_meters
                * self.count_pool
                / self.M_IN_KM
                / self.duration_in_hours)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALORIES_FORMULA_CONST_1)
                * self.CALORIES_FORMULA_CONST_2
                * self.weight_in_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    table: dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type not in table:
        raise KeyError('Нет такого вида тренировки')
    else:
        return table[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
