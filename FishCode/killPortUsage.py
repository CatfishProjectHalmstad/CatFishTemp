import os
import subprocess
#ports to kill on cat 5001/tcp and 5002/tcp
#Ports to kill on fish 5003/tcp
result = subprocess.run(['fuser', '5003/tcp'], stdout=subprocess.PIPE)

try:
    os.system("kill -9 " + str(int(result.stdout)))
except:
    print("5003 already closed")