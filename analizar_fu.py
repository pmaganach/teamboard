# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
from collections import defaultdict

path = 'C:/Users/pablo.magana/Verisure/Customer Intelligence Chile - Documentos/00.Pablo/Fomento de Uso BI/Nuevo Flujo/Consolidado Campa\u00f1as FU.xlsx'
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
ws = wb['Consolidado']

# Contar registros por mes y campaña
data = defaultdict(lambda: defaultdict(int))
total_mes = defaultdict(int)

for row in ws.iter_rows(min_row=2, values_only=True):
    mes_raw, instalacion, campana = row[0], row[1], row[2]
    if not mes_raw or not campana:
        continue
    if hasattr(mes_raw, 'strftime'):
        mes = mes_raw.strftime('%Y-%m')
    else:
        mes = str(mes_raw)[:7]
    data[mes][campana] += 1
    total_mes[mes] += 1

# Imprimir tabla
print(f"{'Mes':<10} {'Campaña':<25} {'Q':>6} {'%':>7}")
print("-" * 52)
for mes in sorted(data.keys()):
    total = total_mes[mes]
    for campana, q in sorted(data[mes].items(), key=lambda x: -x[1]):
        pct = q / total * 100
        print(f"{mes:<10} {campana:<25} {q:>6} {pct:>6.1f}%")
    print(f"{'':10} {'TOTAL':<25} {total:>6} {'100.0%':>7}")
    print()
