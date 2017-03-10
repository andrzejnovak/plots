import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import numpy as np
import pandas as pd

TF = "/eos/uscms/store/user/anovak/QCD/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_234704/0000/"

QCD = ["/eos/uscms/store/user/anovak/QCD/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_234704/0000/", "/eos/uscms/store/user/anovak/QCD/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_234825/0000/", "/eos/uscms/store/user/anovak/QCD/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_234946/0000/", "/eos/uscms/store/user/anovak/QCD/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/160806_235108/0000/","/eos/uscms/store/user/anovak/QCD/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v3/160806_235229/0000/", "/eos/uscms/store/user/anovak/QCD/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_235350/0000/"]

W = ["/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/160806_235511/0000/", "/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_235632/0000/", "/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_235755/0000/", "/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160806_235917/0000/" ,"/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/160807_000038/0000/", "/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/160807_000159/0000/" , "/eos/uscms/store/user/anovak/Wjets/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160807_000322/0000/",  "/eos/uscms/store/user/anovak/Wjets/WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/B2GAnaFW_80X_V2p0_PR53_Aug06_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/160807_000443/0000/"]


def Fill(TreeName): # Loop through events and fill them. Actual Fill step is done at the end, allowing us to make a few quality control cuts.
	total = 0
	for i in files:
		print i
		File = TFile("root://cmsxrootd.fnal.gov/"+TF  + "/" +i)
		Tree = File.Get(TreeName)
		n = Tree.GetEntries()
		total += n
	return total

def count(TF, end=".root"):
	files =[]
	for file in os.listdir(TF):
		if file.endswith(end): # select files, allows you to select a subset of files for running on very large directories
			files.append(file)

	#TreeName = "B2GTTreeMaker/B2GTree"
	TreeName = "tree_T1"
	total = 0
	for i in files:
		#print i
		File = TFile("root://cmsxrootd.fnal.gov/"+TF  + "/" +i)
		Tree = File.Get(TreeName)
		n = Tree.GetEntries()
		total += n
	return total

direc = "/home/storage/andrzejnovak/T"


columns = [3,4,5,6,7,9,10,11]

index = ["QCD_HT300to500", "QCD_HT500to700", "QCD_HT700to1000", "QCD_HT1000to1500", "QCD_HT1500to2000", "QCD_HT2000toInf", "WJetsToLNu_HT-100To200","WJetsToLNu_HT-200To400", "WJetsToLNu_HT-400To600","WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200", "WJetsToLNu_HT-1200To2500", "WJetsToLNu_HT-2500ToInf", "WJetsToQQ", "ZprimeToTprimeT_TprimeToWB_MZp-1500Nar_MTp-900Nar_LH_Tune_T", "ZprimeToTprimeT_TprimeToWB_MZp-2000Nar_MTp-1200Nar_LH_Tune_T", "ZprimeToTprimeT_TprimeToWB_MZp-2500Nar_MTp-1500Nar_LH_Tune_T", "QCD", "W", "Sig", "(QCD+W)/Sig"]
df = pd.DataFrame(index=index, columns=columns)
df = df.fillna(0) # with 0s rather than NaNs




qcd = [10272017, 19005761, 15338355, 4976814, 3475786, 1959055]
w = [1585119, 2047224, 1899917, 3654847, 1539154, 6811765, 253402, 4938577]
sig = [231792, 227647,196935]

for i, t in enumerate([3,4,5,6,7,9,10,11]):
	TF = direc+str(t)
	qcdsum = 0
	for j, n in enumerate(["QCD_HT300to500", "QCD_HT500to700", "QCD_HT700to1000", "QCD_HT1000to1500", "QCD_HT1500to2000", "QCD_HT2000toInf"]):
		try:
			c = count(TF, n+".root")
			r = c/float(qcd[j])*100
			qcdsum += c
			df.ix[n,t] = r
			df.ix["QCD",t] = qcdsum/float(sum(qcd))*100
		except:
			pass
	wsum = 0
	for j, n in enumerate(["WJetsToLNu_HT-100To200","WJetsToLNu_HT-200To400", "WJetsToLNu_HT-400To600","WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200", "WJetsToLNu_HT-1200To2500", "WJetsToLNu_HT-2500ToInf", "WJetsToQQ"]):
		try:
			c = count(TF, n+".root")
			r = c/float(w[j])*100
			wsum += c
			df.ix[n,t] = r
			df.ix["W",t] = wsum/float(sum(w))*100
		except:pass
			
	sigsum = 0
	TF = "/home/storage/andrzejnovak/signal"
	for j, n in enumerate(["ZprimeToTprimeT_TprimeToWB_MZp-1500Nar_MTp-900Nar_LH_Tune_T", "ZprimeToTprimeT_TprimeToWB_MZp-2000Nar_MTp-1200Nar_LH_Tune_T", "ZprimeToTprimeT_TprimeToWB_MZp-2500Nar_MTp-1500Nar_LH_Tune_T"]):
		try:
			c = count(TF, n+str(t)+".root")
			r = c/float(sig[j])*100
			sigsum += c
			df.ix[n,t] = r
			df.ix["Sig", t] = sigsum/float(sum(sig))*100
			df.ix["(QCD+W)/Sig", t] = (qcdsum+wsum)/float(sum(w)+sum(qcd)) / sigsum *float(sum(sig))
		except: pass

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

columns = ["HLT_PFHT900", "HLT_Ele27_eta2p1_WPLoose_Gsf_HT200", "HLT_Mu45_eta2p1", "HLT_Mu50", "HLT_Mu55", "HLT_Mu300", "HLT_Mu350", "HLT_Ele115_CaloIdVT_GsfTrkIdT", "HLT_IsoMu27", "HLT_Ele27_eta2p1_WPLoose_Gsf", "HLT_Ele32_eta2p1_WPTight_Gsf" ]
columns = ["Mu45_eta2p1", "Mu50", "Mu55", "Mu300", "Mu350", "IsoMu27", "Ele27_eta2p1_WPLoose_Gsf", "Ele32_eta2p1_WPTight_Gsf" ]
 
df.columns = (columns)
df.index = ["QCD300to500", "QCD500to700", "QCD700to1000", "QCD1000to1500", "QCD1500to2000", "QCD2000toInf", "WJets100To200","WJets200To400", "WJets400To600","WJetsToLNu_HT-600To800","WJetsToLNu_HT-800To1200", "WJets1200To2500", "WJets2500ToInf", "WJetsToQQ", "1500Nar_MTp-900Nar_LH_Tune_T", "2000Nar_MTp-1200Nar_LH_Tune_T", "2500Nar_MTp-1500Nar_LH_Tune_T", "QCD", "W", "Sig", "(QCD+W)/Sig"]
print df
	
df.to_html('table.html')

	
