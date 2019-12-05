import pickle

with open("userInfo.dat","wb") as f:
    pickle.dump({
        'name' : '',
        'id' : '',
        'password':'',
        'friend':["홍석주"]
        }, f)