import openpyxl
from pathlib import Path

wb_obj = openpyxl.load_workbook('PRM.xlsx') 

# Read the active sheet:
sheet = wb_obj.active
for row in sheet.rows:
    for cell in row:
        print(cell.value)
        print('- - '*20)
