#include <Arduino.h>
#include <Wire.h>
// #include <ESP8266WiFi.h>
// Arduino Uno: SCL = A5, SDA = A4
// There are internal pull-up resistors on SCL and SCD pins of IN219B.

#define CALIB_VALUE         (20420)          // the calibration value
#define CURRENT_LSB         (20)             // uA per bit
#define SHUNT_VOLTAGE_LSB   (10)             // uV per bit
#define BUS_VOLTAGE_LSB     (4)              // mV per bit
#define POWER_LSB           (20*CURRENT_LSB) // uW per bit
#define CONFIG_VALUE        ( INA219_CONFIG_BV_MAX_16V \
                            | INA219_CONFIG_GAIN_2_80MV \
                            | INA219_CONFIG_BV_ADC_12BIT \
                            | INA219_CONFIG_SV_ADC_12BIT_1S_532US \
                            | INA219_CONFIG_MODE_SV_BV_CONTINUOUS )

// Please refer to the datasheet:
//  http://www.ti.com/lit/ds/symlink/ina219.pdf
//  http://learn.adafruit.com/downloads/pdf/adafruit-ina219-current-sensor-breakout.pdf

const byte INA219_I2C_ADDR = 0b1000000; // 0x40 (7-bit I2C slave address)
// Default: A0=A1=GND (with on-board pull-down resistors)
// if the solder jumper is bridged -> logic '1'.
// A1=0,A0=0 => 0x40, A1=0,A0=1 => 0x41, A1=1,A0=0 => 0x44, and A1=1,A0=1 => 0x45

#define INA219_REG_CONFIG                    (0x00)
#define INA219_REG_SHUNT_VOLTAGE             (0x01)
#define INA219_REG_BUS_VOLTAGE               (0x02)
#define INA219_REG_POWER                     (0x03)
#define INA219_REG_CURRENT                   (0x04)
#define INA219_REG_CALIBRATION               (0x05)

#define INA219_CONFIG_GAIN_1_40MV            (0x0000)  // Gain 1, 40mV Range
#define INA219_CONFIG_GAIN_2_80MV            (0x0800)  // Gain 2, 80mV Range
#define INA219_CONFIG_GAIN_4_160MV           (0x1000)  // Gain 4, 160mV Range
#define INA219_CONFIG_GAIN_8_320MV           (0x1800)  // Gain 8, 320mV Range

#define INA219_CONFIG_RST                    (0x8000)  // Soft Reset Bit
#define INA219_CONFIG_BV_MAX_16V             (0x0000)  // 16V Bus Voltage Full Range
#define INA219_CONFIG_BV_MAX_32V             (0x2000)  // 32V Bus Voltage Full Range
#define INA219_CONFIG_BV_ADC_12BIT           (0x0400)  // 12-bit Bus Voltage Sampling
#define INA219_CONFIG_SV_ADC_12BIT_1S_532US  (0x0018)  // 1x 12-bit Shunt Voltage Sampling
#define INA219_CONFIG_MODE_SV_BV_CONTINUOUS  (0x0007)  // Continuous Shunt & Bus Voltage Sampling

void INA219_readReg( uint8_t i2c_addr, uint8_t reg, uint16_t *value ) {
  uint8_t buf[2];
  uint8_t count = 0;

  Wire.beginTransmission( i2c_addr );
  Wire.write( reg );  // write the register address
  Wire.endTransmission();
  delayMicroseconds( 500 );
  Wire.requestFrom( i2c_addr, (uint8_t) 2 ); // read two bytes
  while ( Wire.available() && (count < 2) ) {
    buf[ count++ ] = Wire.read();
  }
  Wire.endTransmission();
  *value = ((uint16_t)buf[0]) << 8 | buf[1];
}

void INA219_writeReg( uint8_t i2c_addr, uint8_t reg, uint16_t value ) {
  Wire.beginTransmission( i2c_addr );
  Wire.write( reg );          // write the register address
  Wire.write( value >> 8 );   // write the higher byte
  Wire.write( value & 0xff ); // write the lower byte
  Wire.endTransmission();
}

void IN219_config() {
  uint16_t value;
  // Perform the soft reset
  value = INA219_CONFIG_RST;
  INA219_writeReg( INA219_I2C_ADDR, INA219_REG_CONFIG, value );
  delay(1);

  // Set the calibration register
  value = CALIB_VALUE;
  INA219_writeReg( INA219_I2C_ADDR, INA219_REG_CALIBRATION, value );

  // Set the config register
  value = CONFIG_VALUE;
  INA219_writeReg( INA219_I2C_ADDR, INA219_REG_CONFIG, value );
}

int32_t INA219_getShuntVoltage() { // in uV
  uint16_t value;
  INA219_readReg( INA219_I2C_ADDR, INA219_REG_SHUNT_VOLTAGE, &value );
  return ((int16_t)value) * (int32_t)SHUNT_VOLTAGE_LSB;
}

int16_t INA219_getBusVoltage() { // in mV
  uint16_t value;
  INA219_readReg( INA219_I2C_ADDR, INA219_REG_BUS_VOLTAGE, &value );
  return (((int16_t)value >> 3) * BUS_VOLTAGE_LSB /*mV*/ );
}

int32_t INA219_getCurrent() { // in uA step
  uint16_t value;
  INA219_readReg( INA219_I2C_ADDR, INA219_REG_CURRENT, &value );
  return ((int16_t)value) * (int32_t)CURRENT_LSB;
}

int32_t INA219_getPower() { // Load Power = Current * Bus Voltage
  uint16_t value;
  INA219_readReg( INA219_I2C_ADDR, INA219_REG_POWER, &value);
  return (((int16_t)value) * (int32_t)POWER_LSB) / 1000;
}

const int sigOut = 14;      // D5 start output
const int finOut = 12;      // D6 finish output
// const int broIn  = 13;      // D7 done input

void setup() {
  // WiFi.mode(WIFI_OFF);
  Wire.begin(4, 5); // use I2C port
  Serial.begin(921600); // use serial port
  IN219_config();
  pinMode(sigOut, OUTPUT);
  pinMode(finOut, OUTPUT);
  // pinMode(broIn, INPUT);
  digitalWrite(sigOut, HIGH);
  digitalWrite(finOut, HIGH);
  attachInterrupt(2, pinChanged, FALLING);
  attachInterrupt(13, donebroker, FALLING);
}

char sbuf[32];
boolean isPressBtn = false;
boolean isStart = false;
boolean isDone = false;
int32_t currentSum = 0;
int32_t voltageSum = 0;
int count = 0;
int32_t current = 0;
void loop() {
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  if (Serial.available()) {
    char inByte = Serial.read();
    if (inByte == 'r') {
      if(!isStart){
        Serial.print('s');
        digitalWrite(sigOut, LOW);
        digitalWrite(finOut, HIGH);
        isStart = true;
        isDone = false;
        delay(5);
        digitalWrite(sigOut, HIGH);
      }
    }else if(inByte == 'f'){
      digitalWrite(sigOut, HIGH);
      digitalWrite(finOut, LOW);
      isStart = false;
      isDone = false;
    }else if(inByte == 'd'){
      digitalWrite(sigOut, HIGH);
      digitalWrite(finOut, HIGH);
      isStart = false;
      isPressBtn = false;
    }
  }
  if (isStart) {
    if (millis() - samplingTime >= 5) {
      voltageSum += INA219_getBusVoltage();
      currentSum += INA219_getCurrent() / 100;
      samplingTime += 5;
      count++;
    }
    if (count == 20) {
      currentSum /= count;
      voltageSum /= count;
      sprintf( sbuf, "%3d.%d,", (int16_t)(currentSum / 10), (int16_t)(abs(currentSum) % 10) );
      Serial.print(sbuf);
      sprintf( sbuf, "%4d, \n", voltageSum );
      Serial.print(sbuf);
      voltageSum = 0;
      currentSum = 0;
      count = 0;
    }
  }
}

void pinChanged() {
  if (!isPressBtn) {
    Serial.print('p');
    digitalWrite(sigOut, HIGH);
    digitalWrite(finOut, HIGH);
    isPressBtn = true;
  }
}

void donebroker(){
  if (!isDone) {
    Serial.print('r');
    isDone = true;
    digitalWrite(sigOut, HIGH);
    digitalWrite(finOut, HIGH);
    isStart = false;
    isPressBtn = false;
  }
}
