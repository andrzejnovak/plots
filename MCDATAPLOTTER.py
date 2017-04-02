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

VAR = ["eventMass", 15, 500, 2000]
YT = "events / "+str((VAR[3]-VAR[2])/VAR[1])+" GeV"
YT = "events"
XT = "event mass (GeV)"
H = "Type 1 (e) control region"
Cut = "(lepIsTight>0.&lepMiniIso<0.1&(lepTopMass>250.&lepTopMass<500)&isEl>0.&lepPt>50.&leadJetPt>100.&wPt>100.&(tagJetSDMass>110&tagJetSDMass<210&tagJetTau3/tagJetTau2<0.50))"

lumi = str(2.1)

Data = TH1F("DATA", "", VAR[1], VAR[2], VAR[3])
Data.Sumw2()
Data.SetLineColor(1)
Data.SetFillColor(0)
Data.SetMarkerColor(1)
Data.SetMarkerStyle(20)
for d in ["Electron_Run2015C_25ns-05Oct2015", "Electron_Run2015D-05Oct2015-v1", "Electron_Run2015D-PromptReco-v4", "Muon_Run2015C_25ns-05Oct2015-v1", "Muon_Run2015D-05Oct2015-v1", "Muon_Run2015D-PromptReco-v4"]:
	quickplot("/home/bjr/trees_round_four/crab_Single"+d+".root", "tree", Data, VAR[0], Cut, "(1.0)")

W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
W.SetFillColor(kGreen-6)
for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
	quickplot("/home/bjr/trees_round_five/WJetsToLNu_HT-"+w+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", W, VAR[0], Cut, "("+lumi+"*weight)")


QCD = TH1F("QCD", "", VAR[1], VAR[2], VAR[3])
QCD.SetFillColor(kYellow-7)
for q in ["100to200", "200to300", "300to500", "500to700", "700to1000", "1000to1500", "1500to2000", "2000toInf"]:
	quickplot("/home/bjr/trees_round_five/QCD_HT"+q+"_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", QCD, VAR[0], Cut, "("+lumi+"*weight)")

TT = TH1F("TT", "", VAR[1], VAR[2], VAR[3])
TT.SetFillColor(kRed-4)
quickplot("/home/bjr/trees_round_five/TT_TuneCUETP8M1_13TeV-powheg-pythia8.root", "tree", TT, VAR[0], Cut, "("+lumi+"*0.9*0.93*weight*2.71828^(-0.00088*(MCantitoppt+MCtoppt)))")

ST = TH1F("ST", "", VAR[1], VAR[2], VAR[3])
ST.SetFillColor(kBlue)
for s in ["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1", "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1", "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"]:
	quickplot("/home/bjr/trees_round_five/"+s+".root", "tree", ST, VAR[0], Cut, "("+lumi+"*0.9*weight)")

sig1 =  TH1F("sig1", "", VAR[1], VAR[2], VAR[3])
sig1.SetLineColor(kMagenta-9)
sig1.SetLineWidth(2)
quickplot("/home/bjr/trees_round_four/ZprimeToTprimeT_TprimeToWB_MZp-1500Nar_MTp-900Nar_LH_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", sig1, VAR[0], Cut, "(21000./230000.)")
sig2 =  TH1F("sig2", "", VAR[1], VAR[2], VAR[3])
sig2.SetLineColor(kCyan-7)
sig2.SetLineWidth(2)
quickplot("/home/bjr/trees_round_four/ZprimeToTprimeT_TprimeToWB_MZp-2000Nar_MTp-1200Nar_LH_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", sig2, VAR[0], Cut, "(21000./230000.)")
sig3 =  TH1F("sig3", "", VAR[1], VAR[2], VAR[3])
sig3.SetLineColor(kViolet)
sig3.SetLineWidth(2)
quickplot("/home/bjr/trees_round_four/ZprimeToTprimeT_TprimeToWB_MZp-2500Nar_MTp-1500Nar_RH_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root", "tree", sig3, VAR[0], Cut, "(21000./230000.)")


for i in [QCD, TT, ST]:
	W.Add(i,1.)
for j in [TT, ST]:
	QCD.Add(j,1.)
for k in [ST]:
	TT.Add(k,1.)

FindAndSetMax([Data, W])
W.SetStats(0)
W.SetTitle("")
W.GetXaxis().SetTitle(XT)
W.GetYaxis().SetTitle(YT)
W.GetXaxis().SetTitleOffset(1.06)
W.GetYaxis().SetTitleOffset(1.06)

leg = TLegend(0.6,0.6,0.89,0.89)
leg.SetHeader(H)
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.AddEntry(Data, "Data (2.1 fb^{-1})", "PL")
leg.AddEntry(W, "W+Jets, W#rightarrow l#nu", "F")
leg.AddEntry(QCD, "QCD", "F")
leg.AddEntry(TT, "t#bar{t}", "F")
leg.AddEntry(ST, "single top", "F")
leg.AddEntry(sig1, "Z'_{1500}#rightarrow tT'_{900}", "L")
leg.AddEntry(sig2, "Z'_{2000}#rightarrow tT'_{1200}", "L")
leg.AddEntry(sig3, "Z'_{2500}#rightarrow tT'_{1500}", "L")

Pull = Data.Clone("pull")
Pull.Add(W,-1.)
for i in range(1, W.GetNbinsX()+1):
		V = Pull.GetBinContent(i)
		Ve = Data.GetBinError(i)
		if Ve > 1.:
			Pull.SetBinContent(i, V/Ve)
		Pull.SetBinError(i, 1.)
Pull.SetStats(0)
Pull.SetLineColor(1)
Pull.SetFillColor(0)
Pull.SetMarkerColor(1)
Pull.SetMarkerStyle(20)
Pull.GetXaxis().SetNdivisions(0)
Pull.GetYaxis().SetNdivisions(4)
Pull.GetYaxis().SetTitle("(Data - Bkg)/#sigma")
Pull.GetYaxis().SetLabelSize(85/15*Pull.GetYaxis().GetLabelSize())
Pull.GetYaxis().SetTitleSize(4.2*Pull.GetYaxis().GetTitleSize())
Pull.GetYaxis().SetTitleOffset(0.175)
Pull.GetYaxis().SetRangeUser(-3.,3.)

CMSLABL = TLatex()
CMSLABL.SetNDC()
CMSLABL.SetTextSize(0.035)

THILABL = TLatex()
THILABL.SetNDC()
THILABL.SetTextSize(0.04)

T0 = TLine(VAR[2],0.,VAR[3],0.)
T0.SetLineColor(kBlue)
T2 = TLine(VAR[2],2.,VAR[3],2.)
T2.SetLineColor(kBlue)
T2.SetLineStyle(2)
Tm2 = TLine(VAR[2],-2.,VAR[3],-2.)
Tm2.SetLineColor(kBlue)
Tm2.SetLineStyle(2)

T1 = TLine(VAR[2],1.,VAR[3],1.)
T1.SetLineColor(kBlue)
T1.SetLineStyle(3)
Tm1 = TLine(VAR[2],-1.,VAR[3],-1.)
Tm1.SetLineColor(kBlue)
Tm1.SetLineStyle(3)


C = TCanvas("C", "", 1800, 1200)
plot = TPad("pad1", "The pad 80% of the height",0,0.15,1,1)
pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.15)
plot.Draw()
pull.Draw()
plot.cd()
W.Draw()
QCD.Draw("same")
TT.Draw("same")
ST.Draw("same")
Data.Draw("same")
sig1.Draw("same")
sig2.Draw("same")
sig3.Draw("same")
leg.Draw("same")
CMSLABL.DrawLatex(0.135,0.85,"CMS Preliminary")
THILABL.DrawLatex(0.71,0.91,"#bf{2.1 fb^{-1}}, #bf{s = #sqrt{13} TeV}")
pull.cd()
Pull.Draw()
T0.Draw("same")
T2.Draw("same")
Tm2.Draw("same")
T1.Draw("same")
Tm1.Draw("same")
Pull.Draw("same")

