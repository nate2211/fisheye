import json
from io import BytesIO

from PIL import Image
import math
import skimage.morphology
import skimage.measure
import numpy as np
from django.core.files import File


class Queue:
    def __init__(self, initNode):
        self.queue = [initNode]

    def put(self, node):
        self.queue.insert(0, node)

    def get(self):
        return self.queue.pop()

    def empty(self):
        if len(self.queue) < 1:
            return True
        else:
            return False

    def __contains__(self, other):
        return other in self.queue

    def __str__(self):
        return str(self.queue)


class RegionGrowing:
    def __init__(self, seed, path, t):
        self.seed = seed
        self.image = Image.open(path).convert('RGB').resize((300, 300))
        self.image.save("Resize.png")
        self.visited = np.zeros((300, 300))
        self.region = []
        self.av = [0, 0, 0]
        self.genAv(self.image.getpixel(seed))
        self.queue = Queue(self.seed)
        self.t = int(t)

    def genAv(self, element):
        n = len(self.region)
        e = []
        for x in range(3):
            e1 = self.av[x] * n + element[x]
            e1 = e1 / (n + 1)
            e.append(e1)
        self.av = e

    def colorCheck(self, value):
        e = 0
        for x in range(len(value)):
            e += (self.av[x] - value[x]) ** 2
        e = math.sqrt(e)
        if e < self.t:
            return True
        else:
            return False

    def regionGrow(self):
        while not self.queue.empty():
            node = self.queue.get()
            if self.visited[node[0]][node[1]] == 0:
                self.visited[node[0]][node[1]] = 1
                if self.colorCheck(self.image.getpixel(node)) and node not in self.region:
                    self.region.append(node)
                    self.genAv(self.image.getpixel(node))
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            if -1 < node[0] + j < 300 and -1 < node[1] + i < 300:
                                if (node[0] + j, node[1] + i) not in self.queue and self.visited[node[0] + j][
                                    node[1] + i] == 0:
                                    self.queue.put((node[0] + j, node[1] + i))

    def boundingBox(self):
        newImage = Image.new('L', (300, 300))
        xmin = 600
        xmax = 0
        ymin = 600
        ymax = 0
        for point in self.region:
            x = point[0]
            y = point[1]
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y
        for point in self.region:
            newImage.putpixel(point, 255)

        crop = newImage.crop((xmin, ymin, xmax, ymax))
        crop = crop.convert('L')

        cropt = skimage.morphology.closing(np.asmatrix(crop))
        crop = Image.fromarray(cropt, 'L')
        crop.thumbnail((150, 150), Image.ANTIALIAS)
        newimage_io = BytesIO()
        crop.save(newimage_io, 'JPEG', quality=85)
        newimage = File(newimage_io, name='output.jpeg')
        return newimage


def ImagetoUint8(path):
    a = []
    image = Image.open(path).resize((300,300))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            data = image.getpixel((x,y))
            for d in data:
                a.append(d)
            a.append(255)
    a = json.dumps(a)
    return a

def boundingBox(region):
    xmin = 600
    xmax = 0
    ymin = 600
    ymax = 0
    image = Image.new('L', (300, 300))
    for point in region:
        x = point[0]
        y = point[1]
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    for point in region:
        image.putpixel(point, 255)
    crop = image.crop((xmin, ymin, xmax, ymax))
    crop = crop.convert('L')

    cropt = skimage.morphology.closing(np.asmatrix(crop))
    crop = Image.fromarray(cropt, 'L')
    crop.thumbnail((150, 150), Image.ANTIALIAS)
    newimage_io = BytesIO()
    crop.save(newimage_io, 'JPEG', quality=85)
    newimage = File(newimage_io, name='output.jpeg')
    return newimage


def canvasRectPoints(path):
    image = Image.open(path).resize((100,100))

    data = {}
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            colors = ""
            for c in image.getpixel((x, y)):
                colors += str(str(c) + " ")
            data[str((x, y))] = colors

    return json.dumps(data)