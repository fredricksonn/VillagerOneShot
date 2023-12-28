# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:18:24 2023

@author: Nathan
"""

import json
from PIL import Image, ImageDraw, ImageFont
from os.path import isfile, isdir
from os import mkdir

Lratio = 1
Sratio = 2.5/3.5
maxRes = 600
fontSize = 18
fontSizeTitle = 32
fontPad = 10

fontFile= ".\middle-earth-font\Middleearth-ao6m.ttf"
fontReg = ImageFont.truetype(fontFile, size=fontSize)
fontTitle = ImageFont.truetype(fontFile, size=fontSizeTitle)

width = int(maxRes * Lratio)
height = int(maxRes * Sratio)

# categories
traits = ['occupation', 'race', 'level', 'proficiency', 'speed' ]
weapons = ['weapon1', 'weapon2']
health = ['armor', 'hp', 'ac']

f = open('Characters.json')
characterData = json.load(f)["characters"]

outputDir = 'CharacterCards\\'
if not isdir(outputDir):
    mkdir(outputDir)

def isNumber(var):
    return type(var) in [float, int]

def placeNumber(m,f,img):
    tW, _ = img.textsize(m,font=f)
    return tW

def calcPoints(x,y,w,h):
    maxX = x+w
    maxY = y+h
    # 0 = upper left
    #given
    # 1 = upper right
    # 2 = lower left
    # 3 = lower right  
    return (x,y),(maxX,y),(x,maxY),(maxX,maxY)

def combineTuples(a,b):
    return (a[0], a[1], b[0], b[1])

def drawBox(x,y,w,h,d):
    points = calcPoints(x,y,w,h)
    d.line(combineTuples(points[0], points[1]))
    d.line(combineTuples(points[0], points[2]))
    d.line(combineTuples(points[1], points[3]))
    d.line(combineTuples(points[2], points[3]))
    return d

def centeredCoordinates(m,f,img):
    tW, tH = img.textsize(m,font=f)
    xText = (width-tW) / 2
    yText = (height-tH) / 2

    return xText,yText

def getPortrait(race=None,job=None):
    filename = '.\\images\\' + race + '\\' + job + '\\portrait1.png'
    if not isfile(filename):    
        filename = '.\images\Whos-That-Pokemon-1.jpg'
    return filename

def createCard(data, fname='default', fext='.png'):
    img = Image.new('RGB', (width, height), color='white')
    img = Image.open('.\images\scroll.jpg').resize((width, height))
    portrait = Image.open(getPortrait(data['race'],data['occupation'])).resize((200, 200))
    
    img.paste(portrait,(40,215))
    imgDraw = ImageDraw.Draw(img)
    vertOffset = 15

    # name
    key='name'
    message = data[key] + '__________'
    font = fontTitle
    cX, _ = centeredCoordinates(message, font, imgDraw)
    imgDraw.text((cX*.75, vertOffset), message, fill=(0, 0, 0), font=font)

    vertOffset += fontSizeTitle + fontPad*3

    # traits
    message = 'Traits'
    cX = fontPad
    font = fontReg
    imgDraw = drawBox(cX-5,vertOffset,275,125,imgDraw)
    imgDraw.text((cX, vertOffset), message, fill=(0, 0, 0), font=font)

    for i,key in enumerate(traits):
        message = key + ": " + str(data[key])
        imgDraw.text((cX, vertOffset+fontPad+(fontSize*(i+1))), message, fill=(0, 0, 0), font=font)

    # health
    message = 'Health'
    font = fontReg
    cX = fontPad + (width/2)
    imgDraw = drawBox(cX-5,vertOffset,275,95,imgDraw)
    imgDraw.text((cX, vertOffset), message, fill=(0, 0, 0), font=font)  
    rightVertOffset = vertOffset + fontSize + fontPad
    
    for i,key in enumerate(health):
        message = key + ": " + str(data[key])
        imgDraw.text((cX, vertOffset+fontPad+(fontSize*(i+1))), message, fill=(0, 0, 0), font=font)
        rightVertOffset = vertOffset+(fontSize*(i+2))
    
    vertOffset += fontPad
    rightVertOffset += fontPad*4
    # weapons
    message = 'Weapons'
    font = fontReg
    cX = fontPad + (width/2)
    
    if data['weapon2'] and data['weapon2']['name'] != '':
        boxSize = 185
    elif not data['weapon1']:
        boxSize = 75
    else:
        boxSize = 130

    imgDraw = drawBox(cX-5,rightVertOffset,275,boxSize,imgDraw)
    
    
    imgDraw.text((cX, rightVertOffset), message, fill=(0, 0, 0), font=font)  
    rightVertOffset += fontSize + fontPad
    for i,key in enumerate(weapons):
        wpn = 'none'
        if data[key]:       
            wpn = str(data[key]['name']) if data[key]['name'] != '' else 'none'
        if key == 'weapon1':
            text = 'primary'
        elif key == 'weapon2':
            text = 'secondary'
        message = text + ": " + wpn
        imgDraw.text((cX, rightVertOffset), message, fill=(0, 0, 0), font=font)
        rightVertOffset += fontSize
        if wpn != 'none':
            for ii,wpnStat in enumerate(data[key].keys()):
                if wpnStat == 'name':
                    pass
                else:
                    message = wpnStat + ": " + str(data[key][wpnStat])
                    imgDraw.text((cX+fontPad*2, rightVertOffset), message, fill=(0, 0, 0), font=font)
                    rightVertOffset += fontSize
    
    img.save(fname+fext)
    
for i,c in enumerate(characterData):
    filename = outputDir + 'c_' + str(i)
    createCard(c,filename)