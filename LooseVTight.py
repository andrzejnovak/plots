#

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
import Plotting_Header
from Plotting_Header import *

W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
W.SetFillColor(kGreen-6)
for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
	quickplot("/home/bjr/trees_round_five/WJetsToLNu_HT-"+w+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", W, VAR[0], Cut, "("+lumi+"*weight)")


