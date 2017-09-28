import glob, os
from subprocess import call

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


for folder in get_immediate_subdirectories("videos/"):
    if folder[:3] == "ENG":
        lang_choice = "en"

        for file in glob.glob("videos/" + folder + "/*.avi"):
            print(file)
            call(["autosub", "-D", lang_choice[:2], file])