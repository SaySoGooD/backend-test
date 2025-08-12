from typing import List, Dict, Tuple, Optional

from dto import SalaryStatsDTO


def get_salary_stats(employees: List[Dict]) -> Optional[SalaryStatsDTO]:
    """
    Анализ списка сотрудников.

    Args:
        employees (List[Dict]): Список сотрудников.
            Каждый элемент — словарь с ключами:
                - "name" (str): имя сотрудника.
                - "position" (str): должность.
                - "salary" (int | float): зарплата.

    Returns:
        Tuple[List[str], float, List[Dict]]:
            - List[str]: Имена сотрудников с зарплатой > 50 000.
            - float: Средняя зарплата всех сотрудников.
            - List[Dict]: Список сотрудников, отсортированный по убыванию зарплаты.
    """
    if not employees:
        return None

    sorted_employees = sorted(employees, key=lambda e: e["salary"], reverse=True)

    high_salary_names = []
    total_salary = 0
    for emp in sorted_employees:
        total_salary += emp["salary"]
        if emp["salary"] > 50000:
            high_salary_names.append(emp["name"])
        else:
            break

    avg_salary = round(total_salary / len(employees), 2)

    return SalaryStatsDTO(high_salary_names, avg_salary, sorted_employees)


employees = [
    {"name": "Иван", "position": "разработчик", "salary": 55000},
    {"name": "Анна", "position": "аналитик", "salary": 48000},
    {"name": "Петр", "position": "тестировщик", "salary": 52000},
]

res = get_salary_stats(employees)

print("Имена с зарплатой > 50000:", res.high_salary_names)
print("Средняя зарплата:", res.average_salary)
print("Отсортированные сотрудники:", res.sorted_employees)
