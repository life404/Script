#! /usr/bin/env python3

import os
import shutil
import argparse


class make_file_dir:
    'make file directory'

    def __init__(self, output, models, msa_file):
        self.output = output
        self.models = models
        self.msa = msa_file
        
    def parse_models(self):
        models_array = self.models.split(":")
        return models_array

    def get_first_dir(self):
        first_path = os.path.join(self.output, os.path.splitext(self.msa)[0])
        return first_path

    def get_second_dir(self):
        second_dir = []
        first_path = self.get_first_dir()
        models_array = self.parse_models()
        for model in models_array:
            second_path = os.path.join(first_path, model)
            second_dir.append(second_path)
        return second_dir        
        
    def make_dir(self):
        second_dir = self.get_second_dir()
        first_path = self.get_first_dir()
        for directory in second_dir:
            os.makedirs(directory)
