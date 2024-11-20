# -------------------Очереди для обмена данными между потоками.-------------------

import threading
import random
import time
from queue import Queue

"""
Класс Table:
Объекты этого класса должны создаваться следующим способом - Table(1)
Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)
"""


class Table:
    guest = None  # по умолчанию стол пустой

    def __init__(self, number):
        self.number = number  # номер стола


"""
Класс Guest:
Должен наследоваться от класса Thread (быть потоком).
Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
Обладать атрибутом name - имя гостя.
Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
"""


class Guest(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name  # Имя гостя

    def run(self):
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)  # Время на трапезу


"""
Класс Cafe:
Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
"""


class Cafe:
    queue = Queue()  # очередь

    def __init__(self, *tables):
        self.tables = tables  # Передаются классы!

        """Метод guest_arrival(self, *guests):
    Должен принимать неограниченное кол-во гостей (объектов класса Guest).
    Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest), запускать поток гостя и выводить 
    на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
    Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue 
    и выводить сообщение "<имя гостя> в очереди"."""

    def guest_arrival(self, *guests):
        for guest in guests:  # берем каждого гостя, который передан как поток на классе с атрибутами и методами
            busy = False  # стол для него пока не нашли
            for table in self.tables:  # и идем проверять каждый стол, который передан как класс и можно обращаться
                if table.guest is None:  # к его атрибутам
                    table.guest = guest
                    guest.start()  # гость сел за стол
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    busy = True  # стол нашли
                    break  # дальше проверять не надо, цикл останавливается
            if not busy:  # стол после всего обхода так и не найден
                self.queue.put(guest)  # закинули гостя (поток) в очередь
                print(f'{guest.name} в очереди')

        """Метод discuss_guests
        Этот метод имитирует процесс обслуживания гостей.
    Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
    Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive), 
    то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". 
    Так же текущий стол освобождается (table.guest = None).
    Если очередь ещё не пуста (метод empty) и один из столов освободился (None), то текущему столу присваивается 
    гость взятый из очереди (queue.get()). Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди 
    и сел(-а) за стол номер <номер стола>"
    Далее запустить поток этого гостя (start)"""

    def discuss_guests(self):
        """ПОКА очередь не пустая или хотя бы один стол занят (В данном случае функция any возвращает
        результат True)"""
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:  # идем по столам
                # Если гость (поток) за столом и поток не живой(закончил трапезу) - надо прибраться и освободить стол
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} за столом {table.number} покушал (-а) и ушёл(ушла)')
                    print(f'стол номер {table.number} свободен')
                    table.guest = None
                # Проверяем, что если за столом пусто и очередь НЕ пустая
                if table.guest is None and not self.queue.empty():
                    guest = self.queue.get()  # назначаем в переменную гостя(поток), которого просим из очереди
                    table.guest = guest  # передаем этот поток в атрибут класса table (садим за стол)
                    guest.start()  # гость начинает трапезничать (запускаем поток и с ним метод run)
                    print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
