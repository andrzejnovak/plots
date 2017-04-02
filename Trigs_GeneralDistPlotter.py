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

def varplot(varname, xmin, xmax, trigger="3", normed=False, stacked=False):
	VAR = [varname, 50, xmin, xmax]
	YT = "events / "+str((VAR[3]-VAR[2])/VAR[1])+" GeV"
	#YT = "events"
	XT = varname+" (GeV)"
	H = "Type 1 (e) control region"
	Cut = "(LepMiniIso<0.1&LepTightness>2.9)"
	treename="tree_T1"

	lumi = str(12700)

	Data = TH1F("DATA", "", VAR[1], VAR[2], VAR[3])
	Data.Sumw2()
	Data.SetLineColor(1)
	Data.SetFillColor(0)
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	quickplot("/home/storage/andrzejnovak/data/SE_Trigger"+trigger+".root", treename, Data, VAR[0], Cut, "(1.0)")
	quickplot("/home/storage/andrzejnovak/data/SM_Trigger"+trigger+".root", treename, Data, VAR[0], Cut, "(1.0)")

	W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
	W.SetLineColor(kGreen-6)
	W.SetLineWidth(2)
	quickplot("/home/storage/andrzejnovak/T"+trigger+"/WJetsToQQ.root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")
	for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
		quickplot("/home/storage/andrzejnovak/T"+trigger+"/WJetsToLNu_HT-"+w+".root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")


	QCD = TH1F("QCD", "", VAR[1], VAR[2], VAR[3])
	QCD.SetLineColor(kYellow)
	QCD.SetLineWidth(2)
	for q in ["300to500", "500to700", "700to1000", "1000to1500", "1500to2000", "2000toInf"]:
		quickplot("/home/storage/andrzejnovak/T"+trigger+"/QCD_HT"+q+".root", treename, QCD, VAR[0], Cut, "("+lumi+"*weight)")

	TT = TH1F("TT", "", VAR[1], VAR[2], VAR[3])
	TT.SetLineColor(kRed-4)
	TT.SetLineWidth(2)
	quickplot("/home/storage/andrzejnovak/T"+trigger+"/TT.root", treename,TT, VAR[0], Cut, "("+lumi+"*weight)")

	ST = TH1F("ST", "", VAR[1], VAR[2], VAR[3])
	ST.SetLineColor(kBlue)
	for s in ["ST_s", "ST_t", "ST_at", "ST_tW", "ST_atW"]:
		quickplot("/home/storage/andrzejnovak/T"+trigger+"/"+s+".root", treename, ST, VAR[0], Cut, "("+lumi+"*weight)")
	
	sig1 =  TH1F("sig1", "", VAR[1], VAR[2], VAR[3])
	sig1.SetLineColor(kMagenta-9)
	sig1.SetLineWidth(2)
	sig1.SetLineStyle(2)
	quickplot("/home/storage/andrzejnovak/signal/ZprimeToTprimeT_TprimeToWB_MZp-1500Nar_MTp-900Nar_LH_Tune_T"+trigger+".root", treename, sig1, VAR[0], Cut, "("+lumi+"*"+str(1./50000.)+")")
	sig2 =  TH1F("sig2", "", VAR[1], VAR[2], VAR[3])
	sig2.SetLineColor(kCyan-7)
	sig2.SetLineWidth(2)
	sig2.SetLineStyle(2)
	quickplot("/home/storage/andrzejnovak/signal/ZprimeToTprimeT_TprimeToWB_MZp-2000Nar_MTp-1200Nar_LH_Tune_T"+trigger+".root", treename, sig2, VAR[0], Cut, "("+lumi+"*"+str(1./50000.)+")")
	sig3 =  TH1F("sig3", "", VAR[1], VAR[2], VAR[3])
	sig3.SetLineColor(kViolet)
	sig3.SetLineWidth(2)
	sig3.SetLineStyle(2)
	quickplot("/home/storage/andrzejnovak/signal/ZprimeToTprimeT_TprimeToWB_MZp-2500Nar_MTp-1500Nar_LH_Tune_T"+trigger+".root", treename , sig3, VAR[0], Cut, "("+lumi+"*"+str(1./50000.)+")")

	if stacked==True:
		for i in [QCD, TT, ST]:
			W.Add(i,1.)
		for j in [TT, ST]:
			QCD.Add(j,1.)
		for k in [ST]:
			TT.Add(k,1.)
	
	if normed==True:
		for histo in ["Data", "QCD", "W", "TT", "sig1", "sig2", "sig3"]:
			eval(histo+".Scale(1./"+histo+".Integral())")

	FindAndSetMax([Data, W, QCD, TT])
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

	leg = TLegend(0.6,0.6,0.89,0.89)
	leg.SetHeader(H)
	leg.SetFillColor(0)
	leg.SetLineColor(0)
	leg.AddEntry(Data, "Data (12.7 fb^{-1})", "PL")
	leg.AddEntry(W, "W+Jets, W#rightarrow l#nu", "F")
	leg.AddEntry(QCD, "QCD", "F")
	leg.AddEntry(TT, "t#bar{t}", "F")
	leg.AddEntry(ST, "Single top", "F")
	leg.AddEntry(sig1, "Z'_{1500}#rightarrow tT'_{900}", "L")
	leg.AddEntry(sig2, "Z'_{2000}#rightarrow tT'_{1200}", "L")
	leg.AddEntry(sig3, "Z'_{2500}#rightarrow tT'_{1500}", "L")

	
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
	Data.Draw()	
	W.Draw("same")
	QCD.Draw("same")
	TT.Draw("same")
	ST.Draw("same")
	sig1.Draw("same")
	sig2.Draw("same")
	sig3.Draw("same")
	leg.Draw("same")
	CMSLABL.DrawLatex(0.135,0.85,"CMS Preliminary")
	CUTLABL.DrawLatex(0.135,0.80,Cut)
	THILABL.DrawLatex(0.71,0.91,"#bf{12.7 fb^{-1}}, #bf{s = #sqrt{13} TeV}")
	
	C.SaveAs("T"+trigger+"_"+varname+"_"+Cut[-15:-2]+".png")

#for num in ["1","2","3", "4", "5", "6", "7", "9", "10", "11"]:	
for num in ["1","3", "4", "5", "6", "7", "9"]:	
	for varname, xmin, xmax in zip(["LepPt","METPt", "TAGPt", "TPRIMEM", "WPt", "lepJetPt","ZPRIMEM"],[50,0,0,0,0,0,200],[500,900,1400,1800,1200,1000,3000]):
		varplot(varname, xmin, xmax, trigger=num, stacked=True)





