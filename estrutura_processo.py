class Process:
    def __init__(self, name,  mem_start, mem_end):
        # Nome do processo
        self.name = name 
        # Registradores do processador
        self.registers = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'PC': 0}
         # Estado do processo
        self.state = 'READY'
		# endereço inicial do espaço de memória do processo
        self.mem_start = mem_start  
         # endereço final do espaço de memória do processo
        self.mem_end = mem_end 
         # espaço de memória do processo
        self.memory = [0] * (self.mem_end - self.mem_start + 1) 
        
	# Carrega um programa na memória do processo
    def load(self, data, address):
        # passa por todos os dados do programa
        for i, d in enumerate(data):
            # Verifica se o endereço de memória está dentro do limite do processo
            if address + i <= self.mem_end:
                # Armazena o dado na memória do processo
                self.memory[address + i - self.mem_start] = d
            else:
                raise MemoryError("Endereço de memória fora do limite.")

	# Armazena um dado na memória do processo
    def store(self, address, length):
        # Verifica se o endereço de memória está dentro do limite do processo
        if address < self.mem_start or address + length > self.mem_end:
            raise MemoryError("Endereço de memória fora do limite.")
        
		# Retorna o dado armazenado na memória do processo
        return self.memory[address - self.mem_start : address - self.mem_start + length]

	# Executa o programa carregado na memória do processo
    def execute(self):
        while self.pc < len(self.memory):
            # Instrução a ser executada, pegamos o valor da proxima instrução e subtraimos o endereço inicial da memória do processo
            instr = self.memory[self.pc - self.mem_start]
            # ... Instruções do processo ...
            # Atualização dos registradores e do PC
            self.pc += 1

	# Retorna o valor de um registrador do processo
    def get_register_value(self, reg):
        return self.registers[reg]

	# insere um valor no registrador do processo
    def set_register_value(self, reg, value):
        self.registers[reg] = value

	# Retorna o valor do PC ou endereço da próxima instrução a ser executada
    def get_pc_value(self):
        return self.pc

	# insere um valor no PC, o valor do pc é o endereço da próxima instrução a ser executada
    def set_pc_value(self, value):
        self.pc = value

	# Retorna o estado do processo
    def get_state(self):
        return self.state

	# insere um valor no estado do processo
    def set_state(self, state):
        self.state = state