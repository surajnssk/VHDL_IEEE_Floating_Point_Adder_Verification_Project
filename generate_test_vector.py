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


    def decimal_to_binary(self, num):

        arr = []
        i = -1 
        while num >0:
            arr.append(int(num/2**(i)))
            num = num%(2**(i))
            i-=1
        return arr

    def convert_num_to_vector(self, num):
        
        Sign = [1] if num < 0 else  [0]


        if num > 1.1754942E-38:
            integer, decimal =  self.interger_to_binary(int(num//1)), self.decimal_to_binary(num%1)
            
            vect = integer+decimal
            decimal_position = len(integer)-1
            fist_1_index = vect.index(1)

            shift = decimal_position - fist_1_index 
            Exp = shift 
            Exp +=127
            Exp = self.interger_to_binary(Exp)
            Exp = [ 0 for i in range(8-len(Exp)) ] + Exp
            Fract = vect[fist_1_index+1:fist_1_index+1+23] if len(decimal) >= 23  else  vect[fist_1_index+1:] + [0 for i in range(23-len(vect[fist_1_index+1:]))]
        else:
            Exp = [0 for i in range(8)]
            decimal = num / (2**(-126))
            decimal = self.decimal_to_binary(decimal)
            print(len(decimal))
            Fract = decimal[0:23] if len(decimal)>23 else decimal + [0 for i in range(23-len(decimal))]
            print(len(Fract))

        return "".join(list(map(lambda x : str(x), Sign+Exp+Fract)))

            

if __name__ == "__main__":
    
    t = Test_Generator()
    print(t.convert_num_to_vector(1.1005E-37))

