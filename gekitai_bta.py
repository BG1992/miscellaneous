import sqlite3
import gekitai_combs_mapping as gcm
import gekitai4 as gh

base = sqlite3.connect('D://gekitai//main_base2.db')

def evaluate(node):
    pass

def get_children(node):
    pass

def set_proof_and_disproof_numbers(node):
    if node.expanded == 1:
        children = get_children(node)
        if node.form == 'AND':
            node.proof = 0
            node.disproof = pow(10,9)
            children = get_children(node)
            for child in children:
                node.proof += child.proof
                node.disproof = min(node.disproof, child.disproof)
        else:
            node.proof = pow(10,9)
            node.disproof = 0
            for child in children:
                node.proof = min(node.proof, child.proof)
                node.disproof += child.disproof
    else:
        if node.result == 1:
            node.proof = pow(10,9)
            node.disproof = 0
        elif node.result == -1:
            node.proof = 0
            node.disproof = pow(10,9)
        else:
            node.proof = 1
            node.disproof = 1

def count_nodes():
    pass

def develop_node(node):
    pass

def select_most_proving_node(node):
    pass

def parent_on_current_search_path(node):
    pass

def update_ancestors(node, root):
    while node is not None:
        if node.base_node is not None:
            bn = node.base_node
        else:
            bn = node
        if bn.proof == 0 or bn.disproof == 0:
            return node
        elif node.repetition: #jak wprowadzić ten atrybut?
            node.possible_draw = True



def check_memo():
    if len(memo) > pow(10,7):
        tbl = []
        for el in memo:
            tbl.append(el + tuple(memo[el]))
        base.execute('insert into states_bta values (?,?,?,?,?,?,?,?)', tbl)
        base.commit()

def update_expanded(node, expanded):
    memo[node][0] = expanded
    check_memo()


memo = {}

class Node():
    def __init__(self, tp, expanded, proof, disproof, form, depth):
        self.tp = tp
        self.expanded = expanded
        self.proof = proof
        self.disproof = disproof
        self.form = form
        self.depth = depth
        self.has_base = False
        memo[tp] = self
        check_memo()

root = Node((0,0,0,0), -1, 0, pow(10,9), 0)

def pns(root):

    while root.proof != 0 and root.disproof != 0:
        most_proving_node = select_most_proving_node(root)
        expand_node(most_proving_node)
        update_ancestors(most_proving_node, root)

    if root.proof == 0: return True
    elif root.disproof == 0: return False
    else: return '?'
