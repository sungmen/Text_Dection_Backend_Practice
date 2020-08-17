import cv2
import pytesseract
import os.path
import numpy as np
import cv2
import json
from flask import Flask, request, Response
import uuid

def textDetect(img):
    detectPublic = 'public'
    if not os.path.isdir(detectPublic):
        os.mkdir(detectPublic)

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    ### Write Image Text
    image_text = pytesseract.image_to_string(img, lang='kor+eng', config='--psm 1 -c preserve_interword_spaces=1')

    with open('public/result.txt', 'w+', encoding='utf-8') as f:
        f.write(image_text)

    ### Detecting Characters
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img, lang='kor+eng', config='--psm 1 -c preserve_interword_spaces=1')
    for b in boxes.splitlines():
        b = b.split(' ')
    #     print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg-y), (w, hImg-h), (0, 50, 255), 1)
    #     cv2.putText(img, b[0], (x, hImg-y), cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),1)

    #save file
    path_file = ('public/%s.jpg' %uuid.uuid4(). hex)
    cv2.imwrite(path_file, img)
    return json.dumps(path_file) # return image file name

# API
app = Flask(__name__)

# route http post to this method
@app.route('/api/upload' , methods=['POST'])
def upload():
    #retrieve image from client
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)

    #process image
    img_processed = textDetect(img)

    #response
    return Response(response=img_processed, status=200, mimetype="application/json") #return json string

#start server
app.run(host="0.0.0.0", port=5000)
