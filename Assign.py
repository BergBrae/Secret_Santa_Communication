import pandas as pd
import numpy as np
import pickle
import random

# Load names and numbers from from namesandnumbers.xlsx
data = np.array(pd.read_excel('namesandnumbers.xlsx'))
name_phone = {}  # Name -> phone
for i in range(len(data)):
    row = data[i]
    name_phone[row[0]] = str(row[1])

tot_people = len(name_phone)

# Add country code
for key, value in name_phone.items():
    name_phone[key] = '+1' + value
phone_name = {phone: name for name, phone in name_phone.items()}  # Phone -> name


def bad_assignment(ar1, ar2):
    """
    Checks if anyone are assigned to themselves.
    :param ar1: A list of names
    :param ar2: A shuffled ar1
    :return: True if anyone is assigned to themselves
    """
    for idx in range(len(ar1)):
        if ar1[idx] == ar2[idx]:
            return True
    return False


# Stacks for assigning
santa_stack = list(name_phone.keys())
child_stack = santa_stack.copy()

santa_child = {}  # Santa -> child assignment

while bad_assignment(santa_stack, child_stack):
    random.shuffle(child_stack)

santa_child = {s: c for s, c in zip(santa_stack, child_stack)}
child_santa = {c: s for s, c in santa_child.items()}

assert tot_people == len(santa_child), 'Number of assignments is not equal to the number of people'

pickle.dump([name_phone, phone_name, santa_child, child_santa], open('assignments', 'wb'))
