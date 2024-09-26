#define DECODE_NEC
#include <IRremote.hpp>

const int IR_RECEIVE_PIN = 2;

const char FLAG[] = "flag{**********}";
const char ENCRYPTED_PIN[] = "BCMIJKLB";  // 89730168
const int XOR_KEY = 0x7A;
char ENTERED_PIN[] = "--------";
int enteredChars = -1;


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
      if (!(data.flags & IRDATA_FLAGS_IS_REPEAT)) {
        char digit;

        switch (data.command) {
          case 0x12:
            digit = '0';
            break;
          case 0x09:
            digit = '1';
            break;
          case 0x1D:
            digit = '2';
            break;
          case 0x1F:
            digit = '3';
            break;
          case 0x0D:
            digit = '4';
            break;
          case 0x19:
            digit = '5';
            break;
          case 0x1B:
            digit = '6';
            break;
          case 0x11:
            digit = '7';
            break;
          case 0x15:
            digit = '8';
            break;
          case 0x17:
            digit = '9';
            break;
          default:
            digit = '\0';
        }

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
