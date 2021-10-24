'''
The tests of the module ProbabilityDensityFunction controll the following things:
 * 
'''

import sys
import unittest

sys.path.append('../') #use to redirect the path for import my modulue
#in a different directory
from ProbabilityDensityFunction import *

class testPDF(unittest.TestCase):
    '''
    Unit test for the ProbabilityDensityFunction module
    '''
    def _test_class_PDF_cos_squered_base(self,x_min,x_max):
        '''
        test the class ProbabilityDensityFunction wiyh a squered cos(x)
        '''
        x=np.linspace(x_min,x_max,200)
        normalization=(1/2)*(-x_min-np.sin(x_min)*np.cos(x_min)+x_max+np.sin(x_max)*np.cos(x_max))
        y=(np.cos(x)**2)/normalization
        
        pdf= ProbabilityDensityFunction(x, y)
        
        norm=pdf.integral(x_min, x_max)#ceck thath the normalization of pdf is 1
        self.assertAlmostEqual(norm,1.,places=5)
        
        delta=abs(pdf.pdf(x)-y)#ceck if the pdf is well evalueted
        self.assertTrue((delta<1e-5).all())
        
        '''
        rnd_array=pdf.rnd(100000)
        plt.figure()
        n, bins, patches = plt.hist(rnd_array,bins=200, density=True)
        n_norm=n*(bins[1]-bins[0])
        sum_n=np.sum(n*(bins[1]-bins[0]))
        print(len(n), len(bins))
        sum_y=np.sum(y)
        diff_sum=abs(sum_n-sum_y)
        self.assertTrue(abs(n_norm-y).all()<1e-1)
        '''
        
        
    def test_class_PDF_(self):
        '''
        Test whith some value of x_min x_max the class pdf
        '''
        self._test_class_PDF_cos_squered_base(0,np.pi)
        #self._test_class_PDF_cos_squered_base(-np.pi,np.pi)
        
if __name__=="__main__":
     unittest.main(exit=not sys.flags.interactive)