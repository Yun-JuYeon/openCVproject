# OpenCV는 Open Source Computer Vision의 약자로 영상 처리에 사용할 수 있는 오픈 소스 라이브러리
import cv2

# 미디어파이프는 구글에서 주로 인체를 대상으로하는 비전인식기능들을  AI모델 개발과 기계학습까지 마친 상태로 제공하는 서비스
# 다양한 프로그램언어에서 사용하기 편하게 라이브러리 형태로 모듈화되어 제공
import mediapipe as mp
import math

# 카메라 읽어오기
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# mediapipe에서 제공하는 오픈소스 사용
mpHands = mp.solutions.hands  # mediapipe에서 제공하는 ML 솔루션 중 hands옵션을 가져온다.
my_hands = mpHands.Hands()  # hands()메서드 사용하여 손에대한 반환값을 가져온다.
mpDraw = mp.solutions.drawing_utils  # drawing_utils 를 사용하여 손이 인식될때 점을 찍는다.


# 손가락 관절 사이 거리 계산 함수 (두 점 사이 거리 게산식)
# math.pow(x, y) 함수는 x의 y 거듭제곱 (x의 y승)을 반환
# math.sqrt(x) 함수는 x의 제곱근을 반환
def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))


# mediapipe에서 지정한 손 랜드마크 번호에 따라 설정 (이미지 참조)
compareIndex = [[18, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
open = [False, False, False, False, False]  # 손이 전부 펴지지 않았을 경우
gesture = [[False, True, False, False, False, "1"],  # 1 손모양
           [False, True, True, False, False, "2"],  # 2 손모양
           [False, True, True, True, False, "3"],  # 3 손모양
           [False, True, True, True, True, "4"],  # 4 손모양
           [True, True, True, True, True, "5"]]  # 5 손모양

openCopy = []  # 출력 값 넣을 새 배열 생성

a = True
while a:
    #   cv2.VideoCapture(video_file)을 통해 동영상의 캡처 객체 cap에 저장
    #   영상의 전체가 담기는게 아니고 첫번째 프레임만 담기기 때문에 연속해서 파일의 프레임을 읽어오기 위해 무한루프로 cap.read()를 호출.
    #   프레임이 잘 읽혀졌다면 success에는 True, img는 프레임 이미지가 됨.
    success, img = cap.read()
    h, w, c = img.shape  # .shape을 사용하여 height, width, channel 구함.

    # rgb 이미지를 hand 객체로 보내기
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR 색상 이미지를 RGB 색상 이미지로 변환
    results = my_hands.process(imgRGB)  # 이미지의 rgb 정보 추출하기

    # handLms == 손 하나
    # mediapipe로 손의 관절에 점을 찍어주기
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for i in range(0, 5):
                # 손가락의 점 사이의 거리를 측정 하여 손가락이 접혀 있는지 펴져있는지 판단, True/False 지정
                open[i] = dist(handLms.landmark[0].x, handLms.landmark[0].y,
                               handLms.landmark[compareIndex[i][0]].x, handLms.landmark[compareIndex[i][0]].y) < \
                          dist(handLms.landmark[0].x, handLms.landmark[0].y,
                               handLms.landmark[compareIndex[i][1]].x, handLms.landmark[compareIndex[i][1]].y)

                # 손가락 점(랜드마크)의 x,y좌표에 w,h를 곱해준다.(텍스트 위치 지정시 사용)
                text_x = (handLms.landmark[0].x * w)
                text_y = (handLms.landmark[0].y * h)

                for i in range(0, len(gesture)):
                    flag = True
                    for j in range(0, 5):
                        # 손가락의 동작이 미리 지정해 놓은 동작이 아닐결우
                        if (gesture[i][j] != open[j]):
                            flag = False

                    if (flag == True):
                        # putText를 이용하여 화면에 Text 출력
                        # cv2.putText(img ,text, 문자열 위치, font, fontSize, font color)
                        cv2.putText(img, gesture[i][5], (round(text_x) - 50, round(text_y) - 250),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                        if (True in open):
                            # print(open)

                            if (open[1] & open[2] == False):  # 모션 1의 조건
                                # print("모션 1")
                                openCopy.append(open)  # 미리 생성해 놓은 배열에 추가
                                if (len(openCopy) == 50):  # 출력 값이 50개가 되면(delay 목적)
                                    print(gesture[i][5])  # 지정해 놓은 문자열 print
                                    print(len(openCopy), "Finish")
                                    a = False  # 반복문 종료
                                    openCopy.clear()  # 담긴 배열 비우기
                                    cap.release()  # 카메라 사용 종료

                            elif (open[1] & open[2] == True and open[3] == False):  # 모션 2의 조건
                                # print("모션 2")
                                openCopy.append(open)
                                if (len(openCopy) == 50):
                                    print(gesture[i][5])
                                    print(len(openCopy), "Finish")
                                    a = False
                                    openCopy.clear()
                                    cap.release()

                            elif (open[1] & open[2] & open[3] == True and open[4] == False):  # 모션 3의 조건
                                # print("모션 3")
                                openCopy.append(open)
                                if (len(openCopy) == 50):
                                    print(gesture[i][5])
                                    print(len(openCopy), "Finish")
                                    a = False
                                    openCopy.clear()
                                    cap.release()

                            elif (open[0] == False and open[3] & open[4] == True):  # 모션 4의 조건
                                # print("모션 4")
                                openCopy.append(open)
                                if (len(openCopy) == 50):
                                    print(gesture[i][5])
                                    print(len(openCopy), "Finish")
                                    a = False
                                    openCopy.clear()
                                    cap.release()

                            elif (open[0] == True):  # 모션 5의 조건
                                # print("모션 5")
                                openCopy.append(open)
                                if (len(openCopy) == 50):
                                    print(gesture[i][5])
                                    print(len(openCopy), "Finish")
                                    a = False
                                    openCopy.clear()
                                    cap.release()

                # 손 관절의 점을 선으로 이어주기
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("HandTracking", img)
    cv2.waitKey(5)