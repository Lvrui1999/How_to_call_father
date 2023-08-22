import json




class Node(object):
    def __init__(self, gender = 2, description = 'Someone'):

        self.description = description
        try:
            if gender in [0, 1, 2]:
                self.gender = gender
            else:
                raise ValueError()
        except:
            print('Triple Gender would be the max, please!')
        self.gender = gender
        self.linked_node = [] #(node_idx, direction:(-1 up, 1 down, 0 same_level))
        self.graph_idx = -1
        # self.lineup_idx = 0

    @classmethod
    def loads(cls, strs):
        temp = json.loads(strs)
        # {'sex' : self.gender, 'desp' : self.description, 'idx': self.graph_idx, 'links' : self.linked_node}
        temp_node = cls(gender = temp['sex'], description = temp['desp'])
        temp_node.set_linked_node(temp['links'])
        temp_node.set_idx(temp['idx'])
        return temp_node
        
    def set_linked_node(self, linked_noed):
        self.linked_node = linked_noed

    def set_graph(self, father_graph):
        self.father_graph = father_graph
        return self
        
    
    def set_idx(self, idx):
        self.graph_idx = idx
        

    #Adding node (Node, direction)
    def add_node(self, node, direction): #direction: (-1 up, 1 down, 0 same_level)
        self.linked_node.append([self.father_graph.add_node(node), direction])
        node.add_reverse_node(self.graph_idx, direction)
        # return True

    def add_reverse_node(self, node_idx, direction):
        self.linked_node.append([node_idx, -direction])
        self.father_graph.update_level(self.graph_idx, node_idx, direction)

    def display_detail(self):
        print('Graph_idx:', self.graph_idx)
        print('Linked_Node:\n', self.linked_node,'\n')
    
    def dumps(self):
        return json.dumps({'sex' : self.gender, 'desp' : self.description, 'idx': self.graph_idx, 'links' : self.linked_node})


        
    

    

class Graph(object):
    def __init__(self) -> None:
        self.node_list = []
        self.level_list = [] 
        self.nodes = 0
    
    @classmethod
    def loads(cls, strs):
        temp = json.loads(strs)
        # {'level_list' : self.level_list, 'node_list' : [tmp.dumps() for tmp in self.node_list]}
        temp_graph = cls()
        true_node_list = [Node.loads(tmp_item).set_graph(temp_graph) for tmp_item in temp['node_list']]
        temp_graph.set_node_list(true_node_list)
        temp_graph.set_level_list(temp['level_list'])
        return temp_graph

    def set_node_list(self, node_list):
        self.node_list = node_list

    def set_level_list(self, level_list):
        self.level_list = level_list
        self.nodes = len(level_list)

    def add_node(self, node_to_add : Node) -> int:
        node_to_add.set_graph(self)
        node_to_add.set_idx(len(self.node_list))
        self.node_list.append(node_to_add)
        self.level_list.append(0)
        self.nodes += 1
        return len(self.node_list) - 1

    def fetch_node(self, idx) -> Node:
        return self.node_list[idx]

    def update_level(self, idx_0, idx_1, direction):
        self.level_list[idx_0] = self.level_list[idx_1] + direction

    def display_graph(self):
        #Basic level displayment, wo link
        level_and_idxs = [[idx, self.level_list[idx]] for idx in range(self.nodes)]
        level_and_idxs.sort(key = lambda x : x[1])
        top_level = level_and_idxs[0][1]
        for virtual_node in level_and_idxs:
            if virtual_node[1] > top_level:
                top_level = virtual_node[1]
                print('')
            print(virtual_node[0],' ',end='')
        print('')

    def display_detail(self):
        print('Nodes:', self.nodes)
        for node in self.node_list:
            node.display_detail()

        print('Levels:\n', self.level_list,'\n')

    def dumps(self):
        return json.dumps({'level_list' : self.level_list, 'node_list' : [tmp.dumps() for tmp in self.node_list]})

    def save_to_file(self, filename):
        f = open(filename, 'w')
        f.write(self.dumps())
        f.close()
    
    def cal_relation(self, node_call, node_be_called):
        pass





def quick_open(filename):
    f = open('graphic.txt','r')
    tm = f.read()
    f.close()
    return Graph.loads(tm)








if __name__ == '__main__':
    # bgraph = Graph()

    # anchor = Node(0, description='Test myself')
    # bgraph.add_node(anchor)
    
    # anchor.add_node(Node(0), 0)
    # anchor.add_node(Node(1), 1)
    # bgraph.fetch_node(1).add_node(Node(),-1)
    # bgraph.fetch_node(3).add_node(Node(),-1)

    # # bgraph.display_detail()

    # bgraph.display_graph()  

    # bgraph.save_to_file('graphic.txt')

    bgraph = quick_open('graphic.txt')
    bgraph.display_graph()  
