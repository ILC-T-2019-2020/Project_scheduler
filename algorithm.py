# import necessary files
import csv
from tests import calculate_points_for_pair
import argparse

# note: this requires similar arguments to the test.py script
parser = argparse.ArgumentParser()
parser.add_argument('--alpha', type=int, default='20', help='weight for preference')
parser.add_argument('--beta', type=int, default='5', help='penalty for difference in classes')
parser.add_argument('--debug', default=False, help='whether to run program in debug mode or not')
args = parser.parse_args()


with open('ilct_studentdata.csv', newline='') as f:
    reader = csv.reader(f)
    data = [tuple(row) for row in reader]
f.close()

#get rid of the headers
data.pop(0)

with open('ilct_studentdata.csv', "rt") as csvfile:
    dataset_contents = list(csv.reader(csvfile, delimiter = ','))


# greedy algorithm solution: (note: could possibly try to optimate which time is used in a better way)
# -------------------------------------------
length = len(data)
matching = list()
i = 0
used_ind = list()
while i < length:
    if i not in used_ind:
        used_ind.append(i)
        n = data[i][4]
        max = ()
        j = 1
        while j < length:
            if j not in used_ind:
                m = data[j][4]
                score = calculate_points_for_pair(args, dataset_contents, i+1, (i,j,n))
                if max == ():
                    max = (score, (i,j,n))
                elif score > max[0]:
                    max = (score, (i,j,n))
            j+=1
        matching.append(max[1])
        used_ind.append(max[1][1])
    i+=1
# -------------------------------------------


with open('test_sol.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(matching)
f.close()