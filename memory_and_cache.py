class Memory:
    def __init__(self, size = 256):
        self.data = [None] * size
        self.instruction_start = 0  #adding here in case i want to set aside a portion of memory for instruction storage
        self.instruction_end = 128   #this will allow me to store up to 128 instructions. may come back to tweak memory for instructions vs data
        self.size = size

    def instruction_check(self, address):
        return self.instruction_start <= address < self.instruction_end

    def read(self, address):
        address = int(address)
        if 0 <= address and address < self.size:
            if self.instruction_check(address):
                print(f"Reading instruction from address: {address}")
            else:
                print(f"Reading data from address: {address}")
            return self.data[address]
        else:
            raise IndexError("memory address does not exist")    

    def write(self, address, data):
        if 0 <= address < self.size:
            if self.instruction_check(address):
                print(f"Writing instruction to address: {address}")
            else:
                print(f"Writing data to address: {address}")
            self.data[address] = data
        else:
            raise IndexError("memory address does not exist")

    def load_instructions_from_file(self, file_name):
        with open(file_name, 'r') as file:
            instrs = file.readlines()
            for idx, instr in enumerate(instrs):                              
                self.write(idx, instr.strip())
                print(instr)                                            

    def load_data_from_file(self, file_name):
        with open(file_name, 'r') as file:
            dataset = file.readlines()
            for idx, data in enumerate(dataset):
                real_idx = idx + self.instruction_end           #using the idx+self.instruction_end to have data stored in memory begin where idx = 128
                real_data = int(data.strip())
                self.write(real_idx, real_data)                 
    
    def print_memory(self):
        for idx, dat in enumerate(self.data):
            print(idx, dat)


class FIFOCache(Memory):
    def __init__(self, cache_size = 16):
        super().__init__()
        self.cache_size = cache_size
        self.cache = []                                             #cache data stored in order of replacement, self.to_be_replaced stores addresses, use index to match address and data
        self.to_be_replaced = []                                    #using the replacement list as my counter for cache size and for storing addresses. since the cache list will be kept the same size i can operate on the understanding that the indexes on both will correctly match up address and data
    
    def cache_check(self, address):
        return address in self.to_be_replaced    
    
    def write_back(self):
        temp_addr = self.to_be_replaced.pop(0)                      #taking address from front of replacement list
        temp_data = self.cache.pop(0)                               #taking data from front of cache list
        super().write(temp_addr, temp_data)                         #writing data from cache to memory in the correct location. skipping dirty flagging here for simplicity: anything about to be overwritten in cache is first written to memory
        print(f"{temp_data} has been written to memory address {temp_addr}")

    def cache_write(self, address, data):
        if len(self.to_be_replaced) == self.cache_size:
            print('Cache full, moving oldest data to memory')
            self.write_back()
        self.to_be_replaced.append(address)
        self.cache.append(data)
        print(f"Writing data ({data}) and address ({address}) to cache")

    def cache_read(self, address):
        idx = self.to_be_replaced.index(address)
        return self.cache[idx]
    
    def print_cache(self):
        for idx in range(self.cache_size):
            print(self.to_be_replaced[idx])
            print(self.cache[idx])