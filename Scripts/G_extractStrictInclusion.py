def loadTests():
    data = {}
    with open('partial_R4.txt') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip().split(":")
            test_suite = line[0]
            tests = set(line[1].split(','))  # Convert to set
            data[test_suite] = tests
    return data

tests = loadTests()

inclusions = []
for t1 in tests:
    for t2 in tests:
        if t1 != t2 and tests[t2] < tests[t1]:  # Strict inclusion check
            inclusions.append(f'"{t1}" -> "{t2}"')

with open("gpartial_R4.txt", 'w') as writer:
    writer.write("\n".join(inclusions))
