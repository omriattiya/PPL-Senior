import numpy as np
import csv

# users = []
# items = []
# with open('ratings.csv', 'rb') as csvfile:
#     rating = csv.reader(csvfile, delimiter=',')
#     next(rating, None)
#     for row in rating:
#         users.append(row[0])
#         items.append(row[1])
# users = set(users)
# items = set(items)
# with open('user_profiles .csv', 'wb') as csvfile:
#     csv_user = csv.writer(csvfile)
#     for user in users:
#         csv_user.writerow([user])
#
# with open('items_profiles .csv', 'wb') as csvfile:
#     csv_item = csv.writer(csvfile, delimiter=',')
#     for item in items:
#         csv_item.writerow([item])


a = np.loadtxt('ratings.csv', delimiter=',', dtype=str, skiprows=1)

# print(a)

#, open('user_profiles', '')
c = np.unique(a[:, 0], return_counts=True)
items = np.split(a[:, 1], np.cumsum(np.unique(a[:, 0], return_counts=True)[1])[:-1])
rating = np.split(a[:, 2], np.cumsum(np.unique(a[:, 0], return_counts=True)[1])[:-1])
data = np.array(c, items, rating)

print items

