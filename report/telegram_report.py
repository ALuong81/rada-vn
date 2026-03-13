import requests
from config import TELEGRAM_TOKEN,TELEGRAM_CHAT_ID
from datetime import datetime

def send_report(sniper, market):

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    msg = f"""
🎯 HỆ THỐNG RADA – BÁO CÁO SNIPER

🕒 Thời gian: {now}

📈 Trạng thái thị trường: {market.get("risk","UNKNOWN")}
📊 Chế độ thị trường: {market.get("mode","UNKNOWN")}

• Độ rộng thị trường: {market.get("breadth","UNKNOWN")}
• Tỷ lệ cổ phiếu tăng: {market.get("advancers","0")}%
"""

    msg += "\n------------------------------------\n"

    for i, s in enumerate(sniper, 1):

        msg += f"""

🔹 Mục tiêu #{i}: {s.get("symbol","")}

• Giá hiện tại: {s.get("price","")}
• Giá vào: {s.get("entry","")}
• Mục tiêu: {s.get("target","")}
• Cắt lỗ: {s.get("stop","")}

• Trạng thái: {s.get("status","")}

• Ngành: {s.get("sector","")}

• Cổ phiếu dẫn dắt: {s.get("leader","")}

• Xu hướng đa khung: {s.get("trend","")}

• Mô hình AI: {s.get("pattern","")}

• Mô hình VCP: {s.get("vcp","")}

• Tích lũy: {s.get("accumulation","")}

• Dòng tiền tổ chức: {s.get("institutional_flow","")}

• Smart Money: {s.get("smart_money","")}

• Xác suất breakout: {s.get("breakout_prob","")}

• Super Breakout: {s.get("super_breakout","")}

• Relative Strength: {s.get("rs_rating","")}

• Meta Score: {s.get("meta_score","")}

• Cảnh báo rủi ro: {s.get("risk","BÌNH THƯỜNG")}
"""

    send(msg)


def send(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }

    requests.post(url, data=data)
    
   # url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

   # requests.post(url,json={"chat_id":TELEGRAM_CHAT_ID,"text":text})
