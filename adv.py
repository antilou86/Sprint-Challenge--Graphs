from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited = {}
needs_exploration = []
#lets try breadth first.

qu = Queue()
qu.enqueue(player.current_room)

#a way to move my player == player.travel(direction)
#a way to track what still needs to be explored (queue or stack, maybe?)

while qu.size() > 0:
    curr_room = qu.dequeue()
    #add current room to visited, create empty dictionary for room-directions
    visited[player.current_room] = {}

    #for each available direction
    for i in curr_room.get_exits():
        #if a room exists
        if curr_room.get_room_in_direction(i) is not None:
            #update room index in visited with avialable directions
            visited[player.current_room][i]=curr_room.get_room_in_direction(i).id
            #add room to 'needs_exploration' array
            needs_exploration.append(curr_room.get_room_in_direction(i).id)
    print(player.current_room.id, visited[player.current_room])

    #travel a direction until you cant.
    if player.current_room.get_room_in_direction('n'):
        if player.current_room.get_room_in_direction('n') not in visited:
            player.travel('n')
            #add movement direction to traversal path
            traversal_path.append('n')
            #if the room is in needs_exploration, remove it.
            if player.current_room.id in needs_exploration:
                needs_exploration.remove(player.current_room.id)
            #enqueue the current room so the loop doesnt break.
            qu.enqueue(player.current_room)
print(needs_exploration)
print(traversal_path)
    #check surroundings and see if you can travel in another direction
    
# TRAVERSAL TEST
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
