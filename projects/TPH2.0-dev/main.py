from Tool import test
from datetime import datetime
import scipy

start = datetime.now()
loop = 100
for i in range(loop):
    print(test(i))
    
end = datetime.now()

print(end- start)