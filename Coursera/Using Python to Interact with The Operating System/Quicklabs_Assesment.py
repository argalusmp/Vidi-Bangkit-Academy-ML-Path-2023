#!/usr/bin/env python3

import re
import operator
import csv

differentError = {}
numUser = {}

with open("syslog.log", "r") as file :
  for line in file:
    error_match = re.search(r"ERROR ([\w\s]+)", line)
    user_match = re.search(r"(INFO|ERROR)\s[\w\s\[\]#']+\(+([\w.]+)\)",line)
    if error_match:
      error = error_match.group(1)
      if error in differentError:
        differentError[error] += 1
      else:
        differentError[error] = 1
    if user_match:
      username = user_match.group(2)
      typeResult = user_match.group(1)
      if username not in numUser:
        numUser[username] = {"INFO": 0, "ERROR": 0}
      numUser[username][typeResult] += 1

sorted_errors = sorted(differentError.items(), key = operator.itemgetter(1), reverse=True)
sorted_users = sorted(numUser.items(), key = operator.itemgetter(0))

# Write error report
with open("error_message.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Error", "Count"])
    writer.writerows(sorted_errors)

# Write user statistics report
with open("user_statistics.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Username", "INFO", "ERROR"])
    for user, counts in sorted_users:
        writer.writerow([user, counts["INFO"], counts["ERROR"]])


# /var/www/html/error_message.html

# /var/www/html/user_statistics.html