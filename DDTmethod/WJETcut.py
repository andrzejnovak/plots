import sys
from optparse import OptionParser
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from Plotting_Header import *
import numpy as np
import timeit

parser = OptionParser()
parser.add_option("-d", "--dir", action="store", dest="pwd", default="/home/storage/andrzejnovak/80Trees/", help="directory where files are")
parser.add_option("-s", "--stacked", action="store_true", dest="stack", default=False, help="stack distributions",)
parser.add_option("-n", "--normed", action="store_true", dest="norm", default=False, help="Normalize distributions to 1",)
parser.add_option("-v", "--variables", action="store", dest="vars", default=["ZPRIMEM"], help="[LepPt,METPt, TAGPt, TPRIMEM, WPt, lepJetPt, TRPIMEM, ZPRIMEM]")
parser.add_option("--all", action="store_true", dest="all", default=False, help="[LepPt,METPt, TAGPt, TPRIMEM, WPt, lepJetPt, TRPIMEM, ZPRIMEM]")
parser.add_option("-c", "--lepcut", action="store", dest="lepcut", default="", help="lep cut")
parser.add_option("--diff", action="store_true", dest="diff", default=False, help="difference",)
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

def rate(window):
	n = 50
	xs, cuts, rates = [], [], []
	for i in range(60,100,1):
		c = window + "&TAGTau32<"
		taucut = float(i)/100
		cuts.append(c+str(taucut))
		xs.append(taucut)

	wtot, tttot = varplot("TAGM", pwd=options.pwd, cut=window, stacked=options.stack, normed=options.norm)
	if wtot < 5: return float(0)
	for i, cut in enumerate(cuts):
		a, b = varplot("TAGM", pwd=options.pwd,cut =cut, stacked=options.stack, normed=options.norm)
		rate = a/wtot
		rates.append(rate)
		if rate > 0.3:
			print rate, xs[i]
			return wtot #xs[i]	

def matrix(lepcut=""):
	mbins = [[90,110],[110,130],[130,150],[150,170],[170,190],[190,210],[210,230],[230,300]]
	ptbins = [[380,430],[430,480],[480,530],[530,580],[580,630],[630,680],[680,730],[780,830],[830,880],[880,930],[930,980],[980,2000]]
	mbins = [[150,170],[170,190],[190,210],[210,230],[230,300]]
	ptbins = [[580,630],[630,680],[680,730],[780,830],[830,880],[880,930],[930,980],[980,2000]]

	m, pt, tau32 = [], [], []

	start_time = timeit.default_timer()
	for i,mbin in enumerate(mbins):
		window = lepcut+"TAGM>"+str(mbin[0])+"&TAGM<"+str(mbin[1])	
		for j, ptbin in enumerate(ptbins):
			newwindow = window + "&TAGPt>"+str(ptbin[0])+"&TAGPt<"+str(ptbin[1])
			print newwindow
			tau32.append(rate(newwindow))
			pt.append(ptbin[0])
			m.append(mbin[0])

			t = timeit.default_timer()
			perloop = (t-start_time)/((i+1)*(j+1))
			print perloop*(len(mbins)*len(ptbins)-(i+1)*(j+1))/60, "min left"
	return m, pt, tau32

def makeplot(lepcut=""):
	m, pt, tau32 = matrix(lepcut=lepcut)
	x = array("d", m) 
	y = array("d", pt)
	z = array("d", tau32)

	C = TCanvas("C", "", 800, 800)
	C.cd()		
	P = TGraph2D(len(m), x,y,z)

	P.SetTitle("Wjet 30\% threshold")
	#P.SetMarkerStyle(21)
	P.GetXaxis().SetTitle("TAGM")
	P.GetYaxis().SetTitle("TAGPt")
	P.GetZaxis().SetTitle("TagTau32 Cut")
	P.Draw("surf1")
	C.SaveAs("outputs/"+lepcut+"Wcount.png")	
	C.SaveAs("outputs/"+lepcut+"Wcount.root")

def makediff():
	m, pt, tau32_1 = matrix(lepcut="LepType>0&")
	x = array("d", m) 
	y = array("d", pt)	
	m, pt, tau32_2 = matrix(lepcut="LepType<0&")
	z = array("d", np.array(tau32_1)-np.array(tau32_2))

	C = TCanvas("C", "", 800, 800)
	C.cd()		
	P = TGraph2D(len(m), x,y,z)

	P.SetTitle("Wjet 30\% threshold")
	#P.SetMarkerStyle(21)
	P.GetXaxis().SetTitle("TAGM")
	P.GetYaxis().SetTitle("TAGPt")
	P.GetZaxis().SetTitle("TagTau32 Cut")
	P.Draw("surf1")
	C.SaveAs("outputs/"+"ElMUDiff"+"Wcut.png")		
	C.SaveAs("outputs/"+"ElMUDiff"+"Wcut.root")

if options.diff == True:
	makediff()
else:
	makeplot(options.lepcut)




		

		



