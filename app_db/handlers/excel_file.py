from datetime import datetime
import os
import pandas as pd
import openpyxl
import tempfile

from app_frontend.handlers.rock_sample.core_analysis import CoreAnalysis


OUTPUT_DIR = 'app_db/excel_calculation'


def list_to_string(lst):
    """Преобразует список в строку, разделяя элементы запятой."""
    return ', '.join(str(item) for item in lst)


class ExcelProcessor:
    """Класс для работы с Excel файлами."""

    def __init__(self):
        """Инициализация экземпляра ExcelProcessor."""
        self.request = None
        self.workbook = None
        self.dataframe = None

    def is_excel_extension(self, filename: str) -> bool:
        """Проверяет, является ли файл файлом Excel."""
        return filename.lower().endswith(('.xlsx', '.xls'))

    def read_excel_file(self, content: bytes) -> bool:
        """Читает содержимое Excel файла и загружает его в DataFrame."""
        temp_file_path = self._create_temporary_file(content)
        try:
            self.workbook = openpyxl.load_workbook(temp_file_path, data_only=True)
            self.dataframe = self._convert_to_dataframe()
            return True
        finally:
            self._remove_temporary_file(temp_file_path)

    def _convert_to_dataframe(self):
        """Преобразует данные из Excel в DataFrame."""
        sheet = self.workbook.active
        data = sheet.values
        columns = next(data)  # Первая строка содержит заголовки столбцов

        # Проверка наличия заголовка
        if not columns or all(cell is None for cell in columns):
            raise ValueError("Таблица не содержит заголовков.")

        # Создание DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Проверка наличия столбца 'description'
        if 'description' not in df.columns:
            raise ValueError("Отсутствует обязательный столбец 'description'.")

        # Проверка наличия данных в столбце 'description'
        if df['description'].empty or df['description'].isna().all():
            raise ValueError("Столбец 'description' пуст.")

        # Добавление недостающих столбцов
        for column in ['lithotype', 'color', 'features', 'structure']:
            if column not in df.columns:
                df[column] = None

        return df

    def _create_temporary_file(self, content: bytes) -> str:
        """Создает временный файл для чтения Excel файла."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(content)
            return tmp.name

    def _remove_temporary_file(self, file_path: str):
        """Удаляет временный файл."""
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Временный файл успешно удален - {file_path}")

    def save_dataframe_to_excel(self, filename: str, dataframe=None):
        """Сохраняет DataFrame в файл Excel."""
        # Если dataframe не передан, используем self.dataframe
        df_to_save = dataframe if dataframe is not None else self.dataframe

        if df_to_save is None:
            raise ValueError("DataFrame пустой или не инициализирован.")

        # Убедитесь, что путь к папке существует
        output_dir = OUTPUT_DIR
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, filename)

        # Сохранение DataFrame в файл Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df_to_save.to_excel(writer, index=False)

        print(f"Файл успешно сохранен: {file_path}")

    def process_descriptions(self, request):
        """Обрабатывает описания и обновляет DataFrame."""
        self.request = request
        for index, row in self.dataframe.iterrows():
            description = row['description']

            # Проверяем, что значение description не равно None и можно преобразовать в строку
            if description is not None:
                try:
                    description_str = str(description)
                    lithotype, color, features, structure = self.analyze_description(description_str)

                    self.dataframe.at[index, 'lithotype'] = lithotype
                    self.dataframe.at[index, 'color'] = color
                    self.dataframe.at[index, 'features'] = features
                    self.dataframe.at[index, 'structure'] = structure
                except Exception as e:
                    print(f"Невозможно преобразовать описание в строку: {description}, Ошибка: {e}")
                    pass
            else:
                print(f"Пропускаем пустое описание: {index} - {description}")
                pass
        return True

    def analyze_description(self, description: str):
        lithotype = ''
        color = []
        features = []
        structure = []

        analysis = CoreAnalysis(self.request)
        result = analysis.run_excel_file(description)

        if isinstance(result, dict):
            lithotype = result.get('lithotype', '')
            color = result.get('color', [])
            features = result.get('features', [])
            structure = result.get('structure', [])

        # Преобразование списков в строки для Excel
        color_str = list_to_string(color)
        features_str = list_to_string(features)
        structure_str = list_to_string(structure)

        return lithotype, color_str, features_str, structure_str

    def save_dataframe_to_excel(self, original_filename: str, dataframe=None):
        """Сохраняет DataFrame в файл Excel, создавая имя файла на основе исходного имени и текущей даты и времени."""
        df_to_save = dataframe if dataframe is not None else self.dataframe

        if df_to_save is None:
            raise ValueError("DataFrame пустой или не инициализирован.")

        # Форматирование текущей даты и времени для добавления к имени файла
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{os.path.splitext(original_filename)[0]}_{current_datetime}.xlsx"

        # Путь для сохранения файла
        output_dir = OUTPUT_DIR
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_path = os.path.join(output_dir, filename)

        # Сохранение DataFrame в файл Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df_to_save.to_excel(writer, index=False)
        print(f"Файл успешно сохранен: {file_path}")
        return True
