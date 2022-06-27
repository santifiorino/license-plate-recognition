import cv2
import LPR

lpr = LPR.LPR()
plates = ["AD440CY", "AB397UK", "AD233LT", "AE182AY", "AE182AW",
          "AE486WE", "AE796GG", "AD023DO", "AC883RA", "AC017TU",
          "AC017TN", "AD440CY", "AA854LC", "AE497FZ", "AC017TR",
          "AE622RT", "AD461GQ", "AA516IP", "AC724YO", "AE250FX",
          "AE521RQ", "AC883RJ", "AE676WN", "AE410HE", "AE444JH"]

for i in range(25):
    img = cv2.imread(f"./imgs/{i:03}.png")
    txt = lpr.read_license(img)
    if txt[:-1] == plates[i]:
        print(f"{i:03} OK")
    else:
        print(f"{i:03} ERROR | Original: {plates[i]}",
                 f"Recognized: {txt}")