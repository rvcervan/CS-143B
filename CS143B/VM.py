#Project Specifics
#1. Physical memory is an integer array PM[524288]
#2. The disk (when implementing demand paging) is an integer array[1024][512]
#3. All VAs and PAs are integers
#4. The size of s, p and w is 9 bits each
#5. The VM manager initializes the PM from an input file consisting of 2 lines
    #> Line 1 contains triples of integers, which define the contents of the ST
    #> Line 2 contains triples of integers, which define the contents of the PTs
    #> The initialization file is syntactically correct in that:
        #* Line 1 correctly specifies 1 or more segment table
        #* Line 2 correctly specifies 0 or more entries in PTs for the segments 
        #  specified on line 1
#6. The VM manager then reads VAs from another input file, attempts to translate each
#   into a PA, and write the results into an output file
#7. The basic version of the VM manager does not support demand paging and is worth
#   60% of the credit for the project.
#8. The extended version of the VM manager must support demand paging and is worth
#   100% of the credit for the project
#9. For demand paging the PM will always have a sufficient number of free frames
#   available so that no page replacement algorithm is needed.

#translation look-aside buffer not required.

#VM: Virtual Memory
#PT: Page Tables
#VA: Virtual Address
#PA: Physical Address
#TLB: Translation Look-aside Buffer
#PM: Physical Memory
#ST: Segment Table

#The VM accepts VAs and translates them into PAs according to the current
#contents of the segment and PTs

#SEGMENTATION WITH PAGING

#With pure segmentation, the logical address space of a process is divided
#into variable-size blocks, each corresponding to a logical component of the process,
#such as the code, the static dtat, the stack, and the dynamic data.
#Each block is mapped into a contiguous portion of PM
#A segment table is used to keep track of the starting addresses of all segments
#
#Each VA is divided into 2 components, (s, w), where s is the segment number and
#w is the offset within the segment. Thus, s is an offset into the segment table.

#With pure paging, the logical address space of a process is divided into fixed-sized
#blocks, called pages. The PA space is divided into fixed-size blocks called page
#frames. The frame size and the page size must be identical and thus any page may
#be mapped into any available frame. A PT is used to keep track of the page numbers
#belonging to the process.
#
#Each VA is divided into 2 components, (p, w), where p is the page number and w is
#the offset within the page. Thus, p is an offset into the PT

#Segmentation advantage: blocks correspond to logical entities of the process, 
#which facilitates linking and sharing
#Paging advantage: efficient memory management by eliminating the need to search for
#and maintain variable-size memory partitions.

#You can combine both segmentation and paging, gaining both advantages, where each
#segment is divided into fixed-size pages, which do not have to be contiguous in PM

#Each entry of the ST points to a PT corresponding to one segment, and each
#entry of the PT points to one page comprising the address space of the process.

#Each VA is then divided into 3 components, (s, p, w), where s is the segment
#number (offset into the segment table), p is the page number (offset into the PT),
#and w is the offest within the page.

#ADDRESS TRANSLATION

#VA is nonnegative int.
#number of bits used to represent the VA determines the size of the VA space
#VA of 32 bits, 2^32 addresses can be created.

#The number of bits used to represent s,p, and w determine the size of the segment
#table, the PT, and each page, respectively.

#A PA is also a nonnegative int
#number of bits used to represent the PA determines the size of the PM.
#~~~~~~
#The task of the VM is to translate VAs into corresponding PAs.
#The first step is to break the VA into 3 components, s, p, and w, each of which 
#becomes a seperate integer.

#VA=(s,p,w) The segement number s is used as an offset in the ST to find the PT.
#The page number p is then used in the PT to find the page.
#Once you find the page address, w is then added to the starting address of the page
# to form the PA corresponding to the original VA.

#Since segments have different sizes, only a subset of the possible VAs is valid.
#To prevent a process from accessing a location outside of a given segment s, the
#segment size is recorded in the ST and is checked against the offset
#within the segment s. ???????

#DEMAND PAGING

#If the size of the VM exceeds the size of the PM, then not all pages can be present
#in PM at all times, but must be loaded from a disk as needed. This is called demand
#paging.
#When a nonresident page is needed and no free frame is available, one of the resident
#pages must be removed and replace by the new page. This is called page replacement.

#Demand paging and page replacement applies also to PTs. Thus, the PT of a given
#segment may not be resident when a VA is being tranlsated.

#To keep track of which pages of a segment s are currently resident, an additional
#bit called present bit(sometimes called the resident bit), is associated with
#each entry of the PT of segment s. Similarly, each entry of an ST contains a present
#bit to record the presence or absence of the corresponding PT. If the bit is true,
#then the entry contains the frame number of the page or PT. If the bit is false, then
#the entry contains the location of the page or PT on the disk.

#Referencing a nonresident page or PT is called a page fault, which the memory
#manager must resolve by locating the missing page or PT on the disk, allocating
#a page frame, and loading the missing page or PT into the frame.

#VM WITHOUT DEMAND PAGING
#VM SPECIFICATION

#or should I make a dict with size:page_num?
#If the segment does not exist, then both fields contain a 0.

#Each entry in a PT contains the number of the frame holding the page.
#If page is 0, then the entry contains a 0.

#A VA is 32 bits, divided into 3 components: s, p, and w. Where each component
#occupies 9 bits

#Size of each page is 512 words (integers). //Dont know if that words/(integers) is 
#                                           relevant in python
#Size of each PT is 512 words
#Size of ST is 1024 words (int), since each entry occupies 2 integers.//?
#The leading 5 bits of the VA are unused.



#REPRESENTATION OF PM (review this later)
#PM contains the ST, PT, and page as one big array/list. 
#Don't know if I have to create a PM if I can just keep it seperate like the lists above

#PM is an array of int, each corresponding to one addressable memory word. It is 
#implemented as an array of 524,288 integers (= 2MB).


#Since each entry consists of 2 integers, the segment number s must be doubled to
#access the corresponding entry.

#PM[2s] = size of segment s
#PM[2s+1] = frame number of the PT of segment s.

#To find the starting address of the PT, the frame number is multiplied by the 
#frame size PM[2s+1]*512

#Adding the page number p to the starting address of the PT yields the PT entry of
#page p: PM[2s+1]*512+p

#PM[PM[2s+1]*512+p] then contains the frame number, f_j, of the corresponding page p.

#To find the starting address of page p, the frame number is again multiplied by
#the frame size: PM[PM[2s+1]*512+p]*512

#Adding the offset w to the starting address of page p yields the final PA corresponding
#to the original VA: PM[PM[2s+1]*512+p]*512+w

#ADDRESS TRANSLATION

#DERIVING S, P, W, AND PW FROM THE VA
#pw is the offset for segment s, represented as a single int, must not exceed the
#segment size.

#s is obtained by right-shifting VA by 18 bits, which discards p and w

#w is extracted by anding the VA with the 9-bit binary constant "1 1111 1111" 
#(or 1FF in hex), which removes all bits other than the last 9 bits-the value of w

#p is extracted by first right-shifting VA by 9 bits to discard w. The result is then
#ANDed with the binary constant "1 1111 1111", whihc removes all bits other than the last
#9 bits-the value of p.

#pw is extracted by ANDing the VA with the 18-bit binary constant "11 1111 1111 1111 1111"
#(or 3FFFF in hex), which removes the leading s component.

#TRANSLATING VA TO PA

#if pw >= PM[2s], the report error.
#else PA = PM[PM[2s+1]*512+p]*512+w

#SYSTEM INITIALIZATION AND EXECUTION
#INITIALIZATION OF THE PM

#The PM is initialized from a file from a file, which specifies the frames of all PTs,
#the corresponding segment lengths, and the frame numbers of all pages.(ST always 
# resides in frames 0 and 1)

#The file consists of 2 lines, each containing a series of integers
#   Line 1: s1, z1, f1, s2, z2, f2...sn, zn, fn
#   Line 2: s1, p1, f1, s2, p2, f2...sn, pn, fn

#For line 1, PT of segment s resides in frame f, and the length of segment s is z.
#Thus line 1 defines the ST.
#8 4000 3 means that the PT of segment 8 resides in frame 3 and the size of 8 is 4000
#That is, the initialization sets PM[2*8] = PM[16] = 4000 and PM[2*8+1] = PM[17] = 3.

#For line 2, s p f means that page p of segment s resides in frame f. Thus, line 2 
#defines the PTs.
#8 5 8 means that page 5 of segment 8 resides in frame 8. That is, the initialization
#sets PM[PM[2*8+1]*512+5] = 8

#This is a manager, you are only calculating PA and not getting contents of pages
#Thus all pages contain zeros as the initial values of PM

#EXECUTING VA TRANSLATIONS

#Once the PM has been initialized, the system is ready to accept VAs and to attempt
#to translate them into PAs. The VAs are given in a second input file, which contains
#a series of integers, each representing one VA.

#The program must read the file and attempt to translate each VA according to the rules
#given in section 3.3. The result of each translation, which is either a corresponding
#PA or "error", is to be written to an output file.


#VM WITH DEMAND PAGING.
#PAGING DISK

#The paging disk is a 2D array, D[B][512], where B is the number of blocks and 
#512 is the block size (equal to the page size)

#The disk may only be accessed one block at a time. The function read_block(b, m)
#copies the entire block D[b] into the PM fram starting at location PM[M]

#All nonresident pages of the VM and Pts are kept on the paging disk.

#EXTENDED CONTENTS OF ST AND PT

#To indicate that a PT is currently not resident in PM, the corresponding ST entry
#contains a negative number, -b, where the absolute value |-b| = b is the block number
#on the paging disk that contains the PT

#Same for PT

#The sign bit in each ST or PT entry represents the present bit.

#LIST OF FREE FRAMES

#Since blocks may need to be moved to PM from the paging disk, the memory
#manager must keep track of which memory frames are free. A linked list can be used
#for that purpose.

#VA TRANSLATIONS
#if pw >= PM[2s], error
#if PM[2s+1] < 0, then page fault PT not resident)
#   Allocate free frame f1 using a list of free frames
#   Update list of free frames, how?
#   Read disk block b = |PM[2s+1]| into PM starting at location f2*512: read_block(b,f1*512)
#   PM[2s + 1] = f1 //update ST entry
#if PM[PM[2s+1]*512+p] < 0 // page fault: page is not resident
#   allocate free frame f2 using list of free frames
#   update list of free frames
#   read disk block b = |PM[PM[2s+1]*512+p]| into PM starting at location f2*512: read_block(b,f2*512)
#   PM[PM[2s+1]*512+p] = f2 //update PT entry
#Return PA = PM[PM[2s+1]*512+p]*512+w

#INITIALIZATION OF PHYSICAL MEMORY


#PM = []
#D = [B][512]

def main():

    PM = [None] * 524288 #PM[524288]
    D = [[None]*512]*1024 #D[1024][512]

    file1 = open('input1.txt', 'r')
    Lines = file1.readlines()

    
    line = Lines[0]
    line = line.strip()
    line = line.split(" ")
    step = int(len(line)/3)
    for i in range(step):
        PM[2*(int(line[3*i]))] = int(line[3*i+1])
        PM[2*(int(line[3*i]))+1] = int(line[3*i+2])
    
    line = Lines[1]
    line = line.strip()
    line = line.split(" ")
    step = int(len(line)/3)
    for i in range(step):
        s = int(line[3*i])
        p = int(line[3*i+1])
        f = int(line[3*i+2])
        inner = PM[2*s+1]*512+p
        PM[inner] = f
    file1.close()
    
    file2 = open("input2.txt", 'r')
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

        if pw >= PM[2*s]:
            output.append(-1)
            break
        else:
            inner1 = (PM[2*s+1])*512+p
            PA = PM[inner1]*512+w
            output.append(PA)
    
    file2.close()


    PAs = " "
    for n in output:
        PAs += str(n)
        PAs += " "
    PAs = PAs.strip()
    file3 = open('output.txt', 'w')
    file3.write(PAs)
    file3.close()



if __name__ == "__main__":
        main()
