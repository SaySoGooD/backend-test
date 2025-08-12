from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    """Модель сотрудника"""
    name: str
    position: str
    salary: int

    def __str__(self):
        return f"Employee(name={self.name}, position={self.position}, salary={self.salary})"
