import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import json
from PIL import Image


class DataArray():
    
    def __init__(self):
        self.data={}
    
    def addToData(self, element):
        label = element[0]
        coors = (element[1], element[2])
        try:
            self.data[label].append(coors)
        except KeyError:
            self.data[label] = [coors]
            

            
def splitLine(line):
   a = line.split("|")
   
   a[len(a) - 1] = a[len(a) - 1].replace("\n", "")
   return a


images = []
plt.rcParams["figure.figsize"] = [25,25]
plt.rcParams["figure.autolayout"] = True

data = DataArray()

with open("database/data.txt") as d1:
    lines = d1.readlines()
    if len(lines) == 0:
        d1.close()
    else:
        for line in lines:
            a = splitLine(line)
            data.addToData(a)
    d1.close()

labels = [x for x in os.listdir("database") if not x.endswith(".txt")]

paths = [ [] for x in range(len(labels))]
os.chdir("database")
for label in labels:    
    os.chdir(label)
    paths = os.listdir()
    os.chdir("../")
    
os.chdir("../")

def getImage(path):
    return OffsetImage(plt.imread(path, format="png"))
 
xcoors = []
ycoors = []

for label, arr in data.data.items():
    for coors in arr:
        xcoors.append(int(coors[0]))
        ycoors.append(int(coors[1]))


mx = max(xcoors)
my = max(ycoors)
xN = []
yN = []

for i, j in zip(xcoors, ycoors):
    xN.append(i / mx)
    yN.append(j / my)

fig, ax = plt.subplots()
for x0, y0, path in zip(xN, yN, paths):
   print(y0)    
   ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
   ax.add_artist(ab)

plt.show()