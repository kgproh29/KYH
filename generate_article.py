import os
import json
import datetime
import google.generativeai as genai

# 1. ตั้งค่า API Key ของ Gemini จาก Environment ของ GitHub
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_blog():
    # กำหนดที่อยู่ของไฟล์ JSON
    json_path = "posts/blog-posts.json"
    
    # 2. เรียกใช้โมเดล Gemini
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "คุณเป็นนักเขียนบทความมืออาชีพ มีความเชี่ยวชาญด้านสินค้าอุตสาหกรรม, อุปกรณ์ประมง และงานเกษตรกรรม "
            "เขียนบทความที่ให้ประโยชน์และความรู้แก่ผู้อ่าน ความยาวบทความประมาณ 300-500 คำ เป็นภาษาไทย"
        )
    )
    
    # 3. สั่งให้ AI เจนเนื้อหาโดยบังคับให้ส่งกลับมาเป็นรูปแบบ JSON เพื่อให้ดึงข้อมูลไปใช้ง่าย
    prompt = (
        "ขอหัวข้อที่น่าสนใจเกี่ยวกับอุปกรณ์อุตสาหกรรม การประมง หรือการเกษตรสำหรับวันนี้ "
        "โปรดตอบกลับมาให้อยู่ในรูปแบบ JSON ที่มี key ดังนี้เท่านั้น:\n"
        "{\n"
        '  "title": "ชื่อหัวข้อบทความ",\n'
        '  "excerpt": "สรุปย่อสั้นๆ สำหรับแสดงหน้าแรก...",\n'
        '  "fullContent": "เนื้อหาบทความแบบเต็ม (ขึ้นบรรทัดใหม่ให้ใช้ตัวอักษร \\n)"\n'
        "}"
    )
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    # แปลงผลลัพธ์จาก AI มาเป็น Dictionary ของ Python
    new_post = json.loads(response.text)
    
    # 4. ใส่ข้อมูลวันที่ (Format: DD MMM YYYY เช่น 06 JUL 2026) ให้ตรงกับรูปแบบเดิมของคุณ
    # เปลี่ยนชื่อเดือนเป็นตัวย่อภาษาอังกฤษตัวใหญ่
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    today = datetime.date.today()
    date_str = f"{today.strftime('%d')} {months[today.month - 1]} {today.year}"
    
    # สร้าง Object บทความชิ้นใหม่เพื่อเตรียมเตรียมบันทึก
    final_post = {
        "title": new_post.get("title"),
        "date": date_str,
        "excerpt": new_post.get("excerpt"),
        "fullContent": new_post.get("fullContent")
    }
    
    # 5. โหลดข้อมูลเก่าจาก blog-posts.json (ถ้ายังไม่มีไฟล์ หรือไฟล์ว่าง ให้สร้างลิสต์เปล่า)
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
        
    # 6. เพิ่มบทความใหม่เข้าไปไว้ด้านหน้าสุด (เพื่อให้เวลาแสดงผลบนเว็บ บทความใหม่จะอยู่บนสุด)
    current_posts.insert(0, final_post)
    
    # 7. บันทึกข้อมูลทั้งหมดกลับลงไฟล์เดิม
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(current_posts, f, ensure_ascii=False, indent=2)
        
    print(f"เพิ่มบทความใหม่ใน blog-posts.json เรียบร้อยแล้ว! หัวข้อ: {final_post['title']}")

if __name__ == "__main__":
    generate_blog()
