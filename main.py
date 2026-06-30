/**
 * Estación Meteorológica e Internet Portátil con ESP32
 * Desarrollado por: José Gabriel Vallejo Túqueres
 * * Características:
 * - Lectura de temperatura y humedad (DHT11)
 * - Monitoreo de luz ambiental (LDR) con alertas físicas (LED/Buzzer)
 * - Conexión Wi-Fi y Reloj Sincronizado por Internet (NTP)
 * - Escáner de redes Wi-Fi activado por botón físico
 * - Pantalla OLED i2C para visualización dinámica
 */

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <WiFi.h>
#include "time.h"

// --- CONFIGURACIÓN WI-FI (Marcadores de posición seguros para GitHub) ---
const char* ssid     = "TU_SSID_AQUI";  
const char* password = "TU_PASSWORD_AQUI"; 

// Servidor de hora de Internet (NTP) para Ecuador
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -18000; // UTC -5            
const int   daylightOffset_sec = 0;            

// Configuración de Pines de Hardware
#define DHTPIN 23       
#define DHTTYPE DHT11   
DHT dht(DHTPIN, DHTTYPE);

#define LDRPIN 34       
#define BUZZER_PIN 18   
#define LED_PIN 19      
#define BOTON_PIN 4     

// Configuración OLED
#define ANCHO_PANTALLA 128
#define ALTO_PANTALLA 64
Adafruit_SSD1306 display(ANCHO_PANTALLA, ALTO_PANTALLA, &Wire, -1);

String estadoAnterior = "";

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BOTON_PIN, INPUT_PULLUP);

  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_PIN, LOW);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("Error OLED"));
    while(1);
  }

  // Pantalla de Inicio
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(10, 20);
  display.print("ESTACION METEO v1.0");
  display.setCursor(10, 40);
  display.print("Iniciando...");
  display.display();
  delay(2000);
}

void loop() {
  // Verificación del Botón Escáner de Wi-Fi
  if (digitalRead(BOTON_PIN) == LOW) {
    ejecutarEscanerWiFi();
    return;
  }

  // Lectura del Sensor de Luz
  int valorLuz = analogRead(LDRPIN);
  String estadoActual = "";

  if (valorLuz < 1000) estadoActual = "Soleado";
  else if (valorLuz >= 1000 && valorLuz < 2800) estadoActual = "Nublado";
  else estadoActual = "Oscuro";

  // Alertas de cambios de estado
  if (estadoActual != estadoAnterior) {
    if (estadoActual == "Soleado") {
      digitalWrite(LED_PIN, HIGH);
      digitalWrite(BUZZER_PIN, HIGH); delay(100);
      digitalWrite(BUZZER_PIN, LOW);  delay(100);
      digitalWrite(BUZZER_PIN, HIGH); delay(100);
      digitalWrite(BUZZER_PIN, LOW);
    } 
    else if (estadoActual == "Nublado") {
      digitalWrite(LED_PIN, LOW);
      digitalWrite(BUZZER_PIN, HIGH); delay(600);
      digitalWrite(BUZZER_PIN, LOW);
    }
    estadoAnterior = estadoActual;
  }

  // Modo Alerta Crítica por Oscuridad
  if (estadoActual == "Oscuro") {
    digitalWrite(LED_PIN, LOW);
    for (int i = 0; i < 4; i++) {
      display.clearDisplay();
      display.invertDisplay(false); 
      display.setTextSize(2); display.setCursor(15, 15); display.print("¡ALERTA!");
      display.setTextSize(1); display.setCursor(15, 45); display.print("Detectada Oscuridad");
      display.display();
      
      digitalWrite(BUZZER_PIN, HIGH); delay(200);
      digitalWrite(BUZZER_PIN, LOW);
      
      display.invertDisplay(true);
      delay(200);
    }
    display.invertDisplay(false); 
    return; 
  }

  // --- BUCLE NORMAL DE PANTALLAS ---
  
  // PANTALLA 1: CLIMA
  float humedad = dht.readHumidity();
  float temperatura = dht.readTemperature();
  String textoLuz = (estadoActual == "Soleado") ? "Soleado / Luz" : "Nublado / Sombra";

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print("Ambiente: " + textoLuz);
  display.drawFastHLine(0, 11, 128, WHITE); 

  if (!isnan(humedad) && !isnan(temperatura)) {
    display.setTextSize(2);
    display.setCursor(5, 20);
    display.print("T: "); display.print(temperatura, 1); display.write(247); display.print("C");
    display.setCursor(5, 45);
    display.print("H: "); display.print(humedad, 0); display.print(" %");
  } else {
    display.setCursor(0, 30); display.print("Error Sensor DHT");
  }
  display.display();
  delay(4000); 

  // PANTALLA 2: RELOJ DE INTERNET (Si está conectado)
  if (WiFi.status() == WL_CONNECTED) {
    struct tm timeinfo;
    if (getLocalTime(&timeinfo)) {
      display.clearDisplay();
      display.setTextSize(1);
      display.setCursor(15, 0);
      display.print("RELOJ DE INTERNET");
      display.drawFastHLine(0, 11, 128, WHITE);

      char bufferHora[9];
      strftime(bufferHora, sizeof(bufferHora), "%H:%M:%S", &timeinfo);
      display.setTextSize(2); display.setCursor(15, 22); display.print(bufferHora);

      char bufferFecha[11];
      strftime(bufferFecha, sizeof(bufferFecha), "%d/%m/%Y", &timeinfo);
      display.setTextSize(1); display.setCursor(30, 48); display.print(bufferFecha);

      display.display();
      delay(4000); 
    }
  } else {
    // Intento automático de conexión de fondo si se pierde la señal
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
  }
}

// Función independiente para el Escáner de Redes
void ejecutarEscanerWiFi() {
  digitalWrite(BUZZER_PIN, HIGH); delay(50);
  digitalWrite(BUZZER_PIN, LOW);

  display.clearDisplay();
  display.setCursor(0, 20);
  display.setTextSize(1);
  display.print("Buscando redes\nWi-Fi...");
  display.display();

  int n = WiFi.scanNetworks();
  display.clearDisplay();
  
  if (n == 0) {
    display.setCursor(0, 20);
    display.print("No redes encontradas");
  } else {
    display.setCursor(0, 0);
    display.print("Redes encontradas: "); display.print(n);
    display.drawFastHLine(0, 9, 128, WHITE);

    int maxRedes = (n > 5) ? 5 : n;
    for (int i = 0; i < maxRedes; ++i) {
      display.setCursor(0, 12 + (i * 10));
      String currentSSID = WiFi.SSID(i);
      if(currentSSID.length() > 12) currentSSID = currentSSID.substring(0, 11) + "..";
      display.print(String(i + 1) + ": " + currentSSID);
      display.setCursor(95, 12 + (i * 10));
      display.print(WiFi.RSSI(i)); display.print("dB");
    }
  }
  display.display();
  delay(8000); // Muestra redes por 8 segundos
}
