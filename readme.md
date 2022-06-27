# License Plate Recognizer (Argentina)

This weekend I set a goal to make a license plate recognizer in 2 days. This is my first image processing project. I've worked with most of the libraries featured on this project before, but for smaller and different things. This is a simple solution, using a very curated set of images (good quality, parked cars, good lighting, etc.). I'm being not so careful with the image filters, thresholds, and the filtering of the contours since I just wanted to learn how all this works- if I wanted to make it work for a bigger quantity of pictures I know exactly which parts I would have to nitpick, and I don't think it's worth it. Now let's get to the procedure.

Let's use this picture as an example.

<img src="https://i.imgur.com/QNRVydN.png"  width="300"/>

First step is turning it into a grayscale image:

<img src="https://i.imgur.com/EnT7oVB.png"  width="300"/>

Now we can apply a threshold to it, and look how defined the license plate looks:

<img src="https://i.imgur.com/fCcV6Pw.png"  width="300"/>

Then using opencv we detect the contours:

<img src="https://i.imgur.com/nkhSpCz.png"  width="300"/>

And now we filter them by aspect ratio, width and height. In 21 of the 25 pictures that was enough for keeping just the license plate contours, but in 4 cases like the one below 2 contours were kept. In all of those cases the license plate was below the other shape, so I decided to just keep the lowest one.

<img src="https://i.imgur.com/gT2ozsd.png"  width="300"/>

Now we can crop the license plate out of the image:

<img src="https://i.imgur.com/wOX0ENr.png"  width="300"/>

And once again grayscale it and apply a threshold

<img src="https://i.imgur.com/iWI84zN.png"  width="300"/>

Now using an skimage function we remove the borders, invert the image, and this is the final result:

<img src="https://i.imgur.com/3lxtMvb.png"  width="300"/>

We can already feed this picture to pytesseract and it succesfully recognizes the characters.
