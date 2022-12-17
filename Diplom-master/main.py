from interpretator import Interpretator


try:
    print("Подмножества языка Паскаль:")
    print("1 – Язык линейных вычислений")
    print("2 – Язык условных вычислений")
    print("3 – Язык циклических вычислений")
    print("4 - Язык вычислений с одномерными массивами")
    print("5 - Язык вычислений с одномерными массивами и циклами")
    print("6 - Язык функциональных вычислений")
    while 1:
        print("Выберите номер языка, на котором написана программа")
        mode = int(input())
        if mode > 6 or mode < 1:
            print("Номер языка должен быть в отрезке [1, 6]")
        else:
            break
    '''print("Введите название файла с программой")
    f = input()'''
    i = Interpretator('test3.txt', mode)
    i.interpretation()
    print("Работа анализатора заверешена успешно!")
except Exception as error:
    print(error)
except FileNotFoundError:
    print("The file is not exist")