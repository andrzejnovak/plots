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

def cutcount(varname):
	VAR = [varname, 50, 0, 100	]
	YT = "events / "+str((VAR[3]-VAR[2])/VAR[1])+" GeV"
	#YT = "events"
	XT = varname+" (GeV)"
	H = "Type 1 (e) control region"
	Cut = "(LepPt<50.)"
	treename="tree_T1"

	lumi = str(12.7)

	Data = TH1F("DATA", "", VAR[1], VAR[2], VAR[3])
	Data.Sumw2()
	Data.SetLineColor(1)
	Data.SetFillColor(0)
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	quickplot("/home/storage/andrzejnovak/March/SE.root", treename, Data, VAR[0], Cut, "(1.0)")
	quickplot("/home/storage/andrzejnovak/March/SM.root", treename, Data, VAR[0], Cut, "(1.0)")

	d = Data.GetEntries()

	W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
	W.SetLineColor(kGreen-6)
	W.SetLineWidth(2)
	quickplot("/home/storage/andrzejnovak/March/WJetsToQQ.root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")
	for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
		quickplot("/home/storage/andrzejnovak/March/WJetsToLNu_HT-"+w+".root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")
	w = W.GetEntries()

	QCD = TH1F("QCD", "", VAR[1], VAR[2], VAR[3])
	QCD.SetLineColor(kYellow)
	QCD.SetLineWidth(2)
	for q in ["300to500", "500to700", "700to1000", "1000to1500", "1500to2000", "2000toInf"]:
		quickplot("/home/storage/andrzejnovak/March/QCD_HT"+q+".root", treename, QCD, VAR[0], Cut, "("+lumi+"*weight)")

	q = QCD.GetEntries()

	TT = TH1F("TT", "", VAR[1], VAR[2], VAR[3])
	TT.SetLineColor(kRed-4)
	TT.SetLineWidth(2)
	quickplot("/home/storage/andrzejnovak/March/TT.root", treename,TT, VAR[0], Cut, "("+lumi+"*weight)")

	t = TT.GetEntries()

	ST = TH1F("ST", "", VAR[1], VAR[2], VAR[3])
	ST.SetLineColor(kBlue)
	for s in ["ST_s", "ST_t", "ST_at", "ST_tW", "ST_atW"]:
		quickplot("/home/storage/andrzejnovak/March/"+s+".root", treename, ST, VAR[0], Cut, "("+lumi+"*weight)")

	s = DSTGetEntries()
	
	return d, q, w, t, s
	


for varname in ["LepPt","METPt", "TAGPt", "TPRIMEM", "WPt", "lepJetPt","ZPRIMEM"]:
	d, q, w, t, s = cutcount(varname)
	print d, q,w,t,s





