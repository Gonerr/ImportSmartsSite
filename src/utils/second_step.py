import random
import re
import time
import pandas as pd
import os 

import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

file_path = "Result_1.xlsx"
# # Загружаем данные
# df = pd.read_excel("input.xlsx")

# # Посмотреть реальные названия колонок
# print(df.columns.tolist())

# # Находим колонку обучения ("ЦИ/ПУЗ/ПК")
# ci_col = [c for c in df.columns if "ЦИ" in c][0]
# print("Столбец обучения:", ci_col)

# # 1️⃣ Заполняем пропуски в названии компании
# df["Название организации"] = df["Название организации"].ffill()

# # 2️⃣ Преобразуем даты в нужный формат для столбца "Дата прохождения ЦИ"
# def convert_date_to_bitrix_format(date_val):
#     """Преобразовать дату в Bitrix формат (YYYY-MM-DDTHH:MM:SS+03:00)"""
#     if pd.isna(date_val):
#         return None
    
#     # Если уже datetime
#     if isinstance(date_val, (datetime, pd.Timestamp)):
#         return date_val.strftime('%Y-%m-%dT%H:%M:%S') + '+03:00'
    
#     # Если строка
#     if isinstance(date_val, str):
#         date_str = date_val.strip()
        
#         # Если уже в формате Bitrix
#         if 'T' in date_str and '+' in date_str:
#             return date_str
        
#         # Пробуем разные форматы
#         formats = [
#             '%d.%m.%y %H:%M',      # 17.01.23 0:00
#             '%d.%m.%Y %H:%M',      # 17.01.2023 0:00
#             '%d.%m.%y',           # 17.01.23
#             '%d.%m.%Y',           # 17.01.2023
#             '%Y-%m-%d %H:%M:%S',  # 2023-01-17 00:00:00
#             '%d/%m/%y %H:%M',     # 17/01/23 0:00
#         ]
        
#         for fmt in formats:
#             try:
#                 dt = datetime.strptime(date_str, fmt)
#                 return dt.strftime('%Y-%m-%dT%H:%M:%S') + '+03:00'
#             except ValueError:
#                 continue
    
#     # Если формат не распознан, возвращаем None
#     return None

# # Фиксируем общую дату прохождения обучения
# common_date_str = "2023-06-27"
# common_date = pd.Timestamp(common_date_str)

# # Преобразуем общую дату в Bitrix формат
# bitrix_common_date = convert_date_to_bitrix_format(common_date)

# # Проверяем, есть ли в данных колонка с датами
# date_columns = [c for c in df.columns if any(keyword in str(c).lower() 
#                 for keyword in ['дата', 'date', 'ци', 'пуз', 'пк'])]

# if date_columns:
#     print(f"Найдены колонки с датами: {date_columns}")
#     # Используем первую найденную колонку с датой
#     date_col = date_columns[0]
#     print(f"Используем колонку '{date_col}' для получения дат")
    
#     # Преобразуем даты в этой колонке
#     df["Дата прохождения ЦИ"] = df[date_col].apply(convert_date_to_bitrix_format)
    
#     # Для строк, где дата не найдена, используем общую дату
#     df["Дата прохождения ЦИ"] = df["Дата прохождения ЦИ"].fillna(bitrix_common_date)
# else:
#     print("Колонки с датами не найдены, используем общую дату")
#     df["Дата прохождения ЦИ"] = bitrix_common_date

# print("\nПримеры дат в столбце 'Дата прохождения ЦИ':")
# for i, val in enumerate(df["Дата прохождения ЦИ"].head(5).tolist()):
#     print(f"  Строка {i+1}: {val}")

# # Для комментария используем стандартный формат даты
# date_str = common_date.strftime("%d.%m.%Y")

# # 3️⃣ Извлекаем фамилию менеджера
# df["Менеджер (фамилия)"] = df["Менеджер"].astype(str).str.split().str[0]

# # 4️⃣ Создаём поле "Комментарий участника"
# def make_person_comment(row):
#     fio = str(row["Участник ЦИ (сертификат )"]).strip()
#     email = str(row["E-mail"]).strip()
#     ci_type = str(row[ci_col]).strip()

#     return f"{fio} ({email}) {ci_type}"

# df["Коммент_участника"] = df.apply(make_person_comment, axis=1)

# # 5️⃣ Группируем по компании
# grouped = df.groupby("Название организации")

# records = []

# for company, group in grouped:
#     # список участников
#     participants = ", ".join(group["Коммент_участника"].tolist())
    
#     # берём ИНН из первой строки (предполагаем, что в группе ИНН одинаковый)
#     inn = str(group["ИНН"].iloc[0]) if "ИНН" in group.columns else ""
    
#     # собираем все email участников
#     emails = ", ".join(group["E-mail"].astype(str).str.strip().tolist())
    
#     # берём фамилию менеджера из первой строки
#     manager = group["Менеджер (фамилия)"].iloc[0]
    
#     # берем дату из первой строки группы (или общую дату)
#     # Если все даты в группе одинаковые, можно использовать первую
#     group_date = group["Дата прохождения ЦИ"].iloc[0]

#     # итоговая строка
#     records.append({
#         "Название организации": company,
#         "ИНН": inn,
#         "E-mail": emails,  # Все email участников
#         "Комментарий": participants,
#         "Дата прохождения ЦИ": group_date,  # Используем преобразованную дату
#         "Менеджер (фамилия)": manager
#     })

# # 6️⃣ Сохраняем результат
# result = pd.DataFrame(records)
# new_data = result
# new_data = new_data[["Название организации", "ИНН", "E-mail", 
#                          "Дата прохождения ЦИ", "Менеджер (фамилия)", "Комментарий"]]
#

# # Проверяем, существует ли файл
# if os.path.exists(file_path):
#     # Читаем существующие данные
#     existing_data = pd.read_excel(file_path)
    
#     # Объединяем старые и новые данные
#     # Вариант 1: Простое объединение (могут быть дубли)
#     result = pd.concat([existing_data, result], ignore_index=True)
    
#     # Вариант 2: Удаление дубликатов по ключевым полям
#     # result = pd.concat([existing_data, result], ignore_index=True)
#     # result = result.drop_duplicates(subset=["ИНН", "Дата прохождения ЦИ"])
    
#     # Вариант 3: Только новые записи (анти-джоин)
#     # mask = ~result[["ИНН", "Дата прохождения ЦИ"]].apply(tuple, 1).isin(
#     #     existing_data[["ИНН", "Дата прохождения ЦИ"]].apply(tuple, 1)
#     # )
#     # new_records = result[mask]
#     # result = pd.concat([existing_data, new_records], ignore_index=True)
# else:
#     # Если файла нет, используем текущий result
#     pass

# # Сохраняем объединенный результат
# result.to_excel(file_path, index=False)

# print("\n" + "="*50)
# print("Структура результата:")
# print(result.columns.tolist())
# print("\nПервые 5 строк:")
# print(result.head())

# print("\nРазмер результата:", result.shape)
# print("Уникальные даты в результате:", result["Дата прохождения ЦИ"].unique()[:5])


from fast_bitrix24 import Bitrix
webhook  = "https://acceptgroup.bitrix24.ru/rest/116/c1o0f03s3eluvrmo/"
wh = Bitrix(webhook)

result = pd.read_excel(file_path) 
def get_company_data_by_filter(wh, filter_field: str, value, INN, email):
    """
    Поиск данных о компании:
    1) По названию (TITLE)
    2) Если ИП и не найдено — по фамилии предпринимателя
    """

    original_value = value

    # ---------- ШАГ 2: Если ИП, пробуем искать по фамилии ----------
    # примеры: "ИП Морозова Н. В.", "ИП Честнова В.В."
    if INN and INN != '+':
        try:
            # Добавляем случайную задержку 1-3 секунды
            time.sleep(random.uniform(1, 3))
            
            result = wh.get_all(
                'crm.company.list',
                params={'filter': {
                    "UF_CRM_1756806096642":INN},
                    'limit': 1}
            )
            
            if result:
                return result 
            
        except Exception as e:
            print(f"Ошибка для ИНН {INN}: {e}")
            # Дополнительная пауза при ошибке
            time.sleep(5)
        
        return None
        

    # ---------- ШАГ 1: Поиск по названию ----------
    if filter_field == "TITLE":
        value = re.sub(r"\s+", " ", value.strip())
        filter_field_bx = f"?{filter_field}"
    else:
        filter_field_bx = filter_field

    companies = wh.get_all(
        'crm.company.list',
        params={'filter': {filter_field_bx: value}}
    )

    if companies:
        return companies  # нашли — возвращаем


    if isinstance(original_value, str) and original_value.strip().lower().startswith("ип") and email:
        parts = original_value.strip().split()
        last_name = None  # Инициализируем переменную
        
        if len(parts) >= 2:
            last_name = parts[1]  # фамилия
        
        # Проверяем, что last_name определена
        if last_name:
            # пробуем искать по фамилии
            companies = wh.get_all(
                'crm.company.list',
                params={'filter': {
                    "?TITLE": last_name,
                    "EMAIL": email}}
            )
            
            if companies:
                return companies

    # ---------- Ничего не найдено ----------
    return None


# 1️⃣ Добавляем пустую колонку
result["CompanyID"] = None

# 2️⃣ Наполняем её ID компаний
for i, row in result.iterrows():
    title = row["Название организации"]
    INN = row["ИНН"]
    email = row["E-mail"]
    companies = get_company_data_by_filter(wh, "TITLE", title, INN, email)

    if companies:
        # берём первую найденную компанию
        result.at[i, "CompanyID"] = companies[0]["ID"]
    else:
        result.at[i, "CompanyID"] = None  # или "NOT FOUND"

# 3️⃣ Сохраняем обновлённый файл
result.to_excel("result_with_id1.xlsx", index=False)

print("Готово! Колонка CompanyID добавлена.")

