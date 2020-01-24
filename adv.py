from room import Room
from player import Player
from world import World
from util import Stack, Queue, LinkedPair

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#need this to track data beyond what the other class allows.
class CustomRoom():
    def __init__(self, from_key, from_dir):
        #track previous room
        self.back=(from_dir,from_key)
        #all connected rooms
        self.connected={
            'n':None,
            'e':None,
            'w':None,
            's':None
        }
        #been here yet?
        self.visited=False
        #pass in where we came from
        if from_key is not None:
            self.connect(from_key,from_dir)
    
    #wires up passed in connection when we add the room
    def connect(self, connected_key,connected_dir):
        self.connected[connected_dir]=connected_key

    #checks for neighbors (during search) 
    def has_neighbor(self, target):
        if target in self.connected.values():
            return True
        else:
            return False

    #grabs neighbor if its stored in a linked pair in the queue
    def get_neighbors(self):
        return [data for data in self.connected.items() if data[1]]

    #will return which direction matches passed in target room if any
    def which_neighbor(self,target):
        if not self.has_neighbor(target):
            return None
        elif self.connected.get('n')==target:
            return 'n'
        elif self.connected.get('e')==target:
            return 'e'
        elif self.connected.get('w')==target:
            return 'w'
        elif self.connected.get('s')==target:
            return 's'

#begins path with a plain custom room 
#and starts the "stack" for what needs to be visited
to_visit=[0]
paths={
    0:CustomRoom(None,None)
}

#will only need to use this when the map is huge
#and contains many loops and forks. 
#key 1 is current room, key 2 is target unvisited room.
def BFS(key1, key2, roomList):
    #reuses a lot of the while loop from below.
    visited = {
        key1:[]
    }
    to_visit = Queue()
    to_visit.enqueue(LinkedPair(key1))

    while to_visit.size() > 0:
        current = to_visit.dequeue()
        node = roomList[current.data]
        #when we find the room
        if current.data == key2:
            return visited.get(current.data)
        #otherwise
        else:
            #check to see what we need to enqueue
            for key, value in node.get_neighbors():
                if not visited.get(value):
                    #avoid pass by referrence error
                    copy = visited[current.data].copy()
                    copy.append(key)
                    #add to visited
                    visited[value] = copy
                    #restart the loop
                    to_visit.enqueue(LinkedPair(value))

    #this print will hopefully never run again, may you RIP.
    print('cant find the rooooooom d00000d')
    return None

while len(to_visit) > 0:
    current = to_visit.pop()
    exits = room_graph[current][1]
    node = paths[current]
    switch = False
    loop = False
    loop_dir = None
    #so i can reverse my path on dead ends
    opposite = ['s','w','n','e']
    directions = ['n','e','s','w']
    times = 0

    #for each direction (enumerate helps when using opposite directions)
    for index, direction in enumerate(directions):
        #if there is a room that isnt already in paths
        target = exits.get(direction)
        if target and not target in paths:
            #create a temp room.
            temp = CustomRoom(current, opposite[index])
            #wire it up to available directions
            node.connect(target, direction)
            #add it to the paths and needs visiting
            paths[target] = temp
            to_visit.append(target)
            #flip that boolean
            switch = True
            #track number of  we'll need to return
            times += 1

        #if there is a room that IS in paths (found a loop)
        elif target and target in to_visit:
            #move it to the end of the list
            to_visit.remove(target)
            to_visit.append(target)
            #wire up the edges.
            node.connect(target, direction)
            #wire up the reversed path
            paths[target].connect(current, opposite[index])
            #flip the boolean for switch and loop 
            switch = True
            loop = True
            #define the loop direction
            loop_dir = direction

    #check if we've completed the loop
    if loop_dir and node.has_neighbor(to_visit[-1]):
        loop_dir = None

    #switch is False but we still have rooms to visit (there's a fork)
    if not switch and len(to_visit) > 0:
        found = False
        path_copy = traversal_path.copy()
        
        while not found:
            if not paths.get(node.back[1]):
                #returns path to target node/room
                result = BFS(current, to_visit[-1], paths)
                #creates a copy of current traversals
                traversal_path = path_copy
                #sort of concats the reverse directions to the end (thanks google)
                traversal_path.extend(result)
                #done.
                loop_dir="?"
                found = True
                break
            #add backward path to movement
            traversal_path.append(node.back[0])
            #"move" to the next node
            node = paths[node.back[1]]
            #is it next to us? 
            if to_visit[-1] in node.connected.values():
                found = True

    #still rooms to explore but we've completed our loop
    if len(to_visit) > 0 and not loop_dir:
        #the last unvisited direction from the room
        direction = node.which_neighbor(to_visit[-1])
        #adds unexplored direction to paths
        traversal_path.append(direction)

    #there's a valid direction to travel
    elif loop_dir is not '?' and loop_dir is not None:
        traversal_path.append(loop_dir)

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
