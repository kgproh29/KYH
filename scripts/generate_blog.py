import google.generativeai as genai
import json
import os
from datetime import datetime

# ตั้งค่า API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_blog_content():
    prompt = (
        "ช่วยเขียนบทความเกี่ยวกับอุปกรณ์ประมง หรือตาข่ายต่างๆ ให้ความรู้เชิงลึก 3 นาทีอ่าน (ประมาณ 600 คำ) "
        "ขอให้ตอบกลับมาเป็น JSON format ที่มีคีย์ title, date, excerpt, fullContent เท่านั้น "
        "ห้ามมีข้อความอื่นนอกจาก JSON"
    )
    
    response = model.generate_content(prompt)
    # Gemini บางครั้งอาจแถม markdown ```json ... ``` มาด้วย ต้องเคลียร์ออกก่อน
    cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(cleaned_text)

# โหลดไฟล์ JSON เดิม
with open('posts/blog-posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# สร้างบทความใหม่
new_post = generate_blog_content()
new_post['date'] = datetime.now().strftime("%d %b %Y").upper()
data.insert(0, new_post)

# บันทึกทับ
with open('posts/blog-posts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
