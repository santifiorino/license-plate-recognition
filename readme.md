# License Plate Recognizer (Argentina)

I set the goal of making a license plate recognizer in a weekend. This is my first image processing project. It's a simple solution, using a very curated set of images (good quality, parked cars, good lighting, etc.). I'm being not so careful with the image filters, thresholds, and the filtering of the contours, since I just wanted to learn the processes and workflow- if I wanted to make it work for a real project, now I know exactly how to approach it and which parts I would have to nitpick. Now let's get to the procedure.

Let's use this picture as an example.

<img src="https://i.imgur.com/QNRVydN.png"  width="300"/>

First step is turning it into a grayscale image:

```python
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

<img src="https://i.imgur.com/EnT7oVB.png"  width="300"/>

Now we apply a threshold. This time I used hard-coded parameters, but in a real-world scenario I would have to be careful in this step. Notice how defined the license plate looks after the threshold:

```python
def apply_threshold(self, img):
    return cv2.threshold(img, 170, 255, cv2.THRESH_BINARY_INV)[1]
```

<img src="https://i.imgur.com/fCcV6Pw.png"  width="300"/>

Then using OpenCV we detect the contours:

```python
def find_contours(self, img):
        return cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
```

<img src="https://i.imgur.com/nkhSpCz.png"  width="300"/>

And now we filter them by aspect ratio, width and height. I searched for the real width and height of the license plates, and calculated the aspect ratio. With these filters, we end up with only one contour, that being the license plate.

<img src="https://i.imgur.com/cW1u9Up.png"  width="300"/>

Now we can crop the license plate out of the image:

```python
def crop_license_plate(self, img, license):
    x, y, w, h = cv2.boundingRect(license)
    return img[y:y+h,x:x+w]
```

<img src="https://i.imgur.com/wOX0ENr.png"  width="300"/>

Once again, grayscale it and apply a threshold:

<img src="https://i.imgur.com/iWI84zN.png"  width="300"/>

Now using an skimage function we remove the borders, invert the image, and this is the final result:

```python
def clear_border(self, img):
    return skimage.segmentation.clear_border(img)

def invert_image(self, img):
    return cv2.bitwise_not(img)
```

<img src="https://i.imgur.com/3lxtMvb.png"  width="300"/>

We can already feed this picture to pytesseract and it succesfully recognizes the characters.
