# El impacto de las nuevas tecnologías en la sociedad: desarrollo y proyección de soluciones informáticas

---

## 📋 Información General
* **Nombre del Proyecto:** Sistema de Monitoreo Climático y Alertas Tempranas (AylluClima)
* **Asignatura:** Logica y programacion 
* **Institución:** Universidad Internacional del Ecuador (UIDE)
* **Fecha:** 26 de junio de 2026[cite: 3]
* **Integrantes:** 
  * VALLEJO TUQUERES JOSE GABRIEL[cite: 3]

---

# Objetivo del Sistema
Desarrollar una solución informática funcional en Python que procese y analice de manera repetitiva variables climáticas esenciales (temperatura y humedad), simulando la captura de datos de hardware (como un microcontrolador ESP32 con un sensor DHT11 y visualización local mediante cableado a una pantalla OLED)[cite: 3]. El sistema busca mitigar el impacto de cambios ambientales bruscos en comunidades agrícolas a través de la evaluación lógica de umbrales de riesgo y la emisión automatizada de alertas preventivas, minimizando la sobrecarga cognitiva de los usuarios finales[cite: 3].

---

# Descripción de Funcionalidades
1. **Simulación de Captura de Datos:** Generación iterativa de lecturas de temperatura (°C) y humedad (%) para representar el flujo continuo de un sensor físico[cite: 3].
2. **Estructuración y Almacenamiento Dinámico:** Organización de los registros históricos mediante estructuras de datos nativas como listas y diccionarios[cite: 3].
3. **Análisis Lógico de Riesgo:** Evaluación en tiempo real mediante operadores relacionales y condicionales para determinar si las lecturas sobrepasan los límites seguros[cite: 3].
4. **Sistema de Alertas Automatizado:** Clasificación del estado ambiental en tres niveles: *Normal*, *Advertencia* (por alta temperatura o sequedad ambiental) y *Crítico* (condiciones de helada o calor extremo)[cite: 3].
5. **Generación de Reportes Estadísticos:** Procesamiento del historial al finalizar el ciclo para calcular promedios, valores máximos y mínimos detectados[cite: 3].

---

## 🛠️ Herramientas de Desarrollo Utilizadas
* **Lenguaje:** Python 3.x[cite: 3]
* **Control de Versiones:** GitHub[cite: 3]
* **Metodología de Diseño:** Diagramas de flujo y casos de uso para la abstracción de la lógica del programa
* arduino uno
* ecp32
* sensor de humedad
* pantalla lcd
---

## 🗺️ Diagramas del Sistema

### 1. Diagrama de Funcionalidad (Casos de Uso)
Este diagrama describe cómo interactúan los actores del sistema (el entorno/hardware y el usuario) con la lógica interna del software.

```mermaid
graph TD
    Usuario((Usuario / Agricultor)) -->|Consulta Variables| Sistema[Sistema AylluClima]
    Hardware[(Sensor DHT11 / ESP32)] -->|Envía Datos Físicos| Sistema
    Sistema -->|Evalúa Lógica de Umbrales| Condicional{¿Supera Límites?}
    Condicional -->|Sí| Alerta[Disparar Alerta Crítica]
    Condicional -->|No| Normal[Registrar Estado Óptimo]
