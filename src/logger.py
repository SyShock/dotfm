import time
import datetime

def create(filename):
    global file
    file = open(filename, 'a')
    def log(string):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(string)
        string = "["+st+"] "+string+"\n"
        file.write(string)
    return log


def destroy():
    global file
    file.close()
