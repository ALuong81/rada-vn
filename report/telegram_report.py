import requests
from config import TELEGRAM_TOKEN,TELEGRAM_CHAT_ID
from datetime import datetime

def send_report(stocks, market):
    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    text = "🎯 HỆ THỐNG RADA – BÁO CÁO SNIPER\n\n"

    text += f"🕒 Thời gian: {now}\n\n"

    text += f"📈 Trạng thái thị trường: {market['market_status']}\n"
    text += f"📊 Chế độ thị trường: {market['market_regime']}\n\n"

    text += f"• Độ rộng thị trường: {market['breadth']}\n"
    text += f"• Tỷ lệ cổ phiếu tăng: {market['adv_ratio']}%\n\n"

    text += "--------------------------------------------------\n\n"
    if not stocks:
        text += "⚠️ Không có cổ phiếu đạt tiêu chuẩn SNIPER hôm nay.\n"
    for i,s in enumerate(stocks,1):

        text+=f"🔹 Mục tiêu #{i}: {s['symbol']}\n\n"
        text+=f"• Giá hiện tại: {s['price']}\n"
        text+=f"• Giá vào: {round(s['price']*1.01,2)}\n"
        text+=f"• Mục tiêu: {round(s['price']*1.2,2)}\n"
        text+=f"• Cắt lỗ: {round(s['price']*0.92,2)}\n"
        text+=f"• Trạng thái: {s['status']}\n"
        text+=f"• Ngành: {s.get('sector','UNKNOWN')}\n"
        text+=f"• Cổ phiếu dẫn dắt: {s.get('leader','KHÔNG')}\n"
        text+=f"• Xu hướng đa khung: {s.get('trend','TRUNG TÍNH')}\n"
        text+=f"• Xác suất breakout: {s.get('breakout_prob','TRUNG BÌNH')}\n"
        text+=f"• Tích lũy: {'CÓ' if s.get('accumulation') else 'KHÔNG'}\n"
        text+=f"• Mô hình VCP: {'CÓ' if s.get('vcp') else 'KHÔNG'}\n"
        text+=f"• Dòng tiền tổ chức: {'CÓ' if s.get('smart_money') else 'KHÔNG'}\n"
        text+=f"• Xếp hạng: {'SIÊU MẠNH' if s.get('meta_score',0)>80 else 'MẠNH'}\n"
        text+=f"• Meta Score: {s.get('meta_score',0)}\n"
        text+=f"• Tín hiệu dòng tiền: {'MẠNH' if s.get('smart_money') else 'BÌNH THƯỜNG'}\n"
        text+=f"• Cảnh báo rủi ro: BÌNH THƯỜNG\n\n\n"

    
    url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url,json={"chat_id":TELEGRAM_CHAT_ID,"text":text})
