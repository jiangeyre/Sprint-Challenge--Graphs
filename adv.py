from room import Room
from player import Player
from world import World

import sys, os
from util import Stack, Queue, bfs, dfs

import random
from ast import literal_eval

# Load world
world = World()

def find_near_unvisited_room(graph, current_room):
    # print("Current room in find_near_unvisited_room is " + str(current_room))
    path_unvisited = bfs(graph, current_room)
    # dfs option
    # path_unvisited = dfs(graph, current_room)

    # directions
    path = []

    for i in range(0, len(path_unvisited) - 1):
        list_graph = list(graph[path_unvisited[i]].items())

        nav = ""

        for x in list_graph:
            if x[1] == path_unvisited[i + 1]:
                nav = x[0]

        path.append(nav)

    return (path)


# how to traverse through the rooms
def traversal_path():
    # initialize an array of visited rooms
    visited = set()
    # creating the player and linking
    player = Player(world.starting_room)
    # add the current room player is in to the array that keeps track of all visited rooms
    visited.add(player.current_room)
    # the path we take
    traversal_path = []
    stack = []
    graph = dict()
    graph[player.current_room.id] = dict()
    exits = player.current_room.get_exits()

    for exit in exits:
        graph[player.current_room.id][exit] = "?"

        # find what movements can work and visit rooms
        unvisited_nav = [item[0] for item in list(graph[player.current_room.id].items()) if item[1] == "?"]

        trek = unvisited_nav[random.randint( 0, len(unvisited_nav) - 1 )]
        stack.append(trek)

        # as long as the total visited rooms is less than total rooms avail
        while len(visited) < len(room_graph):
            trek = stack.pop()

            previous = player.current_room.id
            # use the player's travel method to move the direction
            player.travel(trek)
            traversal_path.append(trek)

            # Add the room to the visited
            visited.add(player.current_room)

            exits = player.current_room.get_exits()

            # Update the graph with the previous room
            graph[previous][trek] = player.current_room.id

            # make current room is it does not already exist in the graph
            if player.current_room.id not in graph:
                graph[player.current_room.id] = dict()

                for exit in exits:
                    graph[player.current_room.id][exit] = '?'

            # Update the entry for the current room.
            opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
            opposite = opposites[trek]

            graph[player.current_room.id][opposite] = previous

            # find the unvisited directions 
            unvisited = [item[0] for item in list(graph[player.current_room.id].items()) if item[1] == "?"]

            # if still unvisited directions, pick a random direction to move in from the current room player is in
            if len(unvisited) > 0:
                move = unvisited[random.randint(
                    0, len(unvisited) - 1)]
                stack.append(move)

            elif len(visited) == len(room_graph):
                #print("Traversal_path is successfully made! " + str(traversal_path))
                return traversal_path

            else:
                # Back up to nearest room with an unexplored direction
                next_move = find_near_unvisited_room(graph, player.current_room.id)

                for i in range(0, len(next_move) - 1):
                    player.travel(next_move[i])

                    # keep track of that direction
                    traversal_path.append(next_move[i])

                    # add to visited
                    visited.add(player.current_room)
                stack.append(next_move[-1])



# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
# room_graph=literal_eval(open(map_file, "r").read())
with open(os.path.join(sys.path[0], map_file), 'r') as f:
    room_graph = literal_eval(f.read())

world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = traversal_path()



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
