def keithshift(s, n):
    r = ""
    for c in s:
        r += chr((ord(c) - ord("A") + n) % 26 + ord("A"))

        n = (n + 1) % 26
    return r


s = "CGULKVIPFRGDOOCSJTRRVMORCQDZG"
for i in range(26):
    print(keithshift(s, i))
