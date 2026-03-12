import requests
from config import TELEGRAM_TOKEN,TELEGRAM_CHAT_ID
from datetime import datetime

def send_report(stocks):

    text="🎯 HỆ THỐNG RADA – BÁO CÁO SNIPER\n\n"

    text+=f"🕒 Thời gian: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"

    text+="--------------------------------------------------\n\n"
    if not stocks:
        text += "⚠️ Không có cổ phiếu đạt tiêu chuẩn SNIPER hôm nay.\n"
    for i,s in enumerate(stocks,1):

        text+=f"🔹 Mục tiêu #{i}: {s['symbol']}\n\n"

        text+=f"• Giá hiện tại: {s['price']}\n"
        text+=f"• Giá vào: {round(s['price']*1.01,2)}\n"
        text+=f"• Mục tiêu: {round(s['price']*1.2,2)}\n"
        text+=f"• Cắt lỗ: {round(s['price']*0.92,2)}\n"
        text+=f"• Trạng thái: {s['status']}\n"
        text+=f"• Meta Score: {s['meta_score']}\n\n"

    url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url,json={"chat_id":TELEGRAM_CHAT_ID,"text":text})
