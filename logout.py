import time
def logout(msg, type=0, printout=True):
    pf = '\033[0m'
    dtype = 'UNKNOW'
    if type==0:
        dtype = 'INFO'
    if type==1:
        pf = '\033[36m'
        dtype = 'REMIND'
    if type==2:
        pf = '\033[32m'
        dtype = 'SUCCESS'
    if type==3:
        pf = '\033[33m'
        dtype='WARN'
    if type==4:
        pf = '\033[31m'
        dtype='ERROR'
    text = "%s[%s][%s]%s\033[0m" % (pf, time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())), dtype, msg)
    if printout:
        print(text)
    return text