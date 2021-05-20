import random

from PIL import Image


def tarnslate_photo_on_treatment(photo):
    img = Image.open(photo)
    im = Image.new('RGB', (img.size[0], 300), (255, 255, 255))

    bwidth, bheight = img.size[0], img.size[1]
    fwidth, fheight = im.size[0], im.size[1]
    x, y = 0, bheight - fheight  # в левый нижний
    img.paste(im, (x, y))

    img.save(f'/Users/macbookpro/Documents/PhotoOptimazerPy/PHOTO/TREATMENT/photo_{random.randint(0, 9999)}.jpg')

