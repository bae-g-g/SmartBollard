
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Adafruit_NeoPixel.h>


// Wi-Fi 설정
const char* ssid = "baegyounggeun";
const char* password = "rudrms123";

// 서버 IP 주소 설정
const char* serverIp = "172.20.10.3";  // Python 서버 IP 주소
const int serverPort = 5000;  // 서버 포트


const int MOTER_PIN = D1;  // LED가 연결된 핀
const int LED_PIN = D2;
const int NUM_LEDS = 24;

int lock;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pinMode(MOTER_PIN, OUTPUT);
  digitalWrite(MOTER_PIN, LOW);

  strip.begin();
  strip.show(); // 초기화: 모든 LED 끔
  
  lock = 1; // 최초는 락이 안걸린 상태로  
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { //연결이 될 때 까지 무한루프
    delay(1000);
  }

}

void loop() {

  WiFiClient client;
  HTTPClient http;
  String payload ="";
    
   
  if(lock){ // 락, 볼라드 작동동안 어떠한 통신도 하지않음, 안해도 되는데 간지나니까 추가함..
      String url = "http://" + String(serverIp) + ":" + String(serverPort) + "/signal";
      http.begin(client, url);  // WiFiClient 객체(client)와 URL을 함께 사용
      int httpCode = http.GET();
      payload = http.getString();
  }

  strip.setPixelColor(i, strip.Color(255, 255, 0)); // 노란색


  Serial.println("응답 본문: " + payload);
  if(payload == "on") {
          
      lock = 0;
      digitalWrite(MOTER_PIN, 1);


        
      for (int i = 0; i < NUM_LEDS; i++) {
      
        strip.setPixelColor(i, strip.Color(255, 255, 0)); // 빨간색
      }

      strip.show();

      // delay(3000); // 작동중가에 off signal받지 않기위해 3초간 정지
      lock = 1;

  } 
  else if (payload == "off") {
      digitalWrite(MOTER_PIN, 0);
      strip.clear();
      strip.show();
  }


  http.end();  // HTTP 연결 종료 
  delay(50);  // 0.05초마다 서버 확인 - 이후 회전에 방해를 주지 않는
}
