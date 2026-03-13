SECTOR_MAP = {

    # DẦU KHÍ
    "BSR": "DẦU KHÍ",
    "PLX": "DẦU KHÍ",
    "PVD": "DẦU KHÍ",
    "PVS": "DẦU KHÍ",
    "OIL": "DẦU KHÍ",

    # PHÂN BÓN
    "DPM": "PHÂN BÓN",
    "DCM": "PHÂN BÓN",
    "BFC": "PHÂN BÓN",
    "DDV": "PHÂN BÓN",
  
    # XÂY DỰNG
    "VCG": "XÂY DỰNG",
    "CTD": "XÂY DỰNG",
    "FCN": "XÂY DỰNG",
    "HBC": "XÂY DỰNG",

    # BẤT ĐỘNG SẢN
    "NVL": "BẤT ĐỘNG SẢN",
    "VHM": "BẤT ĐỘNG SẢN",
    "PDR": "BẤT ĐỘNG SẢN",
    "DXG": "BẤT ĐỘNG SẢN",

    # NGÂN HÀNG
    "VCB": "NGÂN HÀNG",
    "BID": "NGÂN HÀNG",
    "CTG": "NGÂN HÀNG",
    "MBB": "NGÂN HÀNG",
    "TCB": "NGÂN HÀNG",
    "STB": "NGÂN HÀNG",

    # CHỨNG KHOÁN
    "SSI": "CHỨNG KHOÁN",
    "VND": "CHỨNG KHOÁN",
    "HCM": "CHỨNG KHOÁN",
    "SHS": "CHỨNG KHOÁN",

    # ĐIỆN
    "GEG": "ĐIỆN",
    "POW": "ĐIỆN",
    "NT2": "ĐIỆN",
    "REE": "ĐIỆN"
}


def detect_sector(symbol):

    return SECTOR_MAP.get(symbol, "KHÁC")


def sector_rotation(stocks):

    sector_strength = {}

    for s in stocks:

        sector = detect_sector(s["symbol"])
        s["sector"] = sector

        if sector not in sector_strength:
            sector_strength[sector] = 0

        sector_strength[sector] += s.get("change", 0)

    if not sector_strength:
        return stocks

    leader_sector = max(sector_strength, key=sector_strength.get)

    for s in stocks:

        if s["sector"] == leader_sector:
            s["leader"] = "CÓ"
        else:
            s["leader"] = "KHÔNG"

    return stocks
