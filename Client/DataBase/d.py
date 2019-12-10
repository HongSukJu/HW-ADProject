import pickle

with open("userInfo.dat","wb") as f:
    pickle.dump({
        'name' : '홍석주',
        'id' : '0000',
        'password':'0000',
        'friend':["테스트1", "테스트2"]
        }, f)