import numpy as np
import csv
import sys


def get_profiles(data):
    users = np.unique(data[:, 0])
    items = np.unique(data[:, 1])
    user_pro = {i: ([], []) for i in users}
    item_pro = {i: ([], []) for i in items}

    for row in data:
        user_pro[row[0]][0].append(row[1])
        user_pro[row[0]][1].append(row[2])
        item_pro[row[1]][0].append(row[0])
        item_pro[row[1]][1].append(row[2])

    return user_pro, item_pro


def ExtractProfiles(file, user_profile_output, item_profile_output):
    a = np.loadtxt(file, delimiter=',', dtype=str, skiprows=1)

    user_pro, item_pro = get_profiles(a)

    with open(user_profile_output, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for user in user_pro:
            writer.writerow([user, user_pro[user][0], user_pro[user][1]])

    with open(item_profile_output, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in item_pro:
            writer.writerow([item, item_pro[item][0], item_pro[item][1]])


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "not enough args"
    else:
        rating_input_file = sys.argv[1]
        user_profile_output_directory = sys.argv[2]
        if '/' not in user_profile_output_directory[-1:]:
            user_profile_output_directory = user_profile_output_directory + '/'
        item_profile_output_directory = sys.argv[3]
        if '/' not in item_profile_output_directory[-1:]:
            item_profile_output_directory = item_profile_output_directory + '/'
        user_csv = user_profile_output_directory + 'user profile.csv'
        item_csv = item_profile_output_directory + 'items profile.csv'
        ExtractProfiles(rating_input_file, user_csv, item_csv)
