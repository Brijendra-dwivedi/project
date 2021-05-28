import moviepy.editor as mp
import os

def convert_video(path,ext='mp4'):
    print('path',path)
    clip = mp.VideoFileClip(path)
    upath = os.path.join("output",f"{path}.{ext}")
    print('upath',upath)
    clip.write_videofile(upath)
    os.unlink(path)
    print('video converted')
    return upath