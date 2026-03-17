def supply_dryup(s):

    volume = s.get("volume")

    if volume is None or len(volume) < 20:
        return False

    try:

        avg = float(volume.tail(20).mean())
        last = float(volume.iloc[-1])

        return last < avg * 0.7

    except:
        return False
        
