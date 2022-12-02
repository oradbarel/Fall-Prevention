//#include <HX711_ADC.h>
//#include <EEPROM.h>
#include "src/fall_prevention_client/fall_prevention_client.h"

/* Consts. */
#define CAL_FACTOR      19.5
#define TX_RATE         115200
#define SAMPLE_DELAY    200
#define FS_RES          5.0
#define FS_DIV          1023.0
#define VAL_RES         3
#define WIFI_SSID       "Almog's lost Appendix"
#define WIFI_PASS       "dkgv2179"
#define SERVER_PORT     13380
//#define WS_SCL          22

/* Macros */
#define NORM_FS(value) (((value) * FS_RES) / FS_DIV)


enum SENSOR {
    /* Force sensors */
    FORCE_SENSOR1,
    FORCE_SENSOR2,
    FORCE_SENSOR3,
    FORCE_SENSOR4,
    FORCE_SENSOR5,
    FORCE_SENSOR6,
    FORCE_SENSOR7,
    FORCE_SENSOR8,
    /* Weight sensor */
    WEIGHT_SENSOR,
    NUM_SENSORS
};

/* GPIO Configuration */
// todo: config gp
static const int sensor_gpio_map[] {
    [FORCE_SENSOR1] = 33,
    [FORCE_SENSOR2] = 33,
    [FORCE_SENSOR3] = 33,
    [FORCE_SENSOR4] = 33,
    [FORCE_SENSOR5] = 33,
    [FORCE_SENSOR6] = 33,
    [FORCE_SENSOR7] = 33,
    [FORCE_SENSOR8] = 33,
    [WEIGHT_SENSOR] = 33,
};


/* Globals */
WiFiClient client;
IPAddress server(192, 168, 38, 232);
const int port = SERVER_PORT;
char main_buffer[100];

//HX711_ADC weight_sensor(sensor_gpio_map[WEIGHT_SENSOR], WS_SCL);

void setup()
{
    Serial.begin(TX_RATE); 

    /* Init Force sensors*/
    for (int sensor = 0; sensor < NUM_SENSORS - 1; sensor++)
        pinMode(sensor_gpio_map[sensor], INPUT);

    /* Init Weight sensor */
    //weight_sensor.begin();
    //weight_sensor.start(2000, false);
    //weight_sensor.setCalFactor(1.0);

    wifi_connect(WIFI_SSID, WIFI_PASS);
    server_connect(&client, server, port);

    return;
}


void loop()
{
    int sensor_data, idx;
    float vout;

    idx = sprintf(main_buffer, "Sensors reads: ");

    for (int sensor = 0; sensor < NUM_SENSORS - 1; sensor++) {
        sensor_data = analogRead(sensor_gpio_map[sensor]);
        vout = NORM_FS(sensor_data) * CAL_FACTOR;
        idx += sprintf(main_buffer + idx, "%.3f ", vout);
    }

    //while (LoadCell.update()) {}

    //vout = LoadCell.getData();
    //idx += sprintf(main_buffer + idx, "%.3f ", vout);
    //todo: remove
    idx += sprintf(main_buffer + idx, "%.3f ", 3.14);

    Serial.println(main_buffer); 
    client.println(main_buffer); 

    delay(SAMPLE_DELAY); 
    
    return;
}
