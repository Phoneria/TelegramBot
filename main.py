import pandas as pd
from datetime import datetime as dt
import time
from binance import Client
import csv
from datetime import datetime,timedelta
import requests
import pandas_ta as ta



def message(bot_mesaj):
    id_list = ["1598072365"]
    for i in id_list:
        bot_token= "5424258200:AAGNGZlN5HevI2fnyQedvD7v8XPsFFSBBJA"
        url ="https://api.telegram.org/bot"+bot_token+"/sendMessage?chat_id="+i+"&parse_mode=Markdown&text="+bot_mesaj
        response =requests.get(url)



def tg_writer(coin_name,period):



    client =Client(None,None)

    def bring_data(symbol,periot,open,end):
        candles=client.get_historical_klines(symbol,periot,open,end)
        return candles

    def create_csv(symbol,candles):
        csv_file=open(symbol+period+"TG.csv","w",newline="")
        writer=csv.writer(csv_file)
        for candle in candles:
            writer.writerow(candle)

        csv_file.close()

    if period == "30MIN":

        start_time = datetime.today() - timedelta(hours=6)
        finish_time = datetime.today() + timedelta(days=1)
        interval = Client.KLINE_INTERVAL_30MINUTE

    elif period == "1HOUR":

        start_time = datetime.today() - timedelta(hours=9)
        finish_time = datetime.today() + timedelta(days=1)
        interval =  Client.KLINE_INTERVAL_1HOUR

    elif period == "2HOUR":

        start_time = datetime.today() - timedelta(hours=16)
        finish_time = datetime.today() + timedelta(days=1)
        interval = Client.KLINE_INTERVAL_2HOUR

    elif period =="4HOUR":
        start_time = datetime.today() - timedelta(hours=28)
        finish_time = datetime.today() + timedelta(days=1)
        interval = Client.KLINE_INTERVAL_4HOUR

    elif period=="1DAY":

        start_time = datetime.today() - timedelta(days=6)
        finish_time = datetime.today() + timedelta(days=1)
        interval = Client.KLINE_INTERVAL_1DAY




    create_csv(coin_name,bring_data(coin_name, interval, str(start_time), str(finish_time)))


def candle_stick(coin_name,period):

    titles = ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time", "QAV", "NAT", "TBBAV", "TBQAV",
              "ignore"]

    tg_writer(coin_name,period)

    df = pd.read_csv(coin_name + period + "TG.csv", names=titles)






    open_level = df["Open"]
    close_level = df["Close"]
    high_level = df["High"]
    low_level = df["Low"]
    open_time = df["Open Time"]

    def calculate_time(number):
        return dt.fromtimestamp(open_time.iloc[number] / 1000)



    for i in range(5,len(close_level)):
        if True:



            # ENGULF CANDLE
            if  (open_level[i] > close_level[i]) and (close_level[i - 1] > open_level[i - 1]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i-1] - open_level[i-1])):
                message(coin_name + "\nSHORT ENGULF CANDLE")
                message("STRENGTH : 2")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)


            if (open_level[i] < close_level[i]) and (close_level[i - 1] <open_level[i - 1]) and (
                    abs(close_level[i] - open_level[i]) > abs(close_level[i - 1] - open_level[i - 1])):
                message(coin_name + "\nLONG ENGULF CANDLE")
                message("STRENGTH : 2")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            # GREEN CANDLE WITHOUT BOT SHADOW
            if low_level[i] == open_level[i]:
                message(coin_name + "\nGREEN CANDLE WITHOUT BOT SHADOW ")
                message("STRENGTH : 4")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            # RED CANDLE WITHOUT TOP SHADOW
            if high_level[i] == open_level[i]:
                message(coin_name + "\nRED CANDLE WITHOUT TOP SHADOW")
                message("STRENGTH : 4")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            # EVENING STAR
            if (close_level[i] < open_level[i]) and ( abs(close_level[i]-open_level[i])> abs(close_level[i-1]-open_level[i-1])) and (
                    abs(close_level[i-1] - open_level[i-1]) / (high_level[i]-low_level[i]) < 0.3) and (close_level[i-2]>open_level[i-2]) and(
                    abs(close_level[i-2] - open_level[i-2]) >abs (close_level[i]-(open_level[i])))  and(
                    abs(close_level[i-1] - open_level[i-1]) / (high_level[i-1]-low_level[i-1]) < 0.3) and (
                    abs(close_level[i] - open_level[i]) / (high_level[i]-low_level[i]) > 0.3) and (
                    abs(close_level[i-2] - open_level[i-2]) / (high_level[i-2]-low_level[i-2]) > 0.3)  :
                message(coin_name + "\nEVENING STAR")
                message("STRENGTH : 3")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            # MORNING STAR

            if (close_level[i] > open_level[i]) and ( abs(close_level[i]-open_level[i])> abs(close_level[i-1]-open_level[i-1])) and (close_level[i-2]<open_level[i-2]) and(
                    abs(close_level[i-2] - open_level[i-2]) <abs (close_level[i]-(open_level[i]))) and (
                    abs(close_level[i-1] - open_level[i-1]) / (high_level[i-1]-low_level[i-1]) < 0.3) and (
                    abs(close_level[i] - open_level[i]) / (high_level[i]-low_level[i]) > 0.3) and (
                    abs(close_level[i-2] - open_level[i-2]) / (high_level[i-2]-low_level[i-2]) > 0.3) :
                message(coin_name + "\nMORNING STAR")
                message("STRENGTH : 3")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            if (close_level[i] < open_level[i]) and (close_level[i - 1] > open_level[i - 1]) \
                    and (close_level[i - 2] > open_level[i - 2]) and (close_level[i - 3] < open_level[i - 3]) and \
                    (close_level[i - 2] - open_level[i - 2] > open_level[i - 3] - close_level[i - 3]) and \
                    (open_level[i] - close_level[i] > close_level[i - 1] - open_level[i - 1]):
                message(coin_name+ "\nDOUBLE ENGULF SHORT")
                message("STRENGTH : 2")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            if (close_level[i] > open_level[i]) and (close_level[i - 1] < open_level[i - 1]) \
                    and (close_level[i - 2] < open_level[i - 2]) and (close_level[i - 3] > open_level[i - 3]) and \
                    (close_level[i - 2] - open_level[i - 2] < open_level[i - 3] - close_level[i - 3]) and \
                    (open_level[i] - close_level[i] < close_level[i - 1] - open_level[i - 1]):
                message(coin_name+ "\nDOUBLE ENGULF LONG")
                message("STRENGTH : 2")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            if (close_level[i] > open_level[i]) and (close_level[i - 2] > open_level[i - 2]) and (
                    close_level[i - 1] < open_level[i - 1]) and (
                    close_level[i] - open_level[i] > open_level[i - 1] - close_level[i - 1]) and (
                    close_level[i - 2] - open_level[i - 2] > open_level[i - 1] - close_level[i - 1]):

                message(coin_name + "\nTRIPLE CANDLE LONG")
                message("STRENGTH : 3")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
            if (close_level[i] < open_level[i]) and (close_level[i - 2] < open_level[i - 2]) and (
                    close_level[i - 1] > open_level[i - 1]) and (
                    open_level[i] - close_level[i] > close_level[i - 1] - open_level[i - 1]) and (
                    open_level[i - 2] - close_level[i - 2] > close_level[i - 1] - open_level[i - 1]):

                message(coin_name + "\nTRIPLE CANDLE SHORT")
                message("STRENGTH : 3")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)

            if abs(close_level[i]-open_level[i])/(high_level[i]-low_level[i]) < 0.382:
                message(coin_name + "\nDOJI CANDLE")
                message(coin_name+" : "+str(calculate_time(i))+" : "+period)

            if (close_level[i] > open_level[i]) and (close_level[i - 4] > open_level[i - 4]) and (
                    close_level[i - 1] < open_level[i - 1]) and (close_level[i - 2] < open_level[i - 2]) and (
                    close_level[i - 3] < open_level[i - 3]) \
                    and (open_level[i - 4] < open_level[i]):
                message(coin_name + "\nTHREE CANDLE LONG ")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
                message("STRENGTH : 3")

            if (close_level[i] < open_level[i]) and (close_level[i - 4] < open_level[i - 4]) and (
                    close_level[i - 1] > open_level[i - 1]) and (close_level[i - 2] > open_level[i - 2]) and (
                    close_level[i - 3] > open_level[i - 3]) \
                    and (open_level[i - 4] > open_level[i]):
                message(coin_name + "\nTHREE CANDLE SHORT ")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
                message("STRENGTH : 3")


            if (close_level[i]<open_level[i]) and (close_level[i-1]<open_level[i-1]) and (close_level[i-2]<open_level[i-2]) and \
                close_level[i] < low_level[i-1] and close_level[i-1] < low_level[i-2]:

                message(coin_name + "\nTHREE BLACK CROWN")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
                message("STRENGTH : 2")

            if close_level[i] > open_level[i] and close_level[i - 1] > open_level[i - 1] and close_level[i - 2] > open_level[i - 2] and \
                    close_level[i] > high_level[i - 1] and close_level[i - 1] > high_level[i - 2]:
                message(coin_name + "\nTHREE WHITE SOLDIER ")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
                message("STRENGTH : 2")

            if close_level[i] < open_level[i] and \
                    close_level[i - 1] < open_level[i - 1] and \
                    close_level[i - 2] < open_level[i - 2] and \
                    close_level[i - 3] < open_level[i - 3] and \
                    close_level[i - 4] < open_level[i - 4]:
                message(coin_name + "\nFIVE CANDLE SHORT ")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
                message("STRENGTH : 2")
            if close_level[i] > open_level[i] and \
                    close_level[i - 1] > open_level[i - 1] and \
                    close_level[i - 2] > open_level[i - 2] and \
                    close_level[i - 3] > open_level[i - 3] and \
                    close_level[i - 4] > open_level[i - 4]:

                message(coin_name + "\nFIVE CANDLE LONG ")
                message(coin_name + " : " + str(calculate_time(i)) + " : " + period)
                message("STRENGTH : 2")






while True  :
    if (time.localtime().tm_min==29 or time.localtime().tm_min == 59 ) and time.localtime().tm_sec == 0:
        message("NEW MESSAGE!!!!\n30MIN")
        candle_stick("NEARUSDT","30MIN")
        candle_stick("BTCUSDT","30MIN")
        candle_stick("ETHUSDT","30MIN")

    if  time.localtime().tm_min == 59 and time.localtime().tm_sec == 10:
        message("NEW MESSAGE!!!!\n1HOUR")
        candle_stick("NEARUSDT", "1HOUR")
        candle_stick("BTCUSDT", "1HOUR")
        candle_stick("ETHUSDT", "1HOUR")

    if  time.localtime().tm_hour%2 == 1 and time.localtime().tm_min == 59 and time.localtime().tm_sec == 20:
        message("NEW MESSAGE!!!!\n2HOUR")
        candle_stick("NEARUSDT", "2HOUR")
        candle_stick("BTCUSDT", "2HOUR")
        candle_stick("ETHUSDT", "2HOUR")


    if  time.localtime().tm_hour%4 == 2 and time.localtime().tm_min == 59 and time.localtime().tm_sec == 30:
        message("NEW MESSAGE!!!!\n4HOUR")
        candle_stick("NEARUSDT", "4HOUR")
        candle_stick("BTCUSDT", "4HOUR")
        candle_stick("ETHUSDT", "4HOUR")


    if  time.localtime().tm_hour%24 == 2 and time.localtime().tm_min == 59 and time.localtime().tm_sec == 40:
        message("NEW MESSAGE!!!!\n1DAY")
        candle_stick("NEARUSDT", "1DAY")
        candle_stick("BTCUSDT", "1DAY")
        candle_stick("ETHUSDT", "1DAY")
