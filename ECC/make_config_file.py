#! /usr/bin/env python3

import argparse
import os


class make_config_file:

    def __init__(self, msa, tree, second_path, config_values):
        self.msa = msa
        self.tree = tree
        self.path = second_path
        self.config_values = config_values

    def write_config(self):
        config = open(os.path.join(self.path, "codeml.ctl"), "w")
        config.write("###Input & output \n")
        config.write("%15s = %s\n" % ("seqfile", os.path.abspath(self.msa)))
        config.write("%15s = %s\n" % ("treefile", os.path.abspath(self.tree)))
        config.write("%15s = %s\n" % ("outfile", "mlc"))
        config.write("%15s = %s\n" % ("noisy", self.config_values["noisy"]))
        config.write("%15s = %s\n" %
                     ("verbose", self.config_values["verbose"]))
        config.write("%15s = %s\n" % ("getSE", self.config_values["getSE"]))
        config.write("%15s = %s\n" %
                     ("RateAncestor", self.config_values["RateAncestor"]))
        config.write("###Data usage description parameters \n")
        config.write("%15s = %s\n" %
                     ("runmode", self.config_values["runmode"]))
        config.write("%15s = %s\n" %
                     ("fix_blength", self.config_values["fix_blength"]))
        config.write("%15s = %s\n" %
                     ("seqtype", self.config_values["seqtype"]))
        config.write("%15s = %s\n" %
                     ("CodonFreq", self.config_values["CodonFreq"]))
        config.write("%15s = %s\n" %
                     ("cleandata", self.config_values["cleandata"]))
        config.write("%15s = %s\n" %
                     ("ndata", self.config_values["ndata"]))
        config.write("%15s = %s\n" %
                     ("clock", self.config_values["clock"]))
        config.write("%15s = %s\n" %
                     ("Mgene", self.config_values["Mgene"]))
        config.write("%15s = %s\n" %
                     ("icode", self.config_values["icode"]))
        config.write("%15s = %s\n" %
                     ("Small_Diff", self.config_values["Small_Diff"]))
        config.write("###Site replacement model parameters \n")
        config.write("%15s = %s\n" %
                     ("model", self.config_values["model"]))
        config.write("%15s = %s\n" %
                     ("NSsites", self.config_values["NSsites"]))
        config.write("%15s = %s\n" %
                     ("aaRatefile", self.config_values["aaRatefile"]))
        config.write("%15s = %s\n" %
                     ("aaDist", self.config_values["aaDist"]))
        config.write("%15s = %s\n" %
                     ("fix_alpha", self.config_values["fix_alpha"]))
        config.write("%15s = %s\n" %
                     ("alpha", self.config_values["alpha"]))
        config.write("%15s = %s\n" %
                     ("Malpha", self.config_values["Malpha"]))
        config.write("%15s = %s\n" %
                     ("ncatG", self.config_values["ncatG"]))
        config.write("%15s = %s\n" %
                     ("fix_kappa", self.config_values["fix_kappa"]))
        config.write("%15s = %s\n" %
                     ("kappa", self.config_values["kappa"]))
        config.write("%15s = %s\n" %
                     ("fix_omega", self.config_values["fix_omega"]))
        config.write("%15s = %s\n" %
                     ("omega", self.config_values["omega"]))
        config.write("%15s = %s\n" %
                     ("method", self.config_values["method"]))
        config.close()
