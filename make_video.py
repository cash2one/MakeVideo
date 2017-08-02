"""
Script to create the movie
"""
import random 
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
from newspaper import Article


def create_movie(lang_choice, url, directory):

    path_directory = 'videos/' + directory
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    
    # RESOLUTION
    W = 1280
    H = 720
    moviesize = W, H

    article = Article(url)
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
    description =  txt_nowrap[:500].replace('\n\n', '\n')
    print('Text >> ' + description + "...\n")
    txt = '\n'.join(textwrap.wrap(txt_nowrap, 60)).replace("  ", " ")

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
    title_txt = TextClip(title,color='white', bg_color='red', align='Center', fontsize=40, font='Droid Sans', method='label').margin(top=5, opacity=0)
    
    # SCROLL THE TEXT IMAGE BY CROPPING A MOVING AREA
    txt_speed = 8
    fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+int(H*90/100),:]
    moving_txt = clip_txt.fl(fl, apply_to=['mask'])

    # BACKGROUND IMAGE, DARKENED AT 60%
    background_image = ImageClip('background.jpg')
    background_darkened = background_image.fl_image(lambda pic: (0.6*pic).astype('int16'))

    print('Number of images >> ' + str(len(list_images)))

    list_images_new = []
    files_folder_background = os.listdir('background')
    for i in range(15):
        random_number = random.randint(0, len(files_folder_background))
        list_images_new.append('background/' + files_folder_background[random_number-1])

    list_images_new.append('background.jpg')
    # for i in range (len(list_images)):
    #     filepath = 'tmp/' + list_images[i]
    #     size = int(os.stat(filepath).st_size)
    #     width = 0
    #     try:
    #         im = Image.open(filepath)
    #         width = int(im.size[0])
    #     except:
    #         pass
    #     if size > 25000 and width > 600:
    #         list_images_new.append(filepath)

    timing_duration = int(audio_length/len(list_images_new))
    print('Timing Duration >> ' + str(timing_duration))
    print('New number of images >> ' + str(len(list_images_new)))

    logo = ImageClip('logo_' + lang_choice + '.png').set_position(('left','center'))
    clips = []
    for j in range (len(list_images_new)):
        print(list_images_new[j])
        slide = ImageClip(list_images_new[j]).set_duration(timing_duration).set_start(timing_duration * j).set_position('center').crossfadein(.3)
        clips.append(slide)

    clips.append(moving_txt.set_position(('center','bottom')).margin(bottom=15, opacity=0))
    clips.append(title_txt.set_position(('center','top')))
    clips.append(logo)
    videoclip = CompositeVideoClip(clips, moviesize)

    videoclip.set_duration(audio_length).write_videofile(path_directory + '/' + title + ".avi", fps=5, codec='libx264', 
            audio='mp3/' + title + '.mp3', audio_codec='aac', temp_audiofile='mp3/' + title +'.mp3', remove_temp=True)

    print('Title >> ' + title)
    print('Keywords >> ' + list_keywords)
    description_to_save = "URL = " + url + '\n\n' + '*' * 70 + "\n\nTITLE = " + title + '\n\n' + '*' * 70 + '\n\nDESCRIPTION = ' + \
                            description + '\n\n' + '*' * 70  + '\n\nKEYWORDS =  ' + list_keywords + '\n\n' + '*' * 70 + '\n\nTIMING for ADS = ' + \
                            "0:10, 0:20, 0:30, 0:40, 0:50, 1:00"

    # SAVE Url, Title, Description, Keywords to file TXT
    file = open(path_directory + '/' + title + ".txt","w") 
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


if __name__ == "__main__":
    # lang_choice = 'vi' en-us
    # python make_video vi ALL <link for all> == download all links in URL
    # python make_video vi LIST <filename.txt> == download all links in file list_download.txt
    # python make_video vi LINK <link>== download ONLY 1 link in argv3
    if len(sys.argv) > 1:    
        lang_choice = sys.argv[1]
        print('Language >> ' + lang_choice)
        arg_type = sys.argv[2]
        try:
            directory = sys.argv[3]
        except:
            pass

        if arg_type == 'ALL':
            import newspaper
            paper = newspaper.build(url, memoize_articles=False)
            directory = 'ALL'
            for article in paper.articles:
                print(article.url)
                try:
                    create_movie(lang_choice, article.url.strip(), directory)
                except:
                    continue
        elif arg_type == 'LIST':
            file = open(directory + '.txt', 'r')
            list_download = file.readlines()
            file.close()
            for i in range(len(list_download)):
                print(list_download[i])
                try:
                    create_movie(lang_choice, list_download[i].strip(), directory)
                except:
                    continue
        elif arg_type == 'LINK':
            url = directory
            create_movie(lang_choice, url.strip(), directory)
