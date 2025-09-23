def rgb_toFloat(value:list)->float:
    return [value[0]/225,value[1]/225,value[2]/225, value[3]]

def hex_to_rgba(color_item):
    """
    Преобразует ["#RRGGBB", alpha] в [r, g, b, alpha] (0..1).
    
    :param color_item: список ["#RRGGBB", alpha], например ["#0c213c", 1]
    :return: список [r, g, b, alpha]
    """
    hex_color, alpha = color_item
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return [r, g, b, float(alpha)]

def ms_to_time(ms: int, mode: str = "min_sec"):
    """
    Конвертирует миллисекунды в разные форматы.
    
    mode:
      - "min_sec" -> строка "MM:SS"
      - "sec"     -> только секунды (int)
    """
    seconds = ms // 1000
    
    if mode == "sec":
        return seconds
    
    minutes = seconds // 60
    sec = seconds % 60
    return f"{minutes:02d}:{sec:02d}"


def s_to_time(seconds: int):    
    minutes = seconds // 60
    sec = seconds % 60
    return f"{int(minutes):02d}:{int(sec):02d}"