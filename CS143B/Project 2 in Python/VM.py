
PM = [None] * 524288 #PM[524288]
D = [[None]*512]*1024 #D[1024][512]
freeFrame = []
freeFrame.append(0)
freeFrame.append(1)

def read_block(b, m):
    #read_block(int b, int m)
    #copies block b from D and places it in PM starting at location PM[m].
    b = abs(b)
    index = 0
    for i in D[b]:
        if i != None:
            # print(i)

            PM[m+index] = i
            # print(m+index)
            # print(PM[m+index])
            index += 1
    return

def place_in_D(position, pos_two, value):
    #make sure to turn D position
    #places value(f) in D[position]
    positive = abs(position)
    D[positive][pos_two] = value
    return

def findFreeFrame():
    index = 0
    run = True
    while(run):
        if index not in freeFrame:
            run = False
            freeFrame.append(index)
            return index
        index += 1
    return -1
            



def main():
    f = input("Enter Init filename: ")
    file1 = open(f, 'r') # <================ INIT FILE NAME HERE ======
    Lines = file1.readlines()

    
    line = Lines[0]
    line = line.strip()
    line = line.split(" ")
    # print(line)
    step = int(len(line)/3)
    for i in range(step):
        # print(int(line[3*i]))
        PM[2*(int(line[3*i]))] = int(line[3*i+1])
        PM[2*(int(line[3*i]))+1] = int(line[3*i+2])
        if int(line[3*i+2]) > 0:
            freeFrame.append(int(line[3*i+2]))
    
    line = Lines[1]
    line = line.strip()
    line = line.split(" ")
    step = int(len(line)/3)
    for i in range(step):
        s = int(line[3*i])
        p = int(line[3*i+1])
        f = int(line[3*i+2])
        # print(s)
        # print(p)
        # print(f)
        # print()
        withinInner = PM[2*s+1]
        # print(withinInner)
        #if withinInner is < 0, place in D
        if f > 0:
            freeFrame.append(f)
        if withinInner < 0:
            place_in_D(withinInner, p, f)
        else:
            inner = withinInner*512+p
            PM[inner] = f
    file1.close()
    
    f = input("Enter Input filename: ")
    O = input("Enter Output filename: ")
    file2 = open(f, 'r') #<============= INPUT FILE NAME HERE ========= 
    line = file2.readline()
    line = line.strip()
    line = line.split(" ")
    output = []
    for va in line:
        
        zero_ext = "{0:032b}".format(int(va))
        s = zero_ext[5:14]
        p = zero_ext[14:23]
        w = zero_ext[23:32]
        pw = zero_ext[14:32]

        s = int(s, 2)
        p = int(p, 2)
        w = int(w, 2)
        pw = int(pw, 2)

        inner1 = PM[2*s]
        inner1_plus1 = PM[2*s+1]
        InnerWithinInner = PM[inner1_plus1*512+p]

        
        did_we_go_into_else = 0
        lastFree = 0
        if pw >= inner1:
          output.append(-1)
        else:
            
            if inner1_plus1 < 0:
                nextFree = findFreeFrame()
                lastFree = nextFree
                read_block(inner1_plus1, nextFree*512)

                if PM[nextFree*512+p] < 0:
                    nextFree -= 1
                    # nextFree = lastFree
                    output.append(nextFree*512+w)
                    did_we_go_into_else = 1
                else:
                    val = PM[nextFree*512+p]
                    val = val *512 + w
                    output.append(val)
                    did_we_go_into_else = 1
            elif PM[inner1_plus1*512+p] < 0:
                nextFree = findFreeFrame()
                # nextFree = lastFree
                nextFree = nextFree-1
                output.append(nextFree*512+w)
                did_we_go_into_else = 1


            if did_we_go_into_else == 0:
                inner1 = (PM[2*s+1])*512+p
                PA = PM[inner1]*512+w
                output.append(PA)

    
    file2.close()


    PAs = " "
    for n in output:
        PAs += str(n)
        PAs += " "
    PAs = PAs.strip()
    file3 = open(O, 'w')
    file3.write(PAs)
    file3.close()



if __name__ == "__main__":
        main()
