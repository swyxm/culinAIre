import cv2
import pytesseract
import numpy as np
from openai import OpenAI
import os
from django.conf import settings



client = OpenAI()
class imageProcess:
    def __init__(self):
        self.menuItems = []
        self.menuVecs = []

    def capture(self):
        # Initialize video capture
        vcapt = cv2.VideoCapture(0)  # Use 0 for default camera

        # Check if the camera is opened successfully
        if not vcapt.isOpened():
            print("Error: Camera not found or unable to open.")
            exit()


        while True:
            ret, frame = vcapt.read()
            cv2.imshow('Camera', frame)
            # Check if the frame was captured successfully
            if cv2.waitKey(1) == ord(' '):

                media_dir = os.path.join(settings.MEDIA_ROOT, 'clipped.jpg')
                cv2.imwrite(media_dir, frame)  # Save the image as clipped.jpg
                # Preprocess image (optional, but can improve OCR accuracy)
                # Preprocess image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Denoising
                denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

                # Adaptive Thresholding
                processed_image = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                # Resizing (optional)
                processed_image = cv2.resize(processed_image, (0, 0), fx=2, fy=2)

                # Dilation to enhance text features
                kernel = np.ones((3, 3), np.uint8)
                dilated = cv2.dilate(processed_image, kernel, iterations=1)

                # Display the processed image for debugging purposes
                cv2.imshow('Processed Image', dilated)

                # Use Tesseract to extract text from the processed image
                text = pytesseract.image_to_string(dilated)

                # Display the frame and extracted text
                print(text)
                return text
                break

            elif cv2.waitKey(1) == ord('q'):
                break

        # Release the camera
        vcapt.release()
        cv2.destroyAllWindows()

    def reviewMenu(self,text):
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": """You are a culinary and flavor expert. Your task is to parse out or pick out ONLY valid menu items from the input you are given.
                            Output each dish comma seperated."""
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": text
                }
            ]
            }
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )


        responseString = response.choices[0].message.content
        self.menuItems = responseString.split(",")
        return responseString
    
    def analyzeMenu(self, responseString):
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": """You are a culinary and flavor expert. Your task is to evaluate each dish you are given across 7 metrics: 
                        Sweetness, Saltiness, Spiciness, Sourness, Bitterness, Tanginess, Richness (How flavorful/creamy/heavy it is). 
                        You will evaluate these metrics with a number from 0 to 10.  Base this evaluation on how dominant a specific 
                        flavor aspect is in the dish. i.e., Butter Chicken would be higher on the spiciness, tanginess, and richness metrics. 
                        Strictly avoid jumping to the edge cases of 0 to 10 or giving each category the same number unless absolutely necessary. 
                        Honestly evaluate the nuances of the flavor profile of the dish. In many cases, you will have to guess all the ingredients
                        used. In that case, just make an educated guess. Format your response with the 7 numbers space-seperated. Each 7 metric array should be comma-seperated."""
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": responseString
                }
            ]
            }
            ],
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )
        for i in response.choices[0].message.content.split(","):
            # Split each row by spaces to get each element in the row, and convert to integers
            self.menuVecs.append([int(j) for j in i.split()])
        return self.menuVecs

