from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

    
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd

def scanner():
    context = {}
    df = pd.DataFrame({'UPC': ['0028400040112', '0049000006346', '0028400090858', '0028400090858'],
                   'Name': ['Cheetos', 'Coke Can', 'Lays Classic Chip Bag', 'Lays BBQ Chips'],
                   'Recyclable': ['Landfill', 'Recycle', 'Landfill', 'Landfill']})
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    name_data = ""
    recyclable_data = ""

    while True:
        success, img = cap.read()
        code = decode(img)
        for barcode in code:
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            myData = barcode.data.decode('utf-8')

            if myData in df['UPC'].values:
                row = df.loc[df['UPC'] == myData]
                name_data = row['Name'].iloc[0]
                recyclable_data = row['Recyclable'].iloc[0]
                proper_answer = f"UPC {myData} corresponds to '{name_data}', which you place in {recyclable_data}"
                context = {
                    'answer' : proper_answer
                }
                return context
            # pts2 = barcode.rect
            # cv2.putText(img, barcode, (pts2[0], pts2[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255),1,cv2.LINE_AA)

            # print(barcode.data)
        cv2.imshow('Result',img)
        cv2.waitKey(1)

def index(request):
    template = loader.get_template("Scanner/Susmain.html")
    output_test = scanner()
    print(output_test)
    return HttpResponse(template.render(output_test, request))

# Create your views here.
