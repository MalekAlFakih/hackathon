import cv2
import easyocr
from django.shortcuts import render
import numpy as np
def upload_image(request):
    if request.method == 'POST':
        # Read image from request object
        img = cv2.imdecode(np.frombuffer(request.FILES['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
        # Use EasyOCR to read text from image
        reader = easyocr.Reader(['en'])
        result = reader.readtext(img,detail=0 , paragraph = True )

        print(result)

        # Return result to template
        return render(request, 'hhh/upload_image.html', {'result': result})

