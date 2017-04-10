#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

# Our functions:
import Alphabet_Header
from Alphabet_Header import *
import Alphabet
from Alphabet import *
import Plotting_Header
from Plotting_Header import *
import Converters
from Converters import *
import Distribution_Header
from Distribution_Header import *


V = "20"
lumi = str(12.7)

def checkplot(varname="TAGM", xmin=110, xmax=230, savedir="", cut=""):
	Pres =  "TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV>0.46" + cut
	PASSs = Pres + "&Tau32DDT_Sig<0." 
	FAILs= Pres + "&Tau32DDT_Sig>0."
	NonResPasss = TH1F("NRP", "", 36, xmin,xmax)
	NonResFails = TH1F("NRF", "", 36, xmin,xmax)

	Preb =  "TAGM<250&TAGM>50&TAGPt>380&TAGPt<1000&lepJetCSV<0.46" + cut
	PASSb = Preb + "&Tau32DDT_Bkg<0." 
	FAILb = Preb + "&Tau32DDT_Bkg>0."
	NonResPassb = TH1F("NRP", "", 36, xmin,xmax)
	NonResFailb = TH1F("NRF", "", 36, xmin,xmax)

	FAIL_Result = Pres + "&Tau32DDT_Bkg>0."
	NonResFailResult = TH1F("NRF", "", 36, xmin, xmax)

	N_FAILs=  Pres + "&nTau32DDT_Sig>0."
	N_NonResFails = TH1F("NRF", "", 36, xmin,xmax)

	N_FAIL_Result = Pres + "&nTau32DDT_Bkg>0."
	N_NonResFailResult = TH1F("NRP", "", 36, xmin,xmax)

	for w in ["LNu_HT-100To200", "LNu_HT-200To400" ,"LNu_HT-400To600", "LNu_HT-600To800", "LNu_HT-800To1200", "LNu_HT-1200To2500", "LNu_HT-2500ToInf", "QQ"]:
		try:
			print "TRY"
			D = DIST("D", savedir + "/WJetsTo"+w+".root", "tree_T1", "("+lumi+"*weight)", 9)
			NonResPasss.Add(D.plot(varname, 36, xmin,xmax, PASSs, D.name+"NRP", False))  # DATA in signal region
			NonResFails.Add(D.plot(varname, 36, xmin,xmax, FAILs, D.name+"NRF", False))  # Estimate signal Region , Signal DDT
			NonResPassb.Add(D.plot(varname, 36, xmin,xmax, PASSb, D.name+"NRP", False))  # DATA sideband, nonplotted
			NonResFailb.Add(D.plot(varname, 36, xmin,xmax, FAILb, D.name+"NRF", False))  # Estiamte sideband region, nonplotted

			NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, FAIL_Result, D.name+"NRF", False)) #Estiamte signal Region, Sideband DDT

			# new DDT
			N_NonResFails.Add(D.plot(varname, 36, xmin,xmax, N_FAILs, D.name+"NRF", False))  # Estimate signal Region , Signal DDT
			N_NonResFailResult.Add(D.plot(varname, 36,  xmin,xmax, N_FAIL_Result, D.name+"NRF", False)) #Estiamte signal Region, Sideband DDT
		except: print "BAD FILE", w
	NonResFails.Scale(float(V)/(100.-float(V)))
	NonResFailb.Scale(float(V)/(100.-float(V)))
	NonResFailResult.Scale(float(V)/(100.-float(V)))
	N_NonResFails.Scale(float(V)/(100.-float(V)))
	N_NonResFailResult.Scale(float(V)/(100.-float(V)))



	FindAndSetMax([NonResPasss, NonResFails, NonResFailResult], 1.5)

	leg = TLegend(0.5,0.65,0.89,0.89)
	leg.SetHeader("Wjets (DDT~"+V+"%):")
	#leg.AddEntry(NonResPasss, "Signal events T_{32}^{DDT} < 0", "PL")
	#leg.AddEntry(NonResFails, "Signal estimate #frac{"+V+"}{"+str(int(100-int(V)))+"} #times events Tau_{32}^{DDT} > 0", "L")
	leg.AddEntry(NonResPasss, "Signal events", "PL")
	leg.AddEntry(NonResFails, "Signal estimate (full map)", "L")
	#leg.AddEntry(NonResPassb, "Bkg events T_{32}^{DDT} < 0", "PL")
	#leg.AddEntry(NonResFailb, "Bkg #frac{"+V+"}{"+str(int(100-int(V)))+"} #times events Tau_{32}^{DDT} > 0", "L")
	leg.AddEntry(NonResFailResult, "Signal estimate from background (full map)", "L")
	
	leg.AddEntry(N_NonResFails, "Signal estimate (matched cut map)", "L")
	leg.AddEntry(N_NonResFailResult, "Signal estimate from background (matched cut map)", "L")

	leg.SetLineColor(0)
	leg.SetFillColor(0)

	NonResPasss.Sumw2()
	NonResPasss.SetLineStyle(1)
	NonResPasss.SetLineColor(1)
	NonResPasss.SetFillColor(1)
	NonResPasss.SetMarkerColor(1)
	NonResPasss.SetMarkerStyle(20)

	NonResPassb.Sumw2()
	NonResPassb.SetLineStyle(1)
	NonResPassb.SetLineColor(1)
	NonResPassb.SetFillColor(1)
	NonResPassb.SetMarkerColor(1)
	NonResPassb.SetMarkerStyle(20)

	NonResFails.SetStats(0)
	NonResFails.SetLineColor(kBlue)
	NonResFails.SetLineStyle(2)
	NonResFails.SetLineWidth(2)

	NonResFailb.SetStats(0)
	NonResFailb.SetLineColor(kRed)
	NonResFailb.SetLineWidth(2)

	NonResFailResult.SetStats(0)
	NonResFailResult.SetLineColor(kCyan)
	NonResFailResult.SetLineStyle(3)
	NonResFailResult.SetLineWidth(2)

	N_NonResFails.SetStats(0)
	N_NonResFails.SetLineColor(kRed)
	N_NonResFails.SetLineStyle(2)
	N_NonResFails.SetLineWidth(2)

	N_NonResFailResult.SetStats(0)
	N_NonResFailResult.SetLineColor(kMagenta)
	N_NonResFailResult.SetLineStyle(3)
	N_NonResFailResult.SetLineWidth(2)

	NonResFails.GetXaxis().SetTitle(varname+" [GeV]")
	NonResFails.GetYaxis().SetTitle("Events")
	NonResFails.GetXaxis().SetTitleSize(0.045)
	NonResFails.GetYaxis().SetTitleSize(0.045)


	C = TCanvas("C", "", 800, 600)
	C.cd()
	CMSLABL = TLatex()
	CMSLABL.SetNDC()
	CMSLABL.SetTextSize(0.045)
	PRELABL = TLatex()
	PRELABL.SetNDC()
	PRELABL.SetTextSize(0.04)
	THILABL = TLatex()
	THILABL.SetNDC()
	THILABL.SetTextSize(0.045)
	CUTLABL = TLatex()
	CUTLABL.SetNDC()
	CUTLABL.SetTextSize(0.02)
	NonResFails.Draw("hist")
	NonResPasss.Draw("E0 same")
	#NonResFailb.Draw("same")
	#NonResPassb.Draw("E0 same")
	NonResFailResult.Draw("same")

	N_NonResFails.Draw("same")
	N_NonResFailResult.Draw("same")
	leg.Draw("same")
	CMSLABL.DrawLatex(0.1465,0.85,"CMS")
	THILABL.DrawLatex(0.81,0.91,"#bf{13 TeV}")
	PRELABL.DrawLatex(0.1465,0.812,"#bf{#it{Simulation Preliminary}}")
	CUTLABL.DrawLatex(0.1465,0.780,cut)

	C.SaveAs(savedir+varname+".png")

def allvarcheck(save, cut=""):
	checkplot("TAGM", xmin=50, xmax=250, savedir=save, cut=cut)
	checkplot("TAGPt", xmin=380, xmax=1000, savedir=save, cut=cut)
	checkplot("TPRIMEM", xmin=100, xmax=3000, savedir=save, cut=cut)
	checkplot("ZPRIMEM", xmin=100, xmax=3000, savedir=save, cut=cut)

clist = ["LepPt<400", "LepTightness>2.9", "WPt>500"]
for i, c in enumerate(clist):
	save = "C" + str(i)
	cut = "&"+c
	allvarcheck(save, cut=cut)
