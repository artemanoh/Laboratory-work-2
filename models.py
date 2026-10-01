from abc import ABC, abstractmethod


# ==========================================================
# АБСТРАКЦІЯ ТА БАЗОВИЙ КЛАС
# ==========================================================
class Device(ABC):
  """Абстрактний базовий клас пристрою."""

  def __init__(self, model: str, serial_number: str, issue: str):
    self.model = model
    self.serial_number = serial_number
    self.issue = issue
    self._is_fixed = False  # Захищений атрибут (інкапсуляція)

  @property
  def is_fixed(self) -> bool:
    """Геттер: дозволяє читати статус, але не змінювати напряму."""
    return self._is_fixed

  def mark_as_fixed(self):
    """Контрольована зміна стану."""
    self._is_fixed = True

  @abstractmethod
  def run_diagnostics(self) -> str:
    """Абстрактний метод: кожен спадкоємець мусить реалізувати його по-своєму."""
    pass

  def get_status_info(self) -> str:
    status = "Відремонтовано" if self._is_fixed else "Потребує ремонту"
    return f"{self.model} (S/N: {self.serial_number}) | Несправність: {self.issue} | Стан: {status}"


# ==========================================================
# НАСЛІДУВАННЯ ТА ПОЛІМОРФІЗМ
# ==========================================================
class IPhone(Device):
  """Клас-нащадок для смартфонів Apple."""

  def __init__(
      self,
      model: str,
      serial_number: str,
      issue: str,
      battery_health: int = 85,
  ):
    super().__init__(model, serial_number, issue)
    self.battery_health = battery_health

  # Поліморфізм: власна реалізація діагностики для iPhone
  def run_diagnostics(self) -> str:
    return (
        f"Діагностика iPhone [{self.model}]: Ємність АКБ:"
        f" {self.battery_health}%, сенсор екрана OK."
    )


class MacBook(Device):
  """Клас-нащадок для ноутбуків Apple."""

  def __init__(
      self,
      model: str,
      serial_number: str,
      issue: str,
      screen_size: float = 13.6,
  ):
    super().__init__(model, serial_number, issue)
    self.screen_size = screen_size

  # Поліморфізм: власна реалізація діагностики для MacBook
  def run_diagnostics(self) -> str:
    return (
        f"Діагностика Mac [{self.model} {self.screen_size}\"]: Стан SSD 98%,"
        " кулери в нормі."
    )


# ==========================================================
# ІНКАПСУЛЯЦІЯ У СКЛАДІ ТА ЗАМОВЛЕННЯХ
# ==========================================================
class SparePart:
  """Запчастина з повною інкапсуляцією кількості."""

  def __init__(self, part_name: str, stock_quantity: int, price: float):
    self.part_name = part_name
    self.__stock_quantity = max(
        0, stock_quantity
    )  # Приватне поле (не можна зробити < 0)
    self.price = price

  @property
  def stock_quantity(self) -> int:
    return self.__stock_quantity

  def take_one(self) -> bool:
    """Безпечне зменшення залишку без прямого доступу ззовні."""
    if self.__stock_quantity > 0:
      self.__stock_quantity -= 1
      return True
    return False

  def restock(self, qty: int):
    if qty > 0:
      self.__stock_quantity += qty

  def get_info(self) -> str:
    return f"{self.part_name}: {self.__stock_quantity} шт. (Ціна: {self.price:.2f} грн)"


class Master:

  def __init__(self, name: str, max_load: int = 2):
    self.name = name
    self._active_tasks = 0
    self.max_load = max_load

  def can_take_task(self) -> bool:
    return self._active_tasks < self.max_load

  def assign_task(self):
    self._active_tasks += 1

  def complete_task(self):
    if self._active_tasks > 0:
      self._active_tasks -= 1

  def get_info(self) -> str:
    return f"Майстер {self.name} - зайнятість: {self._active_tasks}/{self.max_load}"


class ServiceOrder:

  def __init__(self, order_id: int, client_name: str, device: Device):
    self.order_id = order_id
    self.client_name = client_name
    self.device = device
    self._cost = 0.0

  @property
  def cost(self) -> float:
    return self._cost

  def set_cost(self, part_price: float, labor_price: float = 600.0):
    self._cost = part_price + labor_price

  def print_receipt(self):
    print(f"Квитанція #{self.order_id} | Клієнт: {self.client_name}")
    print(f"  Пристрій: {self.device.model} ({self.device.issue})")
    print(f"  Сума до сплати: {self._cost:.2f} грн")
