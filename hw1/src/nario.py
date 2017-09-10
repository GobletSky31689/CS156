import sys
from collections import namedtuple

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
NODE = namedtuple('NODE', ['state', 'path_cost', 'heuristic_cost', "parent"])


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


def get_action_cost(prev_node, next_node):
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
    return NODE(new_state, node.path_cost+1, get_heuristic_cost(new_state), node)


def remove_nario():
    i = 0
    for line in NARIO_WORLD:
        NARIO_WORLD[i] = line.replace("@", ".")
        i += 1


def print_world(state):
    k = 0
    for row in NARIO_WORLD:
        if k == state.x:
            print row[:state.y] + "@" + row[state.y+1:]
        else:
            print row
        k += 1
    print ""


def get_solution(node):
    solution = []
    while True:
        solution.insert(0, node.state)
        if node.parent is None:
            return solution
        node = node.parent


def perform_a_star_search():
    node = NODE(state=INITIAL_STATE,
                path_cost=0,
                heuristic_cost=get_heuristic_cost(INITIAL_STATE),
                parent=None)
    frontier = FrontierList()
    frontier.add_item(node)
    explored = set([])
    ind = 0
    while True:
        ind += 1
        if len(frontier) == 0:
            return -1
        node = frontier.get_item()
        explored.add(node.state)
        if GOAL_TEST(node):
            return get_solution(node)
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
COST = get_action_cost

# Remove Nario from World
remove_nario()


if __name__ == '__main__':
    precept_sequence = perform_a_star_search()
    if precept_sequence == -1:
        print "NO PATH"
    else:
        # print "Found solution in %s steps\n" % len(precept_sequence)
        for pos in precept_sequence:
            print_world(pos)
