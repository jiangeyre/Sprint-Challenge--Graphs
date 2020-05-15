class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def bfs(graph, starting_vertex):
    visited_vertices = set()
    queue = Queue()
    queue.enqueue([starting_vertex])
    while queue.size() > 0:
        current_path = queue.dequeue()

        current_vertex = current_path[-1]
        # print("current_vertex " + str(current_vertex))
        if current_vertex not in visited_vertices:
            neighbors = get_neighbors(graph, current_vertex)
            for neighbor in neighbors:
                new_path = list(current_path)
                new_path.append(neighbor)
                queue.enqueue(new_path)
                if neighbor == '?':
                    return new_path
            visited_vertices.add(current_vertex)


def dfs(graph, starting_vertex):
    visited_vertices = set()
    stack = Stack()
    stack.push([starting_vertex])
    while stack.size() > 0:
        current_path = stack.pop()

        current_vertex = current_path[-1]
        # print("current_vertex " + str(current_vertex))
        if current_vertex not in visited_vertices:
            neighbors = get_neighbors(graph, current_vertex)
            for neighbor in neighbors:
                new_path = list(current_path)
                new_path.append(neighbor)
                stack.push(new_path)
                if neighbor == '?':
                    return new_path
            visited_vertices.add(current_vertex)

# get the IDs of rooms or unknown
def get_neighbors(graph, room):
    return list(graph[room].values())