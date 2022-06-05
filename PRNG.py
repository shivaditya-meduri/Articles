import matplotlib.pyplot as plt
from scipy.stats import norm, expon, chi2
import sys

def random_generator(n, seed=10):
    '''
    This function will generate random numbers
    between 0.0 and 1.0. The function uses the 
    seed value to generate a number and feeds the result back
    to the generator as the new seed. The function used to
    generate random numbers is (ax+b)mod(m) 
    '''
    rands = []
    for i in range(n):
        ## a = 16 & b=232
        rn = (16*seed + 232)%(10**9)
        seed = rn
        rands.append(rn/(10**9))
    return rands

def uniform_distribution(n, a, b, seed=10):
    '''
    Creates a sample of n elements following a 
    uniform distribution between bounds a and b
    '''
    return [(element*(b-a))+a for element in random_generator(n, seed)]

def normal_distribution(n, mean, std):
    '''
    This function returns a sample of n elements 
    following the normal distribution : N(mean, std)
    '''
    base = random_generator(n)
    return [norm.ppf(i, loc=mean, scale=std) for i in base]  

def exponential_distribution(n, loc, lam):
    '''
    Generates a sample of n elements following
    the distribution Exp(lam)
    '''
    sc = 1/lam ## Controls the rate of decay of the distribution
    base = random_generator(n)
    return [expon.ppf(i, loc=loc, scale=sc) for i in base]     

def chi2_distribution(n, df):
    '''
    Generates a sample of n elements following
    the distribution chi-squared distribution with df degrees of freedom
    '''
    base = random_generator(n)
    return [chi2.ppf(i, df=df) for i in base]     


if __name__ == "__main__":
    '''
    The Command line arguments that should be passed while running 
    this file depends on the distribution to be used.
    sample_size = 1000
    for normal:(mean = 100, std = 10)
        python PRNG.py 1000 normal 100 10
    for uniform:(lower_bound=10, upper_bound=10)
        python PRNG.py 1000 uniform 10 20
    for exponential: (loc=0, lamda=3)
        python PRNG.py 1000 exponential 0 3
    for chi-squared distribution: (degrees_freedom=6)
        python PRNG.py 1000 chi2 6
    The list of numbers generated are stored in a txt file sample.txt
    '''
    cla = sys.argv
    if len(cla) < 2:
        print("Please Enter the sample length, name of the distribution and the arguments as per the distribution")
    n_sample = int(cla[1])
    if cla[2].lower() == "normal":
        mean = float(cla[3])
        std = float(cla[4])
        sample = normal_distribution(n_sample, mean, std)
        plt.hist(sample, bins=100)
        plt.show()
    elif cla[2].lower() == "uniform":
        low_b = float(cla[3])
        upp_b = float(cla[4])
        sample = uniform_distribution(n_sample, low_b, upp_b)
        plt.hist(sample, bins=100)
        plt.show()
    elif cla[2].lower() == "exponential":
        loc = float(cla[3])
        lam = float(cla[4])
        sample = exponential_distribution(n_sample, loc, lam)
        plt.hist(sample, bins=100)
        plt.show()        
    elif cla[2].lower() == "chi2":
        df = int(cla[3])
        sample = chi2_distribution(n_sample, df)
        plt.hist(sample, bins=100)
        plt.show() 

    with open("sample.txt", 'w') as output:
        for row in sample:
            output.write(str(row) + '\n')

    print(f"Sample following a {cla[2]} distribution of size {cla[1]} is stored in a file sample.txt in the current working directory.")

