# Auto Desqueeze and Display Image
# TODO:
#   args:
#       --camera -c     : input camera name
#       --raw_type -r   : input camera raw file type
#       --convert -t    : converts raw to DNG. Boolean [true|false]

try:
    import subprocess
    from tkinter import *
    import time
    from PIL import Image
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import os
except ImportError as error:
    print (error.__class__.__name__ + ': ' + error.message)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print ("File Added")
        with open('monitor/camera_files.txt') as f:
            l = f.read().splitlines()
            line = l[-1]
            print (line)
        
        #TODO:
        #   - get-files for the latest file to save to local storage
        #   - call method for desqueezing the image -> pass image to display
        #   - call method for displaying the latest RAW image
        get_desqueeze()
        get_viewer()

def get_camera():
    list_camera = input('Do you want to see the camera list?[y/n] ')
    if (list_camera == 'yes' or list_camera == 'YES' or list_camera == 'y' or list_camera == 'Y'):
        os.system('cat camera_list.txt | less')
        c_name = input('What is the camera model? ')
    elif (list_camera == 'no' or list_camera == 'NO' or list_camera == 'N' or list_camera == 'n'):
        c_name = input('What is the camera model? ')
    else:
        print('Invalid input')
        exit(0)
    
    return (c_name)
    
def check_name(c_name):
    with open('camera_list.txt') as f:
        found = False
        for line in f:
            if c_name in line:
                print ('Camera Model Found')
                found = True
        if not found:
            print ('Sorry, this camera is not supported.')
            exit(0)

def check_files():
    photo_list = []
    os.system('gphoto2 --list-files > monitor/camera_files.txt' )
    
    with open('monitor/camera_files.txt') as f:
        for line in f:
            if line.startswith('#'):
                photo_list.append(line)

    #print (photo_list)
  
    # get latest entry
    # Use pyinotify
    # this is where we constantly monitor the camera_files.txt for updates
    # if an update occurs, get the latest change and do a function on it.
    
    def monitor():
        print ('MONITORING CHANGES')

        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path='/home/cherzog/Documents/python_scripts/auto_desqueeze/monitor', recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(0)
        except KeyBoardInterrupt:
            observer.stop()
        observer.join()
        print (observer)
        print (event_handler)
    monitor()


def get_desqueeze():
    #needs to be passed the image/img path
    filepath = "/home/cherzog/Pictures/logo-md.f0603b4c28b4.png"

    # get the image size of the img * .33
    img = Image.open(filepath)
    width, height = img.size
    print (width, height)
    
    ana_width = int((width * .33) + width)
    print (ana_width)


    # get the new desqueezed image
    img = img.resize((ana_width, height), Image.ANTIALIAS)
    img.save('ds_pictures/outtest.png')
    print (img)
    
    #img.show()

def get_viewer():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print (screen_width, screen_height)
    
    # display canvas for image
    canvas = Canvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill=BOTH, expand=1)
    img = PhotoImage(file='ds_pictures/outtest.png')
    canvas.create_image(screen_width/2,screen_height/2, image=img)
    mainloop()

def main():
    c_name = get_camera()
    check_name(c_name)
    check_files()
if __name__ == '__main__':
    main()


