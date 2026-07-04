from google import genai
import json
import os
from datetime import datetime

# ใช้ Client ตัวใหม่
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_blog_content():
    prompt = (
        "ช่วยเขียนบทความเกี่ยวกับอุปกรณ์ประมง หรือตาข่ายต่างๆ ให้ความรู้เชิงลึก 3 นาทีอ่าน (ประมาณ 600 คำ) "
        "ขอให้ตอบกลับมาเป็น JSON format ที่มีคีย์ title, date, excerpt, fullContent เท่านั้น "
        "ห้ามมีข้อความอื่นนอกจาก JSON"
    )
    
    # เรียกใช้โมเดลผ่าน client ตัวใหม่
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
    )
    
    # เคลียร์ markdown ออกให้เหลือแต่ JSON
    cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(cleaned_text)

# อ่านไฟล์เดิม
with open('posts/blog-posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# สร้างข้อมูลใหม่
new_post = generate_blog_content()
new_post['date'] = datetime.now().strftime("%d %b %Y").upper()
data.insert(0, new_post)

# บันทึก
with open('posts/blog-posts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
