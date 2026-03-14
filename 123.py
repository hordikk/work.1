def add(a, b):
    return a + b
def sub(a, b):
    return a - b
def mul(a, b):
    return a * b
def div(a, b):
    return a / b
def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Введите коректное число!")


def main():
    history = []
    while True:
        number_1 = get_number("Введите число: ")
        number_2 = get_number("Введите число:")
        while True:
            try:
                operace = int(input("1-сложение\n"
                                    "2-вычитание\n"
                                    "3-умножение\n"
                                    "4-деление:"))
                if operace in [1, 2, 3, 4]:
                    break
                else:
                    print("Введите коректное число")
            except ValueError:
                print("Введите коректное число")


        if operace == 4 and number_2 == 0:
            print("На ноль делить нельзя")
            continue

        try:
            if operace == 1:
                history.append(f"{number_1} + {number_2} = {add(number_1, number_2)} ")
                print(add(number_1, number_2))
            if operace == 2:
                history.append(f"{number_1} - {number_2} = {sub(number_1, number_2)} ")
                print(sub(number_1, number_2))
            if operace == 3:
                history.append(f"{number_1} * {number_2} = {mul(number_1, number_2)} ")
                print(mul(number_1, number_2))
            if operace == 4:
                history.append(f"{number_1} / {number_2} = {div(number_1, number_2)} ")
                print(div(number_1, number_2))
            print(f" Вы провели такие операции:\n")
            for operation in history:
                print(f"{operation}")


            stop = input("Продолжить? (yes/no): ")
            if stop == "no":
               break


        except ZeroDivisionError:
            print("На ноль делить нельзя")
        except ValueError:
            print("Вы ввели не число")
main()







