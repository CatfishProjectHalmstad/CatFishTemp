import os
import subprocess
#ports to kill on cat 5001/tcp and 5002/tcp
#Ports to kill on fish 5003/tcp
result = subprocess.run(['fuser', '5001/tcp'], stdout=subprocess.PIPE)
result2 = subprocess.run(['fuser', '5002/tcp'], stdout=subprocess.PIPE)


try:
    os.system("kill -9 " + str(int(result2.stdout)))
except:
    print("5002 already gone")

try:
    os.system("kill -9 " + str(int(result.stdout)))
except:
    print("5001 already closed")