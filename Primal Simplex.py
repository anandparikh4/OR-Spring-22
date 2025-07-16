import numpy as np

# Primal Simplex Code
# Author : Anand Parikh
# Roll NO: 20CS10007

def make_tables(m,n):
    a = np.zeros((m,m+n))
    z = np.zeros((m+n))
    c = np.zeros((m+n))
    x = np.zeros((m))
    cb = np.zeros((m))
    b = []
    for i in range(m):
        b.append("S{idx}".format(idx = i+1))
    return a,z,c,x,cb,b

def user_input(a,c,z,m,n):

    # input constraints
    print("constraints")

    for i in range(m):
        for j in range(m+n):
            if j<n :
                a[i][j] = int(input())
            elif j-n==i:
                a[i][j] = 1
            else :
                a[i][j] = 0
        x[i] = int(input())

    print("objecive")
    for i in range(m+n):
        if i<n :
            c[i] = int(input())
        else :
            c[i] = 0
        z[i] = -c[i]

def is_optimal(z,m,n):
    for i in range(m+n):
        if z[i] < 0:
            return False
    return True

if __name__ == '__main__':
    n = int(input("Enter number of variables: "))
    m = int(input("Enter number of constraints: "))

    tup = make_tables(m,n)
    a = tup[0]
    z = tup[1]
    c = tup[2]
    x = tup[3]
    cb = tup[4]
    b = tup[5]
    z_opt = 0

    user_input(a,c,z,m,n)

    print(a)
    print(c)
    print(z)

    while(not is_optimal(z,m,n)):
        min_j = 0
        for i in range(m+n):
            if z[i]<z[min_j]:
                min_j=i

        if z[min_j]>=0:
            print("Not feasible!")
            break

        min_i = 0
        flag = False
        for i in range(m):
            if a[i][min_j]==0:
                continue
            elif x[i]/a[i][min_j] < 0:
                continue
            elif x[i]/a[i][min_j] < x[min_i]/a[min_i][min_j]:
                min_i = i
                print("hi")

        #if(flag == False) :
            #print("Not feasible")
            #break

        pivot = a[min_i][min_j]
        print(min_i,min_j)
        print(pivot)

        a[min_i] = a[min_i]/pivot
        x[min_i] = x[min_i]/pivot
        print(x[min_i])


        for i in range(m):
            if i==min_i:
                continue
            k = a[i][min_j]
            a[i] = a[i] - k*a[min_i]
            x[i] = x[i] - k*x[min_i]

        cb[min_i] = c[min_j]

        for j in range(m+n):
            sum=0
            for i in range(m):
                sum += cb[i]*a[i][j]
            z[j] = sum-c[j]

        z_opt = 0
        for i in range(m):
            z_opt += cb[i]*x[i]

        print("x: ")
        print(x)
        print("a : ")
        print(a)
        print("Z optimum = ")
        print(z_opt)






