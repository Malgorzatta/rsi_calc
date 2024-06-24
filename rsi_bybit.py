import pandas as pd
from datetime import datetime, timedelta
days = 14
current_datetime = datetime.now()
current_timestamp = int(current_datetime.timestamp())*1000
previous_datetime = current_datetime - timedelta(days=14)
previous_timestamp = int(previous_datetime.timestamp())*1000
print("Current datetime:", current_datetime, "Start datetime (14 days difference):", previous_datetime)
# print("Current timestamp =",current_timestamp, "Start timestamp (14 days difference):", previous_timestamp)

from pybit.unified_trading import HTTP
session = HTTP(testnet=True)
data = session.get_kline(category="spot", symbol="SOLUSDT", interval=60, start=previous_timestamp, end=current_timestamp, limit = 2000)
# print(data)

prices = []
for close_price in data['result']['list']:
    # print('Close price =', close_price[4])
    prices.append(float(close_price[4]))
# print(prices)

start_times = []
for start_time in data['result']['list']:
    # print('Start time =', start_time[0])
    time=float(start_time[0])/1000
    # print(time)
    dt_object = datetime.fromtimestamp(time)
    # print(dt_object)
    start_times.append(dt_object)
    # print(start_time)
# print(start_times)

df_dict = {'Start time':start_times,'Close price':prices}
df = pd.DataFrame(df_dict)
# print(df)

#Calculate RSI
delta = df['Close price'].diff(1)
delta.dropna(inplace=True)

positive = delta.copy()
negative = delta.copy()
positive[positive<0] = 0
negative[negative>0] = 0

avg_gain = positive.ewm(days).mean()
avg_loss = abs(negative.ewm(days).mean())

rs = avg_gain / avg_loss
rsi = 100 - (100/(1+rs))
# print(rsi)
df['RSI'] = rsi

# for el in rsi:
#     # print(el)
#     if el>=70:
#         print('RSI>70 -> RSI =', el, 'for',days,'days calculation')
#     elif el<=30:
#         print('RSI<30 -> RSI =', el, 'for',days,'days calculation')
last_el = rsi.iloc[-1]
# print(last_el)
if last_el >= 70:
    print('RSI>70 -> RSI =', last_el, 'for RSI period', days, 'days.')
elif last_el <= 30:
    print('RSI<30 -> RSI =', last_el, 'for RSI period', days, 'days.')
# print(df)
# df.to_csv('out.csv')