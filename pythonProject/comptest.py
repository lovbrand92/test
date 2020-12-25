import time

start = time.time()

a = 0

for i in range(100000000):
    a= a+1
    if a%1000000==0:
        print(a)
print("time :", time.time()-start)