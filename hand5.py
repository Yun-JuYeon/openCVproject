# OpenCV는 Open Source Computer Vision의 약자로 영상 처리에 사용할 수 있는 오픈 소스 라이브러리 입니다
import cv2

# 미디어파이프는 구글에서 주로 인체를 대상으로하는 비전인식기능들을  AI모델 개발과 기계학습까지 마친 상태로 제공하는 서비스이다.
# 다양한 프로그램언어에서 사용하기 편하게 라이브러리 형태로 모듈화되어 제공
import mediapipe as mp
import math

#카메라 읽어오기
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# mediapipe에서 제공하는 오픈소스 사용
mpHands = mp.solutions.hands    # mediapipe에서 제공하는 ML 솔루션 중 hands옵션을 가져온다.
my_hands = mpHands.Hands()      # hands()메서드 사용하여 손에대한 반환값을 가져온다.
mpDraw = mp.solutions.drawing_utils     # drawing_utils 를 사용하여 손이 인식될때 점을 찍는다.

# 손가락 관절 사이 거리 계산 함수 (두 점 사이 거리 게산식)
# math.pow(x, y) 함수는 x의 y 거듭제곱 (x의 y승)을 반환
# math.sqrt(x) 함수는 x의 제곱근을 반환
def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))

# mediapipe에서 지정한 손 랜드마크 번호에 따라 설정 (이미지 참조)
compareIndex = [[18, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
open = [False, False, False, False, False]              # 손이 전부 펴지지 않았을 경우
gesture = [[False, True, False, False, False, "1"],     # 1 손모양
           [False, True, True, False, False, "2"],      # 2 손모양
           [False, True, True, True, False, "3"],       # 3 손모양
           [False, True, True, True, True, "4"],        # 4 손모양
           [True, True, True, True, True, "5"],      # 5 손모양
           [True, True, False, False, False, "check"],
           [True, False, False, False, False, "Nice!"],
           [True, True, False, False, True, "peace"]]

openCopy = []

def finger():
    while True:
        success, img = cap.read()
        h, w, c = img.shape

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = my_hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for i in range(0, 5):
                    open[i] = dist(handLms.landmark[0].x, handLms.landmark[0].y,
                                   handLms.landmark[compareIndex[i][0]].x, handLms.landmark[compareIndex[i][0]].y) <\
                              dist(handLms.landmark[0].x, handLms.landmark[0].y,
                                   handLms.landmark[compareIndex[i][1]].x, handLms.landmark[compareIndex[i][1]].y)

                    text_x = (handLms.landmark[0].x * w)
                    text_y = (handLms.landmark[0].y * h)

                    for i in range(0, len(gesture)):
                        flag = True
                        for j in range(0, 5):
                            if(gesture[i][j] != open[j]):
                                flag = False

                        if(flag == True):
                            cv2.putText(img, gesture[i][5], (round(text_x) - 50, round(text_y) - 250),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                            if True in open:
                                # print(open)

                                if open[1] & open[2] == False:
                                    # print("모션 1")
                                    openCopy.append(open)
                                    if len(openCopy) == 50:
                                        print(gesture[i][5])
                                        print(len(openCopy), "Finish")
                                        openCopy.clear()
                                        cap.release()
                                        return '1'

                                elif open[1] & open[2] == True and open[3] == False:
                                    # print("모션 2")
                                    openCopy.append(open)
                                    if len(openCopy) == 50:
                                        print(gesture[i][5])
                                        print(len(openCopy), "Finish")
                                        openCopy.clear()
                                        cap.release()
                                        return '2'


                                elif (open[1] & open[2] & open[3] == True and open[4] == False):
                                    #print("모션 3")
                                    openCopy.append(open)
                                    if (len(openCopy) == 50):
                                        print(gesture[i][5])
                                        print(len(openCopy), "Finish")
                                        openCopy.clear()
                                        cap.release()
                                        return '3'


                                elif (open[0] == False and open[3] & open[4] == True):
                                    #print("모션 4")
                                    openCopy.append(open)
                                    if (len(openCopy) == 50):
                                        print(gesture[i][5])
                                        print(len(openCopy), "Finish")
                                        openCopy.clear()
                                        cap.release()
                                        return '4'


                                elif (open[0] == True):
                                    #print("모션 5")
                                    openCopy.append(open)
                                    if (len(openCopy) == 50):
                                        print(gesture[i][5])
                                        print(len(openCopy), "Finish")
                                        openCopy.clear()
                                        cap.release()
                                        return '5'

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


        cv2.imshow("HandTracking", img)
        cv2.waitKey(5)


finger()