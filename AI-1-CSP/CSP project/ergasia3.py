import csp
import csv
import time
from math import ceil


def read_subjects(csv_sbj):
    # all subjects
    subjects = []
    with open(csv_sbj, 'r', encoding="utf8") as file:
        csvreader = csv.reader(file)
        # Skip the header
        header = next(csvreader)
        for subject in csvreader:
            subjects.append(tuple(subject))
            if subject[4] == "TRUE":
                # Labs are considered as subjects
                lab = (subject[0], subject[1], subject[2], subject[3], "LAB")
                subjects.append(lab)
    return subjects


def time_slots(variable, value):
    # Eye candy prints
    sem, sbj, prof, hard, lab = variable

    if hard == "TRUE":
        hard = "Δύσκολο"
    else:
        hard = "Εύκολο"

    if value % 3 == 1:
        print("9-12:", sem, sbj, prof, hard, lab)
    if value % 3 == 2:
        print("12-3:", sem, sbj, prof, hard, lab)
    if value % 3 == 0:
        print("3-5:", sem, sbj, prof, hard, lab)


class Exams(csp.CSP):

    def __init__(self, csv_sbj):
        self.variables = []
        self.domains = dict()
        self.neighbors = dict()

        subjects = read_subjects(csv_sbj)

        # A Variable is a subject
        for subject in subjects:
            self.variables.append(subject)

        # Domains are the 63 slots
        for var in self.variables:
            self.domains[var] = [i for i in range(1, 64)]

        # Neighbors are all the remaining subjects
        for var in self.variables:
            self.neighbors[var] = []
            self.neighbors[var] = self.variables.copy()
            self.neighbors[var].remove(var)

        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.var_constraints)

    def var_constraints(self, A, a, B, b):
        # One classroom
        if a == b:
            return False

        # Labs
        if A[1] == B[1] and B[4] == "LAB":
            if (b % 21) % 3 == 2 and (a % 21) % 3 == 1 and (b - a) == 1:
                return True
            elif (b % 21) % 3 == 0 and (a % 21) % 3 == 2 and (b - a) == 1:
                return True
            return False
        if A[1] == B[1] and A[4] == "LAB":
            if (a % 21) % 3 == 2 and (b % 21) % 3 == 1 and (a - b) == 1:
                return True
            elif (a % 21) % 3 == 0 and (b % 21) % 3 == 2 and (a - b) == 1:
                return True
            return False

        # Same semester (is not lab)
        if A[0] == B[0] and A[4] != "LAB" and B[4] != "LAB":
            if abs(a - b) <= 2 and (min(a, b) % 21) % 3 == 1:
                return False
            elif abs(a - b) <= 1 and (min(a, b) % 21) % 3 == 2:
                return False

        # Hard subjects
        if A[3] == "TRUE" and B[3] == "TRUE" and A[4] != "LAB" and B[4] != "LAB":
            if abs(a - b) <= 6 and (min(a, b) % 21) % 3 == 1:
                return False
            elif abs(a - b) <= 5 and (min(a, b) % 21) % 3 == 2:
                return False
            elif abs(a - b) <= 4 and (min(a, b) % 21) % 3 == 0:
                return False

        # Same professor
        if A[2] == B[2] and A[4] != "LAB" and B[4] != "LAB":
            if abs(a - b) <= 2 and (min(a, b) % 21) % 3 == 1:
                return False
            elif abs(a - b) <= 1 and (min(a, b) % 21) % 3 == 2:
                return False

        return True

    def display(self, assignment):
        values = dict()

        for var in self.variables:
            values[var] = assignment.get(var)

        max_value = max(values.values())
        # Sort variables to ascending domain order
        sort_values = sorted(values.items(), key=lambda x: x[1], reverse=False)

        # How many weeks?
        # (max_value)-> last slot.
        # Count how many weeks (21-slots) there are
        weeks = int(max_value / 21)

        # How many days left?
        # We need to find the ceil of 3-slots(aka days)
        # within the last week
        days = ceil((max_value - weeks * 21) / 3)

        # We counted from k-1 week
        if days == 7:  # This means we reached k week -> no remaining days
            weeks += 1
            days = 0

        for i in sort_values:
            if 1 <= i[1] % 21 <= 3:
                print("Δευτέρα")
                time_slots(i[0], i[1])
            if 4 <= i[1] % 21 <= 6:
                print("Τρίτη")
                time_slots(i[0], i[1])
            if 7 <= i[1] % 21 <= 9:
                print("Τετάρτη")
                time_slots(i[0], i[1])
            if 10 <= i[1] % 21 <= 12:
                print("Πέμπτη")
                time_slots(i[0], i[1])
            if 13 <= i[1] % 21 <= 15:
                print("Παρασκευή")
                time_slots(i[0], i[1])
            if 16 <= i[1] % 21 <= 18:
                print("Σάββατο")
                time_slots(i[0], i[1])
            if 19 <= i[1] % 21 <= 20 or i[1] % 21 == 0:
                print("Κυριακή")
                time_slots(i[0], i[1])

        print("\nΔιάρκεια:", weeks, "Εβδομάδες και", days, "ημέρες")
        print("Nodes visited:", self.nassigns, "nodes")


if __name__ == '__main__':
    schedule = Exams("Στοιχεία Μαθημάτων.csv")
    alg = input("Enter Algorithm:\n Select between bt, fc, mac, minc: ")

    if alg == "bt":
        tic = time.time()
        schedule.display(csp.backtracking_search(schedule))
        toc = time.time()
        print("Time elapsed:", toc - tic)
        print("BT")
    elif alg == "fc":
        tic = time.time()
        schedule.display(csp.backtracking_search(schedule, csp.mrv, csp.lcv, csp.forward_checking))
        toc = time.time()
        print("Time elapsed:", toc - tic)
        print("FC")
    elif alg == "mac":
        tic = time.time()
        schedule.display(csp.backtracking_search(schedule, csp.mrv, csp.lcv, csp.mac))
        toc = time.time()
        print("Time elapsed:", toc - tic)
        print("MAC")
    elif alg == "minc":
        tic = time.time()
        schedule.display(csp.min_conflicts(schedule,))
        toc = time.time()
        print("Time elapsed:", toc - tic)
        print("MIN CONFLICTS")
    else:
        print("Invalid input")
