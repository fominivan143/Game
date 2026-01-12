from PIL import Image


class Theft:
    def __init__(self, n):
        self.n = n

    def blue_ray(self):
        im = Image.open(self.n)
        pixels = im.load()
        x, y = im.size
        for i in range(x):
            for j in range(y):
                r, g, b = pixels[i, j]
                b = min(255, round(b + r / 3, 0))
                r = r - r / 3
                pixels[i, j] = (r, g, b)
        return self.n

    def right_strip(self, width):
        im = Image.open(self.n)
        x, y = im.size
        im2 = im.crop((x - width, y, x, 0.75 * y))
        im3 = im.crop((x - width, 0.75 * y, x, 0.5 * y))
        im4 = im.crop((x - width, 0.5 * y, x, 0.25 * y))
        im5 = im.crop((x - width, 0.25 * y, x, 0))
        img = Image.new('RGB', (256, 256 * 4))
        img.paste(im3, (0, 0))
        img.paste(im2, (0, 256))
        img.paste(im5, (0, 256 * 2))
        img.paste(im4, (0, 256 * 3))
        img.show()
        return img

    def save(self, image, out_filename):
        image.save(out_filename)


th = Theft('image.jpg')
th.save(th.right_strip(400), 'result.png')









