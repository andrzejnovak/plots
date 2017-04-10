#
import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import pdb

def ComputeDDT(name, point, nPtBins, nRhoBins, H):
	DDT = TH2F(name, "", nRhoBins, 50, 250	, nPtBins, 380, 1000)
	DDT.SetStats(0)
	nXb = H.GetXaxis().GetNbins()
	nYb = H.GetYaxis().GetNbins()
	for x in range(nXb):
		for y in range(nYb):
			proj = H.ProjectionZ("H3"+str(x)+str(y),x+1,x+1,y+1,y+1)
			print str(x+1) + "," + str(y+1) + ":    "+ str(proj.Integral())
			p = array('d', [point*0.01])
			q = array('d', [0.0]*len(p))
			proj.GetQuantiles(len(p), q, p)
			DDT.SetBinContent( x+1, y+1, q[0] )
	return DDT

def DisplayDDT(DDT, toretain, SaveName, cut=""):
	CMSLABL = TLatex()
	CMSLABL.SetNDC()	
	CMSLABL.SetTextSize(0.045)
	PRELABL = TLatex()
	PRELABL.SetNDC()
	PRELABL.SetTextSize(0.04)
	THILABL = TLatex()
	THILABL.SetNDC()
	THILABL.SetTextSize(0.035)
	CUTLABL = TLatex()
	CUTLABL.SetNDC()
	CUTLABL.SetTextSize(0.02)

	C = TCanvas("TempCanvas", "Title", 800, 600)
	plot = TPad("pad1", "The pad 80% of the height",0.02,0,0.95,1)
	plot.Draw()
	plot.cd()
	DDT.SetStats(0)
	DDT.GetXaxis().SetTitle("TAGM")
	DDT.GetXaxis().SetTitleSize(0.045)
	DDT.GetZaxis().SetTitle("TAGTau_{32}")
	DDT.GetZaxis().SetTitleSize(0.045)
	DDT.GetZaxis().SetRangeUser(0.5,0.75)
	DDT.SetTitle("DDT at "+str(toretain)+"% efficinecy")
	if SaveName.startswith("DDTdiff") == True: 
		DDT.GetZaxis().SetRangeUser(-0.1,0.1) 
		DDT.GetZaxis().SetTitle("#Delta TAGTau_{32}") 
		DDT.SetTitle("#Delta DDT at "+str(toretain)+"% efficinecy")
	DDT.GetYaxis().SetTitle("TAGp_{T}")
	DDT.GetYaxis().SetTitleSize(0.045)
	DDT.GetYaxis().SetTitleOffset(1.145)
	DDT.Draw("COLZ")
	CMSLABL.DrawLatex(0.1465,0.85,"CMS")
	THILABL.DrawLatex(0.81,0.91,"#bf{13 TeV}")
	PRELABL.DrawLatex(0.1465,0.812,"#bf{#it{Simulation Preliminary}}")
	CUTLABL.DrawLatex(0.1465,0.780,cut)

	C.Print("MAP_"+SaveName+".png")

def histo(Bkgs, cut="T.lepJetCSV<100"):
	H3 = TH3F("H3", "", 9, 50, 250, 12, 380, 1000, 500, 0, 1)
	H3.SetStats(0)
	for B in Bkgs:
		F = TFile(B)
		T = F.Get("tree_T1")
		n = T.GetEntries()
		for j in range(0, n): # Here is where we loop over all events.
			T.GetEntry(j)
			if T.TAGTau32 > 0.001:
				if eval(cut):
					weight = T.weight
					PT = T.TAGPt
					M = T.TAGM
					H3.Fill(M, PT, T.TAGTau32, weight)
	return H3

# Fetch samples
pwd = "/home/storage/andrzejnovak/March/"
Bkgs =[]
Bkgs.append(pwd+"WJetsToQQ.root")
for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
	Bkgs.append(pwd+"WJetsToLNu_HT-"+w+".root")

def study(cut,savename, toretain=20):
	#Set-up
	#toretain = toretain # Percentage to keep
	if cut != "": Tcut = "T."+cut+" and "   #Preselection cuts on data in pythonic form e.g. T.LepPt < 50 and ..
	else: Tcut = ""
	nbins1, nbins2 = 12, 9

	# Signal Region
	H3 = histo(Bkgs, cut=Tcut +"T.lepJetCSV >0.46")
	DDT_sr = ComputeDDT("DDT_sr", toretain, nbins1, nbins2, H3)
	DisplayDDT(DDT_sr, toretain, "DDT_SR"+cut, cut=cut)

	# Sidebands
	H3 =  histo(Bkgs, cut=Tcut +"T.lepJetCSV <0.46")
	DDT_br = ComputeDDT("DDT_sb", toretain, nbins1, nbins2, H3)
	DisplayDDT(DDT_sb, toretain, "DDT_SB"+cut, cut=cut)

	# Difference
	DisplayDDT(DDT_sr-DDT_sb, toretain, "DDTdiff"+cut, cut=cut)

	# Saving a file
	Fout = TFile(savename+".root", "recreate")
	Fout.cd()
	DDT_sr.Write()
	DDT_sb.Write()
	Fout.Close()

study("", "DDT")
clist = ["LepPt<400", "LepTightness>2.9", "WPt>500"]
for i, c in enumerate(clist):
	study(c, "DDT"+str(i))


