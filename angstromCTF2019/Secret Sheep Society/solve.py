import json
import base64


x = 'jirU9ZpEy+x0J9dOK1AOiU1rRsB+4cY9Hj8b19oQ/iYaK4zM0UdegzxK4dv7aYtv'
bs = bytearray(base64.b64decode(x))

offset = len('{"admin": ')
bs[offset] = bs[offset] ^ ord('f') ^ ord(' ')
bs[offset+1] = bs[offset+1] ^ ord('a') ^ ord('t')
bs[offset+2] = bs[offset+2] ^ ord('l') ^ ord('r')
bs[offset+3] = bs[offset+3] ^ ord('s') ^ ord('u')
# bs[offset] = bs[offset] ^ ord('e') ^ ord('e')

print(base64.b64encode(bs))
