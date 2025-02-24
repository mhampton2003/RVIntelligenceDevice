#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

// CAMERA MODEL - AI Thinker ESP32-CAM (explicitly defined)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// Wi-Fi Access Point Credentials
const char *ssid = "ESP32-CAM-AP";
const char *password = "12345678";

WebServer server(80);  // Web server on port 80

// Function to serve the homepage with a link to the camera stream
void handleRoot() {
    String page = "<h1>ESP32-CAM AP Mode</h1>"
                  "<p><a href='/stream'>Click here to view the camera stream</a></p>";
    server.send(200, "text/html", page);
}

// Stream camera frames
void handleStream() {
    WiFiClient client = server.client();
    String response = "HTTP/1.1 200 OK\r\n";
    response += "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n";
    client.print(response);

    while (client.connected()) {
        camera_fb_t *fb = esp_camera_fb_get();
        if (!fb) {
            Serial.println("Camera capture failed");
            delay(100);
            continue;
        }

        response = "--frame\r\n";
        response += "Content-Type: image/jpeg\r\n";
        response += "Content-Length: " + String(fb->len) + "\r\n\r\n";
        client.print(response);
        client.write(fb->buf, fb->len);
        client.print("\r\n");

        esp_camera_fb_return(fb);
    }
}

// Initialize Camera with explicit model definition
void initCamera() {
    Serial.println("Initializing Camera...");

    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_QVGA;  // Lower resolution for stability
    config.jpeg_quality = 12;  // Medium quality for better performance
    config.fb_count = 1;  // Reduce buffer count to avoid memory issues

    // Ensure the camera framebuffer is correctly placed
    if (psramFound()) {
        config.fb_location = CAMERA_FB_IN_PSRAM;
        config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
        config.fb_location = CAMERA_FB_IN_DRAM;
        config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
    }

    // Delay to ensure the ESP32 is stable before initializing the camera
    delay(2000);

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed with error 0x%x\n", err);
        return;
    }

    Serial.println("Camera initialized successfully!");

    // Get camera sensor and explicitly define it as OV2640
    sensor_t *s = esp_camera_sensor_get();
    if (s == NULL) {
        Serial.println("Failed to get camera sensor!");
        return;
    }

    // Explicitly set sensor type and frame size
    s->set_framesize(s, FRAMESIZE_QVGA);
}

void setup() {
    Serial.begin(115200);

    // Start Wi-Fi Access Point
    WiFi.softAP(ssid, password);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);

    delay(2000);  // Ensure Wi-Fi is fully initialized

    // Initialize Camera
    initCamera();

    // Start Web Server
    server.on("/", handleRoot);
    server.on("/stream", handleStream);
    server.begin();

    Serial.println("ESP32-CAM is ready!");
    Serial.print("Connect to WiFi AP and visit: http://");
    Serial.println(IP);
}

void loop() {
    server.handleClient();
}
