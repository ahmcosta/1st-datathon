import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('files/resulting_data.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots, None)  # skip the headers
    for row in plots:
        x.append(int(row[4]))
        y.append(int(row[0]))

plt.scatter(x, y)
plt.xlabel('Net Score')
plt.ylabel('Number of Retweets')
plt.title('1st Datathon\nSentiments analysis')
plt.show()
