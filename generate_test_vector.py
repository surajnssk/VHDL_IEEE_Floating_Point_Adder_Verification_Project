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


    def convert_normalized_numb_to_vector(self, vector):
        pass 
    
    def convert_vector_to_denormalized_num(self, vector):

        Sig = -1 if vector[0] else 1
        Fract = '0.'+''.join(list(map( lambda x : str(x), vector[9:])))
        
        Fract = self.binary_to_real_number(Fract)

        sum = Sig*2**(-126)*Fract
        
        return sum

    def convert_denormalized_numb_to_vector(self, vector):
        pass 



if __name__ == "__main__":
    
    t = Test_Generator()
    r = [0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    print(t.convert_vector_to_denormalized_num(r))

