from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


class ChargeFlipProducer(Module):
    def __init__(self, elSelection):
        self.elSel = elSelection
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("EventMass", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        eventSum = ROOT.TLorentzVector()
        for lep in muons:
            eventSum += lep.p4()
        for lep in filter(self.elSel,electrons):
            eventSum += lep.p4()
        for j in jets:
            eventSum += j.p4()
        self.out.fillBranch("EventMass", eventSum.M())
        
        #sel=len(lep)>0
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ChargeFlipModule = lambda: ChargeFlipProducer(elSelection=lambda el: el.pt > 5)
