import sys
sys.path.insert(1, '.')
def create_map(size_x,size_y,length,name,raduis,w_v,w_e):
    file=open(name,"w")
    file.write(str((size_x+1)*length)+"\n")
    file.write(str((size_y+1)*length)+"\n")
    file.write(str(length)+"\n")
    file.write(str(length)+"\n")
    file.write(str(raduis)+"\n")
    file.write(str(w_v)+"\n")
    file.write(str(w_e)+"\nvertices")
    for i in range(size_x):
        for j in range(size_y):
            file.write("\n"+str(i*length)+","+str(j*length))
    file.write("\nedges")
    for i in range(size_x):
        for j in range(size_y):
            if i<(size_x-1):
                file.write("\n"+str(i+j*size_x)+","+str(i+j*size_x+1))
            if j<(size_y-1):
                file.write("\n"+str(i+j*size_x)+","+str(i+j*size_x+size_x))
    file.close()
#create_map(10,1,60,"1_10_grid.txt",20,5,5)
#create_map(13,13,40,"13_13_grid.txt",13,3,3)
#create_map(20,20,30,"20_20_grid.txt",10,3,3)
#create_map(19,19,30,"19_19_grid.txt",10,3,3)
#create_map(5,5,60,"5_5_grid.txt",20,5,5)