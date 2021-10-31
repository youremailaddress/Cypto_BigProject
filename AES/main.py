from AES import *
import os.path

dir_path = os.path.dirname(os.path.abspath(__file__))+'\\'

with open(dir_path+"1.txt","r") as f:
    a = f.read()

b = AES("00112233445566778899aabbccddeeff","hex","57674365767ff678ac88cb9ccde56990","hex","cbc",a,"utf-8","PKCSPadding")
with open(dir_path+"4.txt","w") as g:
    g.write(b)