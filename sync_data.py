import pickle

names_file = 'data/names.pkl'
departments_file = 'data/departments.pkl'

with open(names_file, 'rb') as f:
    names = pickle.load(f)

with open(departments_file, 'rb') as f:
    departments = pickle.load(f)

# Ensure both lists have the same length
if len(names) != len(departments):
    # Example logic to fix the length mismatch:
    # Extend the shorter list with a default value
    if len(names) < len(departments):
        names.extend(['Unknown'] * (len(departments) - len(names)))
    else:
        departments.extend(['Unknown'] * (len(names) - len(departments)))

with open(names_file, 'wb') as f:
    pickle.dump(names, f)

with open(departments_file, 'wb') as f:
    pickle.dump(departments, f)

print("Names and departments lists have been synchronized.")
