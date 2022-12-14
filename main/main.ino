#include <Adafruit_ADS1X15.h>
#include <HX711_ADC.h>
#include <EEPROM.h>
#include <Wire.h>

#include "src/fall_prevention_client/fall_prevention_client.h"

/* Consts. */
#define WEIGHT_SDA      4
#define WEIGHT_SCL      5
#define FSR_CAL_FACTOR  19.5
#define WCAL_FACTOR     1
#define TX_RATE         9600
#define SAMPLE_DELAY    200
#define FS_RES          5.0
#define FS_DIV          1023.0
#define VAL_RES         3
#define WIFI_SSID       "Almog's lost Appendix"
#define WIFI_PASS       "dkgv2179"
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
    /* Weight sensor */
    WEIGHT_SENSOR,
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
    [WEIGHT_SENSOR] = 33,
};


/* Globals */
WiFiClient client;
IPAddress server(192, 168, 6, 232);
const int port = SERVER_PORT;
char main_buffer[MSG_BUFFER];

Adafruit_ADS1015 ads;

HX711_ADC weight_sensor(WEIGHT_SDA, WEIGHT_SCL);


void setup()
{
    Serial.begin(TX_RATE); 

    /* Init Flex. Force sensors*/
    for (int sensor = 0; sensor < NUM_FFSR; sensor++)
        pinMode(sensor_gpio_map[sensor], INPUT);

    /* Init Weight sensor */
    //weight_sensor.begin();
    //weight_sensor.start(2000, false);
    //weight_sensor.setCalFactor(WCAL_FACTOR);

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

    idx = sprintf(main_buffer, "Sensors reads: ");

    /* Get FFSR data */
    for (int sensor = 0; sensor < NUM_FFSR; sensor++) {
        sensor_data = analogRead(sensor_gpio_map[sensor]);
        idx += sprintf(main_buffer + idx, "%d ", sensor_data);
    }

    /* Get RFSR data */
    for (int sensor = NUM_FFSR; sensor < NUM_SENSORS - 1; sensor++) {
        sensor_data = ads.readADC_SingleEnded(sensor_gpio_map[sensor]);
        idx += sprintf(main_buffer + idx, "%d ", sensor_data);
    }

    /* Get Weight data */
    //while (weight_sensor.update()) {}
    //sensor_data = weight_sensor.getData();
    //idx += sprintf(main_buffer + idx, "%d ", sensor_data);
    idx += sprintf(main_buffer + idx, "%d ", 31415926);

    Serial.println(main_buffer); 
    client.println(main_buffer); 

    delay(SAMPLE_DELAY); 
    
    return;
}
