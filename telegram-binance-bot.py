from binance.client import Client
import os
import time
import telebot
import yaml

def key_init():
    with open('./keys.yaml', 'r') as f:
        KEYS = yaml.load(f, Loader=yaml.FullLoader)
    
    return KEYS

def get_wallet_balance(BINANCE_API_KEY, BINANCE_API_SECRET):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    info = client.get_account()

    balance_BTC = float(client.get_asset_balance(asset='BTC')['free'])
    balance_BNB = float(client.get_asset_balance(asset='BNB')['free'])

    BTC_TRY = float(client.get_avg_price(symbol='BTCTRY')['price'])
    BNB_TRY = float(client.get_avg_price(symbol='BNBTRY')['price'])

    initial_investment = 3254.32
    tot_balance = (balance_BTC*BTC_TRY) + (balance_BNB*BNB_TRY)
    delta = tot_balance-initial_investment
    margin = ((delta)/initial_investment)*100

    return tot_balance, delta, margin

def telegram_bot(TELEGRAM_BOT_KEY, tot_balance, delta, margin):
    bot = telebot.TeleBot(TELEGRAM_BOT_KEY)

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
        if delta < 0:
            bot.reply_to(message, f"Loss: {str(round(margin, 2))}% {str(round(delta, 2))} TRY")
        else:
            bot.reply_to(message, f"Profit: {str(round(margin, 2))}% {str(round(delta, 2))} TRY")

    bot.polling()

def main():
    KEYS = key_init()
    while True:
        try:
            tot_balance, delta, margin = get_wallet_balance(KEYS['BINANCE_API_KEY'], KEYS['BINANCE_API_SECRET'])
            telegram_bot(KEYS['TELEGRAM_BOT_KEY'], tot_balance, delta, margin)
        except:
            time.sleep(1)

if __name__ == '__main__':
    main()
