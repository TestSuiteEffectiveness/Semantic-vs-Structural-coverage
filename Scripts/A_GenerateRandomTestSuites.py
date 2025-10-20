import random
threshold = 0.3
for i in range(1,21):
   #generate ti
    print("------------------------------------")
    threshold = threshold + 0.02
    tests_in_ti = []
    for j in range(1,133): # random from 1-132
        if random.random()<=threshold:
            tests_in_ti.append(str(j))
    print(f"test suite T{i} ({len(tests_in_ti)}):");
    print(",".join(tests_in_ti))
