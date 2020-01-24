import os
import git
import dvc
import dvc.repo
import numpy as np
import subprocess
import argparse

def create_fix_demo_stages(path):
    os.makedirs(path)
    os.chdir(path)
    gitrepo = git.Repo.init()
    dvcrepo = dvc.repo.Repo.init()

    # TODO: the first stage needs also a dependency !!!

    subprocess.call(['dvc', 'run', '-o', 'out1_1.txt', 'echo text>out1_1.txt'])
    subprocess.call(['dvc', 'run', '-d', 'out1_1.txt', '-o', 'out1_2.txt', 'echo text>out1_2.txt'])
    subprocess.call(['dvc', 'run', '--no-exec', '-d', 'out1_2.txt', '-o', 'out1_3.txt', 'echo text>out1_3.txt'])

    subprocess.call(['dvc', 'run', '-o', 'out2_1.txt', 'echo text>out2_1.txt'])
    subprocess.call(['dvc', 'run', '-d', 'out2_1.txt', '-o', 'out2_2.txt', 'echo text>out2_2.txt'])
    subprocess.call(['dvc', 'run', '-d', 'out2_2.txt', '-o', 'out2_3.txt', 'echo text>out2_3.txt'])
    subprocess.call(['dvc', 'run', '--no-exec', '-d', 'out2_3.txt', '-o', 'out2_4_1.txt', 'echo text>out2_4_1.txt'])
    subprocess.call(['dvc', 'run', '-d', 'out2_3.txt', '-o', 'out2_4_2.txt', 'echo text>out2_4_2.txt'])
    subprocess.call(['dvc', 'run', '-d', 'out2_4_2.txt', '-o', 'out2_4_2_1.txt', 'echo text>out2_4_2_1.txt'])
    subprocess.call(
        ['dvc', 'run', '--no-exec', '-d', 'out2_4_2.txt', '-o', 'out2_4_2_2.txt', 'echo text>out2_4_2_2.txt'])
    subprocess.call(
        ['dvc', 'run', '--no-exec', '-d', 'out2_4_2_2.txt', '-d', 'out2_4_2_1.txt', '-d', 'out2_4_1.txt', '-o',
         'out2_5.txt', 'echo text>out2_5.txt'])

def main():
    parser = argparse.ArgumentParser(description='This argument allow you to create simple local git / dvc structure to test dvc-view on it.')
    parser.add_argument('-p', '--path', type=str, default='dvc-view-sampleproject',help='The path to create the project. If this parameter is not set, it will create in the current dir a "dvc-view-sampleproject" folder with the sample project.')
    args = parser.parse_args()

    create_fix_demo_stages(args.path)