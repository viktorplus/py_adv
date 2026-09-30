from pathlib import Path


BASE_DIR = Path(__file__)           # текущий файл
BASE_DIR2 = Path(__file__).parent   # родительская папка
new_path = BASE_DIR2 / "new_folder" # строим произвольный путь
print(BASE_DIR, BASE_DIR2, new_path) 