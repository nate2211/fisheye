import json
from io import BytesIO

from PIL import Image
import math
import skimage.morphology
import skimage.measure
import numpy as np
from django.core.files import File


class Queue:
    def __init__(self):
        self.queue = []

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


class SeedPoint():
    def __init__(self, seed, value):
        self.seed = seed
        self.value = value
        self.av = [0, 0, 0]
        self.genAv(value, [])

    def genAv(self, element, region):
        n = len(region)
        e = []
        for x in range(3):
            e1 = self.av[x] * n + element[x]
            e1 = e1 / (n + 1)
            e.append(e1)
        self.av = e


class RegionGrowing():
    def __init__(self, seeds, path, t):
        self.image = Image.open(path).convert('RGB').resize((300, 300))
        self.seed = [SeedPoint(x, self.image.getpixel(x)) for x in self.load(seeds)]
        self.visited = np.zeros((300, 300))
        self.regions = []
        self.region = []
        self.queue = Queue()
        self.t = t
        self.data = {}
        self.aRegion = []
    def load(self, seeds):
        jsonSeed = json.loads(seeds)
        seeds = []
        for x in jsonSeed:
            x = str(x)
            x = x.replace("[", "")
            x = x.replace("]", "")
            x = x.replace("'", "")
            x = x.replace("(", "")
            x = x.replace(")", "")
            a = x.split(",")
            seeds.append((int(a[0]), int(a[1])))
        print(seeds)
        return seeds

    def colorCheck(self, value, seedAv):
        e = 0
        for x in range(len(value)):
            e += (seedAv[x] - value[x]) ** 2
        e = math.sqrt(e)
        if e < self.t:
            return True
        else:
            return False

    def regionGrow(self):
        for seedPoint in self.seed:
            self.queue.put(seedPoint.seed)
            while not self.queue.empty():
                node = self.queue.get()
                if self.visited[node[0]][node[1]] == 0:
                    self.visited[node[0]][node[1]] = 1
                    if self.colorCheck(self.image.getpixel(node), seedPoint.av) and node not in self.region:
                        self.region.append(node)

                        seedPoint.genAv(self.image.getpixel(node), self.region)
                        for j in range(-1, 2):
                            for i in range(-1, 2):
                                if -1 < node[0] + j < 300 and -1 < node[1] + i < 300:
                                    if (node[0] + j, node[1] + i) not in self.queue and self.visited[node[0] + j][
                                        node[1] + i] == 0:
                                        self.queue.put((node[0] + j, node[1] + i))
            self.regions.append(self.region)
            self.region = []
        self.aRegion = self.total(self.regions)

    def total(self, lists):
        arr = []
        for l in lists:
            arr = arr + l
        return list(dict.fromkeys(arr))

    def outPut(self):
        newImage = Image.new('RGB', (300, 300))
        n = 0
        self.aRegion = self.total(self.regions)
        for region in self.regions:
            self.data[n] = region
            for point in region:
                newImage.putpixel(point, (255,255,255))
        n += 1

        return newImage


class BoundingBox():
    def __init__(self, image, region):
        self.image = image
        self.region = region
        self.crop = None

    def closing(self, image):
        ne = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                nes = []
                if image.getpixel((x, y)) == (0, 0, 0):
                    for n in ne:
                        nx = x + n[0]
                        ny = y + n[1]
                        if -1 < nx < image.size[0] and -1 < ny < image.size[1]:
                            if image.getpixel((nx, ny)) != (0, 0, 0):
                                nes.append((nx, ny))
                        if len(nes) > 3:
                            image.putpixel((x, y), (255, 255, 0))


    def boundingBox(self, op = False):
        xmin = 10000
        xmax = 0
        ymin = 10000
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

        crop = self.image.crop((xmin, ymin, xmax, ymax)).convert('RGB')
        if op:
            cropA = skimage.morphology.closing(np.asarray(crop))
            crop = Image.fromarray(cropA, 'RGB')
        else:
            self.closing(crop)

        crop.thumbnail((1000, 1000), Image.ANTIALIAS)
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