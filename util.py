import random

count = 0

# algorithm for random room picker
def random_exit(length):
    # finds a random number in the total length of avail exits
    ran = random.randrange(0,length)

    return ran

# imports from the util files we used this week
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


# import the Graph we have been using all week
class Graph:
    def __init__(self):
        self.vertices = {}
    
    def dfs(self, starting_vertex):
        visited = set()
        s = Stack()
        s.push([starting_vertex])
        while s.size() > 0:
            current_room = s.pop()
            room = current_room[-1]
            if room not in visited:
                self.vertices[room.id] = {}
                exits = room.get_exits()
                #add exit directions
                for direction in exits:
                        next_room = room.get_room_in_direction(direction)
                        self.vertices[room.id][next_room.id] = direction
                visited.add(room)
                #if exits exist, loop and add
                while len(exits) > 0:
                    ran_dom = random_exit(len(exits))
                    direction = exits[ran_dom]
                    neighbors = list(current_room)
                    neighbors.append(room.get_room_in_direction(direction))
                    s.push(neighbors)
                    exits.remove(direction)
        return self.vertices

    def bfs(self, starting_vertex, destination_vertex):
        q = Queue()
        q.enqueue([starting_vertex])
        visited = set()

        while q.size() > 0:
            path = q.dequeue()
            room = path[-1]
            if room == destination_vertex:
                    return path
            else:
                if room not in visited:
                    visited.add(room)
                    edges = self.vertices[room]
                    for next_vert in edges:
                        path_copy = list(path)
                        path_copy.append(next_vert)
                        q.enqueue(path_copy)