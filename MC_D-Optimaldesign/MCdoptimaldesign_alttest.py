import pyDOE2 as doe
import numpy as np

def doptimal(df,size,N):
    full=doe.ff2n(df)
    X=np.array([full[0]])
    for i in np.arange(1,size):
        random=np.random.randint(len(full))
        X=np.append(X,[full[random]],axis=0)
    X=np.c_[  np.ones(size),X ]
    Xnew=X.copy()
    H=np.dot(X.transpose(),X)
    Hnew=np.dot(Xnew.transpose(),Xnew)
    H_det=np.linalg.det(H)
    Hnew_det=np.linalg.det(Hnew)
    for i in np.arange(0,N):
        random=np.random.randint(df)
        random2=np.random.randint(size)
        Xnew[random2,random+1]=-1*X[random2,random+1]
        Hnew=np.dot(Xnew.transpose(),Xnew)
        Hnew_det=np.linalg.det(Hnew)
        if Hnew_det>H_det:
            X=Xnew.copy()
            H_det=Hnew_det.copy()
            print(i,H_det)
    return np.delete(X,0,1)

if __name__=='__main__':
    A=doptimal(15,16,1.e8)

