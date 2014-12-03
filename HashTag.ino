int hashPin = 7;
int delayTime = 20;

void setup()
{
  Serial.begin(9600);
  pinMode(hashPin, INPUT);
}

void loop()
{
  int hashIn = digitalRead(hashPin);
  int x;
  Serial.println(x);
  delay(100);
  if(hashIn == 1){
    Serial.println("Bitch");
    int t = 40;
    while(t > 0) {
      hashIn = digitalRead(hashPin);
      Serial.println(hashPin);
      delay(100);
      if(hashIn == 0){
        int t2 = 40;
        while (t2 > 0){
          hashIn = digitalRead(hashPin);
          Serial.println(hashPin);
          delay(100);
          if(hashIn ==1){
            Serial.println("sl");
            sampleAudio();
            t2 = 0;
            t = 0;
          }
          t2--;
        }
        
      }
      t--;
      delay(100);
    }
    
   /* do
    {
      delay(100);          // wait for sensors to stabilize
      x = digitalRead(hashPin);  // check the sensors
      Serial.println(2);
    } while (x == 1);
    int count = 0;
    int inp;
    do
    {
      count++;
      inp = digitalRead(hashPin);
      Serial.println(count);
      delay(100);
      Serial.println(inp);
      delay(100);
    }while(count < delayTime && inp != 1);
    if(inp == 1){
      sampleAudio();
    }*/
  }
}

void sampleAudio()
{
  for(int i = 1; i < 5; i++){
    Serial.println("1000");
    delay(100);
  }
}
