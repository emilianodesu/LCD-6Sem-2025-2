# Sección 2

Se eligió el eje de (**Salud**)

## 2.1 Selección de framwork

### **Six Sigma**

Six sigma utiliza herramientas estadísticas para la caracterización y el estudio de los procesos, de ahí el nombre de la herramienta, ya que sigma es la desviación típica que da una idea de la variabilidad en un proceso, y el objetivo de la metodología six sigma es reducir esta, de modo que el proceso se encuentre siempre dentro de los límites establecidos.

Six Sigma se centra en la reducción de defectos y mejora continua a través de la metodología DMAIC (Por sus siglas en inglés: *Define - Measure - Analyze - Improve - Control*).

* **Definir**: En el sector salud, es crucial definir claramente qué se considera "datos de calidad". Esto incluye identificar los requisitos de los stakeholders (médicos, enfermeras, administradores, pacientes) y establecer métricas de calidad específicas, como la precisión de los diagnósticos, la completitud de los historiales médicos o la consistencia en los registros de medicamentos.
* **Medir**: Medir la calidad de los datos es esencial en salud porque los errores pueden tener consecuencias graves, como diagnósticos incorrectos o tratamientos inadecuados. Se deben utilizar métricas como:
  * Precisión: ¿Los datos reflejan la realidad del paciente?
  * Consistencia: ¿Los datos son coherentes entre diferentes sistemas (historial clínico, farmacia, laboratorio)?
  * Completitud: ¿Faltan datos críticos en los registros médicos?
  * Oportunidad: ¿Los datos están disponibles y actualizados en tiempo real?
* **Analizar**: En salud, es fundamental identificar las causas raíz de los problemas de calidad de los datos, ya que estos pueden estar relacionados con procesos manuales, falta de capacitación del personal, integración deficiente de sistemas o errores humanos.
* **Mejorar**: Las soluciones para mejorar la calidad de los datos en salud deben ser robustas y enfocadas en la seguridad del paciente. Esto puede incluir la automatización de procesos, la implementación de controles de calidad, la capacitación del personal y la actualización de sistemas de información.
* **Controlar**: En salud, es esencial mantener la calidad de los datos a largo plazo. Esto implica:
  * Monitoreo continuo de métricas de calidad.
  * Auditorías periódicas de los registros médicos.
  * Establecimiento de políticas y procedimientos claros para la gestión de datos.

Esta metodología, fundamentalmente, se aplica para establecer la uniformidad en los procesos, en mejorar y dar soluciones a problemas complejos por medio de herramientas de control y reducción de variaciones en los procesos de más alto desempeño, lo cual es esencial en el sector salud, donde la precisión y la oportunidad de los datos pueden impactar directamente en la vida de los pacientes. Además, Six Sigma permite monitorear y optimizar la calidad de los datos de manera estructurada.

Al aplicar Six Sigma en la gestión de datos en salud, se pueden minimizar errores en historiales médicos, mejorar la consistencia entre diferentes sistemas y asegurar que la información sea precisa y accesible cuando se necesite.

## 2.2 Ejes del modelo seleccionados

Dado que el sector salud es altamente regulado y sensible, consideraríamos todos los ejes de Six Sigma, pero con diferentes niveles de prioridad según las cuatro dimensiones clave de calidad de datos (*Accuracy, Timeliness, Consistency, Completeness*).

| **DIMENSION**  | **Prioridad** | **Justificación** |
|----------------|--------------|-------------------|
| **Precisión (Accuracy)** | **Muy alta** | Un dato inexacto (por ejemplo, una dosis incorrecta de medicamento o un diagnóstico erróneo) puede poner en riesgo la vida de los pacientes. Es fundamental garantizar que los datos sean correctos y estén validados con estándares médicos. |
| **Consistencia (Consistency)** | **Alta** | Los registros médicos pueden provenir de múltiples fuentes (hospitales, laboratorios, farmacias). Asegurar que no haya discrepancias entre bases de datos es clave para evitar errores en tratamientos y diagnósticos. |
| **Completitud (Completeness)** | **Media-Alta** | Un expediente clínico incompleto puede afectar la calidad del tratamiento. Es importante asegurar que los datos esenciales estén siempre registrados, aunque se pueden tolerar ciertas ausencias en información menos crítica. |
| **Oportunidad (Timeliness)** | **Muy alta** | En emergencias médicas, el acceso inmediato a datos precisos puede ser la diferencia entre la vida y la muerte. Es crucial minimizar los retrasos en la disponibilidad de información. |

Se priorizaría mayormente la Precisión y la Oportunidad, ya que los errores en datos clínicos pueden ser fatales si no se detectan a tiempo.
De igual manera, la Consistencia y la Completitud son fundamentales para garantizar que los datos sean útiles y confiables en el largo plazo, especialmente en el sector salud, donde la continuidad de la atención y el seguimiento de los pacientes son críticos.

## 2.3 Modelo de clasificación para evaluar la calidad de datos

Para evaluar la calidad de los datos en el sector salud bajo el enfoque Six Sigma, proponemos el siguiente modelo de clasificación:

### **Ponderación de Dimensiones en el Ranking**

| **Dimensión**       | **Peso (%)** | **Justificación** |
|---------------------|-------------|-------------------|
| **Precisión (Accuracy)** | **40%**  | Un error en los datos médicos puede ser mortal. La exactitud en diagnósticos, tratamientos y medicamentos es prioritaria. |
| **Oportunidad (Timeliness)** | **30%**  | En emergencias, los datos deben estar disponibles de inmediato. Un retraso puede afectar decisiones críticas. |
| **Consistencia (Consistency)** | **20%**  | Evitar discrepancias entre registros es clave para garantizar tratamientos adecuados y continuidad del cuidado. |
| **Completitud (Completeness)** | **10%**  | Aunque es importante, se pueden manejar ciertos datos faltantes sin afectar directamente la seguridad del paciente. |

Dado que en el sector salud la precisión y la oportunidad son críticas, estas dimensiones tendrán un mayor peso en la evaluación. La consistencia es fundamental para evitar errores en tratamientos y diagnósticos, mientras que la completitud, aunque importante, puede ser menos crítica en ciertos contextos.

### **Métricas Específicas por Dimensión**  

#### **1. Precisión (Accuracy)**

| **Métrica** | **Fórmula** | **Escala de Puntuación (0-10)** |
|------------|-----------|-------------------------------|
| **Porcentaje de coincidencia con fuentes confiables** | \( \frac{\text{Registros correctos}}{\text{Total de registros evaluados}} \times 100 \) | \( 10 \times \frac{\text{Coincidencia (\%)}}{100} \) |
| **Error medio absoluto (MAE) en datos numéricos** | \( \frac{1}{n} \sum_{i=1}^{n} \) &#124; \( X_i - X_{\text{real}} \) &#124; | \( 10 - \left( \frac{\text{MAE}}{\text{Máximo permitido}} \times 10 \right) \) |
| **Porcentaje de valores fuera de rango** | \( \frac{\text{Valores fuera de rango}}{\text{Total de valores}} \times 100 \) | \( 10 - (10 \times \frac{\text{Valores fuera de rango (\%)}}{100}) \) |

#### **2. Consistencia (Consistency)**

| **Métrica** | **Fórmula** | **Escala de Puntuación (0-10)** |
|------------|-----------|-------------------------------|
| **Desviación estándar de valores en distintas bases de datos** | \( \sigma = \sqrt{\frac{\sum (X_i - \bar{X})^2}{n}} \) | \( 10 - \left( \frac{\sigma}{\text{Máximo permitido}} \times 10 \right) \) |
| **Porcentaje de discrepancia entre sistemas** | \( \frac{\text{Registros inconsistentes}}{\text{Total de registros}} \times 100 \) | \( 10 - (10 \times \frac{\text{Discrepancias (\%)}}{100}) \) |

#### **3. Completitud (Completeness)**

| **Métrica** | **Fórmula** | **Escala de Puntuación (0-10)** |
|------------|-----------|-------------------------------|
| **Porcentaje de registros con campos obligatorios llenos** | \( \frac{\text{Registros completos}}{\text{Total de registros}} \times 100 \) | \( 10 \times \frac{\text{Completitud (\%)}}{100} \) |
| **Tasa de defectos por datos incompletos** | \( \frac{\text{Total de defectos}}{\text{Total de oportunidades}} \times 10^6 \) | \( 10 - \left( \frac{\text{DPMO}}{\text{Máximo permitido}} \times 10 \right) \) |

#### **4. Oportunidad (Timeliness)**

| **Métrica** | **Fórmula** | **Escala de Puntuación (0-10)** |
|------------|-----------|-------------------------------|
| **Tiempo medio de actualización de datos** | Promedio de tiempo entre evento y actualización (en minutos, horas o días). | \( 10 - \left( \frac{\text{Tiempo medio de actualización}}{\text{Límite permitido}} \times 10 \right) \) |
| **Porcentaje de datos retrasados** | \( \frac{\text{Registros con retraso}}{\text{Total de registros}} \times 100 \) | \( 10 - (10 \times \frac{\text{Registros retrasados (\%)}}{100}) \) |

### **Escala de Evaluación**

Cada dimensión se evaluará en una escala de **0 a 10 puntos** y se multiplicará por su peso para obtener un puntaje final de **0 a 10** para el dataset.

La puntuación final es:  

\[
\text{Puntaje Final} = (P_{\text{Precisión}} \times 0.4) + (P_{\text{Oportunidad}} \times 0.3) + (P_{\text{Consistencia}} \times 0.2) + (P_{\text{Completitud}} \times 0.1)
\]

| **Puntaje (0-10)** | **Clasificación** | **Interpretación** |
|--------------------|------------------|--------------------|
| **9.0 - 10**  | **Óptima** | Datos de alta calidad, confiables y listos para su uso clínico. |
| **7.0 - 8.9**  | **Buena** | Datos con pequeños errores o retrasos, pero sin impacto crítico en la atención médica. |
| **5.0 - 6.9**  | **Regular** | Datos con inconsistencias o faltantes que pueden afectar la toma de decisiones. |
| **3.0 - 4.9**  | **Deficiente** | Datos con errores frecuentes, incompletos o no disponibles a tiempo. |
| **0 - 2.9**  | **Crítica** | Datos inservibles para la atención médica. Urge intervención. |

### **Ejemplo de Evaluación de un Dataset Médico**

Supongamos que evaluamos un dataset de historias clínicas electrónicas en un hospital.  

| **Dimensión**  | **Puntaje (0-10)** | **Peso (%)** | **Puntaje Ponderado** |
|---------------|------------------|------------|-----------------|
| **Precisión** | **9.5**  | 40% | **3.8** |
| **Oportunidad** | **8.0**  | 30% | **2.4** |
| **Consistencia** | **7.5**  | 20% | **1.5** |
| **Completitud** | **6.0**  | 10% | **0.6** |
| **Total** | **8.3**  | 100% | **8.3** |

**Clasificación: "Buena" (7.0 - 8.9) → Datos adecuados pero con margen de mejora.**

## 2.4 Mitigación de problemas

### **Problemas Identificados y Acciones de Mejora**  

| **Dimensión**  | **Problema Detectado** | **Acciones Correctivas** | **Acciones Preventivas** |
|----------------|----------------------|------------------------|------------------------|
| **Precisión (Accuracy)** | Datos incorrectos en diagnósticos, dosis de medicamentos o antecedentes médicos. | 🔹 Implementar validaciones automáticas de datos con reglas médicas predefinidas.  🔹 Realizar auditorías periódicas con muestreo aleatorio para corregir datos erróneos. | 🔹 Integrar un sistema de validación en tiempo real que compare datos ingresados con fuentes confiables (ej. terminologías médicas estándar como SNOMED-CT). 🔹 Capacitación continua al personal en la captura de datos clínicos. |
| **Consistencia (Consistency)** | Discrepancias en los datos de un mismo paciente en distintos sistemas (ej. hospital, laboratorio, farmacia). | 🔹 Desarrollar procesos de conciliación automática entre bases de datos. 🔹 Implementar un ETL para limpieza y consolidación de datos. | 🔹 Uso de identificadores únicos para pacientes (ej. número de expediente centralizado). 🔹 Establecer estándares de interoperabilidad con proveedores externos. |
| **Completitud (Completeness)** | Expedientes clínicos con datos faltantes (ej. alergias, antecedentes familiares). | 🔹 Alertas automáticas cuando se detectan campos críticos vacíos. 🔹 Diseño de formularios electrónicos obligatorios en el sistema de historia clínica. | 🔹 Políticas de captura obligatoria para campos esenciales. 🔹 Capacitación del personal sobre la importancia de completar los datos. |
| **Oportunidad (Timeliness)** | Datos desactualizados o retraso en la actualización de resultados médicos. | 🔹 Implementar procesos de actualización automatizada desde sistemas de laboratorio y farmacia. 🔹 Definir Acuerdos de Nivel de Servicio para tiempos máximos de actualización. | 🔹 Sistemas en la nube con acceso en tiempo real a datos clínicos. 🔹 Sensores IoT para monitoreo continuo de signos vitales y actualización inmediata. |

### **Evaluación Continua: Dashboard de Calidad de Datos**

Para monitorear la mejora en la calidad de datos, se puede implementar un dashboard con indicadores de desempeño, tales como:  
**Precisión:** % de registros sin errores vs. total de registros.  
**Consistencia:** % de discrepancias detectadas en bases de datos.  
**Completitud:** % de expedientes con campos obligatorios llenos.  
**Oportunidad:** Tiempo promedio de actualización de datos críticos.
