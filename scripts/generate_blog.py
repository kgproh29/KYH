from google import genai
import json
import os
from datetime import datetime

# ตั้งค่า Client ใหม่ตามมาตรฐานล่าสุด
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_blog_content():
    prompt = (
        "ช่วยเขียนบทความเกี่ยวกับอุปกรณ์ประมง หรือตาข่ายต่างๆ ให้ความรู้เชิงลึก 3 นาทีอ่าน (ประมาณ 600 คำ) "
        "ขอให้ตอบกลับมาเป็น JSON format ที่มีคีย์ title, date, excerpt, fullContent เท่านั้น "
        "ห้ามมีข้อความอื่นนอกจาก JSON"
    )
    
    # ใช้โมเดลรุ่นล่าสุดผ่าน client ใหม่
    response = client.models.generate_content(
        model='gemini-2.0-flash', # เปลี่ยนมาใช้รุ่นใหม่ล่าสุดที่รองรับ
        contents=prompt,
    )
    
    # ทำความสะอาด JSON
    cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(cleaned_text)

# โหลดไฟล์ JSON เดิม
with open('posts/blog-posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# สร้างบทความใหม่
new_post = generate_blog_content()
new_post['date'] = datetime.now().strftime("%d %b %Y").upper()
data.insert(0, new_post)

# บันทึกทับไฟล์เดิม
with open('posts/blog-posts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
