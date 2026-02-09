#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "CANSAT_GROUND";
const char* password = "12345678";

WebServer server(80);

// -------- Sensor Variables --------
float pressure = 0, temperature = 0;
float smoke = 0, lpg = 0, methane = 0, hydrogen = 0;
float ax = 0, ay = 0, az = 0;
float gx = 0, gy = 0, gz = 0;

// -------- Thresholds --------
float TEMP_THRESHOLD = 40.0;
float SMOKE_THRESHOLD = 300.0;

// -------- Parse Function --------
void parseData(String data) {

  sscanf(data.c_str(),
         "P:%f|T:%f|S:%f|L:%f|M:%f|H:%f|AX:%f|AY:%f|AZ:%f|GX:%f|GY:%f|GZ:%f",
         &pressure,
         &temperature,
         &smoke,
         &lpg,
         &methane,
         &hydrogen,
         &ax, &ay, &az,
         &gx, &gy, &gz);

  Serial.println("Data Parsed Successfully");
}

// -------- Web Dashboard --------
void dashboard() {

  String alert = "";

  if (temperature > TEMP_THRESHOLD)
    alert += "⚠ HIGH TEMPERATURE ALERT!<br>";

  if (smoke > SMOKE_THRESHOLD)
    alert += "⚠ HIGH SMOKE ALERT!<br>";

  String page = "<html><head><title>CANSAT Dashboard</title>";

  page += "<style>";
  page += "body{background:black;color:white;font-family:Arial;text-align:center;}";
  page += ".card{background:#1e1e1e;padding:15px;margin:8px;border-radius:10px;display:inline-block;width:200px;}";
  page += ".title{color:cyan;font-size:18px;}";
  page += ".value{color:lime;font-size:24px;}";
  page += ".alert{color:red;font-size:22px;}";
  page += "</style>";

  page += "<meta http-equiv='refresh' content='2'>";
  page += "</head><body>";

  page += "<h1>CANSAT LIVE DASHBOARD</h1>";

  if (alert != "")
    page += "<div class='alert'>" + alert + "</div>";

  // -------- Environmental Data --------
  page += "<h2>Environmental Data</h2>";

  page += "<div class='card'><div class='title'>Pressure</div><div class='value'>" + String(pressure) + " hPa</div></div>";
  page += "<div class='card'><div class='title'>Temperature</div><div class='value'>" + String(temperature) + " °C</div></div>";
  page += "<div class='card'><div class='title'>Smoke</div><div class='value'>" + String(smoke) + "</div></div>";

  page += "<div class='card'><div class='title'>LPG</div><div class='value'>" + String(lpg) + "</div></div>";
  page += "<div class='card'><div class='title'>Methane</div><div class='value'>" + String(methane) + "</div></div>";
  page += "<div class='card'><div class='title'>Hydrogen</div><div class='value'>" + String(hydrogen) + "</div></div>";

  // -------- IMU ACCELEROMETER DATA --------
  page += "<h2>Accelerometer Data</h2>";

  page += "<div class='card'><div class='title'>AX</div><div class='value'>" + String(ax) + "</div></div>";
  page += "<div class='card'><div class='title'>AY</div><div class='value'>" + String(ay) + "</div></div>";
  page += "<div class='card'><div class='title'>AZ</div><div class='value'>" + String(az) + "</div></div>";

  // -------- IMU GYROSCOPE DATA --------
  page += "<h2>Gyroscope Data</h2>";

  page += "<div class='card'><div class='title'>GX</div><div class='value'>" + String(gx) + "</div></div>";
  page += "<div class='card'><div class='title'>GY</div><div class='value'>" + String(gy) + "</div></div>";
  page += "<div class='card'><div class='title'>GZ</div><div class='value'>" + String(gz) + "</div></div>";

  page += "<h3>Ground Station IP: " + WiFi.softAPIP().toString() + "</h3>";

  page += "</body></html>";

  server.send(200, "text/html", page);
}

// -------- Setup --------
void setup() {

  Serial.begin(115200);

  // UART from Pico
  Serial2.begin(115200, SERIAL_8N1, 16, 17);

  WiFi.softAP(ssid, password);

  Serial.println("Ground Station Started");
  Serial.println(WiFi.softAPIP());

  server.on("/", dashboard);
  server.begin();
}

// -------- Loop --------
void loop() {

  if (Serial2.available()) {

    String received = Serial2.readStringUntil('\n');

    Serial.println("Received: " + received);

    parseData(received);
  }

  server.handleClient();
}

