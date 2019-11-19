import random 
import os


class Test_Generator:
    def __init__(self, num_per_case = 100): # number of test for each case
        self.num_per_case = num_per_case

    


    def binary_to_real_number(self, bin_string):
        
        if  '.' in bin_string:

            integer , decimal = bin_string.split('.')

            sum = 0.0
            for n, i in enumerate(integer[::-1]):
                if i == '1':
                    sum += 2**n
            
            for n, i in enumerate(decimal):
                if i == '1':
                    sum += (1/2)**(n+1)
        else:
            sum = 0
            for n, i in enumerate(bin_string[::-1]):
                if i == '1':
                    sum += 2**n
        return sum
            
         




    def convert_vector_to_normalized_num(self, vector):
        
        Sig = -1 if vector[0] else 1
        Exp = ''.join(list(map( lambda x : str(x), vector[1:9])))
        Fract = '1.'+''.join(list(map( lambda x : str(x), vector[9:])))

    
        Exp = self.binary_to_real_number(Exp)
        Fract = self.binary_to_real_number(Fract)
        sum = Sig*2**(Exp-127)*Fract
        
        return sum


    
    def convert_vector_to_denormalized_num(self, vector):

        Sig = -1 if vector[0] else 1
        Fract = '0.'+''.join(list(map( lambda x : str(x), vector[9:])))
        
        Fract = self.binary_to_real_number(Fract)

        sum = Sig*2**(-126)*Fract
        
        return sum



    def interger_to_binary(self, num):
        if num == 0:
            return [0]
        arr = []
        while num >0:
            arr.append(num%2)
            num = num//2
        return arr[::-1]


    def fract_to_binary(self, num):

        arr = []
        if num == 0:
            return [0]
        i = -1 
        while num >0:
            arr.append(int(num/2**(i)))
            num = num%(2**(i))
            i-=1
        return arr

    def convert_num_to_vector(self, num):
        
        Sign = [1] if num < 0 else  [0]
        num = abs(num)

        if num > 1.1754942E-38:
            integer, fract =  self.interger_to_binary(int(num//1)), self.fract_to_binary(num%1)
            
            vect = integer+fract
            decimal_point_position = len(integer)-1
            fist_1_index = vect.index(1)

            shift = decimal_point_position - fist_1_index 
            Exp = shift 
            Exp +=127
            Exp = self.interger_to_binary(Exp)
            Exp = [ 0 for i in range(8-len(Exp)) ] + Exp
            Fract = vect[fist_1_index+1:fist_1_index+1+23] if len(vect[fist_1_index+1:]) > 23  else  vect[fist_1_index+1:] + [0 for i in range(23-len(vect[fist_1_index+1:]))]
        else:
            Exp = [0 for i in range(8)]
            fract = num / (2**(-126))
            fract = self.fract_to_binary(fract)
            Fract = fract[0:23] if len(fract)>23 else fract + [0 for i in range(23-len(fract))]

        return "".join(list(map(lambda x : str(x), Sign+Exp+Fract)))

    def random_normalized_vector(self):
        
        return [ random.randint(0,1) for i in range(32)]
    
    def random_denormalized_vector(self):
        
        return [ random.randint(0,1)]+[0 for i in range(8)]+[ random.randint(0,1) for i in range(23)]
    
    def random_infinity(self):
        return [ random.randint(0,1)] + [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    def random_zero(self):
        return [ random.randint(0,1)] + [0 for i in range(31)]


    def format_num(self,num):
        if num >=0:
            return "....+{:10.4e}".format(num)
        else:
            return  "....{:10.4e}".format(num)



    def generate_test_vector_file(self):
        
        with open("test_vector.txt", "w") as f:

            for i in range(self.num_per_case):
                # normalized + # normalized
                A = self.random_normalized_vector()
                B = self.random_normalized_vector()
                A_num = self.convert_vector_to_normalized_num(A)
                B_num = self.convert_vector_to_normalized_num(B)
                C_num = A_num + B_num
                C = self.convert_num_to_vector(C_num)
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line =self.format_num(C_num) + " "+ C+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # denormalized + # denormalized
                A = self.random_denormalized_vector()
                B = self.random_denormalized_vector()
                A_num = self.convert_vector_to_denormalized_num(A)
                B_num = self.convert_vector_to_denormalized_num(B)
                C_num = A_num + B_num
                C = self.convert_num_to_vector(C_num)
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(C_num) + " "+ C+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # normalized + # denormalized
                A = self.random_normalized_vector()
                B = self.random_denormalized_vector()
                A_num = self.convert_vector_to_normalized_num(A)
                B_num = self.convert_vector_to_denormalized_num(B)
                C_num = A_num + B_num
                C = self.convert_num_to_vector(C_num)
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(C_num) + " "+ C+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # denormalized + # normalized
                A = self.random_denormalized_vector()
                B = self.random_normalized_vector()
                A_num = self.convert_vector_to_denormalized_num(A)
                B_num = self.convert_vector_to_normalized_num(B)
                C_num = A_num + B_num
                C = self.convert_num_to_vector(C_num)
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(C_num) + " "+ C+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # infinity + # normalized
                A = self.random_infinity()
                B = self.random_normalized_vector()
                B_num = self.convert_vector_to_normalized_num(B)
                line = ""
                line = ("..........-INFI" if A[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = ("..........-INFI" if A[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), A)))+"\n"
                f.write(line)

            for i in range(self.num_per_case):
                # normalize + # infinity
                A = self.random_normalized_vector()
                A_num = self.convert_vector_to_normalized_num(A)
                B = self.random_infinity()
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+(("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B))))+"\n"
                f.write(line)
                line = ("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
            

            for i in range(self.num_per_case):
                # infinity + # denormalized
                A = self.random_infinity()
                B = self.random_denormalized_vector()
                B_num = self.convert_vector_to_denormalized_num(B)
                line = ""
                line = ("..........-INFI" if A[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = ("..........-INFI" if A[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), A)))+"\n"
                f.write(line)

            for i in range(self.num_per_case):
                # normalize + # infinity
                A = self.random_denormalized_vector()
                A_num = self.convert_vector_to_denormalized_num(A)
                B = self.random_infinity()
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+(("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B))))+"\n"
                f.write(line)
                line = ("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                #Nan + # normalized
                A = "01111111100000000000000000000001"
                B = self.random_normalized_vector()
                B_num = self.convert_vector_to_normalized_num(B)
                line = ""
                line = "............Nan"+" "+"01111111100000000000000000000001"+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)

            for i in range(self.num_per_case):
                # normalized + #Nan
                A = self.random_normalized_vector()
                A_num = self.convert_vector_to_normalized_num(A)
                B = "............Nan"+" "+"01111111100000000000000000000001"
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+"............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
            for i in range(self.num_per_case):
                #Nan + # denormalized
                A = "01111111100000000000000000000001"
                B = self.random_denormalized_vector()
                B_num = self.convert_vector_to_denormalized_num(B)
                line = ""
                line = "............Nan"+" "+"01111111100000000000000000000001"+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)

            for i in range(self.num_per_case):
                # denormalized + #Nan
                A = self.random_denormalized_vector()
                A_num = self.convert_vector_to_denormalized_num(A)
                B = "............Nan"+" "+"01111111100000000000000000000001"
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+"............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # zero + # normalized
                A = self.random_zero()
                B = self.random_normalized_vector()
                B_num = self.convert_vector_to_normalized_num(B)
                line = ""
                line = (".............-0" if A[0] else ".............+0") +" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # normalized + # zero 
                A = self.random_normalized_vector()
                A_num = self.convert_vector_to_normalized_num(A)
                B = self.random_zero()
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+(".............-0" if B[0] else ".............+0") +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+"\n"
                f.write(line)
            for i in range(self.num_per_case):
                # zero + # denormalized
                A = self.random_zero()
                B = self.random_denormalized_vector()
                B_num = self.convert_vector_to_denormalized_num(B)
                line = ""
                line = (".............-0" if A[0] else ".............+0") +" "+"".join(list(map(lambda x:str(x), A)))+self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(B_num) +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # denormalized + # zero 
                A = self.random_denormalized_vector()
                A_num = self.convert_vector_to_denormalized_num(A)
                B = self.random_zero()
                line = ""
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+(".............-0" if B[0] else ".............+0") +" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = self.format_num(A_num) +" "+"".join(list(map(lambda x:str(x), A)))+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # zero  + # infinity
                A = self.random_zero()
                B = self.random_infinity()
                line = ""
                line = (".............-0" if A[0] else ".............+0") +" "+"".join(list(map(lambda x:str(x), A)))+("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = ("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
            for i in range(self.num_per_case):
                # infinity  + # zero
                A = self.random_infinity()
                B = self.random_zero()
                line = ""
                line = ("..........-INFI" if A[0] else "..........+INFI") +" "+"".join(list(map(lambda x:str(x), A)))+(".............-0" if B[0] else ".............+0")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = ("..........-INFI" if A[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), A)))+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                # zero  + # zero
                A = self.random_zero()
                B = self.random_zero()
                line = ""
                line = (".............-0" if A[0] else ".............+0") +" "+"".join(list(map(lambda x:str(x), A)))+(".............-0" if B[0] else ".............+0")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = (".............-0" if A[0] else ".............+0")+" "+"".join(list(map(lambda x:str(x), A)))+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                #Nan  + # zero
                A = "............Nan"+" "+"01111111100000000000000000000001"
                B = self.random_zero()
                line = ""
                line = "............Nan"+" "+"01111111100000000000000000000001"+(".............-0" if B[0] else ".............+0")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
            for i in range(self.num_per_case):
                # Zero  + #Nan
                A = self.random_zero()
                B = "............Nan"+" "+"01111111100000000000000000000001"
                line = ""
                line = (".............-0" if A[0] else ".............+0")+" "+"".join(list(map(lambda x:str(x), A)))+"............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
            
            for i in range(self.num_per_case):
                #Nan  + # infinity
                A = "............Nan"+" "+"01111111100000000000000000000001"
                B = self.random_infinity()
                line = ""
                line = "............Nan"+" "+"01111111100000000000000000000001"+("..........-INFI" if B[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), B)))+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
            for i in range(self.num_per_case):
                # infinity  + #Nan
                A = self.random_infinity()
                B = "............Nan"+" "+"01111111100000000000000000000001"
                line = ""
                line = ("..........-INFI" if A[0] else "..........+INFI")+" "+"".join(list(map(lambda x:str(x), A)))+"............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)
                line = "............Nan"+" "+"01111111100000000000000000000001"+"\n"
                f.write(line)


            
            
        
            
            f.close()

            

if __name__ == "__main__":
    
    t = Test_Generator(num_per_case=100)
    t.generate_test_vector_file()
