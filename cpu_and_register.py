from memory_and_cache import Memory, FIFOCache


class CPU:
    def __init__(self):
        self.fifocache = FIFOCache()
        self.memory = Memory()
        self.program_counter = 0
        self.halted = False
        self.register = [0] * 32
        self.num_registers = 32       
    
    def get_instruction(self):
        if self.halted:
            return None                                         
        instruction = self.memory.read(self.program_counter)                                 
        return instruction                                      

    def halt(self):
        self.halted = True

    def decode_and_execute(self, instruction_raw):                                  #this is a massive method, could be broken up into multiple methods,
        print(f"Program Counter: {self.program_counter}")                           #but that is a problem for when i come back to refine this model
        if self.halted:
            return
        instruction = instruction_raw.replace('$', '')
        instr_parts = instruction.split(',')
        opcode = instr_parts[0].strip()
        if len(instr_parts) > 1:
            part_1 = int(instr_parts[1].strip())
        if len(instr_parts) > 2:
            if '(' in instr_parts[2]:
                temp = instr_parts[2].strip().replace(')', '').replace('(', ',')
                # print(temp)
                part_2 = temp.split(',')
                # print(part_2)
            else:
                part_2 = int(instr_parts[2].strip())

        if len(instr_parts) > 3:
            part_3 = int(instr_parts[3].strip())
        
        print(f"Opcode: {opcode}")

        if opcode == 'ADD':
            print(f"Adding {self.register[part_2]} and {self.register[part_3]}, storing result in ${part_1}")
            self.register[part_1] = self.register[part_2] + self.register[part_3]
            self.program_counter += 1

        elif opcode == 'ADDI':
            print(f"Adding {self.register[part_2]} and {part_3}, storing result in ${part_1}")
            self.register[part_1] = self.register[part_2] + part_3
            self.program_counter += 1

        elif opcode == 'SUB':
            print(f"Subtracting {self.register[part_3]} from {self.register[part_2]}, storing result in ${part_1}")
            self.register[part_1] = self.register[part_2] - self.register[part_3]
            self.program_counter += 1

        elif opcode == 'SUBI':
            print(f"Subtracting {part_3} from {self.register[part_2]}, storing result in ${part_1}")
            self.register[part_1] = self.register[part_2] - part_3
            self.program_counter += 1
            
        elif opcode == 'MULT':
            print(f"Multiplying {self.register[part_2]} by {self.register[part_3]}, storing result in ${part_1}")
            self.register[part_1] = self.register[part_2] * self.register[part_3]
            self.program_counter += 1
            
        elif opcode == 'DIV':
            if self.register[part_3] != 0:
                print(f"Dividing {self.register[part_2]} by {self.register[part_3]}, storing result in ${part_1}")
                self.register[part_1] = self.register[part_2] // self.register[part_3]
                self.program_counter += 1
            else:
                print('Cannot divide by zero')
                self.halt()
          
        elif opcode == 'LW':
            offset = int(part_2[0])                                                 #i'm including the offset here in case i want to improve on this in the future, for now the offset will effectively be the memory address/index
            base_register = int(part_2[1])                                          #pulling register index, for now this will almost always be zero, but including in case i want to improve this system                                                                                   
            address = base_register + offset                                        #add register location plus offset amount to get memory address from which word will be loaded
            if self.fifocache.cache_check(address):
                print("Cache hit")
                temp_dat = self.fifocache.cache_read(address)
            else:
                print(f"Data not found in cache, seeking data at memory address: {address}")
                temp_dat = self.memory.read(address)
                self.fifocache.cache_write(address, temp_dat)
            # print(temp_dat)
            self.register[part_1] = temp_dat                                        #data in target register location now equals data in memory at given address
            print(f"Loading {temp_dat} to register ${part_1}")
            self.program_counter += 1
            
        elif opcode == 'SW':
            offset = int(part_2[0])                                                 #doing the same thing here as 'LW', just reversing the last line, writing to memory at given address equal data in register at given location 
            base_register = int(part_2[1])     
            address = base_register + offset
            temp_dat = self.register[part_1]
            print(f"Writing data ({temp_dat}) and corresponding memory address ({address}) to cache")                   
            self.fifocache.cache_write(address, temp_dat)                           #writing to cache, FIFOCache.cache_write method will handle FIFOCache.write_back method if/when necessary to maintain data in memory at correct memory address
            self.program_counter += 1   

        elif opcode == 'J':                                                         #jump to specific program counter number
            target = int(instr_parts[1].strip())
            print(f"Setting program counter to {target}")
            self.program_counter = target

        elif opcode == 'JAL':
            target = int(instr_parts[1].strip())
            print(f"Setting program counter to {target}")
            return_address = self.program_counter + 1   
            print(f"Storing return address ({return_address}) in $31")                            #jump, but store next program counter in register idx 31 (standard mips32 choice for storing return address in 'JAL' instruction, so after subroutine completed can return to next planned instruction)
            self.register[31] = return_address                                  
            self.program_counter = target

        elif opcode == 'JR':
            if part_1 == 31:
                print(f"Setting program counter to return address stored in $31")
                self.program_counter = self.register[31]
            else:
                print('Invalid register used')

        elif opcode == 'BNE':
            if self.register[part_1] != self.register[part_2]:
                print(f"Data in ${part_1} does not equal data in ${part_2}")
                print(f"Setting program counter to {part_3}")
                self.program_counter = part_3
            else:
                self.program_counter += 1  

        elif opcode == 'BGT':
            if self.register[part_1] > self.register[part_2]:
                print(f"Data in ${part_1} is greater than data in ${part_2}")
                print(f"Setting program counter to {part_3}")
                self.program_counter = part_3   
            else:
                self.program_counter += 1    

        elif opcode == 'BEQ':
            if self.register[part_1] == self.register[part_2]:
                print(f"Data in ${part_1} is equal to data in ${part_2}")
                print(f"Setting program counter to {part_3}")
                self.program_counter = part_3     
            else:
                self.program_counter += 1                        

        elif opcode == 'HALT':
            self.halt()

        else:
            print(f'{instruction} unknown')
        
    def run(self):
        while not self.halted:
            instruction = self.get_instruction()
            if instruction is None:
                self.halt()
            else:
                self.decode_and_execute(instruction)                

    def print_register_locations(self):
        for idx, dat in enumerate(self.register):
            print(idx, dat)