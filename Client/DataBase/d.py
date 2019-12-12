import pickle

with open("userInfo.dat","wb") as f:
    pickle.dump({
        'name' : '홍석주',
        'id' : '0000',
        'password' : '0000',
        'friend' : {}
        }, f)