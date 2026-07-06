import os
import json
import datetime
from google import genai
from google.genai import types
from pydantic import BaseModel

# 1. ย้ายมาประกาศด้านนอกสุด และใช้ BaseModel เพื่อให้ SDK เข้าใจโครงสร้างข้อมูลอย่างถูกต้อง
class BlogFormat(BaseModel):
    title: str
    excerpt: str
    fullContent: str

def generate_blog():
    json_path = "posts/blog-posts.json"
    
    # 2. เริ่มต้นระบบด้วย SDK ตัวใหม่ล่าสุด
    client = genai.Client()
    
    print("กำลังสั่งให้ Gemini เจนบทความใหม่...")
    
    # 3. เรียกใช้งานโมเดลยุคใหม่ (gemini-2.5-flash)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='สลิงลากตราสิงห์โต อวนฟ้า อวนขี้ม้า ด้ายปะอวน เชือกโปลี เชือกใยยักษ์ เชือกขี้ม้า เชือกทิ้งซั้ง เชือกสายมาน ลูกลอย ทุ่น ลูกยาง เครื่องเหล็ก โซ่ สเก็น ตะกร้า ลังปลา ถังเหลี่ยม ตาข่ายสนามฟุตบอล ตาข่ายสนามกอล์ฟ ตาข่ายกันของตก นี้คือรายการสินค้าที่ผมขาย ช่วยเลือกสินค้ามา 1 อย่าง มาสร้างบทความที่เป็นประโยชน์ต่อกลุ่มคนที่ใช้สินค้าเหล่านี้ โดยในบทความช่วยค้นหาและวิเคราะห์คีย์เวิร์ดที่เป็นที่ต้องการสูงจากระบบ SEO ของ Google มาสร้างบทความภาษาไทยเชิงลึกที่มีความยาวประมาณ 300-500 คำ',

        config=types.GenerateContentConfig(
            system_instruction="คุณเป็นผู้เชี่ยวชาญด้าน Content Marketing สำหรับธุรกิจ B2B และขายส่งอุปกรณ์การเกษตร ประมง และตาข่าย หน้าที่ของคุณคือเขียนบทความภาษาไทยที่อ่านง่าย ได้ประโยชน์จริง และปรับแต่งมาเพื่อ SEO (SEO-optimized) ห้ามใส่คำเกริ่นนำที่ไม่จำเป็น",
            response_mime_type="application/json",
            response_schema=BlogFormat, # ส่ง Schema ที่ถูกต้องเข้าไป
        ),
    )
    
    # 4. แปลงผลลัพธ์ JSON มาเป็น Dictionary ของ Python
    new_post = json.loads(response.text)
    
    # 5. จัดรูปแบบวันที่ (Format: DD MMM YYYY เช่น 06 JUL 2026)
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    today = datetime.date.today()
    date_str = f"{today.strftime('%d')} {months[today.month - 1]} {today.year}"
    
    # สร้าง Object บทความชิ้นใหม่
    final_post = {
        "title": new_post.get("title"),
        "date": date_str,
        "excerpt": new_post.get("excerpt"),
        "fullContent": new_post.get("fullContent")
    }
    
    # 6. เปิดอ่านข้อมูลเดิมจากไฟล์ JSON (ถ้ามีไฟล์อยู่แล้ว)
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                current_posts = json.load(f)
                if not isinstance(current_posts, list):
                    current_posts = []
        except json.JSONDecodeError:
            current_posts = []
    else:
        current_posts = []
        os.makedirs("posts", exist_ok=True)
        
    # 7. แทรกบทความใหม่เข้าไปที่ตำแหน่งบนสุด (index 0)
    current_posts.insert(0, final_post)
    
    # 8. เซฟข้อมูลทั้งหมดกลับลงไฟล์เดิม
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(current_posts, f, ensure_ascii=False, indent=2)
        
    print(f"เพิ่มบทความใหม่เรียบร้อยแล้ว! หัวข้อ: {final_post['title']}")

if __name__ == "__main__":
    generate_blog()
