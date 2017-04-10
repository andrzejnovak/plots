# Dist def
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

import Plotting_Header
from Plotting_Header import *

class DIST:
	def __init__(self, name, File, Tree, weight, color):
		self.name = name
		self.File = File
		self.Tree = Tree
		self.weight = weight
		self.color = color
	def plot(self, VAR, BIN, MIN, MAX, CUT, TITLE, Norm):
		Hist = TH1F(self.name+"_"+VAR, "", BIN, MIN, MAX)
		Hist.GetXaxis().SetTitle(TITLE)
		quickplot(self.File, self.Tree, Hist, VAR, CUT, self.weight)
		Hist.SetLineColor(self.color)
		if Norm:
			Hist.Scale(1/Hist.Integral())
		return Hist
