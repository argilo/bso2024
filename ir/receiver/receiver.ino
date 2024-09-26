#define DECODE_NEC
#include <IRremote.hpp>

const int IR_RECEIVE_PIN = 2;

#if 0
const char FLAG[] = "flag{8_bit_fun!}";
#else
const char FLAG[] = "flag{??????????}";
#endif

const char ENCRYPTED_PIN[] = "BCMIJKLB";  // 89730168
const int XOR_KEY = 0x7A;
char ENTERED_PIN[] = "--------";
int enteredChars = -1;

const char COMMAND_TO_DIGIT[] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, '1', 0, 0, 0, '4', 0, 0,
    0, '7', '0', 0, 0, '8', 0, '9', 0, '5', 0, '6', 0, '2', 0, '3'
};


bool __attribute__ ((noinline)) checkPIN() {
  for (int i = 0; i < 8; i++) {
    if (ENTERED_PIN[i] != (ENCRYPTED_PIN[i] ^ XOR_KEY)) {
      return false;
    }
  }

  return true;
}

void clearDisplay() {
  Serial.write(0xFE);
  Serial.write(0x01);
}

void setCursorPosition(int pos) {
  Serial.write(0xFE);
  Serial.write(0x80 + pos);
}

void setup() {
  Serial.begin(9600);
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
}

void loop() {
  if (enteredChars == -1) {
    clearDisplay();
    Serial.print("   Enter PIN:   ");
    Serial.print("    --------");
    setCursorPosition(68);
    enteredChars = 0;
  }

  if (IrReceiver.decode()) {
    auto data = IrReceiver.decodedIRData;
    if ((data.protocol == NEC) && (data.address == 0x00)) {
      if ((data.command < 0x20) && !(data.flags & IRDATA_FLAGS_IS_REPEAT)) {
        char digit = COMMAND_TO_DIGIT[data.command];

        if (digit) {
          Serial.print(digit);
          ENTERED_PIN[enteredChars++] = digit;

          if (enteredChars == 8) {
            bool success = checkPIN();
            delay(500);
            clearDisplay();

            if (success) {
              Serial.write("Access granted! ");
              Serial.write(FLAG);
            } else {
              Serial.write(" Access denied!");
            }

            delay(5000);
            enteredChars = -1;
          }
        }
      }
    }

    IrReceiver.resume();
  }
}
