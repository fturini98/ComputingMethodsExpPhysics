"""
The ProbabilityDensityFunction is a class that use the method of slpline for
generate the PDF,CDF,PPF from some points of pdf described by their cordinates
x and y. The class have also methods for:
    -generate an array of value distributed like the pdf 
    -plot the graphs of PDF,CDF,PPf
    -Evaluate the probability that an event will be in a certai intervall
    -Return the value of PDF in a certain point
In this Script is also implemented the function PDF_from_function that create
a PDF object with a certain parametric function  used for generatng 
the x and y value of the array, this function must be passed by the owner.
"""
import sys
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from matplotlib import pyplot as plt


class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
    '''
    '''
    def __init__(self,x,y,function_name="Function",k=3,steps=101):
        self._function_name=function_name
        self.pdf=InterpolatedUnivariateSpline(x, y)
        self.range=np.linspace(np.amin(x), np.amax(x), steps)
        self._steps=steps
        InterpolatedUnivariateSpline.__init__(self, x, y) #inherit the function methods
        min_y=np.amin(y)
        error_y=min_y<(-1e-5)
        if error_y:#controll that the probability dosen't have a negative value
            print(f"THE PROBABILITY HAVE A NEGATIVE VALUE AND IT'IS {np.amin(y)}")
            sys.exit()
        print("ok,crash per k inserito sopra")
        self.ycdf = np.array([self.integral(x[0], xcdf) for xcdf in x])#caluclate the value
        # of yCDF for each value of x
        self.max_cdf_value=np.amax(self.ycdf)
        self._cdf = InterpolatedUnivariateSpline(x, self.ycdf)#create the attribute CDF(x)
        xppf, ippf = np.unique(self.ycdf, return_index=True)#Control that we pass only one
        #time the y to xppf(Percent-Point function)
        yppf = x[ippf]#pass only one time the value for single xppf
        self.ppf= InterpolatedUnivariateSpline(xppf, yppf)

    @property
    def cdf(self):
        controll_cdf_value=self.max_cdf_value-1.>1e-5
        if  controll_cdf_value:#controll the normalization of the array
            print(f"The function is not normalized, in the range the max value of cdf is {self.max_cdf_value} maybe you want to renormalize the function by it?")
            sys.exit()
        return self._cdf
        

    def  prob(self, x1, x2):
        """
        Return the probability for the random variable to be included
        between x1 and x2.
        """
        return self.cdf(x2) - self.cdf(x1)

    def rnd(self, size=1000):
        """
        Return an array of random variables distributed like the pdf, the number of bins are equal to size.
        """
        return self.ppf(np.random.uniform(size=size))
    def pd(self,x1):
        """
        return the value of pdf in the point x1
        """
        return self.pdf(x1)

    def Fig_pdf(self):
        """
        Show the distibution pdf
        """
        plt.figure('pdf')
        plt.title(self._function_name)
        plt.plot(self.range, self.pdf(self.range))
        plt.xlabel('x')
        plt.ylabel('pdf(x)')
        plt.show()

    def Fig_cdf(self):
        """
        Show the distibution cdf
        """
        plt.figure('cdf')
        plt.title(self._function_name)
        plt.plot(self.range, self.cdf(self.range))
        plt.xlabel('x')
        plt.ylabel('cdf(x)')
        plt.show()

    def Fig_ppf(self):
        """
        Show the distibution ppf
        """
        plt.figure('ppf')
        plt.title(self._function_name)
        q = np.linspace(0., 1.,self._steps)
        plt.plot(q, self.ppf(q))
        plt.xlabel('q')
        plt.ylabel('ppf(q)')
        plt.show()

def PDF_from_function(f,x_min,x_max,function_name="Function",N=1000,k=3,steps=101):

        """
        Parameters
        ----------
        f : function
           The base function, from that the function pdfClass generate
           a class of type PDF modelled over that function
        x_min : float
          The minimum of range of function f
        x_max : float
          The maximum of range of function f
        function_name: str,optional
          deffine the name of the custom function to insert
        N : int,optional
         Number of point passed to the class PDF for generating the pdf function.
         The default is 1000.
        k : int,optional
         Degree of the smoothing spline used inside the class PDF. Must be 1 <= k <= 5.
         The default is 3.
        steps : TYPE,optional
          Number of bins in the histograms with the shape of PDF.
          The default is 1000.

        Generate a class of type PDF from a determinate function if it is different from the uniform distribution
        """
        x=np.linspace(x_min,x_max,N)
        y=f(x)
        if np.amin(y)==np.amax(y):#the method used here dont'work for uniform distribution
           print("The spline method dont'work very well for costant distibution, consider to use np.random")
           sys.exit()
        else:
           return ProbabilityDensityFunction(x,y,function_name,k,steps)
