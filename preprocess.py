import sys
import numpy as np
from mlp import mlp
import normalize as normal
def readin(fin,fin2):

    arr = []
    study = []
    final =""
    input = open(fin, 'r')
    output = open(fin2, 'w')
 
    for lines in input:
        line = lines.split()

        arr.append(line)
    
    for i in range(len(arr)):
        curr = arr[i]
        if  "@data" in curr:
            sample = arr[i+1:]

    for i in range(len(sample)):
        cur = sample[i]
        for j in range(len(cur)):
            temp = cur[j].split(',')
            if(temp[-1] == "disease"):
                temp[-1] = 1
            else:
                temp[-1] = 0
            study.append(temp)
    for i in range(len(study)):
        cur = study[i]
        curline=""
        for j in range(len(cur)):
            s = str(cur[j])
            curline += s
            if(j!= len(cur)-1):
                curline += ","
            
        output.write(curline)
        output.write("\n")
    output.close()
 
        
    
def main():
    fin = sys.argv[1]
    fin2 = sys.argv[2]
    readin(fin, fin2)
    input2 = open(fin2, 'r')
    nparr = np.loadtxt(fin2,delimiter=',')
    study = normal.normalizer(nparr)
    target = np.zeros((np.shape(study)[0],2))
    index = np.where(study[:,14] == 0)
    target[index,0] = 1
    index = np.where(study[:,14] == 1)
    target[index,1] = 1
    study = study[:,:-1]
    order = range(np.shape(study)[0])
    np.random.shuffle(order)
    study = study[order,:]
    target = target[order,:]
    thelen = 5
    Carray = []
    Tarray=[]
    TP = 0
    FN = 0
    FP = 0
    TN = 0
    for i in range(5):
        Carray.append([])
        Tarray.append([])

    ind = 0
    for i in range(len(study)):
        if (ind <5):
            Carray[ind].append(study[i])
            Tarray[ind].append(target[i])
            ind = ind +1
        else:
            ind = 0

    Errors = []
    Cons= []
    for i in range(20):
        for j in range(5):
            Target1 = np.empty((0,2))
            Target2 = np.empty((0,2))
            x1 = np.empty((0,14))
            x2 = np.empty((0,14))
            for k in range(5):
                if (k!= j):
                    for h in range(len(Carray[k])):
                        x1 = np.vstack((x1,Carray[k][h]))
                        Target1 = np.vstack((Target1,Tarray[k][h]))
                
            x2 = np.vstack((x2,Carray[j]))
            Target2= np.vstack((Target2,Tarray[j]))
            net = mlp(x1,Target1,5,momentum = 0.1, outtype='softmax')
            Errors.append(net.earlystopping(x1,Target1,x2,Target2,0.3))
            num = net.confmat(x2,Target2)
            Cons.append(num)
            print("\n")

    print("The CONS",Cons)
    Errors = np.array(Errors)

    
    Max = np.amax(Errors)
    print("The max error:", Max)
    
    Min = np.amin(Errors)
    print("the min error:", Min)
    
    Mean = np.mean(Errors)
    print("the mean error is:", Mean)

    Std = np.std(Errors)
    print("the STD is :", Std)

    for i in range(len(Cons)): 
        for j in range(2):
            if (j == 1):
                F1 = F1 + Cons[i][j][0]
                T2 = T2 + Cons[i][j][1]
            if (j == 0):
                T1 = T1 + Cons[i][j][0]
                F2 = F2 + Cons[i][j][1]
          
    
    T1 = T1 / len(Cons)
    F2 = F2 / len(Cons)
    F1 = F1 / len(Cons)
    T2 = T2 / len(Cons)
    Accuracy = ((T1 + T2)/(T1+T2+F1+F2))
    Sensitivity = (T1/(T1+F2))
    Specificity = (T2/(T2+F1))

    print("The Accuracy", Accuracy)                
    print("The Sensitivity",Sensitivity)     
    print("The Specificity", Specificity)
        
main()
