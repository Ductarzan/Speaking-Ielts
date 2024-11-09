from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import speech_recognition as sr

# Cấu hình API của Gemini
GOOGLE_API_KEY = 'AIzaSyCfU2DGUHolmawp56N1SBB0srRtLTMcOak'
genai.configure(api_key=GOOGLE_API_KEY)

# Mô tả giả lập về AI là giáo viên IELTS band 8.0
teacher_prompt = """
Hãy tưởng tượng tôi là một giáo viên luyện thi IELTS Speaking band 8.0. Tôi sẽ đánh giá bài nói của bạn dựa trên...
"""

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

# API gọi Gemini để chấm điểm và nhận xét bài nói
@app.route('/evaluate', methods=['POST'])
def evaluate_speaking_text():
    topic = request.form.get('topic')
    text = request.form.get('text')
    if not topic or not text:
        return jsonify({"error": "Vui lòng nhập cả chủ đề và câu trả lời để đánh giá."}), 400

    model_name = 'gemini-1.5-pro-latest'
    model = genai.GenerativeModel(model_name)

    try:
        response = model.generate_content(
            f"{teacher_prompt}\n\nChủ đề: {topic}\n\nĐánh giá bài nói:\n\n{text}\n\n"
            "Chấm điểm và nhận xét dựa trên các tiêu chí IELTS Speaking:\n"
            "- Fluency and Coherence\n- Lexical Resource\n- Grammatical Range and Accuracy\n- Pronunciation\n"
            "Ngoài ra, đánh giá mức độ liên quan giữa chủ đề và nội dung bài nói."
        )
        return jsonify({"feedback": response.text})
    except Exception as e:
        return jsonify({"error": f"Lỗi khi gọi API Gemini: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
