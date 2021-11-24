from flask import Flask, render_template
from flask import request
from skimage.feature import greycomatrix
import numpy as np
application = Flask(__name__)

angle_list = [0, 3*np.pi/4, np.pi/2, np.pi/4]
# rm = np.random.randint(9, size=(4,5))
# d=1
# a=0
# result = greycomatrix(rm, [d], [angle_list[a]], levels=9)
def store_d(val):
    with open('d.txt','w') as file:
        file.write(val)

def store_a(val):
    with open('a.txt','w') as file:
        file.write(val)

def generate_random_matrix():
    ran_mat = np.random.randint(9,size=(4,5))
    return ran_mat

def read_file(name):
    with open(name) as file:
        content = file.readlines()
    return content[0]

def generate_result_matrix(rm,d,a):
    angle_list = [0, 3*np.pi/4, np.pi/2, np.pi/4]
    result = greycomatrix(rm, [d], [angle_list[a]],levels=9)
    return result[:,:,0,0]


def search(rm,ind,val,dis,ang):
    indicies = []
    for v in range(0,val):
        if ang == 0:
            indicies.append(angle_0(rm,ind,dis))
        elif ang == 1:
            indicies.append(angle_1(rm,ind,dis))
        elif ang == 2:
            indicies.append(angle_2(rm,ind,dis))
        else:
            indicies.append(angle_3(rm,ind,dis))
    return indicies

def angle_0(rm,ind,dis):
    temp  = []
    for i in range(0,4):
        for j in range(0,5-dis):
            tup_1 = (rm[i][j],rm[i][j+dis])
            tup_2 = (rm[i][j+dis],rm[i][j])
            if tup_1 == ind:
                temp.append([(i,j),(i,j+dis)])
            elif tup_2 == ind:
                temp.append([(i,j+dis),(i,j)])
            else:
                pass
    return temp

def angle_1(rm,ind,dis):
    temp = []
    for i in range(0,4-dis):
        for j in range(0,5-dis):
            tup_1 = (rm[i][j+dis],rm[i+dis][j])
            tup_2 = (rm[i+dis][j]),(rm[i][j+dis])
            if tup_1 == ind:
                temp.append([(i,j+dis),(i+dis,j)])
            elif tup_2 == ind:
                temp.append([(i+dis,j),(i,j+dis)])
            else:
                pass
            
    return temp


def angle_2(rm,ind,dis):
    temp = []
    for i in range(0,4-dis):
        for j in range(0,5):
            tup_1 = (rm[i][j]),(rm[i+dis][j])
            tup_2 = (rm[i+dis][j]),(rm[i][j])
            if tup_1 == ind:
                temp.append([(i,j),(i+dis,j)])
            elif tup_2 == ind:
                temp.append([(i+dis,j),(i,j)])
    return temp


def angle_3(rm,ind,dis):
    temp = []
    for i in range(0,4-dis):
        for j in range(0,5-dis):
            tup_1 = (rm[i][j],rm[i+dis][j+dis])
            tup_2 = (rm[i+dis][j+dis],rm[i][j])
            print("ind :",ind)
            print("tup_1 :",tup_1)
            print("tup_2 :",tup_2)
            if tup_1 == ind:
                temp.append([(i,j),(i+dis,j+dis)])
            elif tup_2 == ind:
                temp.append([(i+dis,j+dis),(i,j)])
            else:
                pass
    return temp

def all_tuples(ind):
    temp_list = []
    for x in ind:
        for y in x:
            for z in y:
                temp_list.append(z)
    return temp_list




rm = generate_random_matrix()

store_a('0')
store_d('1')


@application.route('/', methods=['GET','POST'])
def home(index_val = (0,0)):
    temp = []
    if request.method == 'POST':
        for i in request.form:
            temp.append(i)
        temp_var = temp[0].split()
        if temp_var[0] == 'd':
            store_d(temp_var[1])
        elif temp_var[0] == 'a':
            store_a(temp_var[1])
        else:
            index_val = (int(temp_var[1]),int(temp_var[0]))

    

    d = int(read_file('d.txt'))
    a = int(read_file('a.txt'))

    result = generate_result_matrix(rm,d,a)

    
    val = int(result[index_val[0]][index_val[1]])

    indicies = search(rm,index_val,val,d,a)
    print("indicies = ",indicies)
    tup = all_tuples(indicies)
    print(tup)



    return render_template("index.html", rm=rm, result=result, iv=index_val, val=val,indi = indicies,lot=tup)



# if __name__ == "__main__":
#     application.run(debug=True,port=5001)
