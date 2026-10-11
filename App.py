from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  # อนุญาตให้หน้าเว็บ (Frontend) เชื่อมต่อเข้ามาได้

@app.route('/api/get-video', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'กรุณาระบุลิงก์วิดีโอ'}), 400

    # ตั้งค่า yt-dlp สำหรับดึงข้อมูลโดยไม่ดาวน์โหลดลงเครื่องเซิร์ฟเวอร์ก่อน
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ดึงข้อมูล Meta Data ของวิดีโอ
            info = ydl.extract_info(url, download=False)
            
            video_data = {
                'title': info.get('title', 'Unknown_Video'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'download_url': info.get('url'), # ลิงก์สตรีมไฟล์วิดีโอตรง (ไม่มีลายน้ำสำหรับ TikTok)
                'platform': info.get('extractor', 'unknown')
            }
            
            return jsonify({'success': True, 'data': video_data})
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'ไม่สามารถดึงข้อมูลวิดีโอได้: {str(e)}'}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
