from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
            'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
            'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
            'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
            'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
            'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
            'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
            'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
            'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
            'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
            'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
            'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
            'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
            'bihar', 'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile', 'dasara',
            'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
            'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
            'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
            'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
            'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
            'voice', 'wednesday', 'weight', 'please wait for sometime', 'what is your mobile number', 'what are you doing', 'are you busy', '1']

arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','dabq']

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    return render_template('display_image.html')

# Route for live voice recognition
@app.route('/recognize', methods=['POST'])
def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()
            for c in string.punctuation:
                text = text.replace(c, "")
            
            if text in isl_gif:
                gif_path = f'static/ISL_Gifs/{text}.gif'
                return jsonify({"type": "gif", "path": gif_path})
            else:
                letters = []
                for char in text:
                    if char in arr:
                        letters.append(f'static/letters/{char}.jpg')
                return jsonify({"type": "letters", "letters": letters})

        except Exception as e:
            return jsonify({"error": str(e)})

# New route for text input recognition
@app.route('/recognize-text', methods=['POST'])
def recognize_text():
    text = request.form['text'].lower()
    for c in string.punctuation:
        text = text.replace(c, "")
    
    if text in isl_gif:
        gif_path = f'static/ISL_Gifs/{text}.gif'
        return jsonify({"type": "gif", "path": gif_path})
    else:
        letters = []
        for char in text:
            if char in arr:
                letters.append(f'static/letters/{char}.jpg')
        return jsonify({"type": "letters", "letters": letters})

# New route to generate and download PDF
@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    letters = request.form.getlist('letters[]')
    
    # Create a PDF in memory
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Add content to the PDF
    c.drawString(100, 750, "Recognized Sign Language Letters")
    y_position = 720  # Starting y position for the images

    for letter in letters:
        # Add each letter image to the PDF
        letter_path = os.path.join('static', 'letters', f'{letter}.jpg')
        c.drawImage(letter_path, 100, y_position, width=50, height=50)  # Adjust size as needed
        y_position -= 60  # Move down for the next image

    c.save()  # Save the PDF
    pdf_buffer.seek(0)  # Move to the beginning of the buffer

    return send_file(pdf_buffer, as_attachment=True, download_name='recognized_letters.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
