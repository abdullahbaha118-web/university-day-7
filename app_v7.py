from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os, re

app = Flask(__name__)
DATA_FILE = "dreams.json"
MAX_BUBBLES = 20

MOTIVATIONAL = [
    " كل شيء يبدا بفكره  🌟",

]

# ── Horoscope forecasts (30 chars max each) ──────────────
HOROSCOPE = {
    "الحمل":    "طاقة متجددة وحظ في العمل ✨",
    "الثور":    "استقرار مالي ونجاح قريب 💛",
    "الجوزاء":  "أفكار إبداعية تفتح آفاقاً 🌟",
    "السرطان":  "علاقات دافئة وقلب سعيد 💙",
    "الأسد":    "تألق وقيادة ونجومية اليوم 👑",
    "العذراء":  "دقة وتنظيم يجلبان الفوز 🎯",
    "الميزان":  "توازن وجمال يملآن حياتك 🌸",
    "العقرب":   "قوة داخلية وتحولات رائعة 🔥",
    "القوس":    "مغامرة وحظ سعيد ينتظرك 🚀",
    "الجدي":    "اجتهادك سيُثمر قريباً جداً 💪",
    "الدلو":    "ابتكار وأفكار تغيّر مجراك 💡",
    "الحوت":    "حدس قوي وحظ في الدراسة 📚",
}

BAD_WORDS = ["كلمة_محظورة"]

def load_dreams():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_dreams(dreams):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dreams, f, ensure_ascii=False, indent=2)

def filter_text(text):
    for word in BAD_WORDS:
        text = re.sub(word, "***", text, flags=re.IGNORECASE)
    return text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/display")
def display():
    return render_template("display.html")

@app.route("/api/horoscope/<zodiac>")
def get_horoscope(zodiac):
    """Return the horoscope forecast for a given zodiac sign"""
    forecast = HOROSCOPE.get(zodiac.strip(), "")
    return jsonify({"forecast": forecast})

@app.route("/api/dreams", methods=["GET"])
def get_dreams():
    dreams = load_dreams()
    return jsonify(dreams[-MAX_BUBBLES:])

@app.route("/api/dreams", methods=["POST"])
def add_dream():
    data = request.get_json()
    required = ["name", "dream", "zodiac", "emoji"]
    for field in required:
        if not data.get(field, "").strip():
            return jsonify({"error": f"حقل {field} مطلوب"}), 400

    dream = {
        "id":          int(datetime.now().timestamp() * 1000),
        "name":        filter_text(data["name"][:11]),
        "dream":       filter_text(data["dream"][:30]),
        "dept":        filter_text(data.get("dept", "")[:13]),
        "birthday":    filter_text(data.get("birthday", "")[:11]),
        "zodiac":      filter_text(data["zodiac"][:7]),
        "emoji":       data["emoji"],
        "dream_type":  data.get("dream_type", "custom"),  # "custom" or "horoscope"
        "timestamp":   datetime.now().isoformat()
    }

    dreams = load_dreams()
    dreams.append(dream)
    if len(dreams) > MAX_BUBBLES:
        dreams = dreams[-MAX_BUBBLES:]
    save_dreams(dreams)

    import random
    msg = random.choice(MOTIVATIONAL)
    return jsonify({"success": True, "message": msg, "dream": dream})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
