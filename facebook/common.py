import datetime
def log(log_text, message="empty", ):
    now_time = new_time()
    # 在文本框中打印日志信息
    log_text.insert("end", now_time+": "+message + "\n")
    # 滚动到文本框底部
    log_text.see("end")
def new_time():
    # 获取当前日期和时间
    current_datetime = datetime.datetime.now()

    # 获取年、月、日
    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day

    # 获取时、分、秒
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second
    return "{}年{}月{}日 {}时{}分{}秒".format(year, month, day, hour, minute, second)
