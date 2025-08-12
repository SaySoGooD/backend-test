from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SalaryStatsDTO:
    high_salary_names: List[str]
    average_salary: float
    sorted_employees: List[dict]