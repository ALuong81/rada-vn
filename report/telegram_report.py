import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime

def send_report(stocks, market, heatmap=None, strong_sectors, weak_sectors):

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    text = "🎯 HỆ THỐNG RADA – BÁO CÁO SNIPER\n\n"
    text += f"🕒 Thời gian: {now}\n\n"

    text += f"📈 Trạng thái thị trường: {market.get('status','UNKNOWN')}\n"
    text += f"📊 Chế độ thị trường: {market.get('mode','UNKNOWN')}\n\n"

    text += f"• Độ rộng thị trường: {market.get('breadth','UNKNOWN')}\n"
    text += f"• Tỷ lệ cổ phiếu tăng: {market.get('adv_ratio',0)}%\n\n"
    # TOP ngành mạnh
    if heatmap:
        text += "🔥 TOP NGÀNH MẠNH\n"
        for i, sec in enumerate(heatmap[:3], 1):
        # heatmap trả tuple (sector, score)
            if isinstance(sec, tuple):
                name = sec[0]
                score = round(sec[1],2)
            elif isinstance(sec, dict):
                name = sec.get("sector","UNKNOWN")
                score = round(sec.get("score",0),2)
            else:
                name = sec
                score = ""
            text += f"{i}. {name} ({score})\n"
    
    text += "------------------------------------\n\n"

    if not stocks:
        text += "⚠️ Không có cổ phiếu đạt tiêu chuẩn SNIPER hôm nay.\n"

    for i, s in enumerate(stocks, 1):

        price = s.get("price", 0)

        text += f"🔹 Mục tiêu #{i}: {s.get('symbol','')}\n\n"

        text += f"• Giá hiện tại: {price}\n"
        text += f"• Giá vào: {round(price*1.01,2)}\n"
        text += f"• Mục tiêu: {round(price*1.2,2)}\n"
        text += f"• Cắt lỗ: {round(price*0.92,2)}\n"

        text += f"• Trạng thái: {s.get('status','')}\n"

        text += f"• Ngành: {s.get('sector','UNKNOWN')}\n"

        text += f"• Cổ phiếu dẫn dắt: {s.get('leader','KHÔNG')}\n"

        text += f"• Xu hướng đa khung: {s.get('trend','TRUNG TÍNH')}\n"

        text += f"• Xác suất breakout: {s.get('breakout_prob','TRUNG BÌNH')}\n"

        text += f"• Tích lũy: {'CÓ' if s.get('accumulation') else 'KHÔNG'}\n"

        text += f"• Mô hình VCP: {'CÓ' if s.get('vcp') else 'KHÔNG'}\n"

        # pattern AI
        text += f"• Mô hình AI: {s.get('pattern','KHÔNG')}\n"

        # institutional flow
        text += f"• Dòng tiền tổ chức: {s.get('institutional_flow','KHÔNG')}\n"

        # smart money
        smart = s.get("smart_money","KHÔNG")

        if isinstance(smart, list):
            smart = "KHÔNG"

        text += f"• Smart Money: {smart}\n"

        # super breakout
        text += f"• Super Breakout: {s.get('super_breakout','THẤP')}\n"

        text += f"• Super Stock: {s.get('super_stock','BÌNH THƯỜNG')}\n"

        text += f"• Xếp hạng: {'SIÊU MẠNH' if s.get('meta_score',0) > 80 else 'MẠNH'}\n"

        text += f"• Meta Score: {s.get('meta_score',0)}\n"

        text += f"• Tín hiệu dòng tiền: {'MẠNH' if s.get('smart_money') else 'BÌNH THƯỜNG'}\n"

        text += f"• Relative Strength: {s.get('rs_rating','')}\n"

        text += f"• Cảnh báo rủi ro: {s.get('risk_warning','')}\n\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }
    )
