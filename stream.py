import boto3
import cv2
import serial
import time


def start(model):
    min_confidence = 70
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    client = boto3.client('rekognition')
    global vid
    vid = cv2.VideoCapture(0)
    i = 0
    while(True):
        ret, frame = vid.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        image = cv2.imencode('.jpg', image)[1].tobytes()
        response = client.detect_custom_labels(Image={'Bytes': image}, MinConfidence=min_confidence, ProjectVersionArn=model)
        imgWidth, imgHeight = 640, 480
        
        for customLabel in response['CustomLabels']:
            print('Label ' + str(customLabel['Name']))
            print('Confidence ' + str(customLabel['Confidence']))
            if 'Geometry' in customLabel:
                box = customLabel['Geometry']['BoundingBox']
                left = imgWidth * box['Left']
                top = imgHeight * box['Top']
                width = imgWidth * box['Width']
                height = imgHeight * box['Height']
                start = (left,top)
                end = (left+width,top+height)

                boxes = [(start[0]+end[0])//2, (start[1]+end[1])//2]
                perim = int(sum(width+height)*2)
                
                ser.write(f"{boxes} {perim}\n")
                # line = ser.readline().decode('utf-8').rstrip()
        i += 1
        yield(i)

def stop():
    vid.release()
    cv2.destroyAllWindows()