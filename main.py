import os
from PIL import Image, ImageStat
from shutil import copyfile


def detect_color_image(file, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    pil_img = Image.open(file)
    bands = pil_img.getbands()
    if bands == ('R', 'G', 'B') or bands == ('R', 'G', 'B', 'A'):
        thumb = pil_img.resize((thumb_size, thumb_size))
        SSE, bias = 0, [0, 0, 0]
        if adjust_color_bias:
            bias = ImageStat.Stat(thumb).mean[:3]
            bias = [b - sum(bias) / 3 for b in bias]
        for pixel in thumb.getdata():
            mu = sum(pixel) / 3
            SSE += sum((pixel[i] - mu - bias[i]) * (pixel[i] - mu - bias[i]) for i in [0, 1, 2])
        MSE = float(SSE) / (thumb_size * thumb_size)
        if MSE <= MSE_cutoff:
            return "grayscale"
        else:
            return "color"
    elif len(bands) == 1:
        return "black_white"
    else:
        return "don't_know"


if __name__ == '__main__':
    imagesPath = "pictures"
    images = os.listdir("pictures")

    if not os.path.exists("color"):
        os.mkdir("color")

    if not os.path.exists("black_white"):
        os.mkdir("black_white")

    for image in images:
        result = detect_color_image("{}/{}".format(imagesPath, image))

        if result == "grayscale" or result == "black_white":
            copyfile("{}/{}".format(imagesPath, image), "black_white/{}".format(image))
        elif result == "color" or result == "don't_know":
            copyfile("{}/{}".format(imagesPath, image), "color/{}".format(image))

