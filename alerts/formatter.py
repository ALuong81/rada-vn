def format_signal(symbol, price, entry, target, stop, prob):

    return f"""
📈 TÍN HIỆU CỔ PHIẾU

Mã: {symbol}

💰 Giá hiện tại: {price}

🎯 Giá vào: {entry}

🏆 Mục tiêu: {target}

🛑 Cắt lỗ: {stop}

📊 Xác suất: {prob:.1f}%

"""
