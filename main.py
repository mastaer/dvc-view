import os
import git
import dvc
import dvc.repo
import numpy as np
import subprocess

def create_fix_demo_stages(path):
    print('1. Create new folder and make this to a local git and dvc repository.')
    os.makedirs(path)
    os.chdir(path)
    gitrepo = git.Repo.init()
    dvcrepo = dvc.repo.Repo.init()
    subprocess.call(['dvc', 'run', '-o', 'out1_1.txt', '"echo text>out1_1.txt"'])
    subprocess.call(['dvc', 'run', '-d', 'out1_1.txt', '-o', 'out1_2.txt', '"echo text>out1_2.txt"'])
    subprocess.call(['dvc', 'run', '--no-exec', '-d', 'out1_2.txt', '-o', 'out1_3.txt', '"echo text>out1_3.txt"'])

    subprocess.call(['dvc', 'run', '-o', 'out2_1.txt', '"echo text>out2_1.txt"'])
    subprocess.call(['dvc', 'run', '-d', 'out2_1.txt', '-o', 'out2_2.txt', '"echo text>out2_2.txt"'])
    subprocess.call(['dvc', 'run', '-d', 'out2_2.txt', '-o', 'out2_3.txt', '"echo text>out2_3.txt"'])
    subprocess.call(['dvc', 'run', '--no-exec', '-d', 'out2_3.txt', '-o', 'out2_4_1.txt', '"echo text>out2_4_1.txt"'])
    subprocess.call(['dvc', 'run', '-d', 'out2_3.txt', '-o', 'out2_4_2.txt', '"echo text>out2_4_2.txt"'])
    subprocess.call(['dvc', 'run', '-d', 'out2_4_2.txt', '-o', 'out2_4_2_1.txt', '"echo text>out2_4_2_1.txt"'])
    subprocess.call(
        ['dvc', 'run', '--no-exec', '-d', 'out2_4_2.txt', '-o', 'out2_4_2_2.txt', '"echo text>out2_4_2_2.txt"'])
    subprocess.call(
        ['dvc', 'run', '--no-exec', '-d', 'out2_4_2_2.txt', '-d', 'out2_4_2_1.txt', '-d', 'out2_4_1.txt', '-o',
         'out2_5.txt', '"echo text>out2_5.txt"'])

def main():
    create_fix_demo_stages("TEST-FOLDER")