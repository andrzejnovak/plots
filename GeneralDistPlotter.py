import sys
from optparse import OptionParser
import ROOT
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from Plotting_Header import *

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

	Data = TH1F("DATA", "", VAR[1], VAR[2], VAR[3])
	Data.Sumw2()
	Data.SetLineColor(1)
	Data.SetFillColor(0)
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	quickplot(pwd+"SE.root", treename, Data, VAR[0], Cut, "(1.0)")
	quickplot(pwd+"SM.root", treename, Data, VAR[0], Cut, "(1.0)")


	W = TH1F("W", "", VAR[1], VAR[2], VAR[3])
	W.SetLineColor(kGreen-6)
	W.SetLineWidth(2)
	quickplot(pwd+"WJetsToQQ.root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")
	#for w in ["100To200", "200To400", "400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
	for w in ["200To400", "400To600", "600To800"]:
		quickplot(pwd+"WJetsToLNu_HT-"+w+".root", treename, W, VAR[0], Cut, "("+lumi+"*weight)")


	QCD = TH1F("QCD", "", VAR[1], VAR[2], VAR[3])
	QCD.SetLineColor(kYellow)
	QCD.SetLineWidth(2)
	#for q in ["300to500", "500to700", "700to1000", "1000to1500", "1500to2000", "2000toInf"]:
	for q in ["300to500", "500to700", "700to1000", "1500to2000", "2000toInf"]:
		quickplot(pwd+"QCD_HT"+q+".root", treename, QCD, VAR[0], Cut, "("+lumi+"*weight)")

	TT = TH1F("TT", "", VAR[1], VAR[2], VAR[3])
	TT.SetLineColor(kRed-4)
	TT.SetLineWidth(2)
	quickplot(pwd+"TT.root", treename,TT, VAR[0], Cut, "("+lumi+"*weight)")

	ST = TH1F("ST", "", VAR[1], VAR[2], VAR[3])
	ST.SetLineColor(kBlue)
#	for s in ["ST_s", "ST_t", "ST_at", "ST_tW", "ST_atW"]:
		#quickplot(pwd+s+".root", treename, ST, VAR[0], Cut, "("+lumi+"*weight)")
	
	sig1 =  TH1F("sig1", "", VAR[1], VAR[2], VAR[3])
	sig1.SetLineColor(kMagenta-9)
	sig1.SetLineWidth(2)
	sig1.SetLineStyle(2)
	quickplot(pwd+"ZprimeToTprimeT_TprimeToWB_MZp-1500Nar_MTp-900Nar_LH_Tune.root", treename, sig1, VAR[0], Cut, "("+lumi+"*"+str(1./50000.)+")")
	sig2 =  TH1F("sig2", "", VAR[1], VAR[2], VAR[3])
	sig2.SetLineColor(kCyan-7)
	sig2.SetLineWidth(2)
	sig2.SetLineStyle(2)
	quickplot(pwd+"ZprimeToTprimeT_TprimeToWB_MZp-2000Nar_MTp-1200Nar_LH_Tune.root", treename, sig2, VAR[0], Cut, "("+lumi+"*"+str(1./50000.)+")")
	sig3 =  TH1F("sig3", "", VAR[1], VAR[2], VAR[3])
	sig3.SetLineColor(kViolet)
	sig3.SetLineWidth(2)
	sig3.SetLineStyle(2)
	quickplot(pwd+"ZprimeToTprimeT_TprimeToWB_MZp-2500Nar_MTp-1500Nar_LH_Tune.root", treename , sig3, VAR[0], Cut, "("+lumi+"*"+str(1./50000.)+")")

	if stacked==True:
		for i in [QCD, TT, ST]:
			W.Add(i,1.)
		for j in [TT, ST]:
			QCD.Add(j,1.)
		for k in [ST]:
			TT.Add(k,1.)
	
	if normed==True:
		for histo in ["Data", "QCD", "W", "TT","ST", "sig1", "sig2", "sig3"]:
			if eval(histo+".Integral()") >0:  eval(histo+".Scale(1./"+histo+".Integral())")

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

	leg = TLegend(0.65,0.6,0.89,0.89)
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
	#sig1.Draw("same")
	#sig2.Draw("same")
	#sig3.Draw("same")
	leg.Draw("same")
	CMSLABL.DrawLatex(0.135,0.85,"CMS Preliminary")
	CUTLABL.DrawLatex(0.135,0.80,Cut)
	THILABL.DrawLatex(0.71,0.91,"#bf{12.7 fb^{-1}}, #bf{s = #sqrt{13} TeV}")
	
	C.SaveAs("outputs/"+varname+"_Cut_"+Cut[-20:].replace("<", "").replace(">", "").replace(".", "").replace("&", "_")+".png")

#  "LepTightness<1.&LepPt>50.&lepJetPt>100.&METPt>50.&TAGPt>350&lepJetCSV<0.46"


clist = ["LepTightness<1","LepPt>50", "lepJetPt>100", "METPt>50", "TAGPt>200", "lepJetCSV<0.46"]

clist = ["LepMiniIso<0.1", "LepTightness>2.9","LepPt>50", "lepJetPt>100", "METPt>50", "TAGPt>400"]

cuts = []
for i in range(1,len(clist)+1):
	c = ""
	for j in range(i):
		c += clist[j]
		if j != i-1: c += "&"
	cuts.append(c)
	print c

for cut in cuts[len(cuts)-1:len(cuts)]:
	#for varname, xmin, xmax in zip(["LepPt","METPt", "TAGPt", "TPRIMEM", "WPt", "lepJetPt","ZPRIMEM"],[50,0,0,0,0,0,200],[500,900,1400,1800,1200,1000,3000]):
		#varplot(varname, xmin, xmax, cut =cut)
	for varname in options.vars:
		varplot(varname, pwd=options.pwd,cut =cut, stacked=options.stack, normed=options.norm)




