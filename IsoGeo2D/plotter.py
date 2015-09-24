import itertools
import numpy as np
import pylab as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

class Plotter:
	def __init__(self, splineInterval, numPixels):
		self.splineInterval = splineInterval
		self.precision = 100
		
		plt.figure(figsize=(12, 12))
		gridSpec = GridSpec(3, 2, height_ratios=[7, 5, 1])
		self.gridSpec = gridSpec
		
		ax = plt.subplot(gridSpec[0, 0])
		ax.axis((-0.6, 1.1, -0.1, 1.1))
		self.gPlot = ax
		
		ax = plt.subplot(gridSpec[0, 1])
		ax.axis((-0.1, 1.1, -0.1, 1.1))
		self.pPlot = ax
		
		ax = plt.subplot(gridSpec[1:3, 0])
		ax.axis((-0.6, 1.1, -0.1, 1.1))
		self.samplingPlot = ax
		
		ax = plt.subplot(gridSpec[1, 1])
		ax.axis((-0.5, numPixels-0.5, 0, 1))
		ax.set_xticks(np.arange(numPixels))
		self.pixelComponentsPlot = ax
		
		ax = plt.subplot(gridSpec[2, 1])
		ax.axis((-0.5, numPixels-0.5, 0, 1))
		ax.set_xticks(np.arange(numPixels))
		ax.yaxis.set_major_locator(plt.NullLocator()) # Removes ticks
		self.pixelPlot = ax
		
		plt.ion()
		plt.show()

	def generatePoints(self, f, xInputs, yInputs):
		xOutput = []
		yOutput = []
		
		for i in range(len(xInputs)):
			fResult = f(xInputs[i], yInputs[i])
			xOutput.append(fResult[0])
			yOutput.append(fResult[1])
		
		return [xOutput, yOutput]
	
	def generatePoints1(self, f, params):
		output = np.empty((len(params), 2))
		
		for i, param in enumerate(params):
			output[i] = f(param)
		
		return output
		
	def plotGrids(self, f, m, n):
		interval = self.splineInterval
		vLines = np.linspace(interval[0], interval[1], m)
		hLines = np.linspace(interval[0], interval[1], n)
		lineColor = '0.5'
		
		for vLine in vLines:
			paramsX = [vLine] * self.precision
			paramsY = np.linspace(interval[0], interval[1], self.precision)
			
			[geomX, geomY] = self.generatePoints(f, paramsX, paramsY)
			
			ax = self.gPlot
			ax.plot(geomX, geomY, color=lineColor)
			
			ax = self.pPlot
			ax.plot(paramsX, paramsY, color=lineColor)
			
		for hLine in hLines:
			paramsX = np.linspace(interval[0], interval[1], self.precision)
			paramsY = [hLine] * self.precision
			
			[geomX, geomY] = self.generatePoints(f, paramsX, paramsY)
			
			ax = self.gPlot
			ax.plot(geomX, geomY, color=lineColor)
			
			ax = self.pPlot
			ax.plot(paramsX, paramsY, color=lineColor)
		
	def plotScalarField(self, rho, transfer):
		interval = self.splineInterval
		uRange = np.linspace(interval[0], interval[1], self.precision)
		vRange = np.linspace(interval[1], interval[0], self.precision)
		
		img = []
		
		for v in vRange:
			row = []
			
			for u in uRange:
				x = rho.evaluate(u,v)
				row.append(transfer(x[0]))
		
			img.append(row)
		
		ax = self.pPlot
		ax.imshow(img, aspect='auto', extent=(interval[0], interval[1], interval[0], interval[1]))
	
	def plotLine(self, f, interval):
		params = np.linspace(interval[0], interval[1], self.precision)
		points = self.generatePoints1(f, params)
		
		ax = self.gPlot
		ax.plot(points[:,0], points[:,1], color='k')
	
	def plotIntersectionPoints(self, points):
		ax = self.gPlot
		
		for point in points:
			ax.plot(point[0], point[1], marker='o', color='b')

	def plotGeomPoints(self, points, colors):
		ax = self.gPlot
		
		for point, c in itertools.izip(points, colors):
			ax.plot(point[0], point[1], marker='.', color=tuple(c))
			
	def plotParamPoints(self, points):
		ax = self.pPlot
		
		for point in points:
			ax.plot(point[0], point[1], marker='x', color='k')
			
	def plotPixelPoints(self, pixels):
		ax = self.gPlot
		
		for i, pixel in enumerate(pixels):
			ax.text(pixel[0], pixel[1], str(i))
		
	def plotPixelColors(self, pixels, pixelColors):
		ax = self.pixelComponentsPlot
		indexes = np.arange(len(pixels))
		
		ax.plot(indexes, pixelColors[:,0], marker='o', color='#ff0000')
		ax.plot(indexes, pixelColors[:,1], marker='o', color='#00ff00')
		ax.plot(indexes, pixelColors[:,2], marker='o', color='#0000ff')		
		
		ax = self.pixelPlot
		
		for i, pixelColor in enumerate(pixelColors):
			r = Rectangle((i-.5, 0), 1, 1, facecolor=tuple(pixelColor))
			ax.add_patch(r)
		
	def draw(self):
		plt.draw()
