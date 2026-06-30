# Estación Meteorológica Inteligente con ESP32 e Internet 🌦️🤖

Este proyecto consiste en un dispositivo embebido portátil montado sobre una protoboard utilizando el microcontrolador **ESP32**. El sistema funciona de forma dual: actúa como un monitor climático en tiempo real y, al conectarse a Internet, se transforma en un reloj digital sincronizado. Además, cuenta con un analizador de espectro Wi-Fi integrado.

## 🚀 Características Principales
* **Monitor de Clima:** Mide temperatura ambiental y humedad relativa usando el sensor DHT11.
* **Sensor Lumínico:** Utiliza una fotoresistencia (LDR) para clasificar el entorno en *Soleado*, *Nublado* u *Oscuro*.
* **Alertas Físicas:** Cuenta con respuestas sonoras (Buzzer) y lumínicas (LED) que reaccionan inmediatamente a los cambios del clima.
* **Modo Alerta Crítica:** Si se detecta oscuridad total, la pantalla OLED entra en un modo intermitente de advertencia visual y sonora.
* **Sincronización NTP:** Conexión inalámbrica a Internet para obtener la hora exacta local (configurado para Ecuador UTC-5).
* **Escáner Wi-Fi Portátil:** Mediante la pulsación de un botón físico, el sistema interrumpe el bucle normal para rastrear las redes Wi-Fi cercanas mostrando su SSID y potencia de señal (RSSI en dB).

## 🛠️ Hardware Utilizado
* Microcontrolador **ESP32** (NodeMCU / DevKit v1)
* Pantalla **OLED SSD1306** i2C (128x64)
* Sensor de Temperatura y Humedad **DHT11**
* Módulo Sensor de Luz **LDR**
* Diodo **LED** de 5mm
* **Zumbador (Buzzer)** Activo
* **Pulsador** (Botón táctil de 4 pines)
* Protoboard y cables de conexión jumper

## ⚙️ Conexión de Pines (Pinout)
* **OLED:** SDA ➡️ GPIO 21 | SCL ➡️ GPIO 22
* **DHT11 Data:** ➡️ GPIO 23
* **Sensor LDR Analógico:** ➡️ GPIO 34
* **Buzzer (+):** ➡️ GPIO 18
* **LED (+):** ➡️ GPIO 19
* **Botón Pulsador:** ➡️ GPIO 4 (Configurado con INPUT_PULLUP interno)

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
