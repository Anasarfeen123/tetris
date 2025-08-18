n = 10  
for i in range(1,n+1):
    print(' '*((n+1-i)//2), end ="")
    for j in range(i):
        print(f"{i}")
