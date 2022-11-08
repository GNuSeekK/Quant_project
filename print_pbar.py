import sys

def visualize_pbar(value: int, endvalue: int, bar_length: int=20):
    """
    pbar 시각화
    
    Args:
        value (int): 현재 값
        endvalue (int): 끝 값
        bar_length (int, optional): 바 길이. Defaults to 20.
    """    
    percent = float(value) / endvalue
    if percent <= 0.33:
        color = 91
    elif percent <= 0.66:
        color = 93
    elif percent == 1:
        color = 92
    else:
        color = 96
    complete = '<' + '▮' * int(round(percent * bar_length))
    remain = '▯' * (bar_length - (len(complete) - 1)) + '>'
    sys.stdout.write(f"\r\033[{color}m Percent: [{complete+remain}] {round(percent*100,2)}%\033[0m")
    sys.stdout.flush()