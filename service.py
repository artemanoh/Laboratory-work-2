from models import Device, Master, ServiceOrder, SparePart


class AppleService:
  """Головна диспетчерська система сервісного центру."""

  def __init__(self, title: str):
    self.title = title
    self.parts = []
    self.masters = []
    self.orders = []
    self.__revenue = (
        0.0  # Приватний баланс (інкапсуляція: не можна переписати ззовні)
    )

  @property
  def revenue(self) -> float:
    return self.__revenue

  def add_part(self, part: SparePart):
    self.parts.append(part)

  def add_master(self, master: Master):
    self.masters.append(master)

  def add_order(self, order: ServiceOrder):
    self.orders.append(order)
    print(
        f"Прийнято #{order.order_id}: {order.device.model} від"
        f" {order.client_name}"
    )

  def process_all_orders(self):
    print(f"\n--- Запуск автоматичної обробки замовлень у {self.title} ---")

    for order in self.orders:
      dev = order.device

      if dev.is_fixed:
        continue

      print(f"\nОбробка замовлення #{order.order_id} ({dev.model}):")

      # ПОЛІМОРФІЗМ В ДІЇ: викликаємо діагностику, не турбуючись про конкретний підтип
      diagnostic_result = dev.run_diagnostics()
      print(f"  [Діагностика] {diagnostic_result}")

      # Пошук деталі
      needed_part = None
      for part in self.parts:
        if part.part_name == dev.issue:
          needed_part = part
          break

      # Пошук майстра
      available_master = None
      for master in self.masters:
        if master.can_take_task():
          available_master = master
          break

      # Логіка обробки
      if needed_part is None or needed_part.stock_quantity <= 0:
        print(
            f"  [ВІДХИЛЕНО] Немає деталі '{dev.issue}' на складі для замовлення"
            f" #{order.order_id}"
        )
      elif available_master is None:
        print("  [ЧЕРГА] Усі майстри зайняті. Замовлення очікує.")
      else:
        available_master.assign_task()
        needed_part.take_one()
        dev.mark_as_fixed()
        order.set_cost(needed_part.price)
        self.__revenue += order.cost  # Інкапсульоване збільшення виручки
        available_master.complete_task()

        print(
            f"  [УСПІХ] Майстер {available_master.name} виконав ремонт."
            f" Чек: {order.cost:.2f} грн"
        )

  def show_report(self):
    print("\n" + "=" * 48)
    print(f"ПІДСУМКОВИЙ ЗВІТ: {self.title}")
    print("=" * 48)

    print("Залишки деталей на складі:")
    for part in self.parts:
      print(" - " + part.get_info())

    print("\nОформлені квитанції:")
    for order in self.orders:
      if order.device.is_fixed:
        order.print_receipt()

    print(f"\nЗагальна виручка сервісу: {self.__revenue:.2f} грн")
