import os
import json
import datetime
from google import genai
from google.genai import types

def generate_blog():
    json_path = "posts/blog-posts.json"
    
    # 1. เริ่มต้นระบบด้วย SDK ตัวใหม่ล่าสุด (จะดึง GEMINI_API_KEY จาก Environment เองอัตโนมัติ)
    client = genai.Client()
    
    # 2. ตั้งค่าบังคับให้ AI ตอบกลับมาเป็นโครงสร้าง JSON ตามที่ต้องการเป๊ะๆ (Structured Outputs)
    class BlogFormat:
        title: str
        excerpt: str
        fullContent: str

    print("กำลังสั่งให้ Gemini เจนบทความใหม่...")
    
    # 3. เรียกใช้งานโมเดลยุคใหม่ (เช่น gemini-2.5-flash หรือ gemini-2.0-flash)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='ขอหัวข้อที่น่าสนใจเกี่ยวกับอุปกรณ์อุตสาหกรรม การประมง หรือการเกษตรสำหรับวันนี้ พร้อมเนื้อหาบทความภาษาไทยเชิงลึก',
        config=types.GenerateContentConfig(
            system_instruction="คุณเป็นนักเขียนบทความมืออาชีพ มีความเชี่ยวชาญด้านสินค้าอุตสาหกรรม อุปกรณ์ประมง และงานเกษตรกรรม เขียนภาษาไทยอ่านง่าย มีประโยชน์ ความยาว 300-500 คำ",
            # บังคับโครงสร้างข้อมูลให้ตรงกับที่เว็บต้องการ
            response_mime_type="application/json",
            response_schema=BlogFormat,
        ),
    )
    
    # 4. แปลงผลลัพธ์จากรูปแบบข้อความ JSON มาเป็น Dictionary ของ Python
    new_post = json.loads(response.text)
    
    # 5. จัดรูปแบบวันที่ (Format: DD MMM YYYY เช่น 06 JUL 2026) ให้เข้ากับโครงสร้างเดิมของคุณ
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
