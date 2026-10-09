from abc import ABC, abstractmethod


# ==========================================================
# 1. АБСТРАКЦІЯ ТА БАЗОВИЙ КЛАС
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
    """Абстрактний метод: кожен спадкоємець реалізує вивід та перевірки по-своєму."""
    pass

  def get_status_info(self) -> str:
    status = "Відремонтовано" if self._is_fixed else "Потребує ремонту"
    return f"{self.model} (S/N: {self.serial_number}) | Несправність: {self.issue} | Стан: {status}"


# ==========================================================
# 2. НАСЛІДУВАННЯ ТА ПОЛІМОРФІЗМ (УНІКАЛЬНА ДІАГНОСТИКА)
# ==========================================================
class IPhone(Device):
  """Клас-нащадок для смартфонів Apple."""

  def __init__(
      self,
      model: str,
      serial_number: str,
      issue: str,
      battery_health: int = 85,
      face_id_ok: bool = True,
  ):
    super().__init__(model, serial_number, issue)
    self.battery_health = battery_health
    self.face_id_ok = face_id_ok

  def run_diagnostics(self) -> str:
    """Запускає унікальну діагностику iPhone з виводом процесів у консоль."""
    print(f"\n[ДІАГНОСТИКА IPHONE] {self.model} (S/N: {self.serial_number})")
    print(f"  ├─ Перевірка АКБ (Battery Health): {self.battery_health}%")

    if self.battery_health < 80:
      print("  │  └─ [ПОПЕРЕДЖЕННЯ] Ємність батареї нижче 80% (потрібна заміна)!")
    else:
      print("  │  └─ [OK] Акумулятор у доброму стані.")

    face_status = "OK (Працює)" if self.face_id_ok else "ПОМИЛКА (Апаратний збій)"
    print(f"  ├─ Сканування модулів Face ID / TrueDepth: {face_status}")
    print("  └─ Перевірка дисплейного модуля та тачскріна: Помилок не виявлено")

    return f"Зафіксовано заявлену несправність: '{self.issue}'."


class MacBook(Device):
  """Клас-нащадок для ноутбуків Apple."""

  def __init__(
      self,
      model: str,
      serial_number: str,
      issue: str,
      screen_size: float = 13.6,
      cpu_temp: float = 45.0,
      ssd_life_percent: int = 98,
  ):
    super().__init__(model, serial_number, issue)
    self.screen_size = screen_size
    self.cpu_temp = cpu_temp
    self.ssd_life_percent = ssd_life_percent

  def run_diagnostics(self) -> str:
    """Запускає унікальну діагностику MacBook з виводом процесів у консоль."""
    print(f"\n[ДІАГНОСТИКА MACBOOK] {self.model} {self.screen_size}\" (S/N: {self.serial_number})")
    print(f"  ├─ Тест ресурсу накопичувача NVMe SSD: {self.ssd_life_percent}%")
    print(f"  ├─ Замір температури CPU/GPU: {self.cpu_temp}°C")

    if self.cpu_temp > 80.0:
      print("  │  └─ [УВАГА] Виявлено критичний перегрів! Необхідне чищення та заміна термопасти.")
    else:
      print("  │  └─ [OK] Температурний режим у межах норми.")

    print("  └─ Тестування портів Thunderbolt та клавіатури: Сканування завершено")

    return f"Зафіксовано заявлену несправність: '{self.issue}'."


# ==========================================================
# 3. ІНКАПСУЛЯЦІЯ ДАНИХ СКЛАДУ, МАЙСТРІВ ТА ЗАМОВЛЕНЬ
# ==========================================================
class SparePart:
  """Запчастина з повною інкапсуляцією кількості."""

  def __init__(self, part_name: str, stock_quantity: int, price: float):
    self.part_name = part_name
    self.__stock_quantity = max(0, stock_quantity)  # Приватне поле
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