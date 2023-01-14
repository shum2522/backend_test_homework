class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    training_type = ' '
    M_IN_KM = 1000
    MIN_IN_H = 60

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения км/ч."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.training_type
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.DURRATION_IN_MIN = self.duration * self.MIN_IN_H

    def get_spent_calories(self):
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM * self.DURRATION_IN_MIN)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = 0.278

    def __init__(self, action: int, duration: float,
                 weight: float, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.DURRATION_IN_MIN = self.duration * self.MIN_IN_H
        self.height_m = self.height / self.CM_IN_M
        self.FKMH_IN_MSEC = self.get_mean_speed() * self.KMH_IN_MSEC

    def get_spent_calories(self):
        calories = ((self.CALORIES_WEIGHT_MULTIPLIER
                    * self.weight + ((self.FKMH_IN_MSEC**2)
                     / self.height_m)
                    * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                    * self.weight)
                    * self.DURRATION_IN_MIN)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    K_1 = 1.1
    K_2 = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self):
        calories = ((self.get_mean_speed() + self.K_1)
                    * self.K_2 * self.weight * self.duration)
        return calories


training_data = {}


def read_package(training_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if training_type == 'SWM':
        training_data['SWM'] = Swimming(data[0], data[1],
                                        data[2],
                                        data[3],
                                        data[4],)
        Training.training_type = 'Swimming'

        return training_data['SWM']
    elif training_type == 'RUN':
        training_data['RUN'] = Running(data[0], data[1], data[2],)

        Training.training_type = 'Running'

        return training_data['RUN']
    elif training_type == 'WLK':
        training_data['WLK'] = SportsWalking(data[0],
                                             data[1],
                                             data[2],
                                             data[3],)

        Training.training_type = 'SportsWalking'

        return training_data['WLK']


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
