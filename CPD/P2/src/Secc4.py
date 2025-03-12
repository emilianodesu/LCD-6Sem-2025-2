from Secc3 import bad_dataset, calculate_and_display_accuracy, calculate_and_display_completeness, calculate_and_display_consistency, calculate_and_display_opportunity,original_dataset
import pandas as pd
def calculate_and_display_accessibility(bad_dataset):

    # Evaluar si las columnas tienen nombres significativos
    meaningful_columns = sum([1 for col in bad_dataset.columns if len(col) > 1])
    columns_percent = round((meaningful_columns / len(bad_dataset.columns)) * 100, 2)
    
    # Evaluar si el dataset tiene un índice significativo (nombre de índice no numérico)
    meaningful_index = not bad_dataset.index.to_series().apply(lambda x: isinstance(x, (int, float))).all()
    index_percent = 100 if meaningful_index else 0
    
    # Evaluar si los datos son legibles (sin valores especiales o basura)
    legible_data = bad_dataset.map(lambda x: isinstance(x, (int, float, str)) and x not in ['N/A', 'NaN', 'null', '']).sum().sum()
    total_elements = bad_dataset.size
    data_legibility_percent = round((legible_data / total_elements) * 100, 2)
    
    # Calcular accesibilidad promedio en una escala de 0 a 100
    accessibility_score_percent = round((columns_percent + index_percent + data_legibility_percent) / 3, 2)
    
    # Convertir accesibilidad promedio a una escala de 0 a 10
    accessibility_score = round((accessibility_score_percent / 100) * 10, 2)
    
    # Mostrar resultados
    print('Accessibility Calculation', accessibility_score)
    print('Accesibilidad de las Columnas')
    print(pd.DataFrame({'Columnas Significativas (%)': [columns_percent]}))
    print('Accesibilidad del Índice')
    print(pd.DataFrame({'Índice Significativo (%)': [index_percent]}))
    print('Legibilidad de los Datos')
    print(pd.DataFrame({'Datos Legibles (%)': [data_legibility_percent]}))
    
    return accessibility_score


cal_accuracy = calculate_and_display_accuracy(bad_dataset, original_dataset)
print("_______________________________________________________\n\n")
cal_consistency = calculate_and_display_consistency(bad_dataset)
print("_______________________________________________________\n\n")

cal_completeness = calculate_and_display_completeness(bad_dataset)
print("_______________________________________________________\n\n")

cal_opportunity = calculate_and_display_opportunity(bad_dataset)
print("_______________________________________________________\n\n")
cal_accesi = calculate_and_display_accessibility(bad_dataset)
print("_______________________________________________________\n\n")
calificacion_final = round((
    0.4*cal_accuracy + \
    0.2*cal_consistency + \
    0.1*cal_completeness + \
    0.2*cal_opportunity + \
    0.1*cal_accesi), 2)
print('Calificación Final', calificacion_final)