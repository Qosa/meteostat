import subprocess
import sys

def soundmeter():
    tab = ''
    process = subprocess.Popen(
        ['soundmeter','--collect','--seconds=2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '' and out!='\n':
            tab=tab+out
            #sys.stdout.write(out)
            sys.stdout.flush()
    rms = tab.replace(" ","")
    return rms

#print(soundmeter())