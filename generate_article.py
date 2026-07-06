import os
import datetime
import google.generativeai as genai

# 1. ตั้งค่า API Key ของ Gemini ที่ดึงมาจาก GitHub Secrets
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_blog():
    # 2. เลือกใช้โมเดล Gemini 1.5 Flash (เหมาะกับงานเขียนบทความทั่วไป รวดเร็ว)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="คุณเป็นนักเขียนบทความมืออาชีพ เขียนบทความอัปเดตความรู้ธุรกิจ เทคโนโลยี หรือการตลาด ความยาวประมาณ 500 คำ เป็นภาษาไทย จัดรูปแบบให้อ่านง่าย"
    )
    
    # 3. สั่งให้ AI เจนเนื้อหา
    response = model.generate_content("ขอหัวข้อที่น่าสนใจและเป็นกระแสสำหรับวันนี้ พร้อมเนื้อหาบทความแบบละเอียด")
    content = response.text
    
    # 4. ตั้งชื่อไฟล์ตามวันที่
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"blog-{today}.html"
    
    # 5. นำเนื้อหามาใส่ใน Template HTML ของเว็บคุณ
    html_template = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>บทความประจำวันที่ {today}</title>
    <link rel="stylesheet" href="style.css"> <!-- เชื่อมไฟล์ดีไซน์เดิมของคุณ -->
</head>
<body>
    <article style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif;">
        <p style="color: #666;">เผยแพร่เมื่อ: {today}</p>
        <div class="content" style="line-height: 1.8;">
            {content.replace('\n', '<br>')}
        </div>
    </article>
</body>
</html>"""
    
    # 6. บันทึกไฟล์ลงโฟลเดอร์ blogs/
    os.makedirs("blogs", exist_ok=True)
    with open(f"blogs/{filename}", "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print(f"สร้างบทความ {filename} ด้วย Gemini สำเร็จแล้ว!")

if __name__ == "__main__":
    generate_blog()
