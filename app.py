import streamlit as st 
from app_config import * 
import imutils
import cv2
import os
from blur_detector_video import detect_video_blur
from blur_detector_image import detect_image_blur

# import the necessary packages


from db import Image, Video, CleanVideo
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_video(file, path):
    try:
        db = opendb()
        file =  os.path.basename(path)
        name, ext = file.split('.') # second piece
        vid = Video(filename=name,extension=ext,filepath=path)
        db.add(vid)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

def save_clean_video(path):
    try:
        db = opendb()
        file =  os.path.basename(path)
        name, ext = file.split('.') # second piece
        vid = CleanVideo(filename=name,extension=ext,filepath=path)
        db.add(vid)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

def save_file(file, path):
    try:
        db = opendb()
        file =  os.path.basename(path)
        name, ext = file.split('.') # second piece
        vid = Image(filename=name,extension=ext,filepath=path)
        db.add(vid)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False

st.title(APP_TITLE)
st.sidebar.header("select an option")
page_names = ['Image', 'video', 'About Project']
page = st.sidebar.radio('Main menu',page_names)
if page == 'Image' :
    st.title("uploading image files")
    

    
    choice = st.sidebar.selectbox("select option",['upload content','view uploads', 'manage uploads', 'remove blur images'])

    if choice == 'upload content':
        files = st.file_uploader("select a image",type=['jpg','png'], accept_multiple_files = True)
        if files:
            for file in files:

                path = os.path.join('uploads',file.name)
                with open(path,'wb') as f:
                    f.write(file.getbuffer())
                    status = save_file(file,path)
                    if status:
                        st.sidebar.success("file uploaded")
                        st.sidebar.image(path,use_column_width=True)
                    else:
                        st.sidebar.error('upload failed')

    if choice == 'view uploads':
        db = opendb()
        results = db.query(Image).all()
        db.close()
        img = st.sidebar.radio('select image',results)
        if img and os.path.exists(img.filepath):
            st.sidebar.info("selected img")
            st.sidebar.image(img.filepath, use_column_width=True)
            if st.sidebar.button("analyse"):
                st.title(f"{img.filename} to be continued")
            

    if choice == 'manage uploads':
        db = opendb()
        #results = db.query(Image).filter(Image.uploader == 'admin') #if u want to use where query
        results = db.query(Image).all()
        db.close()
        img = st.sidebar.radio('select image to remove',results)
        if img:
            st.error("img to be deleted")
            if os.path.exists(img.filepath):
                st.image(img.filepath, use_column_width=True)
            if st.sidebar.button("delete"): 
                try:
                    db = opendb()
                    db.query(Image).filter(Image.id == img.id).delete()
                    if os.path.exists(img.filepath):
                        os.unlink(img.filepath)
                    db.commit()
                    db.close()
                    st.info("image deleted")
                except Exception as e:
                    st.error("image not deleted")
                    st.error(e)
    if choice =='remove blur images':
        db = opendb()
        results = db.query(Image).all()
        db.close()
        img = st.sidebar.radio('select image',results)
        if img and os.path.exists(img.filepath):
            st.image(img.filepath, use_column_width=True)
            result, mean, blurry = detect_image_blur(img.filepath)
            st.image(result)
            if blurry:
                try:
                    db = opendb()
                    db.query(Image).filter(Image.id == img.id).delete()
                    if os.path.exists(img.filepath):
                        os.unlink(img.filepath)
                    db.commit()
                    db.close()
                    st.info("image deleted")
                except Exception as e:
                    st.error("image not deleted")
                    st.error(e)



        # result= st.button("proceed")
        # if result : 
        #     orig = cv2.imread(imlist[0].getbuffer())
        #     orig = imutils.resize(orig, width=500)
        #     gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)

        #     # apply our blur detector using the FFT
        #     (mean, blurry) = detect_blur_fft(gray, size=60,thresh=20, vis =-1)
        #     # draw on the image, indicating whether or not it is blurry
        #     image = np.dstack([gray] * 3)
        #     color = (0, 0, 255) if blurry else (0, 255, 0)
        #     text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
        #     text = text.format(mean)
        #     cv2.putText(image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        #     print("[INFO] {}".format(text))

            

    
elif page == 'video' :
    st.subheader("upload your videos here")
    choice = st.sidebar.selectbox("select option",['upload content', 'manage uploads', 'remove blur in video', 'show corrected video'])

    if choice == 'upload content':
        vidfiles = st.file_uploader('videos uploader', type= ['.mp4','.mkv'], accept_multiple_files= True)
        confirm = st.button("confirm")

        if confirm and vidfiles:
            for file in vidfiles:

                folder = 'videos'
                path = os.path.join(folder,f"{file.name}")
                with open(path,'wb') as f:
                    f.write(file.getbuffer())
                    status = save_video(file,path)
                    if status:
                        st.sidebar.success("video uploaded")
                        
                    else:
                        st.sidebar.error('upload failed')

        db = opendb()
        videos=db.query(Video).all()
        db.close()
        vid = st.selectbox('select a video to play',videos)
        if vid and os.path.exists(vid.filepath):
            st.video(vid.filepath)

    if choice == 'manage uploads':
        db = opendb()
        #results = db.query(Image).filter(Image.uploader == 'admin') #if u want to use where query
        results = db.query(Video).all()
        db.close()
        vid = st.sidebar.radio('select video to remove',results)
        if vid:
            st.error("video to be deleted")
            if os.path.exists(vid.filepath):
                st.video(vid.filepath)
            if st.sidebar.button("delete"): 
                try:
                    db = opendb()
                    db.query(Video).filter(Video.id == vid.id).delete()
                    if os.path.exists(vid.filepath):
                        os.unlink(vid.filepath)
                    db.commit()
                    db.close()
                    st.info("video deleted")
                except Exception as e:
                    st.error("video not deleted")
                    st.error(e)

    if choice =='remove blur in video':
        st.title("remove blur")
        db = opendb()
        
        results = db.query(Video).all()
        db.close()
        vid = st.sidebar.radio('select a video', results)
        if vid:
            
            if os.path.exists(vid.filepath):
                st.video(vid.filepath)
                newpath = detect_video_blur(vid.filepath,vid.filename)
                save_clean_video(newpath)

    if choice == 'show corrected video': 
        db = opendb()
        #results = db.query(Image).filter(Image.uploader == 'admin') #if u want to use where query
        results = db.query(CleanVideo).all()
        db.close()
        vid = st.sidebar.radio('select video to view',results)
        if vid:
            if os.path.exists(vid.filepath):
                st.video(vid.filepath)


else:
    st.text(ABOUT_PROJECT)  


#------------------------dbs--------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------     