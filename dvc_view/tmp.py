"""


           stages_dict = {s.relpath: s for s in dvcrepo.stages}




           """"""
           nodes_of_outs = {}
           for n in list(g.nodes()):
               # create a BiGraph for the outputs
               stage_outs = stages_dict[n].outs
               for so in stage_outs:
                   if n in nodes_of_outs:
                       nodes_of_outs[n].append(so.def_path)
                   else:
                       nodes_of_outs[n] = [so.def_path]
           """"""







               out_i = 0
               for out in nodes_of_outs[mapping[n]]:
                   g.add_node(out)
                   g.add_edge(out, n)
                   factor = 4. / len(order)
                   # TODO: ALLOW MULTIPLE OUTPUTS
                   out_grad = grad + out_i * np.pi / 9.0
                   pos[out] = np.array([np.sin(grad) + factor * np.sin(out_grad) + graph_index * 3.5,
                                        np.cos(grad) + factor * np.cos(out_grad)])
                   out_i += 1

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

           size = 2.0 / len(g.nodes)
           options = {
               'node_color': '#BBDDBB',
               'node_size': 20000 * size,
               'width': 6 * size,
               'arrowstyle': '-|>',
               'arrowsize': 20 * size,
               'font_size': 13 * size ** 0.5
           }
           pos_outs = {p: pos[p] for p in pos if p not in order}
           # 5. call nx.draw_networks
           nx.draw_networkx_nodes(g, pos=pos_outs, nodelist=pos_outs.keys(), **options)

           size = 2.0 / len(g.nodes)
           options = {
               'node_color': '#DDBBBB',
               'node_size': 20000 * size,
               'width': 6 * size,
               'arrowstyle': '-|>',
               'arrowsize': 20 * size,
               'font_size': 13 * size ** 0.5
           }
           pos_outs = {p: pos[p] for p in pos if p not in order}
           # 5. call nx.draw_networks
           nx.draw_networkx_nodes(g, pos=pos_outs, nodelist=pos_outs.keys(), **options)

           # 4. set settings for nx.draw_networkx
           size = 6.0 / len(g.nodes)
           options = {
               'node_color': '#FB6542',
               'node_size': 20000 * size,
               'width': 6 * size,
               'arrowstyle': '-|>',
               'arrowsize': 20 * size,
               'font_size': 13 * size ** 0.5
           }

           # 5. call nx.draw_networks
           changed_status_mapped = [mapping[v] for v in changed_status]
           pos_changed = {v: pos_stages[v] for v in changed_status_mapped}
           print(g.nodes())
           print('g:', g)
           print('pos_changed', pos_changed)
           print('changed_status_mapped: ', changed_status_mapped)
           # nx.draw_networkx(g, pos=pos_changed,nodelist=changed_status_mapped, **options)
           nx.draw_networkx_nodes(g, pos=pos_changed, nodelist=changed_status_mapped, **options)
           # nx.draw_networkx(g, pos=pos, **options)

           nx.draw_networkx_edges(g, pos, **options)
           nx.draw_networkx_labels(g, pos, **options)

           # 6. update graph index
           graph_index += 1
       """