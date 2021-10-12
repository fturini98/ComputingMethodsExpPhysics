from ProbabilityDensityFunction import *

if __name__=="__main__":
    """
    checks if a file is imported as a module or not
    """
    def cos2_norm(x):
        return np.cos(x)**2*(2/np.pi)
    def linear(x):
        return (x)/5.
    def test(f,name="Function"):
        test=PDF_from_function(f, 0., np.pi,name)
        test.Fig_pdf()
        test.Fig_cdf()
        test.Fig_ppf()
        pd=test.pd(np.pi)
        prob=test.prob(0, np.pi)
        plt.figure('Sampling')
        plt.title(test._function_name)
        rnd = test.rnd(1000000)
        plt.hist(rnd, bins=200)        
        print(f"The density function at point PI is {pd}")
        print(f"The probability of find something between 0 and PI is {prob}")
        print(test._function_name)

    test(cos2_norm,"Cos squered")
    test(linear,"Linear")
     
