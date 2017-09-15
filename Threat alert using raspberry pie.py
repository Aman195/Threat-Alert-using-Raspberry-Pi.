import codecs
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
#from watson_developer_cloud import TextToSpeechV1
import subprocess, time, argparse, sys, datetime, socket
from os import system
#from picamera import PiCamera
#—————————————————————————————#
#—————————initialized global variables —————————#
#—————————————————————————————#
# API Key is for Visual Recognition API
# User name and Password are for the Text to Speech API
apiKey = '4bfd78cc64be209b2ba071d82560f63d1dfbeed4'
visual_recognition = VisualRecognitionV3('2016-05-20', api_key=apiKey)
"""username='c146cfb6-c924-43b2-86a8-b70f0b8c484d'
password='dfi1TU0HsL2V'
text_to_speech = TextToSpeechV1(username=username,password=password)"""

def read_input():
    """
    This function parses the input parameters that are passed to this module
    parser = argparse.ArgumentParser(description='Process input parameters.')
    parser.add_argument("input_image_file",required=True)
    parser.add_argument("input_image_file",required=True)
    parser.parse_args()
    """
    pass


def capture_image_from_camera(url):
    """
    This function calls the camera on the Raspberry Pi and captures an image and stores it on the local disk for further processing
    """
    camera = PiCamera()
    camera.start_preview()
    time. sleep(5)
    print ("\nTimestamp before Capture by Raspberry Pi cam: %s\n") % datetime.datetime.now()
    camera.capture(url)
    print ("\nTimestamp after image capture by Raspberry Pi cam: %s\n") % datetime.datetime.now()
    camera.stop_preview()


def get_image_class_and_text(url,file_location):
    """
    This function retreives a given image's class and any text within the image by making use of Watson's Visual Recognition API
    url - Specifies the location of the file, can be a URL on the web or a path on local disk
    file_location - Specifies if the given image file is on the web or a local disk
    """
    #print "\n\n\n\n\File Loc : %s,URL : %s\n\n\n\n" % (url,file_location)
    image_class,image_text  = '',''
    if (file_location == 'web'):
        # Get the image class
        image_class = visual_recognition.classify(images_url=url)
        # Get the text in the image
        image_text = visual_recognition.recognize_text(images_url=url)
    elif (file_location == 'local'):
        with open(url, 'rb') as img:
            image_class = visual_recognition.classify(img)
        with open(url, 'rb') as img:
            image_text = visual_recognition.recognize_text(img)
    elif (file_location == 'cam'):
        capture_image_from_camera(url)
        with open(url, 'rb') as img:
            image_class = visual_recognition.classify(img)
        with open(url, 'rb') as img:
            image_text = visual_recognition.recognize_text(img)
    else:
        print ("\n\nInvalid 'file_location' provided to program. Please pass either 'web' or 'local' or 'cam'.\n\n")
        sys.exit(-1)
    say_image_class="\n\nSorry IBM Watson was not able to classify the image under any category.\n\n"
    try:
        if (image_class['images'][0]['error']):
            say_image_class="\nI B M Watson ran in to the following error : %s \n" % (image_class['images'][0]['error']['description'])
    except:
        e = sys.exc_info()[0]
        print (e)
    try:
        if (image_class['images'][0]['classifiers']):
            say_image_class= ("The image was classified under the following classes : %s.\n\n" % (image_class['images'][0]['classifiers'][0]['classes'][0]['class'] ))
    except:
        e = sys.exc_info()[0]
        print (e)
    
    say_image_text="\n\nSorry, IBM Watson was not able to extract any text from the image.\n\n"
    try:
        if (image_text['images'][0]['error']):
            say_image_text= "\nI B M Watson ran in to the following error : %s \n" % (image_text['images'][0]['error']['description'])
    except:
        e = sys.exc_info()[0]
        print (e)
    try:
        if (image_text['images'][0]['text']):
            say_image_text= ("\n\nThe text in the image is as follows: %s\n\n" % (image_text['images'][0]['text'] ))
    except:
        e = sys.exc_info()[0]
        print (e)
        
    print (say_image_class, say_image_text)
    return (say_image_class,say_image_text)
'''def convert_image_text_to_audio(class_fn,text_fn,say_image_class,say_image_text):
    """
    This function recevies a given image's class and text extracted from it and converts them in to audio
    """
    # Call the Text to Speech API to write the class and text information to audio files
    #class_fn = 'D:\\GRADUATE SCHOOL\\Hackathon\\AT&T Hackathon - Sep 2016\\Audio\\image_to_text_to_audio_class.wav'
    #text_fn = 'D:\\GRADUATE SCHOOL\\Hackathon\\AT&T Hackathon - Sep 2016\\Audio\\image_to_text_to_audio_text.wav'
    with open(class_fn, 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(say_image_class,voice='en-US_MichaelVoice'))
    with open(text_fn, 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(say_image_text,voice='en-US_MichaelVoice'))
    # Play the class and text information audio files
    for fn in (class_fn,text_fn):
        p = subprocess.Popen(["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe",fn,"--play-and-exit"])
        p.wait()
        #time.sleep(5)
        '''

def main():
    if len(sys.argv) > 1:
        image_file = sys.argv[1]
        image_location = sys.argv[2]
    else:
        image_file = "C:\\Users\\rudre\\Desktop\\project\\arnold-gun.jpg"
        image_location = 'local'
    class_fn = 'D:\\GRADUATE SCHOOL\\Hackathon\\AT&T Hackathon - Sep 2016\\audio\\image_to_text_to_audio_class.wav'
    text_fn = 'D:\\GRADUATE SCHOOL\\Hackathon\\AT&T Hackathon - Sep 2016\\audio\\image_to_text_to_audio_text.wav'
    image_class,image_text =  get_image_class_and_text(image_file,image_location)
    #convert_image_text_to_audio(class_fn,text_fn,image_class,image_text)
if _name_ == '_main_':
    main()