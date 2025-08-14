from typing import Tuple


def solution(nums: list) -> Tuple:
    """
    Возвращает количество уникальных чисел, второе по величине число и список чисел, делящихся на 3.    

    Args:
        nums (list): Список чисел.

    Returns:
        tuple: (количество уникальных чисел, второе по величине число, список чисел, делящихся на 3)
    """
    # Параметры по Big O
    # Скорость функции: O(n)
    # Затраты по оперативной памяти: O(n)
    unique_nums = set()
    max_num = None
    second_max = None
    divisible_by_3 = []
    for num in nums:
        unique_nums.add(num)

        # Ищем максимальное число, для нахождения предмаксимального
        if max_num is None or num > max_num:
            second_max = max_num
            max_num = num

        # Ищем предпоследнее по величине число
        elif (second_max is None or num > second_max) and num != max_num:
            second_max = num

        # Собираем числа которые делятся на 3
        if num % 3 == 0:
            divisible_by_3.append(num)

    return len(unique_nums), second_max, divisible_by_3


input_list = [10, 20, 30, 40, 50, 30, 20]

unique_count, second_largest, divisible_by_3_list = solution(input_list)

print(f"Уникальные числа: {unique_count}")
print(f"Второе по величине число: {second_largest}")
print(f"Числа, делящиеся на 3: {divisible_by_3_list}")