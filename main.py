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

  # Створюємо конкретні об'єкти класів-нащадків
  phone1 = IPhone(
      "iPhone 15 Pro",
      "SN-40291",
      "Заміна батареї iPhone",
      battery_health=78,
  )
  laptop = MacBook(
      "MacBook Air M2",
      "SN-55210",
      "Чистка та заміна клавіатури Mac",
      screen_size=13.6,
  )
  phone2 = IPhone(
      "iPhone 13 Pro",
      "SN-10294",
      "Заміна камери iPhone",
      battery_health=89,
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
