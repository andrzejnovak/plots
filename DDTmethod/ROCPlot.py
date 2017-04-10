import sys
from optparse import OptionParser
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from Plotting_Header import *
import numpy as np

parser = OptionParser()
parser.add_option("-d", "--dir", action="store", dest="pwd", default="/home/storage/andrzejnovak/80Trees/", help="directory where files are")
parser.add_option("-s", "--stacked", action="store_true", dest="stack", default=False, help="stack distributions",)
parser.add_option("-n", "--normed", action="store_true", dest="norm", default=False, help="Normalize distributions to 1",)
parser.add_option("-v", "--variables", action="store", dest="vars", default=["ZPRIMEM"], help="[LepPt,METPt, TAGPt, TPRIMEM, WPt, lepJetPt, TRPIMEM, ZPRIMEM]")
parser.add_option("--all", action="store_true", dest="all", default=False, help="[LepPt,METPt, TAGPt, TPRIMEM, WPt, lepJetPt, TRPIMEM, ZPRIMEM]")
(options, args) = parser.parse_args()
if options.all == True: options.vars = ["LepPt", "METPt", "TAGPt", "WPt", "lepJetPt", "TPRIMEM", "ZPRIMEM"]

def varplot(varname, xmin=None, xmax=None, pwd="/home/storage/andrzejnovak/March/", cut= "(LepPt<50.)", normed=False, stacked=False):
	if xmax is None:
		tosize = TFile("root://cmsxrootd.fnal.gov/"+pwd+"SM.root")
		xmax, xmin = tosize.Get("tree_T1").GetMaximum(varname)*0.4, tosize.Get("tree_T1").GetMinimum(varname)

	VAR = [varname, 50, xmin, xmax]
	YT = "events / "+str((VAR[3]-VAR[2])/VAR[1])+" GeV"
	XT = varname+" (GeV)"
	H = "Type 1 (e) control region"
	Cut = cut
	treename="tree_T1"

	lumi = str(12700)

	W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
	W.SetLineColor(kGreen-6)
	W.SetLineWidth(2)
	quickplot(pwd+"WJetsToQQ.root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")
	#for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
	for w in ["200To400", "400To600", "600To800"]:
		quickplot(pwd+"WJetsToLNu_HT-"+w+".root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")

	TT = TH1F("TT", "", VAR[1], VAR[2], VAR[3])
	TT.SetLineColor(kRed-4)
	TT.SetLineWidth(2)
	quickplot(pwd+"TT.root", treename,TT, VAR[0], Cut, "("+lumi+"*weight)")
	
	ntt = TT.Integral()
	nw = W.Integral()

	return nw, ntt

window = "TAGM<220&TAGM>110"
n = 100

xs, cuts = [], []
for i in range(n):
	c = window + "&TAGTau32<"
	taucut = float(i+1)/n
	cuts.append(c+str(taucut))
	xs.append(taucut)

wint, ttint = [], []
for cut in cuts:
	a, b = varplot("TAGM", pwd=options.pwd,cut =cut, stacked=options.stack, normed=options.norm)
	wint.append(a)
	ttint.append(b)
	print cut

wtot, tttot = varplot("TAGM", pwd=options.pwd, cut="TAGM<220&TAGM>110", stacked=options.stack, normed=options.norm)
w =  np.array(wint)/wtot
tt = np.array(ttint)/tttot

W, TT = [], []
for a,b in zip(w,tt):
	print a, b
	if a == 0 or b == 0: continue
	else:
		W.append(a)
		TT.append(b)	

print "W", len(w), len(W)
print "TT", len(tt), len(TT)
W, TT = np.array(W), np.array(TT)

x = array("d", xs) 
y = array("d", TT/W)
#y = array("d", tt) 
#x = array("d", w)

C = TCanvas("C", "", 800, 800)
C.cd()		
#C.SetLogy()
#C.SetLogx()
P = TGraph(len(x),x,y)
P.SetMarkerStyle(20)
P.SetTitle("ROC")
#P.SetTitle("Ratios")
P.GetXaxis().SetTitle("TAGTau32<")
P.GetYaxis().SetTitle("R_{TT}/R_{W}")
#P.GetXaxis().SetTitle("R_{W}")
#P.GetYaxis().SetTitle("R_{tt}")
P.Draw("Ap+")

CMSLABL = TLatex()
CMSLABL.SetNDC()
CMSLABL.SetTextSize(0.035)
CMSLABL.DrawLatex(0.135,0.85,"CMS Preliminary")

C.SaveAs("outputs/ROC_someW.png")



