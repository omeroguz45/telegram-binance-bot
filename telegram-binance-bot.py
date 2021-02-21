from binance.client import Client
import os
import time
import telebot

api_key = '2ZnUznXVAsxk6xjZ89ZEHS5cuKkpiMUvhUH7SNvZg6BWCCzmgY2ijMPfpj14eufd'
api_secret = 'uvf54i7l3gdNPouQD0HJQxNqVp99ge6mkywVTRBQIWvkJgrxWoutBYF1EWj5H7Aa'

bot_key = "1603927687:AAHgFNeR7FLIF6z9LrLqSEonWX1OmPH-TNg"

def main():
    client = Client(api_key, api_secret)

    info = client.get_account()

    balance_BTC = float(client.get_asset_balance(asset='BTC')['free'])
    balance_BNB = float(client.get_asset_balance(asset='BNB')['free'])

    fees = client.get_trade_fee(symbol='BTCUSDT')

    BTC_TRY = float(client.get_avg_price(symbol='BTCTRY')['price'])
    BNB_TRY = float(client.get_avg_price(symbol='BNBTRY')['price'])

    initial_investment = 3254.32
    tot_balance = (balance_BTC*BTC_TRY) + (balance_BNB*BNB_TRY)
    delta = tot_balance-initial_investment
    margin = ((delta)/initial_investment)*100

    return tot_balance, delta, margin

while True:
    try:
        tot_balance, delta, margin = main()
        bot = telebot.TeleBot(bot_key)
    except:
        time.sleep(1)

    @bot.message_handler(commands=['start'])
    def handle_command(message):
        bot.reply_to(message, "Hello, welcome to Ömer's Binance Bot!")

    @bot.message_handler(commands=['help'])
    def handle_command(message):
        bot.reply_to(message, "/total command shows total balance.\n/profit command shows profit delta and margin.")

    @bot.message_handler(commands=['total'])
    def handle_command(message):
        bot.reply_to(message, f"Total balance: {str(round(tot_balance, 2))} TRY")

    @bot.message_handler(commands=['profit'])
    def handle_command(message):
        bot.reply_to(message, f"Profit: {str(round(margin, 2))}% {str(round(delta, 2))} TRY")

    bot.polling()