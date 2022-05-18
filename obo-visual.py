import fastobo
#import pronto
from pyvis.network import Network
import itertools
import numpy as np

# wget -O cv/psi-ms.obo https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo
psi = fastobo.load('cv/psi-ms.obo')

# term_list = dict()
# for frame in psi:
#     if isinstance(frame, fastobo.term.TermFrame):
#         term_list[str(frame.id)] = {'prop': str(frame.id), 'name': '?' , 'edges': []} 
#         for clause in frame:
#             if isinstance(clause, fastobo.term.IsAClause):
#                 term_list[str(frame.id)] = (str(frame.id), str(clause.term))

term_list = dict()
c = 0
for frame in psi:
    if isinstance(frame, fastobo.term.TermFrame):
        term_list[str(frame.id)] = { 'edges_isa': [] , 'edges_cat': [] , 'edges_con': [] , 'edges_uni': [] , 'node_index': c}
        c += 1 
        for clause in frame:
            # print(str(clause) + " = " + str(isinstance(clause, fastobo.term.RelationshipClause)))
            if isinstance(clause, fastobo.term.NameClause):
                term_list[str(frame.id)]['name'] = clause.name
            if isinstance(clause, fastobo.term.DefClause):
                term_list[str(frame.id)]['definition'] = clause.definition
            if isinstance(clause, fastobo.term.IsAClause):
                term_list[str(frame.id)]['edges_isa'].append((str(frame.id), str(clause.term)))
            if isinstance(clause, fastobo.term.RelationshipClause):
                if str(clause.typedef) == 'has_metric_category':
                    term_list[str(frame.id)]['edges_cat'].append(str(clause.term))
                if str(clause.typedef) == 'has_units':
                    term_list[str(frame.id)]['edges_uni'].append(str(clause.term))
                if str(clause.typedef) == 'has_value_concept':
                    term_list[str(frame.id)]['edges_con'].append(str(clause.term))

# len(term_list)

net = Network(height='750px', width='100%', bgcolor='#a0a0a0', font_color='black')
node_list = list(zip(*[(v['node_index'],(v['name'],k)) for k,v in term_list.items()]))
net.add_nodes(node_list[0], label=list(zip(*node_list[1]))[0] ) #, accessions=list(zip(*node_list[1]))[1])
# net.show('nodes.html')

# TODO filter PEFF & MS < 4x10E6
# TODO build edges from relations!

# TODO make layout hierarchical
# add_node knows about level= in hierarchical mode: net = Network(..., layout=True)
# net.add_nodes([3, 4, 5, 6], 
#               label=['Michael', 'Ben', 'Oliver', 'Olivia'],
#               color=['#3da831', '#9a31a8', '#3155a8', '#eb4034'])
# net.show('list_of_nodes_with_color.html')

accession_lookup = {k:v['node_index'] for k,v in term_list.items()}
edge_o = [v['node_index'] for k,v in term_list.items()]
edge_d = [list(map(accession_lookup.get, v['edges_cat'])) for k,v in term_list.items()]

edge_list = list(map(tuple,np.concatenate([list(itertools.product([i], v)) for i,v in zip(edge_o, edge_d) if v])))
edge_list = [tuple(map(int, i)) for i in edge_list]
net.add_edges(edge_list)
net.show('edges.html')

# TODO filter nodes without edges