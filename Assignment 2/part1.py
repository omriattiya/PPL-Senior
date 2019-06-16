import numpy as np
import csv



def ExtractProfiles(file, user_profile_output, item_profile_output):
    a = np.loadtxt(file, delimiter=',', dtype=str, skiprows=1)
    users = np.unique(a[:, 0])
    items = np.unique(a[:, 1])
    user_pro = { i : ([],[]) for i in users }
    item_pro = { i : ([],[]) for i in items }


    for row in a:
        user_pro[row[0]][0].append(row[1])
        user_pro[row[0]][1].append(row[2])
        item_pro[row[1]][0].append(row[0])
        item_pro[row[1]][1].append(row[2])


    with open(user_profile_output, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for user in users:
            writer.writerow([user, user_pro[user][0], user_pro[user][1]])

    with open(item_profile_output, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in item_pro:
            writer.writerow([item, item_pro[item][0], item_pro[item][1]])


ExtractProfiles('ratings.csv', 'user profile.csv', 'items profile.csv')