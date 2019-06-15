import numpy as np
from random import randint
from part1 import *

def calculate_CB(K):
    B = np.zeros((K, K))
    for userCluster in range(K):
        if not U_transpose.has_key(userCluster):
            continue
        for itemCluster in range(K):
            if not V_transpose.has_key(itemCluster):
                continue
            total_avg = 0
            users = U_transpose[userCluster]
            users_count = 0
            for user in users:
                user_items = userTrain_dict[user][1]
                items_inter = set(user_items) & set(V_transpose[itemCluster])
                user_sum = 0
                user_avg = 0
                for item in items_inter:
                    item_index = user_items.index(item)
                    item_rate = userTrain_dict[user][2][item_index]
                    user_sum += item_rate
                if len(items_inter) > 0:
                    user_avg = user_sum / len(items_inter)
                    users_count += 1
                total_avg += user_avg
            if users_count > 0:
                total_avg = total_avg / users_count
                B[userCluster][itemCluster] = total_avg
            else:
                sta_avg = calc_sta_average()
                B[userCluster][itemCluster] = sta_avg
    return B

def ExtractCB(file, K_size=20, T_size=10, E_size=0.01, U_output="", V_output="", B_output=""):
    rows = np.loadtxt(file, delimiter=',', dtype=str, skiprows=1)
    np.random.shuffle(rows)
    size = int(len(rows) * 0.8)
    data_train = rows[:size]
    data_test = rows[size:]
    users, items = get_profiles(data_train)

    for row in rows:
        user = row[0]
        item = row[1]
        random = randint(0, K_size)


ExtractCB('ratings.csv')