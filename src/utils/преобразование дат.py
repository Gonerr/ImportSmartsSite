import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def convert_excel_dates_to_bitrix(input_file, output_file=None):
    """
    Преобразовать даты в существующем Excel файле
    
    Args:
        input_file: путь к исходному файлу
        output_file: путь для сохранения (если None, перезапишет исходный)
    """
    if output_file is None:
        output_file = input_file
    
    # Читаем Excel
    df = pd.read_excel(input_file)
    
    print(f"Колонки в файле: {list(df.columns)}")
    
    # Находим колонку с датой
    date_columns = []
    for col in df.columns:
        if any(keyword in str(col).lower() for keyword in ['дата', 'date', 'ци', 'пуз', 'пк']):
            date_columns.append(col)
    
    if not date_columns:
        print("Не найдены колонки с датами!")
        return
    
    print(f"Найдены колонки с датами: {date_columns}")
    
    def convert_date(date_val):
        """Преобразовать дату в Bitrix формат"""
        if pd.isna(date_val):
            return None
        
        # Если уже datetime
        if isinstance(date_val, (datetime, pd.Timestamp)):
            return date_val.strftime('%Y-%m-%dT%H:%M:%S') + '+03:00'
        
        # Если строка
        if isinstance(date_val, str):
            # Убираем лишние пробелы
            date_str = date_val.strip()
            
            # Если уже в формате Bitrix
            if 'T' in date_str and '+' in date_str:
                return date_str
            
            # Пробуем разные форматы
            formats = [
                '%d.%m.%y %H:%M',      # 17.01.23 0:00
                '%d.%m.%Y %H:%M',      # 17.01.2023 0:00
                '%d.%m.%y',           # 17.01.23
                '%d.%m.%Y',           # 17.01.2023
                '%Y-%m-%d %H:%M:%S',  # 2023-01-17 00:00:00
                '%d/%m/%y %H:%M',     # 17/01/23 0:00
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y-%m-%dT%H:%M:%S') + '+03:00'
                except ValueError:
                    continue
        
        return date_val
    
    # Преобразуем каждую колонку с датами
    for col in date_columns:
        print(f"\nПреобразование колонки '{col}'...")
        df[col] = df[col].apply(convert_date)
        
        # Показываем примеры
        print("Примеры преобразований:")
        for i, val in enumerate(df[col].head(5).tolist()):
            print(f"  Строка {i+1}: {val}")
    
    # Сохраняем результат
    df.to_excel(output_file, index=False)
    print(f"\nФайл сохранен: {output_file}")
    return df

# Использование
input_file = "2023_февраль_январь_на загрузку.xlsx"
convert_excel_dates_to_bitrix(input_file, "файл_с_конвертированными_датами.xlsx")