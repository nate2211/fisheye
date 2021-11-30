from PIL import Image
import numpy as np
import math
import skimage.morphology
import skimage.measure
import os

import matplotlib.pyplot as plt

    
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
        self.av = [0,0,0]
        self.genAv(value, [])
    def genAv(self, element, region):
        n  = len(region)
        e = []
        for x  in range(3):
            e1 = self.av[x] * n + element[x]
            e1 = e1 / (n + 1)
            e.append(e1)
        self.av = e
        
        
class RegionGrowing():
    def __init__(self, seeds, path, t, colors):
        self.image = Image.open(path).convert('RGB').resize((300,300))
        self.seed = [SeedPoint(x, self.image.getpixel(x)) for x in seeds]
        self.visited = np.zeros((300,300))
        self.regions = []
        self.region = []
        self.queue = Queue()
        self.t = t
        self.data = {}
        self.aRegion = []
        self.colors = colors

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
                        for j in range(-1,2):
                            for i in range(-1,2):
                                if -1 < node[0] + j < 300 and -1 < node[1] + i < 300:
                                    if (node[0] + j, node[1] + i) not in self.queue and self.visited[node[0] + j][node[1] + i] == 0:
                                        self.queue.put((node[0] + j, node[1] + i))
            self.regions.append(self.region)
            self.region = []

    
    def total(self,lists):
        arr = []
        for l in lists:
            arr = arr + l
        return list(dict.fromkeys(arr))
    

    def uniqueRegions(self):
        points = {}
        r = 0
        for region in self.regions:
            for point in region:
                try:
                    points[point] = r
                except KeyError:
                    pass
            r += 1
        return points                

    def outPut(self):
        newImage = Image.new('RGB', (300, 300))
        n = 0
        self.aRegion = self.total(self.regions)
        points = self.uniqueRegions()
        for region in self.regions:
            self.data[n] = region
            for point in region:
                color = points[point]
                newImage.putpixel(point, self.colors[color])
            n += 1
              
        return newImage
    
class BoundingBox():
    def __init__(self, image, region):
        self.image = image
        self.region = region
        self.crop = None
        
        
    def closing(self, image):
        ne = [(0,1), (1, 0), (-1, 0), (0, -1), (1,1), (-1,-1), (1, -1), (-1, 1)]
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                nes = []
                if image.getpixel((x,y)) == (0,0,0):
                    for n in ne:
                        nx = x + n[0]
                        ny = y + n[1]
                        if -1 < nx < image.size[0] and -1 < ny < image.size[1]:
                            if image.getpixel((nx, ny)) != (0,0,0):
                                nes.append((nx,ny))
                        if len(nes) > 3:
                            image.putpixel((x, y), (255,255,0))
                            
                            
    def boundingBox(self, op):
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
      
        if crop.size[0] < crop.size[1]:
            crop.rotate(90)
        crop.thumbnail((100,50), Image.ANTIALIAS)
        self.crop = crop

    
class Data():
    def __init__(self, image, colors, labels):
        self.image = image
        self.norm = []
        self.colors = colors
        self.inert = None
        self.labels = labels
        self.distances = {}
    def doNorm(self):
        
        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                if self.image.getpixel((x,y)) in self.colors or self.image.getpixel((x,y)) == (255,255,255) or self.image.getpixel((x,y)) == (255,255,0):
                    self.norm.append((x / self.image.size[0], y / self.image.size[1]))

    

    def bigShow(self):
        temp = self.image.resize((1000, 1000))
        temp.show()
   
        
   
    def calcLabel(self, data):
        currentDistance = 1000000
        currentLabel = None
        self.distances = {}
        for label in self.labels:
            arr = data.data[label]
            for element in arr:
                ex = (self.inert[0] - float(element[0]))**2
                ey = (self.inert[1] - float(element[1]))**2
                distance = math.sqrt(ex + ey)
                try:
                    self.distances[label].append(distance)
                except KeyError:                    
                    self.distances[label] = [distance] 


        
        for label in self.labels:
            a = self.distances[label]
            currentAvg = sum(a) / len(a)
            if  currentAvg < currentDistance:
                currentDistance = currentAvg
                currentLabel = label
        

        return currentLabel
                    
        
        
    def query(self, n, data):
        ir = []
        coors = {}
        self.distances = {}
        for label in self.labels:
            arr = data.data[label]
            for element in arr:
                ex = (self.inert[0] - float(element[0]))**2
                ey = (self.inert[1] - float(element[1]))**2
                distance = math.sqrt(ex + ey)
                self.distances[distance] = label
                coors[distance] = (element[0], element[1])
                ir.append(distance)
                    
        ir = sorted(ir)
            
        
            
       
        output = []
        for x in range(n):
            output.append((self.distances[ir[x]], ir[x], data.images[coors[ir[x]]]))
        
        return output  
        
                   
    def inertia(self):
        self.inert = skimage.measure.inertia_tensor_eigvals(np.asarray(self.norm))
        return self.inert



class DataArray():
    
    def __init__(self):
        self.data={}
        self.images = {}
    

        
    
    def __str__(self):
        s = []
        for label, element in self.data.items():
            s.append([label, element])
        return str(s)
    def addToData(self, element):
        label = element[0]
        coors = (float(element[1]), float(element[2]))
        self.images[coors] = element[3]
        try:
            self.data[label].append(coors)
        except KeyError:
            self.data[label] = [coors]
            
def splitLine(line):
   a = line.split("|")
   
   a[len(a) - 1] = a[len(a) - 1].replace("\n", "")
   return a



def doFullDir(iPath, labels):
    label = input("Label: ")
    paths = os.listdir(iPath)
    os.chdir(iPath)
    for path in paths:
        resize = Image.open(path).resize((300,300))
        os.chdir("../")
        resize.save("resize.png")
        os.chdir(iPath)
        redo = "y"
        plt.imshow(np.asarray(resize), cmap="Greys", interpolation="None")
        plt.show(block=False)
    
        while redo == "y":
            nSeed = int(input("How Many Seed Points: "))
            points = []
            colors = []
            for n in range(nSeed):
                x = int(input("X Coors: "))
                y = int(input("Y Coors: "))
                color = input("Color of Region: ")
                points.append((x,y))
                colors.append(tuple(map(int, color.split(', '))))
            redoT = 'y'
            while redoT == 'y':
                t = int(input("Threshold Value "))
                regiongrow = RegionGrowing(points, path, t, colors)
                regiongrow.regionGrow()
                image = regiongrow.outPut()
                image.show()
                box = BoundingBox(image, regiongrow.aRegion)
                s = input("SkiImage Closing y/n: ")
                redoT = input("Redo T: y/n")
            
            op = False
            if s == "y":
                op = True
            box.boundingBox(op)
            box.crop.show()
            redo = input("Redo: y/n: ")
        
        data = Data(box.crop,  colors, labels)
        data.doNorm()
        i = data.inertia()
        label = label
        name = str(str(os.path.splitext(path)[0]) + ".png")
        os.chdir("../")
        os.chdir("database")
        if not os.path.isdir(str(label)):
            os.mkdir(str(label))
            
        
        os.chdir(str(label))    
        data.image.save(name)

        os.chdir("../../")
        with open("database/data.txt", 'a') as f:
            f.write(str(str(label) + "|" + str(i[0]) + "|" + str(i[1]) + "|" + str(name) + "\n"))
            f.close()
        os.chdir(iPath)





def main(labels):
    path = input("Image Path: ")
    resize = Image.open(path).resize((300,300))
    resize.save("resize.png")
    plt.imshow(np.asarray(resize), cmap="Greys", interpolation="None")
    plt.show(block=False)

    redo = "y"
    while redo == "y":
        nSeed = int(input("How Many Seed Points: "))
        points = []
        colors = []
        for n in range(nSeed):
            x = int(input("X Coors: "))
            y = int(input("Y Coors: "))
            color = input("Color of Region: ")
            points.append((x,y))
            colors.append(tuple(map(int, color.split(', '))))
        redoT = 'y'
        while redoT == 'y':
            t = int(input("Threshold Value "))
            regiongrow = RegionGrowing(points, path, t, colors)
            regiongrow.regionGrow()
            image = regiongrow.outPut()
            image.show()
            box = BoundingBox(image, regiongrow.aRegion)
            s = input("SkiImage Closing y/n: ")
            redoT = input("Redo T: y/n")
           
        op = False
        if s == "y":
            op = True
            
        box = BoundingBox(image, regiongrow.aRegion)
        box.boundingBox(op)
        box.crop.show()
        redo = input("Redo: y/n: ")
        
    data = Data(box.crop,  colors, labels)
    data.doNorm()
    i = data.inertia()
    label = input("Assign Label (Label/n): ")
    if label == "n":
        label = data.calcLabel(dataA)
        print('Calc Label: ', label)
        o = input('OverWrite y/n:')
        if o == 'y':
            label = input("Assign Label") 
    else:
        if label not in labels:
            os.chdir("database")
            os.mkdir(label)
            os.chdir("../")
    name = input("Name Of File: ")
    
    os.chdir("database")
    if not os.path.isdir(str(label)):
        os.mkdir(str(label))
        
    
    os.chdir(str(label))    
    data.image.save(str(name + ".png"))
    query = input("Query y/n:")
    if query == "y":
        queryN = int(input("How Many Results: "))
        print(data.query(queryN, dataA))
    os.chdir("../../")
    with open("database/data.txt", 'a') as f:
        f.write(str(str(label) + "|" + str(i[0]) + "|" + str(i[1]) + "|" + str(name) + ".png" + "\n"))
        f.close()    


if __name__ == "__main__":
    dataA = DataArray()
    labels = [x for x in os.listdir("database") if not x.endswith(".txt")]
    with open("database/data.txt") as d1:
        lines = d1.readlines()
        if len(lines) == 0:
            d1.close()
        else:
            for line in lines:
                a = splitLine(line)
                if len(a) > 1:
                    dataA.addToData(a)
        d1.close()

    
    d = input("Do Full Dir y/n: ")
    if d == 'y':
        path = input("Path: ")
        doFullDir(path, labels)
    else: 
        main(labels)



