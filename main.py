from models import IPhone, MacBook, Master, ServiceOrder, SparePart
from service import AppleService


def main():
  hub = AppleService("iStore Official Lab")

  # Запчастини
  hub.add_part(
      SparePart("Заміна батареї iPhone", stock_quantity=2, price=2800.0)
  )
  hub.add_part(
      SparePart("Чистка та заміна клавіатури Mac", stock_quantity=1, price=3400.0)
  )
  hub.add_part(
      SparePart("Заміна камери iPhone", stock_quantity=0, price=3100.0)
  )  # Немає на складі

  # Майстри
  hub.add_master(Master("Олексій", max_load=2))
  hub.add_master(Master("Артем", max_load=1))

  # Створюємо конкретні об'єкти з новими параметрами діагностики
  phone1 = IPhone(
      model="iPhone 15 Pro",
      serial_number="SN-40291",
      issue="Заміна батареї iPhone",
      battery_health=74,     # Порожить попередження <80%
      face_id_ok=True,
  )

  laptop = MacBook(
      model="MacBook Air M2",
      serial_number="SN-55210",
      issue="Чистка та заміна клавіатури Mac",
      screen_size=13.6,
      cpu_temp=86.4,         # Порожить попередження про перегрів >80°C
      ssd_life_percent=95,
  )

  phone2 = IPhone(
      model="iPhone 13 Pro",
      serial_number="SN-10294",
      issue="Заміна камери iPhone",
      battery_health=89,
      face_id_ok=False,      # Покаже помилку Face ID
  )

  # Додаємо до замовлень
  hub.add_order(ServiceOrder(101, "Артем", phone1))
  hub.add_order(ServiceOrder(102, "Вікторія", laptop))
  hub.add_order(ServiceOrder(103, "Максим", phone2))

  # Запуск
  hub.process_all_orders()

  # Звіт
  hub.show_report()


if __name__ == "__main__":
  main()
