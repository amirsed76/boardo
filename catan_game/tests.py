import random


def not_neighbor_list(number, can_accept_list):
    t1 = [2, 4, 5]
    t2 = [1, 3, 5, 6]
    t3 = [2, 6, 7]
    t4 = [1, 5, 8, 9]
    t5 = [1, 2, 4, 6, 9, 10]
    t6 = [2, 3, 5, 7, 10, 11]
    t7 = [3, 6, 11, 12]
    t8 = [4, 9, 13]
    t9 = [4, 5, 8, 10, 13, 14]
    t10 = [5, 6, 9, 11, 14, 15]
    t11 = [6, 7, 10, 12, 15, 16]
    t12 = [7, 11, 16]
    t13 = [8, 9, 14, 17]
    t14 = [9, 10, 13, 15, 17, 18]
    t15 = [10, 11, 14, 16, 18, 19]
    t16 = [11, 12, 15, 19]
    t17 = [13, 14, 18]
    t18 = [14, 15, 17, 19]
    t19 = [15, 16, 18]
    tiles = [[], t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19]
    result = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    # numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    return [x for x in can_accept_list if (x != number and x not in tiles[number])]


def find_place_for_6_8():
    threshold = 4
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    result = []
    for i in range(0, 4):
        if threshold == 0:
            return [4, 10, 11, 16]

        if len(numbers) != 0:
            number = random.choice(numbers)
            numbers = not_neighbor_list(number, numbers)
            result.append(number)
        else:
            threshold -= 1

    return result


if __name__ == '__main__':
    print(find_place_for_6_8())
