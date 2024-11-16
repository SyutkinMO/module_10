# ----------------Введение в потоки----------------

import time
import threading

"""Необходимо создать функцию write_words(word_count, file_name), где word_count - количество записываемых слов,
file_name - название файла, куда будут записываться слова.
Функция должна вести запись слов "Какое-то слово № <номер слова по порядку>" в соответствующий файл с прерыванием
после записи каждого на 0.1 секунду.
В конце работы функции вывести строку "Завершилась запись в файл <название файла>
Измерьте время затраченное на выполнение функций и потоков."""


def write_words(word_count, file_name):
    file = open(f'{file_name}', 'w+', encoding='utf-8')
    for i in range(word_count):
        file.write(f'Какое-то слово №{i + 1} \n')
    file.close()
    print(f'Завершилась запись в файл {file_name}')


# начальное время
start_time1 = time.time()

write_words(10, 'example1.txt')
write_words(30, 'example2.txt')
write_words(200, 'example3.txt')
write_words(100, 'example4.txt')

# конечное время
end_time1 = time.time()

# разница между конечным и начальным временем
elapsed_time1 = end_time1 - start_time1
print('Работа потоков', elapsed_time1)

thread1 = threading.Thread(target=write_words, args=(10, 'example5.txt'))
thread2 = threading.Thread(target=write_words, args=(30, 'example6.txt'))
thread3 = threading.Thread(target=write_words, args=(200, 'example7.txt'))
thread4 = threading.Thread(target=write_words, args=(100, 'example8.txt'))

start_time2 = time.time()

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()

end_time2 = time.time()

elapsed_time2 = end_time2 - start_time2

print('Работа потоков', elapsed_time2)
