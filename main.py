import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

detector = HandDetector(detectionCon=0.8)


class Buttom:
    def __init__(self, pos, value, size=[75, 75]):

        self.pos = pos
        self.size = size
        self.value = value

    def draw(self, img):
        x, y = self.pos

        w, h = self.size
        cv2.rectangle(img, self.pos, (x+w, y+h),
                      (255, 0, 255), cv2.FILLED)
        cv2.rectangle(img, self.pos, (x+w, y+h), (0, 0, 0), 2)
        cv2.putText(img, self.value, (self.pos[0]+30, self.pos[1]+70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
        return img

    def marker(self, pos):
        x, y = pos
        if self.pos[0] < x < self.pos[0]+self.size[0] and self.pos[1] < y < self.pos[1]+self.size[1]:
            # print(self.value)
            return self.value


# button = Buttom([100, 100], "Q")
# pos = []
text = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ":"],
        ["z", "x", "c", "v", "b", "n", "m", "<", ">", "."]]
buttons = []
for x in range(3):
    for y in range(10):
        # pos.append([100+y*100, 100+x*100, text[x][y]])
        buttons.append(Buttom([100 + y*100, 100 + x*100], text[x][y]))
# print(pos)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=True)
    for button in buttons:
        img = button.draw(img)

    if hands:

        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        # print(lmList1[8])
        for i, button in enumerate(buttons):
            key = button.marker(lmList1[8][0:2])
            if key is not None:
                print(key)

    # img = button.draw(img)
    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
