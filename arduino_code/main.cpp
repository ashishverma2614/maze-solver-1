#include <iostream>

class Motor {
public:
    void run(int i) {}
};

Motor leftMotor;
Motor rightMotor;

int RELEASE = 0;
int FORWARD = 1;
int BACKWARD = 2;

bool digitalRead(int i) {
    return rand() > i;
}

//define line follower
void turnRight() {
    rightMotor.run(RELEASE);
    while ()
    leftMotor.run(FORWARD);
}

void turnLeft() {
    printf_s("Turn Left");
}

void straightForward() {
    printf_s("Go Straight");
}

void stop() {
    printf_s("Stop");
}

bool hasStraight() {
    return digitalRead(5) && digitalRead(6);
}

/*
 * Signal Code
 *
 * LTR : Leaning to the right ( RSr in Line RSl out line )
 * LTL : Leaning to the left ( RSl in Line RSr out line )
 * RSl : Rear Sensor Left ( Line Detector ) digitalRead(5)
 * RSr : Rear Sensor Right ( Line Detector ) digitalRead(6)
 * TDbTSl : Track Detected by Tracker Sensor Left ( Track Detector ) digitalRead(9)
 * TDbTSr : Track Detected by Tracker Sensor Right ( Track Detector ) digitalRead(10)
 * TDbMS : Track Detected by Middle Sensor ( Track Detector ) digitalRead(11)
 *
 * 0 : On Track ( RSl & RSr in line)
 * 1 : LTL
 * 2 : LTR
 * 3 : TDbTSl
 * 4 : TDbTSr
 * 5 : Junction (TDbTSl & TDbTSr)
 * 6 : Left Junction (TDbTSl & TDbMS)
 * 7 : Right Junction (TDbTSr & TDbMS)
 * 8 : Crossroads (TDbTSl & TDbTSr & TDbMS)
 * 9 : Stop
 * */

int getSignal() {

    //is get signal?
    if (digitalRead(9) && !digitalRead(10) && !digitalRead(11)) {
        return 3;
    } else if (!digitalRead(9) && digitalRead(10) && !digitalRead(11)) {
        return 4;
    } else if (digitalRead(9) && digitalRead(10) && !digitalRead(11)) {
        return 5;
    } else if (digitalRead(9) && !digitalRead(10) && digitalRead(11)) {
        return 6;
    } else if (!digitalRead(9) && digitalRead(10) && digitalRead(11)) {
        return 7;
    } else if (digitalRead(9) && digitalRead(10) && digitalRead(11)) {
        return 8;
    }

    //is in line ?
    if (digitalRead(5) && digitalRead(6)) {
        return 0;
    } else if (digitalRead(5) && !digitalRead(6)) {
        return 1;
    } else if (!digitalRead(5) && digitalRead(6)) {
        return 2;
    }

    return 9;

}

int main() {
    char navigate[] = "#lrlrrls#";
    if (navigate[0] == '#') {
        bool isEnd = false;
        int counter = 1;

        while (!isEnd) {
            if (navigate[counter] == '#') {
                isEnd = true;
            } else {
                switch (getSignal()) {
                    case 0 :
                        straightForward();
                    case 1 :
                        turnRight();
                    case 2 :
                        turnLeft();
                    case 3 :


                    default:
                        stop();
                }
            }
        }
    }

    return 0;
}

