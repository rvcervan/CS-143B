


def createBitmap():
    bitmap = []
    for i in range(64):
        bitmap.append(0)
    
    return bitmap

def initDisk():
    D = []
    for i in range(64):
        D.append(-1)
    return D

class file_descriptor():
    def __init__(self, file_size, file_id):
        self.file_size = file_size #max of 1536
        # block_1 = 0
        # block_2 = 0
        # block_3 = 0
        self.file_id = file_id # correlates to the Simulated_directory index. Same number means they belong to same file

class Simulated_directory():
    def __init__(self, name, index):
        self.name = name #can only hold 3 chars, 0 means free
        self.index = index #index of file descriptor from 1 to 192 or D[1]-D[6], 0 is reserved for directory 

class open_file_table():
    def __init__(self, buffer, position, file_size, file_id):
        self.buffer = buffer #max of 1536?
        self.position = position #position of char index of file. begin writing chars to 0, -1 is free
        self.file_size = file_size #length of buffer 
        self.file_id = file_id #index on one of the disk blocks

class init():
    #create disk
    #D[0] is bitmap
    def __init__(self):
        self.D = initDisk()
        bitmap = createBitmap()
        self.D[0] = bitmap

    #D[1-6] are file descriptors. since lists are dynamic in python without byte sizes limiting them
    #I'll make it so that each block 1-6 can hold at most 32 file descriptors
    
        FD = []
        self.D[1] = FD
        self.D[2] = FD
        self.D[3] = FD
        self.D[4] = FD
        self.D[5] = FD 
        self.D[6] = FD

        # dir_descriptor = file_descriptor(0, 0)
        # self.D[1].append(dir_descriptor)


    #D[7] is reserved for directory
    #D[7][0] contains info of directory
        Directo = []
        Directo.append(Simulated_directory(0,0))
        self.D[7] = Directo


    #D[8-63] are free blocks
    #I'll make it so that each block holds 1536 so each block acts as 3 blocks
    #partition the block by 512 so that bytes < 512 is b1, 512 > bytes < 1024 is b2, bytes > 1024 is b3 


        self.M = "" #main memory area holding up to 512 chars

        self.OFT = []
        for i in range(4):
            self.OFT.append(open_file_table("", -1, 0, 0))

        self.unused_id = 8 #unused id to give to directory and file descriptor, max is 191

    def create(self, name):
        #D[7] is the directory
        #D[7][0] is the main directory that doesn't get index
        #iterate through D[7][1-192] to find a file that matches with name using the seek function
        #if seek() returns 0, error: duplicate name. 
        #if seek() reutrns an int, that is index where file was found.
        result = ""
        #D[1][0] is file descriptor for directory
        for i in self.D[7]:
            if name == i.name:
                return "error"
        yep = 0
        temp = self.unused_id
        for i in range(1, 7):
            if len(self.D[i]) == 191:
                return "error"
            elif yep == 0:
                file_d = file_descriptor(0, self.unused_id)
                self.D[i].append(file_d)

                new_file = Simulated_directory(name, self.unused_id)
                self.D[7].append(new_file)
                self.unused_id += 1

                # print(name, "created")
                result = str(name) + " created"
                yep = 1
                break
        
        return result

    def destroy(self, name):
        #use seek to find position of file, seek will return id of file
        result = ""
        #look for 
        file_id = -1
        for i in self.D[7]:
            if i.name == name:
                file_id = i.index
                self.D[7].remove(i)
                break
        
        #if file_id is still -1, couldn't find file to destroy 
        if file_id == -1:
            
            return "error"
        
        for i in range(1, 7):
            for x in self.D[i]:
                if x.file_id == file_id:
                    self.D[i].remove(x)
                    break
        # print(name, "destroyed")
        result = name + " destroyed"
        return result

    #seek(i, p) moves the current position within an open file at index i to a new position, p
    def seek(self, index, position):
        result = ""
        #if p > file size, exit with error: current position is past the end of file
        if index == 0:
            return "error"
        
        if index < 0 or index > 3:
            return "error"
        current_file = self.OFT[index]

        if current_file.file_id == -1:
            return "error"
        if position > current_file.file_size:
            return "error"

        self.OFT[index].position = position
        # print("position is", position)
        result = "position is " + str(position)

        return result

    def read(self, index, location_m, n_bytes):
        
        if self.OFT[index].position == -1:
            return "error"

        result = ""
        if index == 0:
            return "error"
        
        if index < 0 or index > 3:
            return "error"

        if len(self.OFT[index].buffer) < n_bytes:
            n_bytes = len(self.OFT[index].buffer)


        if location_m > len(self.M):
            diff = location_m - len(self.M)
            for i in range(diff):
                self.M += "@"

        buff_str = self.OFT[index].buffer[self.OFT[index].position:]
        buff_str = buff_str[:n_bytes]
        
        add_to_position = len(buff_str)
        buff_str = self.M[:location_m] + buff_str + self.M[len(buff_str) + location_m:]
        self.M = buff_str
        self.OFT[index].position = self.OFT[index].position + add_to_position

        # self.M = self.M[:location_m] + buff_str + self.M[location_m:]
        # self.OFT[index].position = self.OFT[index].position + n_bytes


        # print(n_bytes, "bytes read from", index)
        result = str(n_bytes) + " bytes read from " + str(index)
        return result

    def write(self, index, location_m, n_bytes):
        #writes from Memory to buffer of oft
        result = ""

        if self.OFT[index].file_size == 1536:
            return "0 bytes written to " + str(index)

        if index == 0:
            return "error"
        
        if index < 0 or index > 3:
            return "error"

        # Dont know here
        if n_bytes > len(self.M):
            diff = n_bytes - len(self.M)
            for i in range(diff):
                self.M += "@"


        file_id = -1
        mem_string = self.M[location_m:]
        mem_string = mem_string[:n_bytes]
        # mem_string = self.OFT[index].buffer[self.OFT[index].position:] + mem_string + self.OFT[index].buffer[:self.OFT[index].position] #
        # if len(self.OFT[index].buffer > len(mem_string)):
        add_to_position = len(mem_string)
        mem_string = self.OFT[index].buffer[:self.OFT[index].position] + mem_string + self.OFT[index].buffer[len(mem_string) + self.OFT[index].position:]
        self.OFT[index].position = self.OFT[index].position + add_to_position
        # else:


        if len(mem_string) > 1536:
            byte_to_sub = len(mem_string) - 1536
            n_bytes = n_bytes - byte_to_sub
            mem_string = mem_string[:1536]

        self.OFT[index].buffer = mem_string
        file_id = self.OFT[index].file_id
        # if self.OFT[index].position > self.OFT[index].file_size:
        # self.OFT[index].file_size = self.OFT[index].file_size + n_bytes
        self.OFT[index].file_size = len(mem_string)


        for i in range(1, 7):
            for x in self.D[i]:
                if x.file_id == file_id:
                    x.file_size = self.OFT[index].file_size
                    # print(n_bytes, "bytes written to", index)
                    result = str(n_bytes) + " bytes written to " + str(index)
                    return result
        return "error"
    
    def open(self, name):

        #checks if file is opened in oft.

        #search directory for a match on file name
        Directory = self.D[7]
        result = ""
        #for oft table
        file_id = -1
        current_position = 0
        file_size = -1
        buff = ""

        for i in Directory:
            if name == i.name:
                file_id = i.index
                break
        if file_id == -1:
            return "error"
        found = 0
        for i in range(1, 7):
            for x in self.D[i]:
                if x.file_id == file_id:
                    file_size = x.file_size
                    found = 1
                    break
            if found == 1:
                break
        
        for i in self.OFT:
            if file_id == i.file_id and i.position != -1:
                return "error"


        if file_size > 0:
            buff = self.D[file_id]
        
        oft_space_checker = 0 #if 0, no space in oft, if 1, oft register succesful
        OFT_opened_at = -1
        for i in range(1, 4):
            if self.OFT[i].position == -1: # free spot in oft
                self.OFT[i].position = current_position
                self.OFT[i].file_size = file_size
                self.OFT[i].buffer = buff
                self.OFT[i].file_id = file_id
                oft_space_checker = 1
                OFT_opened_at = i
                # print(name,"opened",OFT_opened_at)
                result = str(name) + " opened " + str(OFT_opened_at)
                return result
                
    
        return "error"

    def close(self, index):
        result = ""

        if self.OFT[index].position == -1:
            return "error"

        file_id = -1
        file_id = self.OFT[index].file_id
        self.D[file_id] = self.OFT[index].buffer
        for i in range(1, 7):
            for x in self.D[i]:
                if x.file_id == file_id:
                    x.file_size = self.OFT[index].file_size
                    break
        
        self.OFT[index].position = -1
        
        # print(index, "closed")
        result = str(index) + " closed"

        return result

    def directory(self):
        result = ""

        skip = 0 #if skip is = 0, skip first entry, 1, go with directory contents
        names_size = {}
        for i in self.D[7]:
            for x in range(1, 7):
                for y in self.D[x]:
                    if i.index == y.file_id:
                        names_size[i.name] = y.file_size

        for x in names_size:
            # print(x, names_size[x], end = " ")
            result += str(x) + " " + str(names_size[x]) + " "
        return result

    def read_memory(self, m, n):

        mem = ""
        mem = self.M[m:]
        mem = mem[:m+n]
        remove = mem.replace("@", "")
        return remove
    
    def write_memory(self, m, s):
        result = ""
        self.M = self.M[:m] + s + self.M[m:]
        result = str(len(s)) + " bytes written to M"

        return result
    
    #dont know if I actually need read_block() and write_block() in python.

def main():

    running = True
    System = "a"

    file1 = open('input.txt', 'r')
    Lines = file1.readlines()

    # while running:
        # command = input()
        # command = command.split(" ")
        # arg_num = len(command)

    Output = []
    for line in Lines:
        command = line
        command = command.strip()
        command = command.split(" ")
        arg_num = len(command)
        command_without_newLine = []
        for sub in command:
            command_without_newLine.append(sub.replace("\n", ""))
        command = command_without_newLine
        if arg_num == 1:
            if command[0] == "dr":
                Output.append(System.directory() + "\n")
            elif command[0] == "in":
                System = init()
                Output.append("system initialized\n")
            else:
                Output.append("\n")
        elif arg_num == 2:
            if command[0] == "cr":
                
                Output.append(System.create(command[1]) + "\n")
            elif command[0] == "de":
                Output.append(System.destroy(command[1]) + "\n")
            elif command[0] == "op":
                Output.append(System.open(command[1]) + "\n")
            elif command[0] == "cl":
                Output.append(System.close(int(command[1])) + "\n")
            else:
                print("error 2")
        elif arg_num == 3:
            if command[0] == "sk":
                Output.append(System.seek(int(command[1]), int(command[2])) + "\n")
            elif command[0] == "rm":
                Output.append(System.read_memory(int(command[1]), int(command[2])) + "\n")
            elif command[0] == "wm":
                Output.append(System.write_memory(int(command[1]), str(command[2])) + "\n")
            else:
                print("error 3")
        elif arg_num == 4:
            if command[0] == "rd":
                Output.append(System.read(int(command[1]), int(command[2]), int(command[3])) + "\n")
            elif command[0] == "wr":
                Output.append(System.write(int(command[1]), int(command[2]), int(command[3])) + "\n")
            else:
                print("error 4")
        else:
            print("wrong args count")

    file2 = open('output.txt', 'w')
    file2.writelines(Output)
    file2.close()
    


    


if __name__ == "__main__":
        main()