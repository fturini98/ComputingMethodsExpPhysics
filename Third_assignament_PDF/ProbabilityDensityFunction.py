'''
The ProbabilityDensityFunction is a module that use the methods of slpline class
for generate the PDF,CDF,PPF from some campioned points of a certain pdf.
In this module there is a calas and a function that works togheter for make this
job.
'''
import sys
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from matplotlib import pyplot as plt


class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
    
    ''' 
    The **ProbabilityDensityFunction** is a class that use the method of mother class
    spline for evaluate:
    
     * *Probability Density Function*
 
     * *Comulative Density Function*

     * *Percent Point Function*
 
    from a series of campioned points of a certain PDF passed like two arrays of x and
    y cordinates.
    The class have also a serie of checks that in case are not passed the
    program is interrupted:

     * Check the max CDF value, if is greater than 1 with a
       incertain of 1e-5, the program is interrupted
 
     * Check if the value of PDF is lesser than 0 with a incertain of 1e-5, in
       this case the program is interrupted

    Properties
    ----------

    _function_name: str, optional, private
       Is the name that the user could attribute to the function, it will show in
       the graphs
   
    pdf: scipy.interpolate.InterpolatedUnivariateSpline
         The PDF evalueted over the input points

    cdf: scipy.interpolate.InterpolatedUnivariateSpline
         The CDF evalueted over the input points

    ppf: scipy.interpolate.InterpolatedUnivariateSpline
         The PPF evalueted over the input points

    range: array
         An array that describes the range in which the function is define, it had
         a number of entries equal to the input parameter *steps*

    _steps: int, private
         The number of bins over which are drawn the probability functions(PDF,CDF,PPF)

    ycdf: float_array
         The array of values of CDF

    max_cdf: float
         The max value of CDF

    
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
        The *PDF_from_function* is a function that takes the following parameters
        for arguments and return a
        **ProbabilityDensitiyFunction.ProbabilityDensityFunction** create over an
        array of points distributed like the function f.
        The function f works like a PDF far all the distributions exludig the uniform distribution,
        in that case is suggest to use the function of numpy.random.uniform.
        
        Parameters
        ----------

        f: function
           The base function, from that the function pdfClass generate
           a class of type PDF modelled over that function
        x_min: float
          The minimum of range of function f
        x_max: float
          The maximum of range of function f
        function_name: str, optional
          deffine the name of the custom function to insert
        N: int, optional
         Number of point passed to the class PDF for generating the pdf function.
         The default is 1000.
        k: int, optional
         Degree of the smoothing spline used inside the class PDF. Must be 1 <= k <= 5.
         The default is 3.
        steps: int, optional
          Number of bins in the histograms with the shape of PDF.
          The default is 1000.

        Returns
        -------
        
        ProbabilityDensityFunction: **ProbabilityDensityFunction**
          The **PDF** class that have the properties distributed in accord to the PDF==>f
        """
        x=np.linspace(x_min,x_max,N)
        y=f(x)
        if np.amin(y)==np.amax(y):#the method used here dont'work for uniform distribution
           print("The spline method dont'work very well for costant distibution, consider to use np.random")
           sys.exit()
        else:
           return ProbabilityDensityFunction(x,y,function_name,k,steps)
