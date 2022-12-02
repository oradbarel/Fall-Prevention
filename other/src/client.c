//#include <EEPROM.h>
//#include <HX711_ADC.h>
#include <WiFi.h>

/* Consts. */
#define CAL_FACTOR      19.5
#define TX_RATE         115200
#define SAMPLE_DELAY    200
#define FS_RES          5.0
#define FS_DIV          1023.0
#define VAL_RES         3
#define WIFI_DELAY      500
#define WIFI_SSID       "Almog's lost Appendix"
#define WIFI_PASS       "dkgv2179"
#define SERVER_PORT     13380

/* Macros */
#define NORM_FS(value) (((value) * FS_RES) / FS_DIV)

enum SENSOR {
    /* Force sensor */
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

WiFiClient client;
IPAddress server(192, 168, 38, 232);
const int port = SERVER_PORT;
char buffer[100];


void wifi_connect(char* ssid, char* password)
{
    WiFi.begin(WIFI_SSID, WIFI_PASS);
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

void server_connect(IPAddress server, int port)
{
    Serial.println("Connecting to the server...");
    while (!client.connect(server, port)) {
        Serial.print(".");
        delay(WIFI_DELAY);
    }

    Serial.println("Connected!");

    return;
}

void setup()
{
    Serial.begin(TX_RATE); 

    for (int sensor = 0; sensor < NUM_SENSORS; sensor++)
        pinMode(sensor_gpio_map[sensor], INPUT);

    wifi_connect(WIFI_SSID, WIFI_PASS);
    server_connect(server, port);

    return;
}

void loop()
{
    int sensor_data, idx;
    float vout;

    idx = sprintf(buffer, "Sensors reads: ");

    for (int sensor = 0; sensor < NUM_SENSORS; sensor++) {
        sensor_data = analogRead(sensor_gpio_map[sensor]);
        vout = NORM_FS(sensor_data) * CAL_FACTOR;
        idx += sprintf(buffer + idx, "%.3f ", vout);
    }

    Serial.println(buffer); 
    client.println(buffer); 

    delay(SAMPLE_DELAY); 
    
    return;
}