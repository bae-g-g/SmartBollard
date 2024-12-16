#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_NeoPixel.h>


// Wi-Fi 설정
const char* ssid = "baegyounggeun";
const char* password = "rudrms123";

// 서버 IP 주소 설정
const char* serverIp = "172.20.10.3";  // Python 서버 IP 주소
const int serverPort = 5000;  // 서버 포트

//핀 설정
const int MOTER_PIN = D1;  // 모터핀
const int LED_PIN = D2;    //LED핀

//LED 설정
const int NUM_LEDS = 24;
Adafruit_NeoPixel strip;
unsigned int LED_bright;

//신호 상태 저장 변수 선언
String prev_payload;
int state;

void setup() {

    //와이파이 연결
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) delay(1000);  

    //모터셋업
    pinMode(MOTER_PIN, OUTPUT);
    digitalWrite(MOTER_PIN, LOW);

    //LED셋업업
    strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
    strip.begin();
    strip.show();
    LED_bright = 0;

    //신호 상태 셋업
    prev_payload = "off";
    state = 0;

}



void loop() {

    //http 통신 
    WiFiClient client;
    HTTPClient http;
    String payload = "";
    String url = "http://" + String(serverIp) + ":" + String(serverPort) + "/signal";
    
    http.begin(client, url);
    payload = http.getString();
  

    // 이전응답과 다른경우(새로운 신호를 받은경우) state(on/off)를 변경경
    if( payload != prev_payload ){

        state = ( state + 1 ) % 2;
        LED_bright = 0;
        strip.clear();
    }


    if(state == 1 ){
        
        for (int i = 0; i < NUM_LEDS; i++){
            strip.setPixelColor(i, strip.Color(255, 0, 0)); // 빨간색으로로
        } 
    } 
    else if (state == 0){

        LED_bright += 1;
        for (int i = 0; i < NUM_LEDS; i++){
            strip.setPixelColor(i, strip.Color( LED_bright%255, (LED_bright%255)/2, 0)); //노란색
        } 
    }
    digitalWrite(MOTER_PIN, state);
    strip.show();
    

    prev_payload = payload; // 이전상태저장장
    http.end();  // HTTP 연결 종료 
    delay(10);

}
