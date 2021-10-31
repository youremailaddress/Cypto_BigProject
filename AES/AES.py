from Fast_init import *
from function import *
import random,os
import base64

def T(word,j):
    Rcon = [0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,0x40000000,0x80000000,0x1b000000,0x36000000]
    word = ((word<<8)&0xffffffff)^(word>>24)
    word = (S_box[(word&0xf0000000)>>28][(word&0x0f000000)>>24]<<24)^(S_box[(word&0x00f00000)>>20][(word&0x000f0000)>>16]<<16)^(S_box[(word&0x0000f000)>>12][(word&0x00000f00)>>8]<<8)^(S_box[(word&0x000000f0)>>4][word&0x0000000f])
   
    return word^Rcon[j]

def Subword(word):
    return (S_box[(word&0xf0000000)>>28][(word&0x0f000000)>>24]<<24)^(S_box[(word&0x00f00000)>>20][(word&0x000f0000)>>16]<<16)^(S_box[(word&0x0000f000)>>12][(word&0x00000f00)>>8]<<8)^(S_box[(word&0x000000f0)>>4][word&0x0000000f])

def generate_key(strbytekey):
    '''
    input hexstr
    output dec list
    '''
    key = hexStr2byte(strbytekey)
    if keylength(strbytekey) == 16:
        key_map = [0 for i in range(44)]
        key_map[0] = int.from_bytes(key[:4],"big")
        key_map[1] = int.from_bytes(key[4:8],"big")
        key_map[2] = int.from_bytes(key[8:12],"big")
        key_map[3] = int.from_bytes(key[12:16],"big")
        for i in range(4,44):
            if i%4!=0:
                key_map[i] = key_map[i-4]^key_map[i-1]
            else:
                key_map[i] = key_map[i-4]^T(key_map[i-1],int(i/4)-1)
    elif keylength(strbytekey) == 24:
        key_map = [0 for i in range(52)]
        key_map[0] = int.from_bytes(key[:4],"big")
        key_map[1] = int.from_bytes(key[4:8],"big")
        key_map[2] = int.from_bytes(key[8:12],"big")
        key_map[3] = int.from_bytes(key[12:16],"big")
        key_map[4] = int.from_bytes(key[16:20],"big")
        key_map[5] = int.from_bytes(key[20:24],"big")
        for i in range(6,52):
            if i%6!=0:
                key_map[i] = key_map[i-6]^key_map[i-1]
            else:
                key_map[i] = key_map[i-6]^T(key_map[i-1],int(i/6)-1)
    elif keylength(strbytekey) == 32:
        key_map = [0 for i in range(60)]
        key_map[0] = int.from_bytes(key[:4],"big")
        key_map[1] = int.from_bytes(key[4:8],"big")
        key_map[2] = int.from_bytes(key[8:12],"big")
        key_map[3] = int.from_bytes(key[12:16],"big")
        key_map[4] = int.from_bytes(key[16:20],"big")
        key_map[5] = int.from_bytes(key[20:24],"big")
        key_map[6] = int.from_bytes(key[24:28],"big")
        key_map[7] = int.from_bytes(key[28:32],"big")
        for i in range(8,60):
            if i%8 == 4:
                key_map[i] = key_map[i-8]^Subword(key_map[i-1])
            elif i%8 == 0:
                key_map[i] = key_map[i-8]^T(key_map[i-1],int(i/8)-1)
            else:
                key_map[i] = key_map[i-8]^key_map[i-1]
    else:
        errorlog(3,"Unsupported Key length:%d bytes.16,24,32 bytes are expected." % keylength(strbytekey))
    return key_map

def split_by_bytes(address,methods,need,fromfile):
    '''
    address:input bytes/address
    methods:padding methods
    need/fromfile: bool
    output:bytes list
    '''
    splitresult = []
    if fromfile:
        with open(address,"rb",encoding="utf-8") as f:
            c = f.read(16)
            while len(c) == 16:
                splitresult.append(c)
                c = f.read(16)
            if not need:
                splitresult.append(c)
            elif methods == "NoPadding":
                if len(c) != 0:
                    errorlog(3,"PaddingError:NoPadding method can't encrypt this input")
            elif methods == "ZerosPadding":
                c = dec2byte(byte2dec(c)<<(128-8*len(c)))
                splitresult.append(c)
            elif methods == "PKCSPadding":
                num = byte2dec(c)
                for j in range(0,16-len(c)):
                    num = (num<<(8)) + (16-len(c))
                splitresult.append(dec2byte(num))
            elif methods == "ISOPadding":
                num = byte2dec(c)
                for j in range(0,15-len(c)):
                    num = (num<<(8)) + random.randint(0,255)
                num = (num<<(8)) + (16-len(c))
                splitresult.append(dec2byte(num))
            else:
                errorlog(3,"Unsupported Padding method %s" % methods)
        return splitresult
    else:
        splitresult = [address[i:i + 16] for i in range(len(address)) if i % 16 == 0]
        if not need:
            return splitresult
        elif methods == "NoPadding":
            if len(splitresult[-1])!=16:
                errorlog(3,"PaddingError:NoPadding method can't encrypt this input")
        elif methods == "ZerosPadding":
            if len(splitresult) == 0 or len(splitresult[-1])==16:
                splitresult.append(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
                return splitresult
            else:
                lastblock = splitresult.pop()
            splitresult.append(dec2byte(byte2dec(lastblock)<<128-8*len(lastblock)))
        elif methods == "PKCSPadding":
            if len(splitresult) == 0 or len(splitresult[-1])==16:
                splitresult.append(b'\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10')
                return splitresult
            else:
                lastblock = splitresult.pop()
            num = byte2dec(lastblock)
            for j in range(0,16-len(lastblock)):
                num = (num<<(8)) + (16-len(lastblock))
            splitresult.append(dec2byte(num))
        elif methods == "ISOPadding":
            if len(splitresult) == 0 or len(splitresult[-1])==16:
                tem =os.urandom(15)+b'\x10'
                splitresult.append(tem)
                return splitresult
            else:
                lastblock = splitresult.pop()
            num = byte2dec(lastblock)
            for j in range(0,15-len(lastblock)):
                num = (num<<(8)) + random.randint(0,255)
            num = (num<<(8)) + (16-len(lastblock))
            splitresult.append(dec2byte(num))
        else:
            errorlog(3,"Unsupported Padding method %s" % methods)
        return splitresult

def convert(i):
    i = i % 4294967296
    n4 = i % 256
    i = int(i / 256)
    n3 = i % 256
    i = int(i / 256)
    n2 = i % 256
    n1 = int(i / 256)
    return [n1,n2,n3,n4]

def Around(key,input):
    temp = [0 for i in range(4)]
    neww = []
    temp[0] = (T_0[(input[0]>>4)][(input[0]&0x0f)])^(T_1[(input[5]>>4)][(input[5]&0x0f)])^(T_2[(input[10]>>4)][(input[10]&0x0f)])^(T_3[(input[15]>>4)][(input[15]&0x0f)])^key[0]
    temp[1] = (T_0[(input[4]>>4)][(input[4]&0x0f)])^(T_1[(input[9]>>4)][(input[9]&0x0f)])^(T_2[(input[14]>>4)][(input[14]&0x0f)])^(T_3[(input[3]>>4)][(input[3]&0x0f)])^key[1]
    temp[2] = (T_0[(input[8]>>4)][(input[8]&0x0f)])^(T_1[(input[13]>>4)][(input[13]&0x0f)])^(T_2[(input[2]>>4)][(input[2]&0x0f)])^(T_3[(input[7]>>4)][(input[7]&0x0f)])^key[2]
    temp[3] = (T_0[(input[12]>>4)][(input[12]&0x0f)])^(T_1[(input[1]>>4)][(input[1]&0x0f)])^(T_2[(input[6]>>4)][(input[6]&0x0f)])^(T_3[(input[11]>>4)][(input[11]&0x0f)])^key[3]
    for i in range(4):
        neww.extend(convert(temp[i]))
    return neww

def AESStantardForBlock(input,key):
    '''
    input type:128 bits bytes
    key type:key_array
    output type:128 bits hexstr
    '''
    input_list = [input[i]^convert(key[int(i/4)])[i%4] for i in range(len(input))]
    for i in range(4,len(key)-4,4):
        use_key = [key[i] for i in range(i,i+4)]
        '''
        现在key是[int32,int32,int32,int32]
        input_list是[char(8),char,...char]
        '''
        input_list = Around(use_key,input_list)
    use_key = [convert(key[len(key)-4]),convert(key[len(key)-3]),convert(key[len(key)-2]),convert(key[len(key)-1])]
    output = []
    for i in range(16):
        output.append((S_box[(input_list[(5*i)%16]>>4)][(input_list[(5*i)%16]&0x0f)])^use_key[int(i/4)][i%4])
    return "".join([byte2hexStr(dec2byte(i)) if i!=0 else "00" for i in output])

def NeedPadding(mode):
    if mode.strip().lower() in ['ecb','cbc']:
        return True
    if mode.strip().lower() in ['ofb','cfb','ctr']:
        return False
    errorlog(3,"Unsupported mode:%s" % mode)

def AES(key,keytype,iv,ivtype,mode,input,intype,methods):
    if keytype.strip().lower() == "base64":
        key = base64.b64decode(key)
        key = byte2hexStr(key)
    elif keytype.strip().lower() == "hex":
        pass
    else:
        try:
            key = key.encode(keytype)
            key = byte2hexStr(key)
        except LookupError as e:
            errorlog(3,str(e))

    if mode.strip().lower() != "ecb":
        if ivtype.strip().lower() == "base64":
            iv = base64.b64decode(iv)
            iv = byte2hexStr(iv)
        elif ivtype.strip().lower() == "hex":
            pass
        else:
            try:
                iv = iv.encode(ivtype)
                iv = byte2hexStr(iv)
            except LookupError as e:
                errorlog(3,str(e))
        if keylength(iv) != 16:
            errorlog(3,"Unsupported IV length:%d bytes.16 bytes are expected." % keylength(iv))

    if intype.strip().lower() == "base64":
        input = base64.b64decode(input)
        message_array = split_by_bytes(input,methods,NeedPadding(mode),False)
    elif intype.strip().lower() == "hex":
        message_array = split_by_bytes(hexStr2byte(input),methods,NeedPadding(mode),False)
    elif intype.strip().lower() == "file":
        message_array = split_by_bytes(input,methods,NeedPadding(mode),True)
    else:
        try:
            input = input.encode(intype)
        except LookupError as e:
            errorlog(3,str(e))
        message_array = split_by_bytes(input,methods,NeedPadding(mode),False)
    key_array = generate_key(key)

    if mode.strip().lower() == "ecb":
        cipherarray = [AESStantardForBlock(i,key_array) for i in message_array]
        return "".join(cipherarray)
    elif mode.strip().lower() == "ctr":
        iv_array = []
        iv = hexStr2byte(iv)
        for i in range(len(message_array)):
            iv_array.append(AESStantardForBlock(iv,key_array))
            iv = dec2byte(byte2dec(iv)+1)
        iv_array[-1] = iv_array[-1][:2*len(message_array[-1])]
        for i in range(len(iv_array)):
            iv_array[i] = byte2hexStr(dec2byte(byte2dec(hexStr2byte(iv_array[i]))^byte2dec(message_array[i])))
        return "".join(iv_array)
    elif mode.strip().lower() == "cbc":
        beforeinput = byte2dec(message_array[0])^byte2dec(hexStr2byte(iv))
        out = []
        for i in range(1,len(message_array)+1):
            m = AESStantardForBlock(dec2byte(beforeinput).zfill(16),key_array)
            out.append(m)
            if i == len(message_array) or len(message_array) == 1:
                break
            beforeinput = byte2dec(hexStr2byte(m))^byte2dec(message_array[i])
        return "".join(out)
    elif mode.strip().lower() == "cfb":
        beforeinput = byte2dec(hexStr2byte(AESStantardForBlock(hexStr2byte(iv),key_array)))
        out = []
        for i in range(len(message_array)):
            if i == len(message_array) -1:
                m = byte2dec(hexStr2byte(byte2hexStr(dec2byte(beforeinput))[:2*len(message_array[-1])]))^byte2dec(message_array[i])
            else:
                m = beforeinput^byte2dec(message_array[i])
            out.append(byte2hexStr(dec2byte(m)))
            if i!= len(message_array)-1:
                beforeinput = byte2dec(hexStr2byte(AESStantardForBlock(dec2byte(m),key_array)))
        return "".join(out)
    elif mode.strip().lower() == "ofb":
        out = []
        iv = hexStr2byte(iv)
        for i in range(len(message_array)):
            iv = AESStantardForBlock(iv,key_array)
            if i == len(message_array)-1:
                iv = iv[:2*len(message_array[-1])]
            out.append(byte2hexStr(dec2byte(byte2dec(message_array[i])^byte2dec(hexStr2byte(iv)))))
            iv = hexStr2byte(iv)
        return "".join(out)
    else:
        errorlog(3,"Unsupported encrypt mode")

def dAround(key,input):
    temp = [0 for i in range(4)]
    neww = []
    temp[0] = (T_0_re[(input[0]>>4)][(input[0]&0x0f)])^(T_1_re[(input[13]>>4)][(input[13]&0x0f)])^(T_2_re[(input[10]>>4)][(input[10]&0x0f)])^(T_3_re[(input[7]>>4)][(input[7]&0x0f)])^key[0]
    temp[1] = (T_0_re[(input[4]>>4)][(input[4]&0x0f)])^(T_1_re[(input[1]>>4)][(input[1]&0x0f)])^(T_2_re[(input[14]>>4)][(input[14]&0x0f)])^(T_3_re[(input[11]>>4)][(input[11]&0x0f)])^key[1]
    temp[2] = (T_0_re[(input[8]>>4)][(input[8]&0x0f)])^(T_1_re[(input[5]>>4)][(input[5]&0x0f)])^(T_2_re[(input[2]>>4)][(input[2]&0x0f)])^(T_3_re[(input[15]>>4)][(input[15]&0x0f)])^key[2]
    temp[3] = (T_0_re[(input[12]>>4)][(input[12]&0x0f)])^(T_1_re[(input[9]>>4)][(input[9]&0x0f)])^(T_2_re[(input[6]>>4)][(input[6]&0x0f)])^(T_3_re[(input[3]>>4)][(input[3]&0x0f)])^key[3]
    # print(hex(T_0_re[(input[0]>>4)][(input[0]&0x0f)]),hex(T_1_re[(input[13]>>4)][(input[13]&0x0f)]),hex(T_2_re[(input[10]>>4)][(input[10]&0x0f)]),hex(T_3_re[(input[7]>>4)][(input[7]&0x0f)]),hex(key[0]))
    for i in range(4):
        neww.extend(convert(temp[i]))
    return neww

def dkey(key):
    l = len(key)
    rkey = [0 for i in range(l)]
    for i in range(0,l,4):
        rkey[i] = key[l-i-4]
        rkey[i+1] = key[l-i-3]
        rkey[i+2] = key[l-i-2]
        rkey[i+3] = key[l-i-1]
    for i in range(4,l-4):
        tmp = [0 for i in range(4)]
        tmp2 = [0]*4
        tmp[0] = rkey[i] >> 24
        tmp[1] = (rkey[i] >> 16) & 0xff
        tmp[2] = (rkey[i] >> 8) & 0xff
        tmp[3] = rkey[i] & 0xff
        tmp2[0] = Mule(tmp[0]) ^ Mulb(tmp[1]) ^ Muld(tmp[2]) ^ Mul9(tmp[3])
        tmp2[1] = Mul9(tmp[0]) ^ Mule(tmp[1]) ^ Mulb(tmp[2]) ^ Muld(tmp[3])
        tmp2[2] = Muld(tmp[0]) ^ Mul9(tmp[1]) ^ Mule(tmp[2]) ^ Mulb(tmp[3])
        tmp2[3] = Mulb(tmp[0]) ^ Muld(tmp[1]) ^ Mul9(tmp[2]) ^ Mule(tmp[3])
        rkey[i] = tmp2[0] << 24 | tmp2[1] << 16 | tmp2[2] << 8 | tmp2[3]
    # print([hex(i) for i in rkey])
    return rkey

def dAESStantardForBlock(input,key):
    '''
    input:bytes,generated_key_array
    '''
    key = dkey(key)
    input_list = [input[i]^convert(key[int(i/4)])[i%4] for i in range(len(input))]
    for i in range(4,len(key)-4,4):
        use_key = [key[i] for i in range(i,i+4)]
        input_list = dAround(use_key,input_list)
    use_key = [convert(key[len(key)-4]),convert(key[len(key)-3]),convert(key[len(key)-2]),convert(key[len(key)-1])]
    ####
    output = []
    for i in range(16):
        output.append((S_box_re[(input_list[(13*i)%16]>>4)][(input_list[(13*i)%16]&0x0f)])^use_key[int(i/4)][i%4])
    return "".join([byte2hexStr(dec2byte(i)) if i!=0 else "00" for i in output])

def dsplit_by_bytes(mode,input,key,iv,padding):
    '''
    input:bytes
    mode:mode
    key:generated key
    iv:hexstr
    '''
    splitresult = [input[i:i + 16] for i in range(len(input)) if i % 16 == 0]
    out = []
    if mode.strip().lower() == "ecb":
        if input == b"" or len(splitresult[-1])%16!=0:
            errorlog(3,"can't decrypt this")
        out.extend([dAESStantardForBlock(splitresult[i],key) for i in range(len(splitresult)-1)])
        if padding.strip() == "NoPadding":
            out.append(dAESStantardForBlock(splitresult[len(splitresult)-1],key))
        elif padding.strip() == "ZerosPadding":
            out.append(dAESStantardForBlock(splitresult[len(splitresult)-1],key).rsplit("00")[0])
        elif padding.strip() == "PKCSPadding" or "ISOPadding":
            t = dAESStantardForBlock(splitresult[len(splitresult)-1],key)
            index = byte2dec(hexStr2byte(t[-2:]))
            t = t[:32-2*index]
            out.append(t)
        else:
            errorlog(3,"Unsupported Padding method %s" % padding)
  
    elif mode.strip().lower() == "cbc":
        if input == b"" or len(splitresult[-1])%16!=0:
            errorlog(3,"can't decrypt this")
        out.append(byte2hexStr(dec2byte(byte2dec(hexStr2byte(dAESStantardForBlock(splitresult[0],key)))^byte2dec(hexStr2byte(iv)))))
        if len(splitresult) != 1:
            out.extend([byte2hexStr(dec2byte(byte2dec(hexStr2byte(dAESStantardForBlock(splitresult[i],key)))^byte2dec(splitresult[i-1]))) for i in range(1,len(splitresult)-1)])
            tempp = byte2hexStr(dec2byte(byte2dec(hexStr2byte(dAESStantardForBlock(splitresult[len(splitresult)-1],key)))^byte2dec(splitresult[len(splitresult)-2])))
        else:
            tempp = out.pop()
        if padding.strip() == "NoPadding":
            out.append(tempp)
        elif padding.strip() == "ZerosPadding":
            out.append(tempp.rsplit("00")[0])
        elif padding.strip() == "PKCSPadding" or "ISOPadding":
            index = byte2dec(hexStr2byte(tempp[-2:]))
            tempp = tempp[:32-2*index]
            out.append(tempp)
        else:
            errorlog(3,"Unsupported Padding method %s" % padding)

    
    elif mode.strip().lower() == "cfb":
        if input == b'':
            errorlog(3,"can't decrypt this")
        beforeinput = byte2dec(hexStr2byte(AESStantardForBlock(hexStr2byte(iv),key)))
        for i in range(len(splitresult)):
            if i == len(splitresult) -1:
                m = byte2dec(hexStr2byte(byte2hexStr(dec2byte(beforeinput))[:2*len(splitresult[-1])]))^byte2dec(splitresult[i])
            else:
                m = beforeinput^byte2dec(splitresult[i])
            out.append(byte2hexStr(dec2byte(m)))
            if i!= len(splitresult)-1:
                beforeinput = byte2dec(hexStr2byte(AESStantardForBlock(dec2byte(m),key)))
    
    elif mode.strip().lower() == "ofb":
        iv = hexStr2byte(iv)
        for i in range(len(splitresult)):
            iv = AESStantardForBlock(iv,key)
            if i == len(splitresult)-1:
                iv = iv[:2*len(splitresult[-1])]
            out.append(byte2hexStr(dec2byte(byte2dec(splitresult[i])^byte2dec(hexStr2byte(iv)))))
            iv = hexStr2byte(iv)

    elif mode.strip().lower() == "ctr":
        iv = hexStr2byte(iv)
        for i in range(len(splitresult)):
            out.append(AESStantardForBlock(iv,key))
            iv = dec2byte(byte2dec(iv)+1)
        out[-1] = out[-1][:2*len(splitresult[-1])]
        for i in range(len(out)):
            out[i] = byte2hexStr(dec2byte(byte2dec(hexStr2byte(out[i]))^byte2dec(splitresult[i])))

    else:
        errorlog(3,"Unsupported decrypt mode")

    return "".join(out)  

def dAES(key,keytype,iv,ivtype,mode,input,intype,methods):
    if keytype.strip().lower() == "base64":
        key = base64.b64decode(key)
        key = byte2hexStr(key)
    elif keytype.strip().lower() == "hex":
        pass
    else:
        try:
            key = key.encode(keytype)
            key = byte2hexStr(key)
        except LookupError as e:
            errorlog(3,str(e))
    
    if mode.strip().lower() != "ecb":
        if ivtype.strip().lower() == "base64":
            iv = base64.b64decode(iv)
            iv = byte2hexStr(iv)
        elif ivtype.strip().lower() == "hex":
            pass
        else:
            try:
                iv = iv.encode(ivtype)
                iv = byte2hexStr(iv)
            except LookupError as e:
                errorlog(3,str(e))
        if keylength(iv) != 16:
            errorlog(3,"Unsupported IV length:%d bytes.16 bytes are expected." % keylength(iv))
    
    key_array = generate_key(key)
    if intype.strip().lower() == "base64":
        input = base64.b64decode(input)
        return dsplit_by_bytes(mode,input,key_array,iv,methods)
    elif intype.strip().lower() == "hex":
        return dsplit_by_bytes(mode,hexStr2byte(input),key_array,iv,methods)
    else:
        try:
            input = input.encode(intype)
        except LookupError as e:
            errorlog(3,str(e))
        return dsplit_by_bytes(mode,input,key_array,iv,methods)

# print(AES("00112233445566778899aabbccddeeff","hex","57674365767ff678ac88cb9ccde56990","hex","cbc","1122336666666666666666666666666666","hex","PKCSPadding"))
# print(dAES("00112233445566778899aabbccddeeff","hex","57674365767ff678ac88cb9ccde56990","hex","cbc","55e10f29d7014b335481f264d4a66bb017563535c5db12b20b3323bbd226b699","hex","PKCSPadding"))