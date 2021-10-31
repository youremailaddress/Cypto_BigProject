def errorlog(errorcode,errormsg):
    if errorcode == 1:
        print("[Info]"+errormsg)
    if errorcode == 2:
        print("[Warning]"+errormsg)
    if errorcode == 3:
        print("[Fatal]"+errormsg)
        exit(1)

def byte2dec(byte):
    '''
    input b'jU'
    output 27221
    '''
    return int.from_bytes(byte,byteorder='big')

def dec2byte(dec):
    i = 0
    if dec == 0:
        return b''
    while dec>>i != 1:
        i += 1
    if i%8 == 7:
        length = int((i+1)/8)
    else:
        length = int(i/8) + 1
    return (dec).to_bytes(length,"big")

def byte2hexStr(byte):
    '''
    input b'jU'
    output '6a55'
    
    '''
    hexStr = byte.hex()
    return hexStr

def hexStr2byte(hexStr):
    '''
    input '6a55'
    output b'jU'
    '''
    if len(hexStr)%2 == 1:
        hexStr = hexStr[:-1]+"0"+hexStr[-1]
        errorlog(2,"odd hex code found,changed to normal code.")
    try:
        byte = bytes.fromhex(hexStr)
    except ValueError:
        errorlog(3,"Invalid hex code "+hexStr)
    return byte

def hexStr2binStr(hexStr):
    '''
    input '6a55'
    output '0110101001010101'
    '''
    dec = int(hexStr, 16)
    bl = len(hexStr) * 4
    binStr = "{:0{}b}".format(dec, bl)
    return binStr

def binStr2hexStr(binStr):
    '''
    input '0110101001010101'
    output '6a55'
    '''
    dec_value = int(binStr, 2)
    hexStr = hex(dec_value)[2:]
    return hexStr

def keylength(hexstr):
    if len(hexStr2binStr(hexstr))%8 != 0:
        return int(len(hexStr2binStr(hexstr))/8)+1
    else:
        return int(len(hexStr2binStr(hexstr))/8)

def Mul2(i):
    if (i & 0x80) != 0:
        return 0x1b^((i << 1) & 0xFF)
    else:
        return 0^((i << 1) & 0xFF)

def Mul3(i):
    return (Mul2(i) ^ i)

def Mul4(i):
    return (Mul2(Mul2(i)))

def Mul8(i):
    return (Mul4(Mul2(i)))

def Mul9(i):
    return (Mul8(i) ^ i)

def Mulb(i):
    return (Mul8(i) ^ Mul2(i) ^ i)

def Muld(i):
    return (Mul8(i) ^ Mul4(i) ^ i)

def Mule(i):
    return (Mul8(i) ^ Mul4(i) ^ Mul2(i))

if __name__=='__main__':
    input = b"192371812190238iqwushajkajxnkja\x00sx"
    splitresult = [input[i:i + 16] for i in range(len(input)) if i % 16 == 0]
    print(splitresult)