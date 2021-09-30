import os
import time
import sys
import datetime

t = datetime.datetime.now()
directory_name = "data"
file_name = directory_name + "/" + t.strftime("%c") + '.txt'

idle_threshold = 300

if len(sys.argv) > 1:
    try:
        idle_threshold = int(sys.argv[1])
    except ValueError:
        print('Idle threshold must be an integer.')
        exit()

idle_detected = False
idle_counted = False

total_seconds = 0
current_idle_penalty = 0
total_idle_penalty = 0

start = time.time()
total_time = 0

try:
    while True:
        os.system("clear")

        idle_milliseconds = os.popen("xprintidle").read()
        idle_seconds = int(idle_milliseconds) / 1000

        if idle_seconds >= idle_threshold:
            print("Idle detected.")
            idle_detected = True
            current_idle_penalty = idle_seconds
        elif idle_detected:
            idle_detected = False
            total_idle_penalty += current_idle_penalty
            current_idle_penalty = 0

        total_seconds = time.time() - start - total_idle_penalty - current_idle_penalty
        total_time = datetime.timedelta(seconds=total_seconds)

        print("Total time: ", total_time)

        if not idle_detected:
            print("Idle in: ", idle_threshold - idle_seconds)

        time.sleep(0.5)
except KeyboardInterrupt:
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        
    with open(file_name, 'w') as file:
        file.write(str(total_time))

        print()
        print("Total time spent: ", total_time)
        print("Time saved in: ", file_name)
