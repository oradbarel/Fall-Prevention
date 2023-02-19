#ifndef FALL_PREVENTION_CLIENT_H
#define FALL_PREVENTION_CLIENT_H

#include <WiFi.h>

/* Consts. */
#define WIFI_DELAY      500

void wifi_connect(char* ssid, char* password);

void server_connect(WiFiClient* client, IPAddress server, int port);

#endif /* FALL_PREVENTION_CLIENT_H_ */
