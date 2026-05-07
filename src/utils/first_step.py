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
df = pd.read_excel("first.xlsx")

print(df.columns.tolist())

ci_col = [c for c in df.columns if "ЦИ" in c][0]
print("Столбец обучения:", ci_col)

df["Название организации"] = df["Название организации"].ffill()

def convert_date_to_bitrix_format(date_val):
    """Преобразовать дату в Bitrix формат (YYYY-MM-DDTHH:MM:SS+03:00)"""
    if pd.isna(date_val):
        return None
    
    if isinstance(date_val, (datetime, pd.Timestamp)):
        return date_val.strftime('%Y-%m-%dT%H:%M:%S') + '+03:00'
    
    if isinstance(date_val, str):
        date_str = date_val.strip()
        
        if 'T' in date_str and '+' in date_str:
            return date_str
        
        # Пробуем разные форматы
        formats = [
            '%d.%m.%y %H:%M',     
            '%d.%m.%Y %H:%M',      
            '%d.%m.%y',           
            '%d.%m.%Y',           
            '%Y-%m-%d %H:%M:%S',  
            '%d/%m/%y %H:%M',     
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%dT%H:%M:%S') + '+03:00'
            except ValueError:
                continue
    
    return None

common_date_str = "2023-09-19"
common_date = pd.Timestamp(common_date_str)

bitrix_common_date = convert_date_to_bitrix_format(common_date)

date_columns = [c for c in df.columns if any(keyword in str(c).lower() 
                for keyword in ['дата', 'date', 'ци', 'пуз', 'пк'])]

if date_columns:
    print(f"Найдены колонки с датами: {date_columns}")
    date_col = date_columns[0]
    print(f"Используем колонку '{date_col}' для получения дат")
    
    df["Дата прохождения ЦИ"] = df[date_col].apply(convert_date_to_bitrix_format)
    
    df["Дата прохождения ЦИ"] = df["Дата прохождения ЦИ"].fillna(bitrix_common_date)
else:
    print("Колонки с датами не найдены, используем общую дату")
    df["Дата прохождения ЦИ"] = bitrix_common_date

print("\nПримеры дат в столбце 'Дата прохождения ЦИ':")
for i, val in enumerate(df["Дата прохождения ЦИ"].head(5).tolist()):
    print(f"  Строка {i+1}: {val}")

date_str = common_date.strftime("%d.%m.%Y")

df["Менеджер (фамилия)"] = df["Менеджер"].astype(str).str.split().str[0]

def make_person_comment(row):
    fio = str(row["Участник ЦИ (сертификат)"]).strip()
    email = str(row["E-mail"]).strip()
    ci_type = str(row[ci_col]).strip()

    return f"{fio} ({email}) {ci_type}"

df["Коммент_участника"] = df.apply(make_person_comment, axis=1)

grouped = df.groupby("Название организации")

records = []

for company, group in grouped:
    participants = ", ".join(group["Коммент_участника"].tolist())
    inn = str(group["ИНН"].iloc[0]) if "ИНН" in group.columns else ""
    
    valid_emails = []
    for email in group["E-mail"]:
        if pd.notna(email):  
            email_str = str(email).strip()
            if email_str and email_str != 'nan':  # Проверяем, не пустая ли строка
                valid_emails.append(email_str)

    emails = ", ".join(valid_emails)
    
    manager = group["Менеджер (фамилия)"].iloc[0]
    
    group_date = group["Дата прохождения ЦИ"].iloc[0]

    records.append({
        "Название организации": company,
        "ИНН": inn,
        "E-mail": emails, 
        "Комментарий": participants,
        "Дата прохождения ЦИ": group_date,  
        "Менеджер (фамилия)": manager
    })

result = pd.DataFrame(records)
new_data = result
new_data = new_data[["Название организации", "ИНН", "E-mail", 
                         "Дата прохождения ЦИ", "Менеджер (фамилия)", "Комментарий"]]


if os.path.exists(file_path):
    existing_data = pd.read_excel(file_path)
    
    # Объединяем старые и новые данные
    # Вариант 1: Простое объединение (могут быть дубли)
    result = pd.concat([existing_data, result], ignore_index=True)
    
    # Вариант 2: Удаление дубликатов по ключевым полям
    # result = pd.concat([existing_data, result], ignore_index=True)
    # result = result.drop_duplicates(subset=["ИНН", "Дата прохождения ЦИ"])
    
    # Вариант 3: Только новые записи (анти-джоин)
    # mask = ~result[["ИНН", "Дата прохождения ЦИ"]].apply(tuple, 1).isin(
    #     existing_data[["ИНН", "Дата прохождения ЦИ"]].apply(tuple, 1)
    # )
    # new_records = result[mask]
    # result = pd.concat([existing_data, new_records], ignore_index=True)
else:
    # Если файла нет, используем текущий result
    pass

# Сохраняем объединенный результат
result.to_excel(file_path, index=False)

print("\n" + "="*50)
print("Структура результата:")
print(result.columns.tolist())
print("\nПервые 5 строк:")
print(result.head())

print("\nРазмер результата:", result.shape)
print("Уникальные даты в результате:", result["Дата прохождения ЦИ"].unique()[:5])
