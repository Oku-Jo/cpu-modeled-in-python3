from cpu_and_register import CPU

data_file = 'rng_data.txt'
instruction_file = 'instructions.txt'

if __name__ == '__main__':
    cpu = CPU()


cpu.memory.load_data_from_file(data_file)
cpu.memory.load_instructions_from_file(instruction_file)   #i've included the instructions to populate the cpu register at the beginning of this file
cpu.memory.print_memory()
cpu.run()

# cpu.print_register_locations()
# cpu.memory.print_memory()
# cpu.fifocache.print_cache()