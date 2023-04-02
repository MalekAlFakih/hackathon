import cv2
import easyocr
from django.shortcuts import render
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def upload_image(request):
    if request.method == 'POST':
        # Get list of uploaded images from request object
        images = request.FILES.getlist('image')

        # Loop over the uploaded images and process them
        results = []
        for img in images:
            # Read image from request object
            img_data = img.read()
            img_np = np.frombuffer(img_data, np.uint8)
            img_cv2 = cv2.imdecode(img_np, cv2.IMREAD_UNCHANGED)
            
            # Use EasyOCR to read text from image
            reader = easyocr.Reader(['en'])
            result = reader.readtext(img_cv2, detail=0, paragraph=True)

            # Filter out stop words from the text
            filtered_result = [word for word in result if not word.lower() in stop_words]

            # Add filtered result to list
            results.append(filtered_result)

        # Return results to template
        return render(request, 'hhh/upload_image.html', {'results': results})
    else:
        return render(request, 'hhh/upload_image.html')