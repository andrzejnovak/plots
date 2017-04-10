import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import pdb

import Plotting_Header
from Plotting_Header import *


class MicroTree:
	def __init__(self, name, pwd, File, cutn, add=False):
		self.name = name
		self.cutn = str(cutn)
		self.add = add
		self.File = File
		self.__book__()
		self.TransFile = TFile("DDT"+self.cutn+".root")
		self.CorrSig = self.TransFile.Get("DDT_sr")
		self.CorrBkg = self.TransFile.Get("DDT_sb")
		self.FillMicroTree()

	def __book__(self):
		File = TFile("root://cmsxrootd.fnal.gov/"+ pwd +self.File)
		Tree = File.Get("tree_T1")
		self.f = ROOT.TFile("C"+self.cutn+"/"+ self.name, "recreate" )
        	self.f.cd()
		self.tree = Tree.CopyTree("")
		if self.add == True:
			self.nTau32DDT_Bkg = array('f', [-1.0])
			self.addBranch('nTau32DDT_Bkg', self.nTau32DDT_Bkg, self.tree)
			self.nTau32DDT_Sig = array('f', [-1.0])
			self.addBranch('nTau32DDT_Sig', self.nTau32DDT_Sig, self.tree)
		else:
			self.Tau32DDT_Bkg = array('f', [-1.0])
			self.addBranch('Tau32DDT_Bkg', self.Tau32DDT_Bkg, self.tree)
			self.Tau32DDT_Sig = array('f', [-1.0])
			self.addBranch('Tau32DDT_Sig', self.Tau32DDT_Sig, self.tree)

	def FillMicroTree(self):
		File = TFile("root://cmsxrootd.fnal.gov/"+ pwd +self.File)
		print "Path = " + self.File
		Tree = File.Get("tree_T1")
		n = Tree.GetEntries()
		for j in range(0, n): # Here is where we loop over all events.
			if j % 50000 == 0 or j == 1:
				percentDone = float(j) / float(n) * 100.0
				print 'Processing '+self.name+' {0:10.0f}/{1:10.0f} : {2:5.2f} %'.format(j, n, percentDone )
			Tree.GetEntry(j)			
			self.tree.Fill()
			TAGM = Tree.TAGM
			TAGPt = Tree.TAGPt
			if TAGM > 110 and TAGM < 230 and TAGPt > 380 and TAGPt < 1000:				
				rind6 = self.CorrSig.GetXaxis().FindBin(TAGM)
				pind6 = self.CorrSig.GetYaxis().FindBin(TAGPt)
				if TAGM >  self.CorrSig.GetXaxis().GetBinUpEdge( self.CorrSig.GetXaxis().GetNbins() ) :
					rind6 = self.CorrSig.GetXaxis().GetNbins()
				if TAGM <  self.CorrSig.GetXaxis().GetBinLowEdge( 1 ) :
					rind6 = 1 
				if TAGPt >  self.CorrSig.GetYaxis().GetBinUpEdge( self.CorrSig.GetYaxis().GetNbins() ) :
					pind6 = self.CorrSig.GetYaxis().GetNbins()
				if TAGPt < self.CorrSig.GetYaxis().GetBinLowEdge( 1 ) :
					pind6 = 1

				if self.add == True: self.nTau32DDT_Sig[0] = Tree.TAGTau32 -  self.CorrSig.GetBinContent(rind6,pind6)
				else: self.Tau32DDT_Sig[0] = Tree.TAGTau32 -  self.CorrSig.GetBinContent(rind6,pind6)

				rind6 = self.CorrBkg.GetXaxis().FindBin(TAGM)
				pind6 = self.CorrBkg.GetYaxis().FindBin(TAGPt)
				if TAGM >  self.CorrBkg.GetXaxis().GetBinUpEdge( self.CorrBkg.GetXaxis().GetNbins() ) :
					rind6 = self.CorrBkg.GetXaxis().GetNbins()
				if TAGM <  self.CorrBkg.GetXaxis().GetBinLowEdge( 1 ) :
					rind6 = 1 
				if TAGPt >  self.CorrBkg.GetYaxis().GetBinUpEdge( self.CorrBkg.GetYaxis().GetNbins() ) :
					pind6 = self.CorrBkg.GetYaxis().GetNbins()
				if TAGPt < self.CorrBkg.GetYaxis().GetBinLowEdge( 1 ) :
					pind6 = 1
				
				if self.add == True:self.nTau32DDT_Bkg[0] = Tree.TAGTau32 -  self.CorrBkg.GetBinContent(rind6,pind6)
				else: self.Tau32DDT_Bkg[0] = Tree.TAGTau32 -  self.CorrBkg.GetBinContent(rind6,pind6)

				self.tree.Fill()

		File.Close()
		self.f.cd()
	        self.f.Write()
	        self.f.Close()

	def addBranch(self, name, var, T): 
		T.Branch(name, var, name+'/F')
	def __del__(self):
	        print "done!"

#pwd = "/home/storage/andrzejnovak/March/"
pwd = ""
Ws =[]
Ws.append("WJetsToQQ.root")
for w in ["100To200", "200To400" ,"400To600", "600To800", "800To1200", "1200To2500", "2500ToInf"]:
	Ws.append("WJetsToLNu_HT-"+w+".root")

clist = ["LepPt<400", "LepTightness>2.9", "WPt>500"]
for i, c in enumerate(clist):
	for w in Ws:
		W = MicroTree(w ,pwd, w, cutn=i, add=True)
		#except: continue




