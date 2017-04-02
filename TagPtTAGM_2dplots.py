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

def varplot(varname, xmin, xmax, cut= "(LepPt<50.)", normed=False, stacked=False):
	VAR = [varname, 50, xmin, xmax]
	YT = "events / "+str((VAR[3]-VAR[2])/VAR[1])+" GeV"
	YT = "TAGPt (Gev)"
	XT = "TAGM (GeV)"
	H = "Type 1 (e) control region"
	#Cut = "(LepMiniIso<0.1&LepTightness>2.9)"
	Cut = cut
	treename="tree_T1"

	lumi = str(12.700)

	Data = TH2F("DATA", "",  50, 50, 350, 50,  150, 1000)
	Data.Sumw2()
	Data.SetLineColor(1)
	Data.SetFillColor(0)
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	quick2dplot("/home/storage/andrzejnovak/March/SE.root", treename, Data, VAR[0], "TAGPt", Cut, "(1.0)")
	quick2dplot("/home/storage/andrzejnovak/March/SM.root", treename, Data, VAR[0], "TAGPt", Cut, "(1.0)")

	Data.SetStats(0)
	if stacked==True:
		Data.SetTitle("Stacked plot")
	elif normed==True:
		Data.SetTitle("Normed plot")
	else: Data.SetTitle("Correct weights")
	Data.GetXaxis().SetTitle(XT)
	Data.GetYaxis().SetTitle(YT)
	Data.GetXaxis().SetTitleOffset(1.06)
	Data.GetYaxis().SetTitleOffset(1.06)

	leg = TLegend(0.6,0.8,0.89,0.89)
	leg.SetHeader(H)
	leg.SetFillColor(0)
	leg.SetLineColor(0)
	leg.AddEntry(Data, "Data (12.7 fb^{-1})", "PL")
		
	CMSLABL = TLatex()
	CMSLABL.SetNDC()
	CMSLABL.SetTextSize(0.035)

	THILABL = TLatex()
	THILABL.SetNDC()
	THILABL.SetTextSize(0.04)

	CUTLABL = TLatex()
	CUTLABL.SetNDC()
	CUTLABL.SetTextSize(0.02)
	
	C = TCanvas("C", "", 1800, 1200)
	plot = TPad("pad1", "The pad 80% of the height",0,0,1,1)
	plot.Draw()
	plot.cd()
	Data.Draw("COLZ")	
	leg.Draw("same")
	CMSLABL.DrawLatex(0.135,0.85,"CMS Preliminary")
	CUTLABL.DrawLatex(0.335, 0.12,Cut)
	THILABL.DrawLatex(0.71,0.91,"#bf{12.7 fb^{-1}}, #bf{s = #sqrt{13} TeV}")
	
	C.SaveAs("2D"+varname+"_"+Cut[-20:-1]+".png")

#
clist = ["LepTightness<1","LepPt>50", "lepJetPt>100", "METPt>50", "TAGPt>200", "lepJetCSV<0.46" ]
cuts = []
for i in range(1,len(clist)+1):
	c = ""
	for j in range(i):
		c += clist[j]
		if j != i-1: c += "&"
	cuts.append(c)
	print c

for cut in cuts:
	#for varname, xmin, xmax in zip(["LepPt","METPt", "TAGPt", "TPRIMEM", "WPt", "lepJetPt","ZPRIMEM"],[50,0,0,0,0,0,200],[500,900,1400,1800,1200,1000,3000]):
		#varplot(varname, xmin, xmax, cut =cut)
	varplot("TAGM", 0, 500, cut =cut)




