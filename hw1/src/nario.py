import sys
from collections import namedtuple
from Queue import PriorityQueue

BOARD_FILE = sys.argv[1]
HEURISTIC = sys.argv[2]
H_MANHATTAN = "manhattan"
H_EUCLIDEAN = "euclidean"
H_MY_OWN = "my_own"
CHAR_NARIO = "@"
CHAR_OBSTACLE = "="
CHAR_EMPTY = "."
MOVE_LEFT = 'left'
MOVE_RIGHT = 'right'
MOVE_TOP = 'top'
STATE = namedtuple("STATE", ["x", "y"])
NODE = namedtuple('NODE', ['state', 'path_cost', 'heuristic_cost'])


class Actions:
    def __init__(self):
        pass
    left, right, top = range(3)


class FrontierList(list):
    def has_item(self, node):
        for item in self:
            if item.state == node.state:
                return True
        return False

    def get_item(self):
        item = self[0]
        self.remove(item)
        return item

    def add_item(self, node):
        ind = 0
        for item in self:
            # This can be strictly greater also! Have to test which is better
            if (item.heuristic_cost+item.path_cost) >= (node.heuristic_cost+node.path_cost):
                self.insert(ind, node)
                return
            ind += 1
        self.append(node)

    def update_item_if_better(self, node):
        ind = 0
        for item in self:
            if item.state == node.state:
                if (item.heuristic_cost+item.path_cost) > (node.heuristic_cost+node.path_cost):
                    self.remove(item)
                    self.add_item(node)
                return
            ind += 1


def read_board_file():
    # Reads board_file specified in system args and returns board as list of lines
    board_file = open(BOARD_FILE, "r")
    nario_board = []
    for line in board_file:
        nario_board.append(line.rstrip('\n'))
    board_file.close()
    return nario_board


def get_nario_pos(nario_board):
    i = 0
    for line in nario_board:
        j = line.find(CHAR_NARIO)
        if j != -1:
            return STATE(i, j)
        i += 1
    return STATE(-1, -1)


def goal_check(node):
    # Can we write this as get_heuristic_distance(0)==0?
    return node.state.x == 0


def get_heuristic_cost(state):
    if HEURISTIC == H_MANHATTAN:
        return state.x
    if HEURISTIC == H_EUCLIDEAN:
        return state.x
    if HEURISTIC == H_MY_OWN:
        return state.x


def read_initial_state(board):
    nario_pos = get_nario_pos(board)
    initial_h_cost = get_heuristic_cost(nario_pos)
    initial_path_cost = 0
    return NODE(nario_pos, initial_path_cost, initial_h_cost)


def get_possible_actions(state):
    actions = []
    current_floor = NARIO_WORLD[state.x]
    left_y = (state.y - 1) % len(current_floor)
    if current_floor[left_y] == CHAR_EMPTY:
        actions.append(MOVE_LEFT)
    right_y = (state.y + 1) % len(current_floor)
    if current_floor[right_y] == CHAR_EMPTY:
        actions.append(MOVE_RIGHT)
    top_x = (state.x - 1) % len(current_floor)
    if NARIO_WORLD[top_x][state.y] == CHAR_EMPTY:
        actions.append(MOVE_TOP)
    return actions


def get_total_cost(prev_node, next_node):
    return (prev_node.path_cost + 1) + get_heuristic_cost(next_node.state)


def perform_action(node, action):
    # new_node = node
    # print new_node
    mod_w = len(NARIO_WORLD[0])
    if action == MOVE_TOP:
        new_state = STATE((node.state.x-1) % mod_w, node.state.y)
    elif action == MOVE_LEFT:
        new_state = STATE(node.state.x, (node.state.y-1) % mod_w)
    else:
        new_state = STATE(node.state.x, (node.state.y+1) % mod_w)
    return NODE(new_state, node.path_cost+1, get_heuristic_cost(new_state))


def print_world(state):
    k = 0
    for row in NARIO_WORLD:
        if k == state.x:
            print row[:state.y] + "@" + row[state.y+1:]
        else:
            print row
        k += 1


def perform_a_star_search():
    node = NODE(INITIAL_STATE, path_cost=0, heuristic_cost=get_heuristic_cost(INITIAL_STATE))
    frontier = FrontierList()
    frontier.add_item(node)
    explored = set([])
    percept_sequence = []
    while True:
        if len(frontier) == 0:
            return -1
        node = frontier.get_item()
        percept_sequence.append(node)
        explored.add(node.state)
        if GOAL_TEST(node):
            return percept_sequence
        for action in POSSIBLE_ACTIONS(node.state):
            child = SUCCESSOR(node, action)
            if child.state not in explored and not frontier.has_item(child):
                frontier.add_item(child)
            elif frontier.has_item(child):
                frontier.update_item_if_better(child)


NARIO_WORLD = read_board_file()

# PROBLEM DEFINITION
INITIAL_STATE = get_nario_pos(NARIO_WORLD)
POSSIBLE_ACTIONS = get_possible_actions
SUCCESSOR = perform_action
GOAL_TEST = goal_check
COST = get_total_cost


# Remove Nario from World
def remove_nario():
    i = 0
    for line in NARIO_WORLD:
        NARIO_WORLD[i] = line.replace("@", ".")
        i += 1
remove_nario()


if __name__ == '__main__':
    solution = perform_a_star_search()
    if solution == -1:
        print "NO PATH"
    else:
        print "Found solution in %s steps\n" % len(solution)
        for sol in solution:
            print_world(sol.state)
            print "\n"








