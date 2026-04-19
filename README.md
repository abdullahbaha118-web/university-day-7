# 🌟 أحلام الطلاب — دليل النشر العام

## نشر الموقع مجاناً على الإنترنت (Render)

### الخطوة 1 — ارفع المشروع على GitHub
1. افتح github.com وسجّل دخول
2. اضغط New repository → اسمه: ahlam-al-tullab
3. ارفع جميع ملفات المشروع (app.py, templates/, requirements.txt, Procfile)

### الخطوة 2 — انشر على Render
1. افتح render.com وسجّل بحساب GitHub
2. اضغط New → Web Service
3. اختر الـ repository
4. الإعدادات:
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
   - Plan: Free
5. اضغط Deploy وانتظر 2-3 دقائق

### الخطوة 3 — الروابط
بعد النشر تحصل على رابط مثل:
  https://ahlam-al-tullab.onrender.com

للطلاب (QR Code): https://ahlam-al-tullab.onrender.com/
شاشة العرض:       https://ahlam-al-tullab.onrender.com/display

---
تشغيل محلي:
  pip install flask
  python app.py
