def factorial_recursion(num):

    if num < 0:
        return 0
    if num == 0:
        return 1

    return num * factorial_recursion(num - 1)


def factorial_loop(num):
    if num < 0:
        return 0
    if num == 0:
        return 1

    factorial = 1
    for i in range(1, num + 1):
        factorial = factorial * i
    return factorial
