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

def rename_stage_names(old_name):
    # if file is in folder than make two new lines between path to file and file name.
    if old_name.find('/') > -1:
        pos = len(old_name) - 1 - old_name[::-1].find('/')
        new_name = old_name[:pos] + '/\n\n' + old_name[pos + 1:]
    elif old_name.find('\\') > -1:
        pos = len(old_name) - 1 - old_name[::-1].find('\\')
        new_name = old_name[:pos] + '\\\n\n' + old_name[pos + 1:]
    else:
        new_name = old_name

    # insert a new line between the filename (without ending) and the (datatype) ending
    pos = len(new_name) - 1 - new_name[::-1].find('.')
    new_name = new_name[:pos] + '\n.' + new_name[pos + 1:]

    return new_name


def set_plt_lim(positions, buffer):
    # convert from dict to numpy array
    positions = np.array([positions[p] for p in positions])
    xmin = np.min(positions[:, 0])
    xmax = np.max(positions[:, 0])
    xcenter = xmin + (xmax - xmin) / 2.0
    ymin = np.min(positions[:, 1])
    ymax = np.max(positions[:, 1])
    ycenter = ymin + (ymax - ymin) / 2.0

    dist = np.max([xmax - xmin, ymax - ymin])/2.0 + buffer

    plt.xlim([xcenter - dist, xcenter + dist])
    plt.ylim([ycenter - dist, ycenter + dist])

    return xcenter, ycenter, dist

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
    pipe_id = 0
    for g in pipelines:
        # create a new figure for each pipeline
        plt.figure(figsize=(args.figure_size, args.figure_size))
        plt.title('Dependency-Graph ' + str(pipe_id+1))

        # use the path in repo to the dvc file instead of the DataTyoe "Stage"
        g = nx.relabel_nodes(g, {s: s.path_in_repo for s in g.nodes()}, copy=True)


        # get the status of each name
        status_of_stages = list(dvcrepo.status(targets=g.nodes(), with_deps=True))

        # rename nodes for a better visualization of the node names in the plot.
        mapping = {}
        for n in g.nodes():
            new_n = rename_stage_names(n)
            mapping[n] = new_n
            mapping[new_n] = n

        g = nx.relabel_nodes(g, mapping, copy=True)

        # Find optimal order for the stages
        order = [n for n in list(reversed(list(nx.topological_sort(g))))]

        # calc position for each node
        rad_each_segment = 2. * np.pi / len(order)
        pos = {}
        for i in range(len(order)):
            n = order[i]
            rad = rad_each_segment * float(i)
            pos[n] = np.array([np.sin(rad), np.cos(rad)])

        # calculate the optimal radius of a stage-node for the unit circle
        optimal_radius = np.power(np.power(np.sin(rad_each_segment),2.)+np.power(1-np.cos(rad_each_segment),2.),0.5) / 2.

        # calculate the positions that are needed
        pos_stages = {p: pos[p] for p in pos if p in order}

        # set plt lim
        _, _, dist = set_plt_lim(pos_stages, optimal_radius)

        optimal_radius /= dist

        # set basic options for the drawing of the network
        #TODO: the size of each component can be a parameter!
        options = {
            'node_color': '#6FB98F',
            'node_size': 80000 * np.power(optimal_radius,2.0) * np.pi, # volumen!!!! of node
            'width': 20 * optimal_radius, # width of arrow; linear value
            'arrowstyle': '-|>',
            'arrowsize': 50 * optimal_radius, # width of head of arrow; linear value
            'font_size': 40 * optimal_radius # linear value
        }

        # draw; all stages
        nx.draw_networkx_nodes(g, pos=pos_stages, nodelist=order, **options, label='Stages executed')

        # draw; all stages that are changed
        changed_status_mapped = [mapping[v] for v in status_of_stages]
        print(changed_status_mapped)
        options['node_color'] = '#FB6542'
        nx.draw_networkx_nodes(g, pos=pos_stages, nodelist=changed_status_mapped, **options,  label='Stages to be executed')

        # draw edges
        nx.draw_networkx_edges(g, pos_stages, **options)

        # draw labels
        nx.draw_networkx_labels(g, pos_stages, **options)

        # plot legend
        #TODO change the legend and add parameters!
        plt.legend(scatterpoints=1, markerscale=0.1)

        if args.path is not None:
            plt.savefig(args.path + '_' + str(pipe_id+1) + '.jpg')


        pipe_id += 1
    if args.path is None:
        plt.show()

