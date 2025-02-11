import pygame
import sys
import math
import sys
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

    def draw(self, screen):
        pygame.draw.line(screen, EDGE_COLOR, (self.start_node.x, self.start_node.y), (self.end_node.x, self.end_node.y), edge_width)
def messege(string):
    pygame.init()
    
    width, height = 400, 300
    messege_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('messege')
    
    font = pygame.font.Font(None, 60)
    #text_surface = font.render(string, True, (255, 255, 255))
    lines = string.split('\n')  # Split the text into lines
    text_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]  # Create surfaces for each line
    text_rects = [surface.get_rect(center=(width // 2, height // 2 + i * 30)) for i, surface in enumerate(text_surfaces)]  # Adjust the vertical position for each line
    
    #windows.append(messege_window)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        messege_window.fill((0, 0, 0))
        for surface, rect in zip(text_surfaces, text_rects):
            messege_window.blit(surface, rect)
        pygame.display.flip()

    #windows.remove(messege_window)
    pygame.display.flip()
    #show_map()
    #pygame.quit()
# Main function
def load(file_path):
    global WIDTH, HEIGHT
    global NODE_RADIUS
    global Node_width
    global edge_width
    global sel_width
    global nodes
    global edges
    file=open(file_path)
    WIDTH=int(file.readline()[:-1])
    HEIGHT=int(file.readline()[:-1])
    x_w=int(file.readline()[:-1])
    y_w=int(file.readline()[:-1])
    NODE_RADIUS=int(file.readline()[:-1])
    Node_width=int(file.readline()[:-1])
    edge_width=int(file.readline()[:-1])
    file.readline()
    file_str=file.read()
    file.close()
    vert_spl=file_str.split("\nedges\n")[0].split("\n")
    edge_spl=file_str.split("\nedges\n")[1].split("\n")
    nodes=[]
    edges=[]
    for vert in vert_spl:
        nodes+=[Node(int(vert.split(",")[0])+x_w,int(vert.split(",")[1])+y_w)]
    for edge_i in edge_spl:
        edges+=[Edge(nodes[int(edge_i.split(",")[0])],nodes[int(edge_i.split(",")[1])])]
def set_attributs(X=None,Y=None,r=None,w_v=None,w_e=None,vert=None,edg=None,file_n=None):
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
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Graph Editor')
    clock = pygame.time.Clock()
    dragging_node = None
    first_node = None
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
                    for node in nodes:
                        if math.hypot(node.x - event.pos[0], node.y - event.pos[1]) < NODE_RADIUS:
                            node.selected = not node.selected
                            node.selected_left = False
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging_node:
                    dragging_node.selected_left = False
                    dragging_node.selected = False
                    dragging_node = None
                    first_node = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_node:
                    dragging_node.x, dragging_node.y = event.pos
                else:
                    for node in nodes:
                        if node.selected_left and event.buttons[0]:  # Drag if left mouse is held down
                            dragging_node = node
                            break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Delete selected nodes
                    selected_nodes = [node for node in nodes if node.selected]
                    for node in nodes:
                        node.selected = False
                    if first_node in selected_nodes:
                        first_node = None
                    nodes[:] = [node for node in nodes if node not in selected_nodes]
                    edges[:] = [edge for edge in edges if edge.start_node not in selected_nodes and edge.end_node not in selected_nodes]
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
                    messege("Saved")
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    main()
#main()
