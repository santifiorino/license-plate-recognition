import numpy as np
import cv2
import pytesseract
import skimage
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

class LPR:
    def __init__(self, min_w=80, max_w=110, min_h=25, max_h=52, ratio=3.07692307692):
        self.min_w = min_w
        self.max_w = max_w
        self.min_h = min_h
        self.max_h = max_h
        self.ratio = ratio

    def grayscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def apply_threshold(self, img):
        return cv2.threshold(img, 170, 255, cv2.THRESH_BINARY_INV)[1]

    def apply_adaptive_threshold(self, img):
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)

    def find_contours(self, img):
        return cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    def filter_candidates(self, contours):
        candidates = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if (np.isclose(aspect_ratio, self.ratio, atol=0.7) and
               (self.max_w > w > self.min_w) and
               (self.max_h > h > self.min_h)):
                candidates.append(cnt)
        return candidates

    def get_lowest_candidate(self, candidates):
        ys = []
        for cnt in candidates:
            x, y, w, h = cv2.boundingRect(cnt)
            ys.append(y)
        return candidates[np.argmax(ys)]

    def crop_license_plate(self, img, license):
        x, y, w, h = cv2.boundingRect(license)
        return img[y:y+h,x:x+w]

    def clear_border(self, img):
        return skimage.segmentation.clear_border(img)

    def invert_image(self, img):
        return cv2.bitwise_not(img)

    def read_license(self, img, psm=7):
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(alphanumeric)
        options += " --psm {}".format(psm)

        gray = self.grayscale(img)
        thresh = self.apply_threshold(gray)
        contours = self.find_contours(thresh)
        candidates = self.filter_candidates(contours)
        if candidates:
            license = candidates[0]
            if len(candidates) > 1:
                license = self.get_lowest_candidate(candidates)
            cropped = self.crop_license_plate(gray, license)
            thresh_cropped = self.apply_adaptive_threshold(cropped)
            clear_border = self.clear_border(thresh_cropped)
            final = self.invert_image(clear_border)
            txt = pytesseract.image_to_string(final, config=options)
            return txt
        else:
            return "No license plate found"