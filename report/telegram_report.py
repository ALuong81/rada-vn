import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime


# =========================
# VIỆT HOÁ THUẬT NGỮ
# =========================

STATUS_MAP = {
    "RISK ON": "THỊ TRƯỜNG TÍCH CỰC",
    "RISK OFF": "THỊ TRƯỜNG RỦI RO"
}

MODE_MAP = {
    "UPTREND": "XU HƯỚNG TĂNG",
    "DOWNTREND": "XU HƯỚNG GIẢM",
    "SIDEWAY": "ĐI NGANG"
}

TIMING_MAP = {
    "CONFIRMED UPTREND": "XU HƯỚNG TĂNG XÁC NHẬN",
    "UPTREND": "XU HƯỚNG TĂNG",
    "MARKET UNDER PRESSURE": "THỊ TRƯỜNG CHỊU ÁP LỰC",
    "SIDEWAY": "ĐI NGANG",
    "DOWNTREND": "XU HƯỚNG GIẢM"
}

TREND_MAP = {
    "STRONG": "ĐỒNG THUẬN MẠNH",
    "UP": "TĂNG",
    "SIDEWAY": "TRUNG TÍNH",
    "DOWN": "GIẢM"
}

BREAKOUT_MAP = {
    "HIGH": "CAO",
    "MEDIUM": "TRUNG BÌNH",
    "LOW": "THẤP"
}

RS_MAP = {
    "VERY STRONG": "SIÊU MẠNH",
    "STRONG": "MẠNH",
    "NORMAL": "TRUNG BÌNH",
    "WEAK": "YẾU"
}


# =========================
# GỬI BÁO CÁO TELEGRAM
# =========================

def send_report(
    stocks,
    market,
    heatmap=None,
    strong_sectors=None,
    weak_sectors=None
):
    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    status = STATUS_MAP.get(market.get("status"), market.get("status"))
    mode = MODE_MAP.get(market.get("mode"), market.get("mode"))
    timing = TIMING_MAP.get(market.get("timing"), market.get("timing"))

    text = "🎯 HỆ THỐNG RADA – BÁO CÁO SNIPER\n\n"
    text += f"🕒 Thời gian: {now}\n\n"

    text += f"📈 Trạng thái thị trường: {status}\n"
    text += f"📊 Xu hướng thị trường: {mode}\n\n"
    text += f"⏱ Nhịp thị trường: {timing}\n\n"

    text += f"• Độ rộng thị trường: {market.get('breadth','UNKNOWN')}\n"
    text += f"• Tỷ lệ cổ phiếu tăng: {market.get('adv_ratio',0)}%\n\n"

    # =========================
    # TOP NGÀNH MẠNH
    # =========================

    if heatmap:

        text += "🔥 TOP NGÀNH MẠNH\n"

        for i, sec in enumerate(heatmap[:3], 1):

            if isinstance(sec, tuple):

                name = sec[0]
                score = round(sec[1], 2)

            elif isinstance(sec, dict):

                name = sec.get("sector", "UNKNOWN")
                score = round(sec.get("score", 0), 2)

            else:

                name = sec
                score = ""

            text += f"{i}. {name} ({score})\n"

    text += "\n------------------------------------\n\n"

    # =========================
    # KHÔNG CÓ SNIPER
    # =========================

    if not stocks:

        text += "⚠️ Không có cổ phiếu đạt tiêu chuẩn SNIPER hôm nay.\n"


    # =========================
    # DANH SÁCH CỔ PHIẾU
    # =========================

    for i, s in enumerate(stocks, 1):

        price = s.get("price", 0)

        trend = TREND_MAP.get(s.get("trend"), s.get("trend"))
        breakout = BREAKOUT_MAP.get(s.get("breakout_prob"), s.get("breakout_prob"))
        rs = RS_MAP.get(s.get("rs_rating"), s.get("rs_rating"))

        smart = s.get("smart_money", "KHÔNG")

        if isinstance(smart, list):
            smart = "KHÔNG"

        text += f"🔹 Mục tiêu #{i}: {s.get('symbol','')}\n\n"

        text += f"• Giá hiện tại: {price}\n"
        text += f"• Giá vào dự kiến: {round(price*1.01,2)}\n"
        text += f"• Mục tiêu chốt lời: {round(price*1.2,2)}\n"
        text += f"• Cắt lỗ: {round(price*0.92,2)}\n"

        text += f"• Trạng thái: {s.get('status','')}\n"

        text += f"• Ngành: {s.get('sector','UNKNOWN')}\n"

        text += f"• Cổ phiếu dẫn dắt ngành: {s.get('leader','KHÔNG')}\n"

        text += f"• Xu hướng đa khung: {trend}\n"

        text += f"• Khả năng bứt phá: {breakout}\n"

        text += f"• Tích luỹ: {'CÓ' if s.get('accumulation') else 'KHÔNG'}\n"

        text += f"• Mô hình VCP: {'CÓ' if s.get('vcp') else 'KHÔNG'}\n"

        text += f"• Mô hình AI: {s.get('pattern','KHÔNG')}\n"

        text += f"• Dòng tiền tổ chức: {s.get('institutional_flow','KHÔNG')}\n"

        text += f"• Dòng tiền thông minh: {smart}\n"

        text += f"• Super Breakout: {s.get('super_breakout','THẤP')}\n"

        text += f"• Early Breakout: {'CÓ' if s.get('early_breakout') else 'KHÔNG'}\n"

        text += f"• Dòng tiền cá voi: {s.get('whale_flow','BÌNH THƯỜNG')}\n"

        text += f"• Super Stock: {s.get('super_stock','BÌNH THƯỜNG')}\n"

        text += f"• Xếp hạng: {'SIÊU MẠNH' if s.get('meta_score',0) > 80 else 'MẠNH'}\n"

        text += f"• Meta Score: {s.get('meta_score',0)}\n"

        text += f"• Sức mạnh tương đối: {rs}\n"

        text += f"• Cảnh báo rủi ro: {s.get('risk_warning','BÌNH THƯỜNG')}\n\n"

    # =========================
    # GỬI TELEGRAM
    # =========================

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }
    )
