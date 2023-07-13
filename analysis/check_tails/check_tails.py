import ROOT
 
ROOT.gROOT.ProcessLineSync(".x ../../fit_library/CB2Pdf.cxx+")
ROOT.gROOT.ProcessLineSync(".x ../../fit_library/VWGPdf.cxx+")
ROOT.gROOT.ProcessLineSync(".x ../../fit_library/NA60Pdf.cxx+")
ROOT.gROOT.ProcessLineSync(".x ../../fit_library/Pol4ExpPdf.cxx+")
# Read workspace from file
# -----------------------------------------------
fIn_CB2_VWG = ROOT.TFile("CB2_CB2_VWG__tails.root")
w_CB2_VWG = fIn_CB2_VWG.Get("w")
w_CB2_VWG.Print()

m_CB2_VWG = w_CB2_VWG["m"]
model_CB2_VWG = w_CB2_VWG["JpsiPdf"]
model_CB2_VWG.Print("mean_Jpsi")

fIn_CB2_Pol4Exp = ROOT.TFile("CB2_CB2_Pol4Exp__tails.root")
w_CB2_Pol4Exp = fIn_CB2_Pol4Exp.Get("w")
w_CB2_Pol4Exp.Print()

m_CB2_Pol4Exp = w_CB2_Pol4Exp["m"]
model_CB2_Pol4Exp = w_CB2_Pol4Exp["JpsiPdf"]
model_CB2_Pol4Exp.Print("mean_Jpsi")

fIn_NA60_VWG = ROOT.TFile("NA60_NA60_VWG__tails.root")
w_NA60_VWG = fIn_NA60_VWG.Get("w")
w_NA60_VWG.Print()

m_NA60_VWG = w_NA60_VWG["m"]
model_NA60_VWG = w_NA60_VWG["JpsiPdf"]
model_NA60_VWG.Print("mean_Jpsi")
# ---------------------------------------------------------
# Plot data and PDF overlaid
mframe_CB2_VWG = m_CB2_VWG.frame(Title="Tail comparison CB2")
model_CB2_VWG.plotOn(mframe_CB2_VWG)
model_CB2_Pol4Exp.plotOn(mframe_CB2_VWG, ROOT.RooFit.LineColor(ROOT.kRed+1))
mframe_NA60_VWG = m_NA60_VWG.frame(Title="Tail compariso NA60")
model_NA60_VWG.plotOn(mframe_NA60_VWG)




canvasCompTailsCB2 = ROOT.TCanvas("canvasCompTailsCB2", "canvasCompTailsCB2", 1200, 600)
ROOT.gPad.SetLeftMargin(0.15)
canvasCompTailsCB2.SetLogy(1)
mframe_CB2_VWG.GetYaxis().SetTitleOffset(1.4)
mframe_CB2_VWG.Draw()
ROOT.gPad.BuildLegend(0.78, 0.65, 0.980, 0.935, "", "L")
canvasCompTailsCB2.SaveAs("CB2_tails_comparison.pdf")


canvasCompTailsNA60 = ROOT.TCanvas("canvasCompTailsNA60", "canvasCompTailsNA60", 1200, 600)
ROOT.gPad.SetLeftMargin(0.15)
canvasCompTailsNA60.SetLogy(1)
mframe_NA60_VWG.GetYaxis().SetTitleOffset(1.4)
mframe_NA60_VWG.Draw()
canvasCompTailsNA60.SaveAs("NA60_tails_comparison.pdf")