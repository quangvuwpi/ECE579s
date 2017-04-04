#include <avr/power.h>

uint32_t modPow32(uint32_t b, uint32_t e, uint32_t m) {
  uint32_t idx;
  uint32_t res;

  // Locate MSB of exponent
  idx = 31;
  while (e & (1 << idx) == 0) {
    idx--;
  }

  // Modulo exponentiation
  res = b;
  while (idx > 0) {
    res = (res * res) %m;
    if (e & (1 << idx) == 1) {
      res = (res * b) % m;
    }
    idx--;
  }

  // Last bit
  res = (res * res) %m;
  if (e & (1 << idx) == 1) {
    res = (res * b) % m;
  }

  return res;
}

void setup() {
  // Change the running speed
  // The ATMega328p on the CryptoCape uses a 8MHz external crystal oscillator
  // Should change the speed to 8MHz / 8 = 1MHz
  clock_prescale_set(clock_div_8);

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

#define P      (31)
#define Q      (2053)
#define N      (63643)
#define E      (727)
#define D      (8383)
#define PHI_N  (61560)

void loop() {
  uint32_t data = 0x12345678;

  do { 
    // Trigger ADC capture on the falling edge
    digitalWrite(A0, LOW);
    delayMicroseconds(50);

    // Pseudo-randomize input for next round
    data = modPow32(data, D, N);

    // Reset trigger pin for next loop
    digitalWrite(A0, HIGH);
    delayMicroseconds(50);
  } while (1);
}
