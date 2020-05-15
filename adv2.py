from room import Room
from player import Player
from world import World
from util2 import Stack, Queue, Graph

from ast import literal_eval

# Loads the world
world = World()

# Use for testing.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

count = 0

def play():
    visited = set()
    graph = Graph()
    trav_path = []
    d_rooms = graph.dfs(player.current_room)
    rooms = [d_room for d_room in d_rooms]

    while(len(visited) < len(room_graph) - 1):
        curr_room = rooms[0]

        next_room = rooms[1]

        # use a bfs to find the shortest path to destination
        shortest = graph.bfs(curr_room, next_room)
        # loop through shortest until nothing left
        while len(shortest) > 1:
            # find the neighbours
            curr_room_nays = d_rooms[shortest[0]]
            next_room = shortest[1]
            # if the next room (in the shortest path) exists in the current neighbours of curr room
            if next_room in curr_room_nays:
                trav_path.append(curr_room_nays[next_room])
            # remove the first room from the queue
            shortest.remove(shortest[0])
        
        rooms.remove(curr_room)
        visited.add(curr_room)
    
    return trav_path

# traversal test to call upon in the find shorty - slightly modified the test below
def test_traversal(test_traversal_path):
    visited_rooms = set()
    # create new test player since player is used below
    testplayer = Player(world.starting_room)
    testplayer.current_room = world.starting_room
    visited_rooms.add(testplayer.current_room)

    for move in test_traversal_path:
        testplayer.travel(move)
        visited_rooms.add(testplayer.current_room)

    if len(visited_rooms) == len(room_graph):
        print(f"TESTS PASSED: {len(test_traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

traversal_path = []

# Find the shortest path.
def find_shorty():
    global traversal_path
    traversal_path = play()

    if len(traversal_path) < 960:
        print("3: Tests pass with length < 960!")
        return

    prev_trav = len(traversal_path)
    trav_count = 0
    # TRYING TO FIND THE SHORTEST ABOVE 950
    while len(traversal_path) > 950:
        trav_count += 1
        # IINCREMENT FOR EACH MOVE
        # KEEPS RUNNING TO FIND THE SHORTEST PATH
        if trav_count in range(0, 200000, 1000):
            print("Running ", trav_count)

        traversal_path = play()

        if len(traversal_path) < prev_trav:
            print("Shortest ATM - " , len(traversal_path), "AT: ", trav_count)
            prev_trav = len(traversal_path)
            print("*********************************")
            test_traversal(traversal_path)
            print("*********************************")
    # at the end        
    print("Total runs: ", trav_count)
    
# run the function
find_shorty()

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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")