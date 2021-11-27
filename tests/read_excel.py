from openpyxl import load_workbook
from pathlib import Path
from rich import print

if __name__ == '__main__':
    wb = load_workbook('data/inventory.xlsx')
    en = wb['EN']
    for row in en.rows:
        record = ''.join([str(cell.value) for cell in row if cell.value])
        print(record)