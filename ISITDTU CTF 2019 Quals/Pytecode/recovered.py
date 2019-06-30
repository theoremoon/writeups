def C0rr3ct():
    print("Wow!!!")


def F41l():
    print("Bye!!")


def Ch3cking():
    flag = ""
    if ord(flag[0]) + 52 != ord(flag[-1]):
        return
    if ord(flag[-1]) - 4 != ord(flag[7]):
        return

    if flag[:7] != "ISITDTU":
        return

    if flag[9] != flag[14]:
        return

    if flag[14] != flag[19]:
        return

    if flag[19] != flag[24]:
        return

    if ord(flag[8]) != 49:
        return
    if flag[8] != flag[16]:
        return
    if flag[10:14] != "d0nT":
        return

    if int(flag[18]) + int(flag[23]) + int(flag[28]) != 9:
        return

    if flag[18] != flag[28]:
        return

    if flag[15] != "L":
        return

    if ord(flag[17]) ^ (-10) != -99:
        return

    if ord(flag[20]) + 2 != ord(flag[27]):
        return

    if ord(flag[27]) > 123:
        return

    if ord(flag[20]) < 97:
        return

    if ord(flag[27]) % 100 != 0:
        return

    if flag[25] != "C":
        return

    if ord(flag[26]) % 2 != 0:
        return

    if ord(flag[26]) % 3 != 0:
        return

    if ord(flag[26]) % 4 != 0:
        return

    if not ("0" <= flag[26] <= "9"):
        return

    if int(flag[23]) != 3:
        return

    if flag[22] != flag[13].lower():
        return

    tmp = 0
    for i in flag:
        tmp = tmp + ord(i)

    if tmp != 2441:
        return

    C0rr3ct()
