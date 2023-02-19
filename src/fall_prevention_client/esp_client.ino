#include <Adafruit_ADS1X15.h>
#include <Wire.h>

#include "src/fall_prevention_client/fall_prevention_client.h"

/* Consts. */
#define WEIGHT_SDA      4
#define WEIGHT_SCL      5
#define FSR_CAL_FACTOR  19.5
#define WCAL_FACTOR     1
#define TX_RATE         9600
#define SAMPLE_DELAY    300
#define FS_RES          5.0
#define FS_DIV          1023.0
#define VAL_RES         3
#define WIFI_SSID       "Fall Prevention Wifi" // router
#define WIFI_PASS       "95334448" // router
// #define WIFI_SSID       "Pi wifi" // hotspot
// #define WIFI_PASS       "31415926" // hotspot
#define SERVER_PORT     13380
#define WS_SCL          22
#define ADS_ADDR        0x48
#define NUM_FFSR        4
#define NUM_RFSR        4
#define MSG_BUFFER      100

/* Macros */
#define NORM_FS(value) (((value) * FS_RES) / FS_DIV)


enum SENSOR {
    /* Force sensors */
    FFSR1,
    FFSR2,
    FFSR3,
    FFSR4,
    RFSR1,
    RFSR2,
    RFSR3,
    RFSR4,
    NUM_SENSORS
};

/* GPIO Configuration */
static const int sensor_gpio_map[] {
    [FFSR1] = 36,
    [FFSR2] = 39,
    [FFSR3] = 34,
    [FFSR4] = 35,
    [RFSR1] = 0,
    [RFSR2] = 1,
    [RFSR3] = 2,
    [RFSR4] = 3,
};


/* Globals */
WiFiClient client;
IPAddress server(192, 168, 0, 101); // router
// IPAddress server(192, 168, 6, 232); // hotspot
const int port = SERVER_PORT;
char main_buffer[MSG_BUFFER];

Adafruit_ADS1015 ads;


void setup()
{
    Serial.begin(TX_RATE); 

    /* Init Flex. Force sensors*/
    for (int sensor = 0; sensor < NUM_FFSR; sensor++)
        pinMode(sensor_gpio_map[sensor], INPUT);

    /* Init I2C ADS */
    ads.begin(ADS_ADDR);

    /* Init Client */
    wifi_connect(WIFI_SSID, WIFI_PASS);
    server_connect(&client, server, port);

    return;
}


void loop()
{
    int sensor_data, idx;
    
    /* if not currently connected to WiFi (connection dropped) */
    if (WiFi.status() != WL_CONNECTED) {
        wifi_connect(WIFI_SSID, WIFI_PASS);
        server_connect(&client, server, port);
    }
    /* if not currently connected to server (connection dropped) */
    else if (!client.connected()) {
        server_connect(&client, server, port);
    }

    idx = sprintf(main_buffer, "Sensors reads: ");

    /* Get FFSR data */
    for (int sensor = 0; sensor < NUM_FFSR; sensor++) {
        sensor_data = analogRead(sensor_gpio_map[sensor]);
        idx += sprintf(main_buffer + idx, "%d ", sensor_data);
    }

    /* Get RFSR data */
    for (int sensor = NUM_FFSR; sensor < NUM_SENSORS; sensor++) {
        sensor_data = ads.readADC_SingleEnded(sensor_gpio_map[sensor]);
        idx += sprintf(main_buffer + idx, "%d ", sensor_data);
    }

    Serial.println(main_buffer); 
    client.println(main_buffer); 

    delay(SAMPLE_DELAY); 
    
    return;
}
