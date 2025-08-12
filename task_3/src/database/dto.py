from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CustomerTotalDTO:
    customer_id: int
    total_amount: Decimal

    def __str__(self):
        return f"Сумма всех покупок юзера {self.customer_id}: {self.total_amount:.2f}"


@dataclass(frozen=True)
class MaxCustomerTotalDTO:
    customer_id: int
    total_amount: Decimal

    def __str__(self):
        return f"Клиент с максимальной суммой заказов: {self.customer_id} = {self.total_amount:.2f}"


@dataclass(frozen=True)
class OrdersCountDTO:
    year: int
    orders_count: int

    def __str__(self):
        return f"Количество заказов за {self.year} год: {self.orders_count}"


@dataclass(frozen=True)
class CustomerAvgDTO:
    customer_id: int
    avg_amount: Decimal

    def __str__(self):
        return f"Средняя сумма заказов по клиенту {self.customer_id}: {self.avg_amount:.2f}"
