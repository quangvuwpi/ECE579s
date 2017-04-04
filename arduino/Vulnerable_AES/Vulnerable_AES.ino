#include <avr/power.h>
#include <AESLib.h>

//
// Target AES implementation
//
// Running on the ATMega328p of the CryptoCape
//  - similar to the Arduino Pro Mini, according to the website
//  - CPU speed is set to 8MHz
//

uint8_t key128[16]    = {0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 
                         0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F};
uint8_t plaintext[16] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
                         0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F};

void setup() {
  // Change the running speed
  // The ATMega328p on the CryptoCape uses a 8MHz external crystal oscillator
  // Should change the speed to 8MHz / 8 = 1MHz
  //clock_prescale_set(clock_div_8);

  // Disable interrupts
  noInterrupts();

  // Initialize GPIO
  pinMode(13, OUTPUT);  // LED
  pinMode(A0, OUTPUT);  // AIN0 pin is set to output

  // Initialize GPIO state
  digitalWrite(13, HIGH);
  digitalWrite(A0, HIGH);
  delay(1);  // Let output "settles"
}

void loop() {
  uint8_t  temp[16];

  // Copy plaintext to temp block since encryption is in-place
  memcpy(temp, plaintext, sizeof plaintext);
 
  while (1) {
    // Trigger ADC capture on the falling edge
    digitalWrite(A0, LOW);
    delayMicroseconds(50);
  
    // Encrypt one block of plaintext with 128-bit key
    aes128_enc_single(&key128[0], &temp[0]);

    // Reset trigger pin for next loop
    digitalWrite(A0, HIGH);
    
    // Copy plaintext to temp block since encryption is in-place
    // Use small delays before and after to separate from encryption
    delayMicroseconds(50);
    memcpy(temp, plaintext, sizeof plaintext);
    delay(1);
  }
}
