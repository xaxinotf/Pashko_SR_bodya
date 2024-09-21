import random
import matplotlib.pyplot as plt
import scipy.stats
from typing import Callable

# Опис основних компонентів:
# Клас Experiment:
#
# Цей клас призначений для моделювання випадкових подій на основі заданого розподілу ймовірностей та генератора випадкових значень.
# Конструктор приймає два параметри:
# distribution: словник, який містить можливі значення випадкової події та їх відповідні ймовірності.
# generator: функція, яка генерує випадкове значення згідно з цим розподілом.
# Метод generate(n) виконує моделювання
# n разів і підраховує кількість появ кожного можливого результату.

# Метод check() аналізує отримані результати:
# Проводить тест хі-квадрат для перевірки того, чи спостережувані результати статистично відрізняються від очікуваних значень (розподілу).
# Виводить результат тесту і будує гістограму результатів.
# Експерименти:

# Підкидання монети (coin_toss): ймовірність кожної сторони монети (герб чи цифра) становить 50%.
# Підкидання кубика (dice_roll): ймовірність випадання кожної зі сторін кубика дорівнює

# Підкидання двох кубиків (two_dice_roll): ймовірність появи суми очок від 2 до 12 залежить від кількості комбінацій, які можуть утворити цю суму. Наприклад, сума 7 є найбільш ймовірною, оскільки найбільше комбінацій кубиків можуть дати цей результат.
# Тестування:

# Фізичні експерименти перевіряють уже зібрані результати з підкидання монети, кубика та двох кубиків.
# Обчислювальні експерименти генерують нові дані за допомогою випадкових чисел для перевірки відповідності очікуваним теоретичним результатам.
# Тест хі-квадрат:

# Цей тест використовується для того, щоб перевірити, чи є статистично значущі відхилення між спостережуваними результатами експерименту та теоретично очікуваними значеннями.
# Якщо значення p більше за 0.05, це означає, що немає статистично значущих відхилень (спостережувані результати узгоджуються з очікуваними).

class Experiment:
    def __init__(self, distribution: dict[int, float], generator: Callable[[], int]):
        self.distribution = distribution
        self.generator = generator
        assert abs(sum(distribution.values()) - 1) < 1e-6

    def generate(self, n):
        result = {key: 0 for key in self.distribution}
        for _ in range(n):
            result[self.generator()] += 1
        return result

    def check(self, name, observed: dict[int, float]):
        print(name)
        n = sum(observed.values())
        print(f'Всього {n} спостережень, а саме {observed}')
        expected = {key: value * n for key, value in self.distribution.items()}
        assert list(observed.keys()) == list(expected.keys())
        chi2, p = scipy.stats.chisquare(list(observed.values()), list(expected.values()))
        alpha = 0.05
        print(f'Критерій хі-квадрат: p = {p}',
              f'> {alpha} (дані не показують статистично значущих відхилень від очікуваних)' if p > alpha else
              f'< {alpha} (дані статистично значущо відрізняються від очікуваних)')
        print()
        plt.bar(observed.keys(), observed.values())
        plt.xticks(list(observed.keys()))
        plt.title(name)
        plt.show()


# Експерименти
coin_toss = Experiment({i: 1 / 2 for i in range(2)}, lambda: random.randint(0, 1))
dice_roll = Experiment({i: 1 / 6 for i in range(1, 7)}, lambda: random.randint(1, 6))
two_dice_roll = Experiment({i: min(i - 1, 13 - i) / 36 for i in range(2, 13)},
                           lambda: random.randint(1, 6) + random.randint(1, 6))

# Фізичні експерименти
coin_toss.check('Підкидання монети (фізичний експеримент)', {0: 48, 1: 52})
dice_roll.check('Підкидання кубика (фізичний експеримент)', {1: 19, 2: 17, 3: 8, 4: 18, 5: 19, 6: 19})
two_dice_roll.check('Підкидання двох кубиків (фізичний експеримент)',
                    {2: 5, 3: 6, 4: 8, 5: 17, 6: 6, 7: 19, 8: 16, 9: 7, 10: 7, 11: 6, 12: 3})

# Обчислювальні експерименти
coin_toss.check('Підкидання монети (обчислювальний експеримент)', coin_toss.generate(100))
dice_roll.check('Підкидання кубика (обчислювальний експеримент)', dice_roll.generate(100))
two_dice_roll.check('Підкидання двох кубиків (обчислювальний експеримент)', two_dice_roll.generate(100))