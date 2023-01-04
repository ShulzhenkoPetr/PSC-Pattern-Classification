from datetime import datetime

x = '2016-01-06 07:00:00'
y = '2017-01-06 07:00:00'

x_d = datetime.strptime(x.split(' ')[0], '%Y-%m-%d')
y_d = datetime.strptime(y.split(' ')[0], '%Y-%m-%d')
print(x_d + 0.5 * (y_d - x_d))
print(datetime.strftime(x_d, '%Y-%m-%d'))
print(str(x_d))