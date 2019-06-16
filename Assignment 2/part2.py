import math
from flask import Flask
from flask import request
import numpy as np
from random import randint
from part1 import *

app = Flask(__name__)

def init_vec(K, users, items):
    # U = map(lambda x: x, users)
    U = {x: randint(0, K - 1)for x in users}
    V = {x: randint(0, K - 1)for x in items}

    cluster4user = cluster4vec(K, U, users)
    cluster4item = cluster4vec(K, V, items)
    return cluster4user, cluster4item, U, V

def cluster4vec(K, vec, lst):
    T = {}
    for id in lst:
        if T.has_key(vec[id]):
            T[vec[id]].append(id)
        else:
            T[vec[id]] = [id]
    return T

def average_rating(users):
    temp = np.array([])
    for arr in users.values():
        temp = np.append(temp, arr[1], axis=0)
    stAvg = np.mean(temp.astype(np.float))
    return stAvg

def update_B(K, data_train, cluster4user, cluster4item):
    B = np.zeros((K, K))
    avg_ast = 0
    for userU in range(K):
        if not cluster4user.has_key(userU):
            continue
        for itemV in range(K):
            if not cluster4item.has_key(itemV):
                continue
            avg = 0
            users_count = 0
            for user in cluster4user[userU]:
                user_items = data_train[user][0]
                combain_item = set(user_items) & set(cluster4item[itemV])
                user_sum = 0
                user_avg = 0
                for item in combain_item:
                    item_index = user_items.index(item)
                    user_sum += float(data_train[user][1][item_index])
                if len(combain_item) > 0:
                    user_avg = user_sum / len(combain_item)
                    users_count += 1
                avg += user_avg

            B[userU][itemV] = avg / users_count if users_count > 0 else avg_ast if avg_ast != 0 else average_rating(data_train)
    return B

def updateVector(data, cluster, B, vecToUpdate, secondVec):
    for key in data:
        user_profile = data[key]
        match_user_cluster = {}
        for k in cluster:
            sum = 0
            for index in range(len(user_profile[1])):
                item_id = user_profile[0][index]
                temp = math.pow(float(user_profile[1][index]) - float(B[k][secondVec[item_id]]), 2)
                sum += temp

            match_user_cluster[k] = sum
        user_new = min(match_user_cluster, key=match_user_cluster.get)
        cluster[vecToUpdate[key]].remove(key)
        vecToUpdate[key] = user_new
        cluster[user_new].append(key)


def updet_rmse(users, B, U, V):
    sumSqr = 0
    item_count = 0
    average = 0
    items_count = 0
    for row in range(B.shape[0]):
        for col in range(B.shape[1]):
            if B[row][col] > 0:
                average += B[row][col]
                items_count += 1
    B_mean = average / items_count
    for userId in users:
        user_profile = users[userId]
        for index in range(len(user_profile[1])):
            item_id = user_profile[0][index]
            if U.has_key(userId):
                b_rating = B[U[userId]][V[item_id]] if V.has_key(item_id) else B_mean
            else:
                b_rating = B_mean
            test_rating = user_profile[1][index]
            temp = math.pow(float (b_rating) - float(test_rating), 2)
            sumSqr += temp
            item_count += 1
    return math.sqrt(sumSqr / item_count )


def ExtractCB(file, K_size=20, T_size=10, E_size=0.01, U_output="", V_output="", B_output=""):
    rows = np.loadtxt(file, delimiter=',', dtype=str, skiprows=1)
    np.random.shuffle(rows)
    size = int(len(rows) * 0.8)
    data_train = rows[:size]
    data_test = rows[size:]
    users, items = get_profiles(data_train)
    cluster4user, cluster4item, U, V = init_vec(K_size, users, items)
    B = update_B(K_size, users, cluster4user, cluster4item)
    min_gap = 10000
    rmse = 0
    iters=1
    while T_size > iters and min_gap > E_size:
        updateVector(users, cluster4user, B, U, V)
        B2 = update_B(K_size, users, cluster4user, cluster4item)
        updateVector(items, cluster4item, B2, V, U)
        B2 = update_B(K_size, users, cluster4user, cluster4item)
        i = updet_rmse(users, B2, U, V)
        min_gap = math.fabs(i - rmse)
        B = B2
        rmse = i
        iters = iters + 1


    write(U_output, U)
    write(V_output, V)

    with open(B_output, 'wb') as b_file:
        writer = csv.writer(b_file)
        writer.writerows(B)


def write(filename, data):
    with open(filename, 'wb') as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])


@app.route('/', methods=['GET','POST'])
def serve_part2():
    # get request arguments
    user_id = request.args.get('userid')
    n = request.args.get('n')

    # input validations
    if user_id is None:
        return "user id is invalid"
    if n is None:
        return "n is invalid"
    try:
        int(n)
    except Exception:
        return "n is not a number"


    # ExtractCB(argsDict['rating_file'], argsDict['K'], argsDict['T'], argsDict['epsilon'], argsDict['u_file'],
    #           argsDict['v_file'], argsDict['b_file'])
    # return highest_predictions


if __name__ == '__main__':
    print "web service is running"
    app.run(debug=True)
    # ExtractCB('ratings.csv', U_output="U_output2.csv", V_output="V_output2.csv", B_output="B_output2.csv")