import pygame
import sys
import math
from interactive_things import message
sys.path.insert(1, '.')
NODE_COLOR = (0, 0, 255)
EDGE_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (255, 255, 0)
sel_width=2
# Node class
class Node:
    def __init__(self, x, y):
        global number_of_nodes
        self.x = x
        self.y = y
        self.node_number=0
        #number_of_nodes+=1
        self.selected = False
        self.selected_left = False

    def draw(self, screen, first_node):
        pygame.draw.circle(screen, NODE_COLOR, (self.x, self.y), NODE_RADIUS, Node_width)
        pygame.draw.circle(screen, BACKGROUND_COLOR, (self.x, self.y), NODE_RADIUS-Node_width, 0)
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), NODE_RADIUS, sel_width)
        if self.selected_left or (self==first_node):
            pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), NODE_RADIUS, sel_width)

# Edge class
class Edge:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.selected = False

    def distance_to(self, pos):
        # Distance from a point to the edge's line segment
        ax, ay = self.start_node.x, self.start_node.y
        bx, by = self.end_node.x, self.end_node.y
        dx, dy = bx - ax, by - ay
        length_sq = dx * dx + dy * dy
        if length_sq == 0:
            return math.hypot(pos[0] - ax, pos[1] - ay)
        t = max(0, min(1, ((pos[0] - ax) * dx + (pos[1] - ay) * dy) / length_sq))
        return math.hypot(pos[0] - (ax + t * dx), pos[1] - (ay + t * dy))

    def draw(self, screen):
        color = (255, 0, 0) if self.selected else EDGE_COLOR
        width = edge_width + 2 if self.selected else edge_width
        pygame.draw.line(screen, color, (self.start_node.x, self.start_node.y), (self.end_node.x, self.end_node.y), width)
# Main function
def load(file_path):
    global WIDTH, HEIGHT
    global NODE_RADIUS
    global Node_width
    global edge_width
    global sel_width
    global nodes
    global edges
    try:
        file=open(file_path)
    except FileNotFoundError:
        message("File not found: " +str(file_path))
        return "error"
    try:
        WIDTH=int(file.readline()[:-1])
        HEIGHT=int(file.readline()[:-1])
        x_w=int(file.readline()[:-1])
        y_w=int(file.readline()[:-1])
        NODE_RADIUS=int(file.readline()[:-1])
        Node_width=int(file.readline()[:-1])
        edge_width=int(file.readline()[:-1])
        file.readline()
        lines=file.read().split("\n")
        edges_index=lines.index("edges")
        vert_spl=[line for line in lines[:edges_index] if line]
        edge_spl=[line for line in lines[edges_index+1:] if line]
        nodes=[]
        edges=[]
        for vert in vert_spl:
            nodes+=[Node(int(vert.split(",")[0])+x_w,int(vert.split(",")[1])+y_w)]
        for edge_i in edge_spl:
            edges+=[Edge(nodes[int(edge_i.split(",")[0])],nodes[int(edge_i.split(",")[1])])]
    except (ValueError, IndexError):
        message("Could not read the map file (wrong format): " +str(file_path))
        return "error"
    finally:
        file.close()
    return "ok"
def set_attributes(X=None,Y=None,r=None,w_v=None,w_e=None,vert=None,edg=None,file_n=None):
    global WIDTH, HEIGHT
    global NODE_RADIUS
    global Node_width
    global edge_width
    global nodes
    global edges
    global file_name
    #file=open(file_path)
    if not(X==None):
        WIDTH=X
    if not(Y==None):
        HEIGHT=Y
    if not(r==None):
        NODE_RADIUS=r
    if not(w_v==None):
        Node_width=w_v
    if not(w_e==None):
        edge_width=w_e
    if not(vert==None):
        nodes=vert
    if not(edg==None):
        edges=edg
    if not(file_n==None):
        file_name=file_n

def main():
    #pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Graph Editor')
    clock = pygame.time.Clock()
    dragging_node = None
    first_node = None
    selection_start = None
    selection_end = None
    group_drag_node = None
    group_drag_last = None
    group_drag_moved = False
    group_drag_deselect = False
    run=True
    while run:
        #screen = pygame.display.set_mode((WIDTH, HEIGHT))
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                #pygame.quit()
                #sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    clicked_node = None
                    for node in nodes:
                        if math.hypot(node.x - event.pos[0], node.y - event.pos[1]) < NODE_RADIUS:
                            clicked_node = node
                            break
                    
                    if clicked_node:
                        if first_node is None:
                            # Start creating an edge
                            first_node = clicked_node
                            first_node.selected_left = True
                            first_node.selected = True
                        elif not(first_node==clicked_node):
                            to_draw=True
                            for edge in edges:
                                if ((edge.start_node==first_node) and (edge.end_node==clicked_node))or((edge.start_node==clicked_node) and (edge.end_node==first_node)):
                                    to_draw=False
                            # Finish creating the edge
                            if to_draw:
                                edges.append(Edge(first_node, clicked_node))
                                first_node.selected_left = False
                                first_node.selected = False
                                first_node = None
                    else:
                        # Create a new node
                        nodes.append(Node(event.pos[0], event.pos[1]))
                
                elif event.button == 3:  # Right mouse button
                    # Check if a node was clicked for selection
                    clicked_node = None
                    for node in nodes:
                        if math.hypot(node.x - event.pos[0], node.y - event.pos[1]) < NODE_RADIUS:
                            clicked_node = node
                            break
                    if clicked_node:
                        # Toggle on release, or drag all selected nodes if the mouse moves
                        group_drag_node = clicked_node
                        group_drag_last = event.pos
                        group_drag_moved = False
                        if not clicked_node.selected:
                            clicked_node.selected = True
                            clicked_node.selected_left = False
                            group_drag_deselect = False
                        else:
                            group_drag_deselect = True
                    else:
                        clicked_edge = None
                        for edge in edges:
                            if edge.distance_to(event.pos) <= max(edge_width / 2 + 3, 5):
                                clicked_edge = edge
                                break
                        if clicked_edge:
                            clicked_edge.selected = not clicked_edge.selected
                        else:
                            # Start an area selection
                            selection_start = event.pos
                            selection_end = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging_node:
                    dragging_node.selected_left = False
                    dragging_node.selected = False
                    dragging_node = None
                    first_node = None
                elif event.button == 3 and selection_start:
                    # Select all nodes inside the area
                    sel_rect = pygame.Rect(selection_start, (0, 0))
                    sel_rect.union_ip(pygame.Rect(event.pos, (0, 0)))
                    for node in nodes:
                        if sel_rect.left <= node.x <= sel_rect.right and sel_rect.top <= node.y <= sel_rect.bottom:
                            node.selected = True
                            node.selected_left = False
                    for edge in edges:
                        if all(sel_rect.left <= n.x <= sel_rect.right and sel_rect.top <= n.y <= sel_rect.bottom for n in (edge.start_node, edge.end_node)):
                            edge.selected = True
                    selection_start = None
                    selection_end = None
                elif event.button == 3 and group_drag_node:
                    # A right click without dragging deselects an already selected node
                    if not group_drag_moved and group_drag_deselect:
                        group_drag_node.selected = False
                        group_drag_node.selected_left = False
                    group_drag_node = None

            elif event.type == pygame.MOUSEMOTION:
                if selection_start:
                    selection_end = event.pos
                elif group_drag_node:
                    # Move all selected nodes with the mouse
                    dx = event.pos[0] - group_drag_last[0]
                    dy = event.pos[1] - group_drag_last[1]
                    if dx or dy:
                        group_drag_moved = True
                        for node in nodes:
                            if node.selected:
                                node.x += dx
                                node.y += dy
                    group_drag_last = event.pos
                elif dragging_node:
                    dragging_node.x, dragging_node.y = event.pos
                else:
                    for node in nodes:
                        if node.selected_left and event.buttons[0]:  # Drag if left mouse is held down
                            dragging_node = node
                            break

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE) or (event.key == pygame.K_KP_PERIOD and not (event.mod & pygame.KMOD_NUM)):
                    # Delete selected nodes and edges
                    selected_nodes = [node for node in nodes if node.selected]
                    for node in nodes:
                        node.selected = False
                    if first_node in selected_nodes:
                        first_node = None
                    nodes[:] = [node for node in nodes if node not in selected_nodes]
                    edges[:] = [edge for edge in edges if not edge.selected and edge.start_node not in selected_nodes and edge.end_node not in selected_nodes]
                elif event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL):
                    # Select all nodes and edges
                    for node in nodes:
                        node.selected = True
                        node.selected_left = False
                    for edge in edges:
                        edge.selected = True
                elif event.key == pygame.K_SPACE:
                    # Deselect all nodes and edges
                    for node in nodes:
                        node.selected = False
                        node.selected_left = False
                    for edge in edges:
                        edge.selected = False
                    first_node = None
                    dragging_node = None
                elif event.key == pygame.K_s:
                    file=open(file_name,"w")
                    file.write(str(WIDTH)+"\n")
                    file.write(str(HEIGHT)+"\n")
                    file.write("0\n")
                    file.write("0\n")
                    file.write(str(NODE_RADIUS)+"\n")
                    file.write(str(Node_width)+"\n")
                    file.write(str(edge_width)+"\nvertices")
                    for i in range(len(nodes)):
                        node=nodes[i]
                        node.node_number=i
                        file.write("\n"+str(node.x)+","+str(node.y))
                    file.write("\nedges")
                    for edge in edges:
                        file.write("\n"+str(edge.start_node.node_number)+","+str(edge.end_node.node_number))
                    file.close()
                    message("Saved")
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption('Graph Editor')
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_UP])or(keys[pygame.K_KP8]):
            for node in nodes:
                if node.selected:
                    node.y-=1
        if (keys[pygame.K_RIGHT])or(keys[pygame.K_KP6]):
            for node in nodes:
                if node.selected:
                    node.x+=1
        if (keys[pygame.K_DOWN])or(keys[pygame.K_KP2]):
            for node in nodes:
                if node.selected:
                    node.y+=1
        if (keys[pygame.K_LEFT])or(keys[pygame.K_KP4]):
            for node in nodes:
                if node.selected:
                    node.x-=1
                    # Deselect all nodes after deletion

        # Draw edges
        for edge in edges:
            edge.draw(screen)

        # Draw nodes
        for node in nodes:
            node.draw(screen,first_node)

        # Draw area selection rectangle
        if selection_start:
            sel_rect = pygame.Rect(selection_start, (0, 0))
            sel_rect.union_ip(pygame.Rect(selection_end, (0, 0)))
            pygame.draw.rect(screen, (255, 0, 0), sel_rect, 1)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    # Constants
    WIDTH, HEIGHT = 800, 600
    NODE_RADIUS = 20
    Node_width=5
    edge_width=2
    #number_of_nodes=0
    file_name="v_map.txt"
    nodes = []
    edges = []
    pygame.init()
    main()
#main()
