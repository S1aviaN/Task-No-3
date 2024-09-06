import csv
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

# Функция для чтения данных о продажах из файла и записи ошибок в отдельный файл
def read_sales_data(file_path, error_file_path):
    sales_data = []
    with open(file_path, mode='r', encoding='utf-8') as file, open(error_file_path, mode='w', encoding='utf-8') as error_file:
        reader = csv.reader(file)
        for row in reader:
#            print(f"Чтение строки: {row}")
            if len(row) < 4:
                error_message = f"Пропуск строки из-за недостаточного количества данных: {row}\n"
                error_file.write(error_message)
                print(error_message.strip())
                continue
            product_name, quantity, price, date = map(str.strip, row)
            try:
                sales_data.append({
                    'product_name': product_name,
                    'quantity': int(quantity),
                    'price': float(price),
                    'date': datetime.strptime(date, '%Y-%m-%d')
                })
            except ValueError as e:
                error_message = f"Ошибка в строке {row}: {e}\n"
                error_file.write(error_message)
                print(error_message.strip())
                continue
    return sales_data

# Функция для расчета общей суммы продаж по каждому продукту
def total_sales_per_product(sales_data):
    total_sales = defaultdict(float)
    for sale in sales_data:
        total_sales[sale['product_name']] += sale['quantity'] * sale['price']
    return total_sales

# Функция для расчета общей суммы продаж по датам
def sales_over_time(sales_data):
    sales_by_date = defaultdict(float)
    for sale in sales_data:
        sales_by_date[sale['date']] += sale['quantity'] * sale['price']
    return dict(sorted(sales_by_date.items()))

# Чтение данных о продажах из файла
file_path = 'sales_data.csv'
error_file_path = 'sales_errors.log'
sales_data = read_sales_data(file_path, error_file_path)

# Расчет общей суммы продаж по каждому продукту
total_sales = total_sales_per_product(sales_data)

# Проверка на пустоту данных перед выводом
if total_sales:
    print("Общая сумма продаж по каждому продукту:")
    for product, total in total_sales.items():
        print(f"{product}: {total}")

    # Определение продукта с наибольшей выручкой
    max_product = max(total_sales, key=total_sales.get)
    print(f"\nПродукт с наибольшей выручкой: {max_product} ({total_sales[max_product]})")
else:
    print("Нет данных для вычисления максимального продукта.")

# Расчет общей суммы продаж по датам
sales_by_date = sales_over_time(sales_data)

# Проверка на пустоту данных перед выводом
if sales_by_date:
    print("\nОбщая сумма продаж по датам:")
    for date, total in sales_by_date.items():
        print(f"{date.strftime('%Y-%m-%d')}: {total}")

    # Определение дня с наибольшей суммой продаж
    max_date = max(sales_by_date, key=sales_by_date.get)
    print(f"День с наибольшей суммой продаж: {max_date.strftime('%Y-%m-%d')} ({sales_by_date[max_date]})")
else:
    print("Нет данных для вычисления сумм продаж по датам.")

# Построение графика общей суммы продаж по каждому продукту
if total_sales:
    plt.figure(figsize=(10, 5))
    plt.bar(total_sales.keys(), total_sales.values())
    plt.xlabel('Продукт')
    plt.ylabel('Общая сумма продаж')
    plt.title('Общая сумма продаж по каждому продукту')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Нет данных для построения графика продаж по продуктам.")

# Построение графика общей суммы продаж по датам
if sales_by_date:
    plt.figure(figsize=(10, 5))
    plt.plot(list(sales_by_date.keys()), list(sales_by_date.values()), marker='o')
    plt.xlabel('Дата')
    plt.ylabel('Общая сумма продаж')
    plt.title('Общая сумма продаж по датам')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Нет данных для построения графика продаж по датам.")

