from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import speech_recognition as sr

# Cấu hình API Gemini
GOOGLE_API_KEY = 'AIzaSyCfU2DGUHolmawp56N1SBB0srRtLTMcOak'
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

# Route trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# API ghi âm và chuyển đổi giọng nói thành văn bản
@app.route('/recognize', methods=['POST'])
def recognize_speech():
    recognizer = sr.Recognizer()
    audio_file = request.files.get('file')
    if not audio_file:
        return jsonify({"error": "Không có tệp âm thanh."}), 400

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="en-US")
            return jsonify({"text": text})

    except sr.UnknownValueError:
        return jsonify({"error": "Không thể nhận diện giọng nói, vui lòng thử lại."}), 500
    except sr.RequestError:
        return jsonify({"error": "Có lỗi xảy ra khi sử dụng API nhận diện giọng nói."}), 500

# API gọi API Gemini để đánh giá văn bản
@app.route('/evaluate', methods=['POST'])
def evaluate_speaking_text():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "Vui lòng nhập câu trả lời để đánh giá."}), 400

    # Giả lập gọi API Gemini
    response = {
        "score": 7.5,
        "details": {
            "fluency": {"score": 7, "feedback": "Tốc độ nói tự nhiên nhưng cần cải thiện."},
            "coherence": {"score": 8, "feedback": "Ý tưởng trình bày rõ ràng và logic."},
            "lexical_resource": {"score": 7, "feedback": "Sử dụng từ vựng tốt nhưng cần đa dạng hơn."},
            "grammatical_range": {"score": 6.5, "feedback": "Một số lỗi ngữ pháp ảnh hưởng đến điểm."},
            "pronunciation": {"score": 7, "feedback": "Phát âm ổn nhưng cần cải thiện ngữ điệu."}
        }
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
