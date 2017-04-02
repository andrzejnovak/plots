import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy
import Plotting_Header
from Plotting_Header import *

import SignalPlotter
from SignalPlotter import *
import Distribution_Header
from Distribution_Header import *

# PUT A SIGNAL POINT IN!
ce2 = "(lepIsTight>0.&lepMiniIso<.1&(lepTopMass2>120&lepTopMass2<270)&(hadTopMass2>500)&lepPt>50&metPt>25&wPt>100.&leadJetCSV<1.0&(tagJetSDMass>70&tagJetSDMass<100&leadJetCSV>0.68&((leadJetPt+offJetPt+tagJetPt+wPt)>800)))"
ce2off = "(lepIsTight>0.&lepMiniIso<.1&(lepTopMass2>120&lepTopMass2<270)&(hadTopMass2>500)&lepPt>50&metPt>25&wPt>100.&leadJetCSV<1.0&(tagJetSDMass>70&tagJetSDMass<100&leadJetCSV<0.68&offJetCSV>0.68&((leadJetPt+offJetPt+tagJetPt+wPt)>800)))"
SSS = []
SSS.append(["2000","900","L"])
SSS.append(["2000","1200","R"])
SSS.append(["2000","1500","L"])
SSS.append(["1500","1200","L"])
SSS.append(["1500","700","L"])
SSS.append(["1500","900","L"])
SSS.append(["2500","1200","L"])
SSS.append(["2500","1500","L"])
for s in SSS:
	sig = DIST("sig", "/home/bjr/trees_round_four/ZprimeToTprimeT_TprimeToWB_MZp-"+s[0]+"Nar_MTp-"+s[1]+"Nar_"+s[2]+"H_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", "(1.0)")
	sm2 = make_signal_point(["sr", "sig"+s[0]+s[1]], ce2, sig, ["eventMass2", 26, 400., 3000.])
	sm2off = make_signal_point(["0ffsr", "0ffsig"+s[0]+s[1]], ce2off, sig, ["eventMass2", 26, 400., 3000.])
	print "----   Z'"+s[0]+" T'"+s[1]+"   ----"
	print str(sm2off.Integral()*100./sm2.Integral())+"% increase"
