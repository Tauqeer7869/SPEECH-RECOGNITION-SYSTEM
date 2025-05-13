from flask import Flask, render_template, request, jsonify
import os
import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audioFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['audioFile']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            
            with open(os.path.join(OUTPUT_FOLDER, 'transcription.txt'), 'w') as f:
                f.write(text)

            return jsonify({'transcription': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'})
    except sr.RequestError as e:
        return jsonify({'error': f'Service error: {e}'})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'})

if __name__ == '__main__':
    app.run(debug=True)
