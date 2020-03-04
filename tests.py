import argparse
import csv

# Evaluate points for a given pairing solution
def calculate_points_for_pair(args, dataset_contents, key, pairing):
    alpha = args.alpha
    beta = args.beta
    debug = args.debug

    student1 = dataset_contents[int(pairing[0]) + 1]
    student2 = dataset_contents[int(pairing[1]) + 1]
    if debug:
        print("Evaluating pairing #{} pairing {}".format(key, pairing))

    if student1[1] != student2[1]:
        if debug:
            print("Point 0: Student 1 and 2 not in same class")
        return 0
    else:
        diff = abs(int(student1[3]) - int(student2[3]))
        diff *= beta
        preference = 14 - (student1.index(pairing[2]) + student2.index(pairing[2]))
        preference *= alpha
        point = preference - diff
        if debug:
            print('Point {}: diff penalty {}, preference point {}'.format(point, diff, preference))
        return point



if __name__ == "__main__":
    print("Running tests:")

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_path', type=str, default='./ilct_studentdata.csv', help='path to input data csv file')
    parser.add_argument('--sol_path', type=str, default='./submissions/test_sol.csv', help= 'path to the solution csv file')
    parser.add_argument('--alpha', type=int, default='20', help='weight for preference')
    parser.add_argument('--beta', type=int, default='5', help='penalty for difference in classes')
    parser.add_argument('--lefterover_penalty', type=int, default='50', help='penalty for leaving someone alone')
    parser.add_argument('--debug', default=False, help='whether to run program in debug mode or not')
    args = parser.parse_args()

    dataset_path = args.dataset_path
    sol_path = args.sol_path
    debug = args.debug

    with open(dataset_path, "rt") as csvfile:
        dataset_contents = list(csv.reader(csvfile, delimiter = ','))
        # print(contents)

    with open(sol_path, "rt") as csvfile:
        sol_contents = list(csv.reader(csvfile, delimiter = ","))

    points = 0
    for key, pairing in enumerate(sol_contents):
        points += calculate_points_for_pair(args, dataset_contents, key, pairing)

    num_leftover_students = len(dataset_contents) - 2 * len(sol_contents) - 1
    if debug:
        print("Lonely student num: ", num_leftover_students)
    points -= num_leftover_students * args.lefterover_penalty

    print("Total point: {} \nTotal pairing: {}".format(points, len(sol_contents)))
