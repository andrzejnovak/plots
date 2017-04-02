#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

# Our functions:
import Plotting_Header
from Plotting_Header import *

def make_signal_point(name, cut, sig, VAR):
	S = TH1F(name[0]+"__"+name[1], "", VAR[1], VAR[2], VAR[3])
	quickplot(sig.File, sig.Tree, S, VAR[0], cut, sig.weight)
	return S
