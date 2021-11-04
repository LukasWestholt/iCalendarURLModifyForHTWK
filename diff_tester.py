file1 = "HTWK2iCal.ics"
file2 = "ModifiedHTWK2iCal.ics"


def b(a):
    return a.strip().replace(r",", r"\,").replace(r"\\,", r"\,")


for x, y in [(file1, file2), (file2, file1)]:
    x = open(x).readlines()
    y = open(y).readlines()
    line_num = 0
    for line in x:
        line_num += 1
        line = b(line)
        if not line or line == "" or line.startswith("DTSTAMP"):
            continue

        if line not in [b(i) for i in y] \
                and line not in [(b(y[i]) + b(y[i+1]) if i+1 != len(y) else "") for i in range(len(y))] \
                and line not in [(b(y[i]) + " " + b(y[i+1]) if i+1 != len(y) else "") for i in range(len(y))] \
                and line + b(x[line_num]) not in [b(i) for i in y] \
                and line + b(x[line_num]) not in [(b(y[i]) + b(y[i+1]) if i+1 != len(y) else "") for i in range(len(y))] \
                and line + b(x[line_num]) not in [(b(y[i]) + " " + b(y[i+1]) if i+1 != len(y) else "") for i in range(len(y))] \
                and line + " " + b(x[line_num]) not in [(b(y[i]) + b(y[i+1]) if i+1 != len(y) else "") for i in range(len(y))]:
            print("[" + str(line_num) + "] " + line)
