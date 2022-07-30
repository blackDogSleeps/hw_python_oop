class InfoMessage():
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self) -> str:
        training_type = self.training_type
        duration = format(self.duration, '.3f')
        distance = format(self.distance, '.3f')
        speed = format(self.speed, '.3f')
        calories = format(self.calories, '.3f')
        return str(f'Тип тренировки: {training_type}; '
                   + f'Длительность: {duration} ч.; '
                   + f'Дистанция: {distance} км; '
                   + f'Ср. скорость: {speed} км/ч; '
                   + f'Потрачено ккал: {calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = str(type(self).__name__)
        duration = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type,
                           duration,
                           distance,
                           speed,
                           calories)


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        mean_speed: float = self.get_mean_speed()
        weight = self.weight
        duration = self.duration * 60
        m_in_km = self.M_IN_KM
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        calories: float = ((coeff_calorie_1
                           * mean_speed
                           - coeff_calorie_2)
                           * weight
                           / m_in_km
                           * duration)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        mean_speed: float = self.get_mean_speed()
        duration = self.duration * 60
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        weight = self.weight
        height = self.height
        return ((coeff_calorie_1
                * weight
                + (mean_speed**2 // height)
                * coeff_calorie_2
                * weight)
                * duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        length_pool = self.length_pool
        count_pool = self.count_pool
        m_in_km = self.M_IN_KM
        duration = self.duration
        return (length_pool * count_pool / m_in_km / duration)

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        weight = self.weight
        return ((mean_speed
                + coeff_calorie_1)
                * coeff_calorie_2
                * weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    table = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    activity = table[workout_type]
    if activity.__name__ == 'Swimming':
        new_object = activity(data[0], data[1], data[2], data[3], data[4])
        new_object.show_training_info()
    elif activity.__name__ == 'SportsWalking':
        new_object = activity(data[0], data[1], data[2], data[3])
        new_object.show_training_info()
    elif activity.__name__ == 'Running':
        new_object = activity(data[0], data[1], data[2])
        new_object.show_training_info()
    return new_object


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

    f = format(float(1), '.3f')
    print(f)
