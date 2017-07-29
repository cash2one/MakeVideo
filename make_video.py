"""
Script to create the movie
"""
import numpy as np
from skimage import transform as tf
from moviepy.editor import *
from moviepy import *
from gtts import gTTS
import os.path
from moviepy.video.tools.drawing import color_gradient

# RESOLUTION
w = 1920
h = 1080
moviesize = w, h

# THE RAW TEXT
txt = '\n\nHiện trường bít bùng khiến 8 người không kịp thoát Hiện trường bít bùng khiến 8 người không kịp thoát\n\nKhoảng 10h30, sau tiếng nổ lớn từ xưởng sản xuất bánh kẹo nằm ven quốc lộ 32, xã Đức Thượng (Hoài Đức, Hà Nội), khói lửa bốc lên nghi ngút, cao vài chục mét. Hàng chục công nhân bị mắc kẹt sau cánh cổng sắt đóng kín.\n\nCảnh sát phòng cháy chữa cháy cùng nhiều xe cứu hỏa được điều đến hiện trường. Đến khoảng 12h, đám cháy được dập tắt. Một số thi thể được đưa lên xe cứu thương chở tới bệnh viện.\n\nHiện trường vụ nổ. Ảnh: Phạm Dự.\n\nGhi nhận của phóng viên VnExpress, đến 13h55, thêm hai thi thể được đưa ra. Nhà xưởng một tầng, rộng trên 100 m3 cháy trơ trụi. Những tấm tôn lợp mái và tôn bao quanh xưởng nằm ngổn ngang, che chắn hết lối đi.\n\nThoát ra khỏi đám cháy, một nữ công nhân kể sau tiếng nổ lớn, những tấm sắt gần cửa sập xuống, bịt mất lối ra vào duy nhất. Các công nhân chạy dồn vào phía trong, bất lực nhìn lửa càng lúc càng bốc mạnh.\n\nMột nguồn tin cũng cho biết, các nạn nhân dồn vào phía cuối xưởng, "khi cảnh sát phát hiện, tất cả đang trong tư thế ôm nhau, thi thể cháy đen".\n\nNhân chứng kể lại vụ cháy\n\nĐến 15h, theo báo cáo của UBND huyện Hoài Đức, có khoảng 7-8 người tử vong do mắc kẹt trong xưởng, 2 người bị thương được đưa tới Bệnh viện huyện Đan Phượng trong tình trạng hôn mê. Nguyên nhân cháy là xưởng đang sửa chữa, thợ hàn xì làm bắn tia lửa điện vào trần gác xép được ghép bằng xốp.\n\nÔng Bùi Văn Sơn, Phó giám đốc Bệnh viện huyện Đan Phượng cho biết, khoảng 11h30, bệnh viện tiếp nhận 3 nạn nhân vụ cháy thì một người đã tử vong từ trước, hai người còn lại bỏng rất nặng, khoảng độ 3 kèm thêm bỏng hô hấp. Sau khi sơ cứu, chống sốc, các nạn nhân đã được chuyển lên Viện Bỏng Quốc gia.\n\nXưởng bị cháy chỉ có một lối ra vào duy nhất. Ảnh: Phạm Dự.\n\nXưởng bị cháy rộng 170 m2, mặt tiền khoảng 7 m, được lợp tôn, tường gạch, có một gác xép chừng 100 m2 nằm giữa một xưởng sản xuất thép và nhà dân cao 3 tầng. Cơ sở này do ông Nguyễn Văn Được (Phúc Thọ, Hà Nội) thuê đất để sản xuất bánh kem và chocolate.\n\nXưởng cũng là nơi ở của gia đình ông Được cùng một số công nhân.\n\nẢnh: Hiện trường vụ cháy khiến 8 người chết'


# Add blanks
txt = 10*"\n" + txt + 10*"\n"

if os.path.exists('txt.mp3') is False:
	tts = gTTS(text=txt, lang='vi')
	tts.save("txt.mp3")

# CREATE THE TEXT IMAGE
clip_txt = TextClip(txt,color='white', align='West', fontsize=50, font='NotoSerifTamil-Bold', method='label')

# SCROLL THE TEXT IMAGE BY CROPPING A MOVING AREA
txt_speed = 27
fl = lambda gf,t : gf(t)[int(txt_speed*t):int(txt_speed*t)+int(h),:]
moving_txt = clip_txt.fl(fl, apply_to=['mask'])

# BACKGROUND IMAGE, DARKENED AT 60%
background_image = ImageClip('stars.jpg')
stars_darkened = background_image.fl_image(lambda pic: (0.6*pic).astype('int16'))

# COMPOSE THE MOVIE
#audio = AudioFileClip("hello.mp3")
background_2 = ImageClip('2.png').set_pos('center').set_duration(10)

videoclip = CompositeVideoClip([
         background_image, background_2,
         moving_txt.set_pos(('center','bottom'))], moviesize)

videoclip.set_duration(len(txt)/8).write_videofile("videoclip.avi", fps=25,
  codec='libx264', 
  audio="txt.mp3",
  audio_codec='aac', 
  temp_audiofile='txt.mp3', 
  remove_temp=True
)
