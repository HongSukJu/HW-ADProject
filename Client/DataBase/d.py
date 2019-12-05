import pickle

f = open("userInfo.dat","wb")
pickle.dump({'name':'채원찬','password':'000','friend':['홍석주','장석희','김지명','강현민']},f)
f.close()