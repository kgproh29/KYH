import openai
import json
import os
from datetime import datetime

# ตั้งค่า API Key จาก GitHub Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_blog_content():
    # prompt สำหรับสั่ง AI
    prompt = "ช่วยเขียนบทความเกี่ยวกับอุปกรณ์ประมง หรือตาข่ายต่างๆ ให้ความรู้เชิงลึก 3 นาทีอ่าน (ประมาณ 600 คำ) โดยขอเป็น JSON format ที่มีคีย์ title, date, excerpt, fullContent"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

# โหลดไฟล์ JSON เดิม
with open('posts/blog-posts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# สร้างบทความใหม่และเพิ่มเข้าไป
new_post = generate_blog_content()
new_post['date'] = datetime.now().strftime("%d %b %Y").upper()
data.insert(0, new_post) # เพิ่มบทความใหม่ไว้หน้าสุด

# บันทึกทับไฟล์เดิม
with open('posts/blog-posts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
