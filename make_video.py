"""
Script to create the movie
"""
import os
import shutil
import sys
#import datetime
from PIL import Image
from gtts import gTTS
from mutagen.mp3 import MP3
import urllib.request
from moviepy.editor import *
import textwrap
from moviepy.video.tools.drawing import color_gradient
#import numpy as np
from skimage import transform as tf


# RESOLUTION
W = 1280
H = 720
moviesize = W, H
lang_choice = 'en-us'
if len(sys.argv) > 1:
    from newspaper import Article
    try:
        lang_choice = sys.argv[1]
    except:
        pass
    try:
        url = sys.argv[2]
    except:
        pass
    print('Language >> ' + lang_choice)
    article = Article(url)
else:
    import newspaper
    paper = newspaper.build('http://cnn.com', memoize_articles=False)
    article = paper.articles[0]
article.download()
article.parse()
authors = article.authors
title = article.title
top_image = article.top_image
images = article.images

list_images = []
j = 0
for i in images:
    try:
        j += 1
        filename = str(j) + '.jpg'
        urllib.request.urlretrieve(i, 'tmp/' + filename)
        list_images.append(filename)
    except:
        if j > 0:
            j =- 1
        continue

try:
    article.nlp()
except:
    print('Error NLP')
    pass

keywords = article.keywords
list_keywords = ', '.join(keywords)

txt_nowrap = article.text
description =  txt_nowrap[:500]
print('Text >> ' + description + "...\n")
txt = '\n'.join(textwrap.wrap(txt_nowrap, 70)).replace("  ", " ")

# Add blanks
txt = 10*"\n" + txt + 10*"\n"

if os.path.exists('mp3/' + title + '.mp3') is False:
    if txt_nowrap != '':
        tts = gTTS(text=txt_nowrap, lang=lang_choice)
        tts.save('mp3/' + title + ".mp3")

try:
    audio = MP3('mp3/' +title + ".mp3")
    audio_length = int(audio.info.length)
except:
    pass

# CREATE THE TEXT IMAGE
clip_txt = TextClip(txt,color='white', bg_color='black' ,align='Center', fontsize=20, font='Droid Sans', method='label')
title_txt = TextClip(title,color='white', bg_color='red', align='Center', fontsize=32, font='Droid Sans', method='label')
# SCROLL THE TEXT IMAGE BY CROPPING A MOVING AREA
txt_speed = 8
fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+int(H),:]
moving_txt = clip_txt.fl(fl, apply_to=['mask'])


# BACKGROUND IMAGE, DARKENED AT 60%
background_image = ImageClip('background.jpg')
background_darkened = background_image.fl_image(lambda pic: (0.6*pic).astype('int16'))


#clips.append(background_image)
print('Number of images >> ' + str(len(list_images)))
list_images_new = []
list_images_new.append('background.jpg')
for i in range (len(list_images)):
    filepath = 'tmp/' + list_images[i]
    size = int(os.stat(filepath).st_size)
    width = 0
    try:
        im = Image.open(filepath)
        width = int(im.size[0])
    except:
        pass
    if size > 15000 or width > 400:
        list_images_new.append(filepath)


timing_duration = int(audio_length/len(list_images_new))
print('Timing Duration >> ' + str(timing_duration))
print('New number of images >> ' + str(len(list_images_new)))

clips = []
for j in range (len(list_images_new)):
    slide = ImageClip(list_images_new[j]).set_duration(timing_duration).set_start(timing_duration * j).set_pos(lambda t: ('center', 50+t) ).crossfadein(.3)
    clips.append(slide)

clips.append(moving_txt.set_pos(('center', 'bottom')))
clips.append(title_txt.set_pos(('center','top')))
videoclip = CompositeVideoClip(clips, moviesize)
videoclip.set_duration(audio_length).write_videofile('videos/' + title + ".avi", fps=5, codec='libx264', 
        audio='mp3/' + title + '.mp3', audio_codec='aac', temp_audiofile='mp3/' + title +'.mp3', remove_temp=True)

print('Title >> ' + title)
print('Keywords >> ' + list_keywords)
description_to_save = "TITLE = " + title + '\n\n' + '*' * 70 + '\n\nDESCRIPTION = ' + description + '\n\n' + '*' * 70  + '\n\nKEYWORDS =  ' + list_keywords + '\n'

file = open("videos/" + title + ".txt","w") 
file.write(description_to_save) 
file.close() 

#UPLOAD
#os.system('python filename.py')

# DELETE TEMPORY FILES IMAGES
folder = 'tmp'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)
