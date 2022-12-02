#include "fall_prevention_client.h"

char buffer[100];

void wifi_connect(char* ssid, char* password)
{
    WiFi.begin(ssid, password);
    Serial.println("Connecting to WIFI:");

    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(WIFI_DELAY);
    }

    Serial.print("Connected! IP: ");
    Serial.println(WiFi.localIP());
    Serial.println();

    return;
}

void server_connect(WiFiClient* client, IPAddress server, int port)
{
    Serial.println("Connecting to the server...");
    while (!client->connect(server, port)) {
        Serial.print(".");
        delay(WIFI_DELAY);
    }

    Serial.println("Connected!");

    return;
}