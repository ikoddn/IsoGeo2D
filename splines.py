import numpy as np
from scipy import interpolate

class Spline2D:
    '''
    coeffs - numpy array
    '''
    def __init__(self, degree, uKnots, vKnots, coeffs):
        self.coeffs = coeffs
        self.coeffElems = len(coeffs)
        self.uCoeffsLength = len(uKnots) - degree - 1
        self.vCoeffsLength = len(vKnots) - degree - 1
        self.tcks = []
        
        for i in range(self.coeffElems):
            self.tcks.append([uKnots, vKnots, coeffs[i], degree, degree])
    
    def __coeffsExtremum(self, coeffElem, f):
        coeffs = self.coeffs[coeffElem]
        extremum = coeffs[0]
        
        for i in range(1, len(coeffs)):
            extremum = f(extremum, coeffs[i])
            
        return extremum
        
    def coeffMin(self, coeffElem):
        return self.__coeffsExtremum(coeffElem, min)
    
    def coeffMax(self, coeffElem):
        return self.__coeffsExtremum(coeffElem, max)
        
    def evaluate(self, x, y):
        result = np.empty(self.coeffElems)
        
        for i in range(self.coeffElems):
            result[i] = interpolate.bisplev(x, y, self.tcks[i])
            
        return result
    
    def evaluatePartialDerivativeU(self, x, y):
        result = np.empty(self.coeffElems)
        
        for i in range(self.coeffElems):
            result[i] = interpolate.bisplev(x, y, self.tcks[i], dx=1)
            
        return result
        
    def evaluatePartialDerivativeV(self, x, y):
        result = np.empty(self.coeffElems)
        
        for i in range(self.coeffElems):
            result[i] = interpolate.bisplev(x, y, self.tcks[i], dy=1)
            
        return result

    def jacob(self, u, v):
        return np.matrix([self.evaluatePartialDerivativeU(u, v), 
                          self.evaluatePartialDerivativeV(u, v)]).transpose()

class Spline2DTrivialR1:
    def evaluate(self, x, y):
        return np.array([y])    
    
class Spline2DTrivialR2:
    def coeffMin(self, coeffElem):
        return 0.0
    
    def coeffMax(self, coeffElem):
        return 1.0
        
    def evaluate(self, x, y):
        return np.array([x, y])
    
    def evaluatePartialDerivativeU(self, x, y):
        return np.array([1.0, 0.0])
    
    def evaluatePartialDerivativeV(self, x, y):
        return np.array([0.0, 1.0])
    
    def jacob(self, u, v):
        return np.matrix([[1.0, 0.0], [0.0, 1.0]])