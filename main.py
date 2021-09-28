import os
import time
import sys
from datetime import datetime

t = datetime.now()
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

        print("Total seconds: ", total_seconds)
        print("Idle seconds: ", idle_seconds)

        time.sleep(0.5)
except KeyboardInterrupt:
    with open(file_name, 'w') as file:
        file.write(str(total_seconds))
        print()
        print("Total time spend: ", total_seconds)
        print("Time saved in: ", file_name)
