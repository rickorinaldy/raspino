import boto3
import cv2
import time

model='arn:aws:rekognition:ap-southeast-1:587870167769:project/TargetDetection/version/TargetDetection.2021-12-09T16.52.37/1639043557442'
min_confidence=95
client=boto3.client('rekognition')

with open(r"C:\Users\ICRAVER\Desktop\Screenshot 2021-12-09 123715.png",'rb') as img:
    response = client.detect_custom_labels(Image={'Bytes': img.read()}, MinConfidence=min_confidence, ProjectVersionArn=model)

print(response)