"""ZH-cn and english check tools"""


def is_chinese(uchar):
    if u"\u4e00" <= uchar <= u"\9fa5":
        return True
    return False
