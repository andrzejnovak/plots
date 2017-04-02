import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
import Plotting_Header
from Plotting_Header import *


files = [
	"ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.root",
	"ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.root",
	"ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root",
	"ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.root"
]

for i in files:
	print "Looking at file: " + i
	HIST = TH1F(i, i, 50, 0, 5000)
	cut = "lepMiniIso<0.1&lepIsTight>0.&lepPt>50&metPt>25&wPt>100.&(lepTopMass2>120&lepTopMass2<270)&(hadTopMass2>500)&((leadJetPt+offJetPt+tagJetPt+wPt)>800)"
	quickplot("../../bjr/trees_zprime_freeze/" + i, "tree", HIST, "eventMass", cut, "(weight)")
	print str(HIST.Integral())
