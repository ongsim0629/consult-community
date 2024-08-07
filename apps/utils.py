from datetime import datetime, timedelta


def formatDateTimeToStr(datetime):
    return datetime.strftime("%Y/%m/%d %H:%M:%S")


def createNow():
    # TODO: 현지시각 맞춰서 변경되도록, 현재는 UTC+9 한국만 지원
    return datetime.now() + timedelta(hours=9)
