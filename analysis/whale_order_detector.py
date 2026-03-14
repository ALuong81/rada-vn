def detect_whale_orders(s):

    volume = s.get("volume",0)
    avg_volume = s.get("avg_volume",0)

    if avg_volume == 0:
        return False

    if volume > avg_volume * 3:
        return "CÁ VOI MUA"

    if volume > avg_volume * 2:
        return "DÒNG TIỀN LỚN"

    if volume > avg_volume * 2:
        return "CÓ DẤU HIỆU"
    
    return "BÌNH THƯỜNG"
