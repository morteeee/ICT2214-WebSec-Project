import json

file = open('fingerprint.txt', 'r').read()

csvText = "id,data\n"
i = 1
for line in file.split('\n'):
    csvText += f"{i},{line}\n"
    i = i + 1

file = open('fingerprint.csv', 'w')
file.writelines(csvText)
file.close()

# file = open('v2.csv', 'r').read()
# existing = file.replace('id,data\n', '')

# new = ""

# for line in existing.split('\n'):
#     if line != "":
#         newFormatLine = '{"' + line.split(',{"')[1]
#         new += f"{newFormatLine}\n"

# file = open('fingerprint.txt', 'w')
# file.writelines(new)
# file.close()