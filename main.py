import csv
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = 'data.csv'
DATA_LENGTH = 1000  # 1039
START_MONEY = 10000
NUMBER_OF_ACTIONS = 0


def draw_chart(data):
    plt.plot(data)


def calc_macd(dataa, day):
    ema1 = calc_ema(dataa, day, 12)
    ema2 = calc_ema(dataa, day, 26)
    return ema1 - ema2


def calc_ema(values, end, days):
    result = 0.0
    denominator = 0.0
    one_minus_alfa = (1.0 - (2.0 / (days + 1)))
    for i in range(0, days):
        exponent = one_minus_alfa ** i
        if (end - i) > 0:
            result += (values[end - i] * exponent)
        else:
            result += values[0] * exponent
        denominator += exponent
    return result / denominator


def calc_signal(data, day):
    return calc_ema(data, day, 9)


def sell(prices, number_of_actions, index):
    roi = number_of_actions * prices[index]
    return roi


def buy(prices, money, index):
    number_of_actions = money / prices[index]
    return number_of_actions


def check_signals(macd, signal, day):
    if macd[day - 1] < signal[day - 1] and macd[day + 1] > signal[day + 1]:
        return 1
    elif macd[day - 1] > signal[day - 1] and macd[day + 1] < signal[day + 1]:
        return -1
    else:
        return 0


if __name__ == '__main__':
    with open(DATA_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        input_data = []
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
                # print(#f'\t data: {row["Data"]}  cena: {row["Zamkniecie"]} ')
            line_count += 1
            input_data.append(float(row['Zamkniecie']))
        print(f'Processed {line_count} lines.')
        DATA_LENGTH = line_count - 1
    macd_line = []
    macd_signal = []
for i in range(0, 1000):
    macd_line.append(calc_macd(input_data, i))
    macd_signal.append(calc_signal(macd_line, i))

draw_chart(input_data)
plt.legend(["wig 20"])
plt.grid()
plt.show()

draw_chart(macd_line)
draw_chart(macd_signal)
plt.legend(['macd', 'signal'])
plt.axis([0, 1000, -100, 100])
plt.grid()
# x = np.arange(0, 1000)
# f = np.array(macd_line)
# g = np.array(macd_signal)
# idx = np.argwhere(np.diff(np.sign(f - g))).flatten()
# plt.plot(x[idx], f[idx], 'ro', markersize=2.0)


money = START_MONEY
actions = NUMBER_OF_ACTIONS
bankrupt = False

for day in range(1, 999):
    check = check_signals(macd=macd_line, signal=macd_signal, day=day)
    if check == 1 and money != 0:
        actions = buy(prices=input_data, money=money, index=day)
        money = 0
        print("Bought {0} actions on day {1}".format(actions, day))

    elif check == -1 and actions != 0:
        money = sell(prices=input_data, number_of_actions=actions, index=day)
        actions = 0
        print("Sold for {0} money on day {1}".format(money, day))
    if money == 0 and actions == 0:
        bankrupt = True
        break

if actions != 0:
    money = sell(input_data, actions, 999)

print("\nMoney: ", money)
if money > START_MONEY and START_MONEY != 0:
    print("You earned {0} percent".format((money - START_MONEY) / START_MONEY * 100))
if money < START_MONEY and START_MONEY != 0:
    print("You lost {0} percent".format((money - START_MONEY) / START_MONEY * 100))
plt.show()
