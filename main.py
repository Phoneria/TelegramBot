import pandas as pd
from datetime import datetime as dt
import time
from binance import Client
import csv
from datetime import datetime, timedelta
import pandas_ta as ta
import requests


def message(bot_mesaj):
    id_list = ["1598072365"]
 
 
    for i in id_list:
        bot_token = "5424258200:AAGNGZlN5HevI2fnyQedvD7v8XPsFFSBBJA"
        url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + i + "&parse_mode=Markdown&text=" + bot_mesaj
        response = requests.get(url)


def tg_writer(coin_name):
    client = Client(None, None)

    def bring_data(symbol, periot, open, end):
        candles = client.get_historical_klines(symbol, periot, open, end)
        return candles

    def create_csv(symbol, candles):
        csv_file = open(symbol + "30MINTG.csv", "w", newline="")
        writer = csv.writer(csv_file)
        for candle in candles:
            writer.writerow(candle)

        csv_file.close()

    start_time = datetime.today() - timedelta(hours=50)
    finish_time = datetime.today() + timedelta(days=1)
    interval = Client.KLINE_INTERVAL_30MINUTE

    create_csv(coin_name, bring_data(coin_name, interval, str(start_time), str(finish_time)))


def candle_stick(coin_name):
    titles = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "QAV", "NAT", "TBBAV", "TBQAV",
              "ignore"]

    tg_writer(coin_name)

    df = pd.read_csv(coin_name + "30MINTG.csv", names=titles)

    open_level = df["Open"]
    close_level = df["Close"]
    high_level = df["High"]
    low_level = df["Low"]
    open_time = df["Open Time"]

    def calculate_time(number):
        return dt.fromtimestamp(open_time.iloc[number] / 1000)

    max_level = 0
    min_level = 0
    for i in range(5, len(close_level)):


        if calculate_time(i).hour == time.localtime().tm_hour and calculate_time(i).day==datetime.today().day:
            if max_level[i] < high_level[i]:
                message(
                    coin_name + "\nSON 100 MUMUN EN YÜKSEK SEVİYESİ" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            if min_level[i] < low_level[i] :
                message(
                    coin_name + "\nSON 100 MUMUN EN DÜŞÜK SEVİYESİ" + " \nZAMAN :  " + str(
                        calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))


            # ENGULF CANDLE
            if (open_level[i] > close_level[i]) and (close_level[i - 1] > open_level[i - 1]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])):
                message(coin_name + "\nSHORT ENGULF MUMU" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (open_level[i] < close_level[i]) and (close_level[i - 1] < open_level[i - 1]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])):
                message(coin_name + "\nLONG ENGULF MUMU" + "\nZAMAN : " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            # GREEN CANDLE WITHOUT BOT SHADOW
            if low_level[i] == open_level[i]:
                message(coin_name + "\nALT İĞNESİZ YEŞİL MUM " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            # RED CANDLE WITHOUT TOP SHADOW
            if high_level[i] == open_level[i]:
                message(
                    coin_name + "\nÜST İĞNESİZ KIRMIZI MUM" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                        calculate_time(i).minute))

            # EVENING STAR
            if (close_level[i] < open_level[i]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])) and (
                    abs(close_level[i - 1] - open_level[i - 1]) / (high_level[i] - low_level[i]) < 0.3) and (
                    close_level[i - 2] > open_level[i - 2]) and (
                    abs(close_level[i - 2] - open_level[i - 2]) > abs(close_level[i] - (open_level[i]))) and (
                    abs(close_level[i - 1] - open_level[i - 1]) / (high_level[i - 1] - low_level[i - 1]) < 0.3) and (
                    abs(close_level[i] - open_level[i]) / (high_level[i] - low_level[i]) > 0.3) and (
                    abs(close_level[i - 2] - open_level[i - 2]) / (high_level[i - 2] - low_level[i - 2]) > 0.3):
                message(coin_name + "\nGECE YILDIZI" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            # MORNING STAR

            if (close_level[i] > open_level[i]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])) and (
                    close_level[i - 2] < open_level[i - 2]) and (
                    abs(close_level[i - 2] - open_level[i - 2]) < abs(close_level[i] - (open_level[i]))) and (
                    abs(close_level[i - 1] - open_level[i - 1]) / (high_level[i - 1] - low_level[i - 1]) < 0.3) and (
                    abs(close_level[i] - open_level[i]) / (high_level[i] - low_level[i]) > 0.3) and (
                    abs(close_level[i - 2] - open_level[i - 2]) / (high_level[i - 2] - low_level[i - 2]) > 0.3):
                message(coin_name + "\nSABAH YILDIZI" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 1] > open_level[i - 1]) \
                    and (close_level[i - 2] > open_level[i - 2]) and (close_level[i - 3] < open_level[i - 3]) and \
                    (close_level[i - 2] - open_level[i - 2] > open_level[i - 3] - close_level[i - 3]) and \
                    (open_level[i] - close_level[i] > close_level[i - 1] - open_level[i - 1]):
                message(coin_name + "\nİKİLİ ENGULF SHORT" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] > open_level[i]) and (close_level[i - 1] < open_level[i - 1]) \
                    and (close_level[i - 2] < open_level[i - 2]) and (close_level[i - 3] > open_level[i - 3]) and \
                    (close_level[i - 2] - open_level[i - 2] < open_level[i - 3] - close_level[i - 3]) and \
                    (open_level[i] - close_level[i] < close_level[i - 1] - open_level[i - 1]):
                message(coin_name + "\nİKİLİ ENGULF LONG" + "\nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] > open_level[i]) and (close_level[i - 2] > open_level[i - 2]) and (
                    close_level[i - 1] < open_level[i - 1]) and (
                    close_level[i] - open_level[i] > open_level[i - 1] - close_level[i - 1]) and (
                    close_level[i - 2] - open_level[i - 2] > open_level[i - 1] - close_level[i - 1]):
                message(coin_name + "\nSANDVİÇ LONG" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 2] < open_level[i - 2]) and (
                    close_level[i - 1] > open_level[i - 1]) and (
                    open_level[i] - close_level[i] > close_level[i - 1] - open_level[i - 1]) and (
                    open_level[i - 2] - close_level[i - 2] > close_level[i - 1] - open_level[i - 1]):
                message(coin_name + "\nSANDVİÇ SHORT" + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] > open_level[i]) and (close_level[i - 4] > open_level[i - 4]) and (
                    close_level[i - 1] < open_level[i - 1]) and (close_level[i - 2] < open_level[i - 2]) and (
                    close_level[i - 3] < open_level[i - 3]) \
                    and (open_level[i - 4] < open_level[i]):
                message(coin_name + "\nÜÇLÜ ENGULF LONG " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 4] < open_level[i - 4]) and (
                    close_level[i - 1] > open_level[i - 1]) and (close_level[i - 2] > open_level[i - 2]) and (
                    close_level[i - 3] > open_level[i - 3]) \
                    and (open_level[i - 4] > open_level[i]):
                message(coin_name + "\nÜÇLÜ ENGULF SHORT " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if (close_level[i] < open_level[i]) and (close_level[i - 1] < open_level[i - 1]) and (
                    close_level[i - 2] < open_level[i - 2]) and \
                    close_level[i] < low_level[i - 1] and close_level[i - 1] < low_level[i - 2]:
                message(coin_name + "\nÜÇ KARA KARGA" + "\nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if close_level[i] > open_level[i] and close_level[i - 1] > open_level[i - 1] and close_level[i - 2] > \
                    open_level[i - 2] and \
                    close_level[i] > high_level[i - 1] and close_level[i - 1] > high_level[i - 2]:
                message(coin_name + "\nÜÇ BEYAZ ASKER " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if close_level[i] < open_level[i] and \
                    close_level[i - 1] < open_level[i - 1] and \
                    close_level[i - 2] < open_level[i - 2] and \
                    close_level[i - 3] < open_level[i - 3] and \
                    close_level[i - 4] < open_level[i - 4]:
                message(coin_name + "\nBEŞ MUM SHORT " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute))

            if close_level[i] > open_level[i] and \
                    close_level[i - 1] > open_level[i - 1] and \
                    close_level[i - 2] > open_level[i - 2] and \
                    close_level[i - 3] > open_level[i - 3] and \
                    close_level[i - 4] > open_level[i - 4]:
                message(coin_name + "\nBEŞ MUM LONG " + " \nZAMAN :  " + str(calculate_time(i).hour + 3) + " : " + str(
                    calculate_time(i).minute ))



        else:
            if high_level[i] >= max_level:
                max_level = high_level[i]
            if low_level[i] <= min_level:
                min_level = low_level[i]




message("YENİDEN BAŞLADI")
candle_stick("NEARUSDT")
candle_stick("BTCUSDT")



