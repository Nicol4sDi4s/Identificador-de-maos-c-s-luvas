import cv2 as cv
import time
import mediapipe as mp

class handDetcetor():
    def __init__(self, mode = False, maxHands = 2, complexity = 1, detectionCon = 0.75, trackCon = 0.75 ):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw= True):
        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #self.results = self.hands.process(frame)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks: 
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame     

    def findPosition(self, frame, handNo = 0, draw = True):
            
            lmList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    #print(id, lm)
                    h, w, c= frame.shape
                    cx, cy= int(lm.x*w), int(lm.y*h)
                    #print(id, cx, cy)
                    lmList.append([id, cx, cy])
                    if draw :
                        cv.circle(frame, (cx, cy), 3, (255,0,255), cv.FILLED)

            return lmList
    
    def findPosition1(self, frame, handNo = 1, draw = True):
            
            lmList1 = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    #print(id, lm)
                    h, w, c= frame.shape
                    cx, cy= int(lm.x*w), int(lm.y*h)
                    #print(id, cx, cy)
                    lmList1.append([id, cx, cy])
                    if draw :
                        cv.circle(frame, (cx, cy), 3, (255,0,255), cv.FILLED)

            return lmList1

def pointing_up(lmList1):
    if((lmList1[12][2] > lmList1[8][2] and lmList1[16][2] > lmList1[8][2] and lmList1[12][2] > lmList1[8][2]) and lmList1[0][2] > lmList1[8][2] and lmList1[8][2] < lmList1[6][2] and lmList1[8][2] < lmList1[7][2]  and lmList1[4][2] > lmList1[8][2]):
        if((lmList1[8][1] > lmList1[20][1]) and (lmList1[6][1] > lmList1[4][1])):
            return True
        if((lmList1[8][1] < lmList1[20][1]) and (lmList1[6][1] < lmList1[4][1])):
            return True
        
def pointing_down(lmList):
    if((lmList[12][2] < lmList[8][2] and lmList[16][2] < lmList[8][2] and lmList[12][2] < lmList[8][2]) and lmList[0][2] < lmList[8][2] and lmList[8][2] > lmList[6][2] and lmList[8][2] > lmList[7][2] and lmList[4][2] < lmList[8][2]):
        if((lmList[8][1] > lmList[20][1]) and (lmList[6][1] > lmList[4][1])):
            return True
        if((lmList[8][1] < lmList[20][1]) and (lmList[6][1] < lmList[4][1])):
            return True

def main():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    pTime = 0
    cTime = 0
    detector = handDetcetor()
    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
        action = []
        if len(lmList) != 0:
            # Gesto 1
            if(pointing_up(lmList)):
                action.append("pointing up")
            # Gesto 2
            if(pointing_down(lmList)):
                action.append("pointing down")

        if len(action) != 0:
            cv.putText(frame, action[0], (100,170), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            
        #FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv.imshow('Imagem', frame)
        if cv.waitKey(1) == 27:
            break


if __name__ == "__main__":
    main()