#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "CANSAT_GROUND";
const char* password = "12345678";

WebServer server(80);

String receivedData = "Waiting for Pico Data...";

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 16, 17);

  WiFi.softAP(ssid, password);

  Serial.println("Ground Station Started");
  Serial.println(WiFi.softAPIP());

  server.on("/", dashboard);
  server.begin();
}

void loop() {

  if (Serial2.available()) {
    receivedData = Serial2.readStringUntil('\n');
    Serial.println(receivedData);
  }

  server.handleClient();
}

void dashboard() {

  String page = "<html><head>";
  page += "<title>CANSAT Dashboard</title>";

  page += "<style>";
  page += "body{background:black;color:white;font-family:Arial;text-align:center;}";
  page += ".card{background:#1e1e1e;padding:20px;margin:20px;border-radius:10px;display:inline-block;width:200px;}";
  page += ".title{font-size:20px;color:cyan;}";
  page += ".value{font-size:30px;color:lime;}";
  page += "</style>";

  page += "<meta http-equiv='refresh' content='2'>";
  page += "</head><body>";

  page += "<h1>CANSAT LIVE TELEMETRY DASHBOARD</h1>";

  page += "<div class='card'><div class='title'>Raw Data</div>";
  page += "<div class='value'>" + receivedData + "</div></div>";

  page += "<h3>Connected to: " + WiFi.softAPIP().toString() + "</h3>";

  page += "</body></html>";

  server.send(200, "text/html", page);
}
