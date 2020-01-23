import os
import git
import dvc
import dvc.repo
import numpy as np
import subprocess
import argparse
from dvc.repo import Repo as DVCRepo
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from dvc.repo import Repo as DVCRepo


def main():
    parser = argparse.ArgumentParser(description='With this script you can visualize your Data Version Control (DVC) - Pipeline.')

    parser.add_argument('-p', '--path', type=str, default=None,
                        help='The path to save the graphs. If this is not set it will plot the dependencies.')

    parser.add_argument('--path-to-repository', type=str, default=None,
                        help='The path to the repository. If this is not set, it will use the current dir.')


    parser.add_argument('--figure-size', type=int, default=15,
                        help='The size of the matplotlib figure that gets created with this script.')


    parser.add_argument('--ignore-outputs', action='store_true', default=False,
                        help='Currently this have no meaning!')
    parser.add_argument('--ignore-dependencies', action='store_true', default=False,
                        help='Currently this have no meaning!')
    args = parser.parse_args()

    # Get the pipeline
    if args.path_to_repository is not None:
        dvcrepo = DVCRepo(args.path_to_repository)
    else:
        dvcrepo = DVCRepo('.')
    pipelines = dvcrepo.pipelines

    # for each pipeline of the graph
    i = 0
    for g in pipelines:
        plt.figure(figsize=(args.figure_size, args.figure_size))
        plt.title('Dependency-Graph ' + str(i+1))

        paths_to_stages = [s.path_in_repo for s in g.nodes()]

        changed_status_of_stages = list(dvcrepo.status(targets=paths_to_stages, with_deps=True))

        # 1. rename nodes for a better visualization of the node names in the plot.
        mapping = {}
        for n in paths_to_stages:
            new_n = n
            # insert new lines between the path to the directory and the filename
            pos = len(n) - 1 - n[::-1].find('/')
            new_n = n[:pos] + '/\n\n' + n[pos + 1:]
            # insert a new line between the filename (without ending) and the (datatype) ending
            pos = len(new_n) - 1 - new_n[::-1].find('.')
            new_n = new_n[:pos] + '\n.' + new_n[pos + 1:]
            mapping[n] = new_n
            mapping[new_n] = n
        g = nx.relabel_nodes(g, mapping, copy=True)

        # 2. Find best order
        order = list(reversed(list(nx.topological_sort(g))))

        # 3. calc position for each node
        pos = {}
        for i in range(len(order)):
            n = order[i]
            grad = 2 * np.pi * (float(i) / len(order))
            pos[n] = np.array([np.sin(grad), np.cos(grad)])

        # 4. set settings for nx.draw_networkx
        size = 6.0 / len(g.nodes)
        options = {
            'node_color': '#6FB98F',
            'node_size': 20000 * size,
            'width': 6 * size,
            'arrowstyle': '-|>',
            'arrowsize': 20 * size,
            'font_size': 13 * size ** 0.5
        }

        pos_stages = {p: pos[p] for p in pos if p in order}

        # 5. call nx.draw_networks
        nx.draw_networkx_nodes(g, pos=pos_stages, nodelist=order, **options)


        i += 1
    plt.show()

