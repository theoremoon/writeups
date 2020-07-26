import collections

lines = open("instructions").read().strip().split("\n")
bf = ""
for line in lines:
    inst = int(line[-2:], 16)
    count = int(line[8:10], 16)

    if inst == 18: #A
        bf += "+" * count
    elif inst == 15: #B
        bf += "<" * count
    elif inst == 14: #F
        bf += ">" * count
    elif inst == 13: #Z
        bf += "[-]"
    elif inst == 12: #]
        bf += "]"
    elif inst == 11: #[
        pass
    elif inst == 10: #[
        pass
    elif inst == 9: #[
        bf += "["
    elif inst == 6: #.
        pass
    elif inst == 5: #.
        bf += "."

print(bf)
