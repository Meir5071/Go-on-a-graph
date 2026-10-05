#from time import wait
import pygame
import pygame.locals
from pygame._sdl2 import Window
import sys
import copy
from interactive_things import message
import bot
import time
#sys.path.insert(1, '.')
def ops_color(color):
    if color=="w":
        return("b")
    else:
        return("w")

class graph:
    def __init__(self,file_path):
        if file_path=="":
            self.vertices=[]
            self.vertices_colors=[]
            self.edges=[]
            self.neighbors_list=[]
            self.history=[]
            self.error = False
        else:
            try:
                file=open(file_path)
            except FileNotFoundError:
                message("File not found: " + str(file_path))
                self.error = True
                return
            self.error = False
            global X
            global Y
            global x_w
            global y_w
            global r
            global w_v
            global w_e
            try:
                X=int(file.readline()[:-1])
                Y=int(file.readline()[:-1])
                x_w=int(file.readline()[:-1])
                y_w=int(file.readline()[:-1])
                r=int(file.readline()[:-1])
                w_v=int(file.readline()[:-1])
                w_e=int(file.readline()[:-1])
                file.readline()
                lines=file.read().split("\n")
                edges_index=lines.index("edges")
                vert_spl=[line for line in lines[:edges_index] if line]
                edge_spl=[line for line in lines[edges_index+1:] if line]
                self.vertices=[]
                self.vertices_colors=[]
                self.edges=[]
                for vert in vert_spl:
                    self.vertices+=[[int(vert.split(",")[0]),int(vert.split(",")[1])]]
                    self.vertices_colors+=["e"]
                for edge in edge_spl:
                    self.edges+=[[int(edge.split(",")[0]),int(edge.split(",")[1])]]
            except (ValueError, IndexError):
                message("Could not read the map file (wrong format): " + str(file_path))
                self.error = True
                return
            finally:
                file.close()
            #self.vertices=[[0,0],[0,100],[0,200],[100,0],[100,100],[100,200],[200,0],[200,100],[200,200]]
            #self.vertices_colors=["e","e","e","e","e","e","e","e","e"]
            #self.edges=[[0,1],[1,2],[0,3],[3,4],[4,5],[1,4],[2,5],[3,6],[6,7],[7,8],[4,7],[5,8]]
            self.neighbors_list=[self.find_neighbors(i) for i in range(len(self.vertices))]
            self.history=[self.vertices_colors[:]]
    def find_neighbors(self,point_index):
        neighbors=[]
        for edge in self.edges:
            if edge[0]==point_index:
                neighbors+=[edge[1]]
            elif edge[1]==point_index:
                neighbors+=[edge[0]]
        return list(set(neighbors))
    def find_neighbors_of_list(self,point_indices):
        neighbors=[]
        for point_index in point_indices:
            for neighbor in self.neighbors_list[point_index]:
                    if (not(neighbor in point_indices)):
                        neighbors+=[neighbor]
        return list(set(neighbors))
    def find_same_color_neighbors_of_list(self,point_indices,color,found_points):
        neighbors=[]
        for point_index in point_indices:
            for neighbor in self.neighbors_list[point_index]:
                    if (self.vertices_colors[neighbor]==color) and (not(neighbor in found_points)):
                        neighbors+=[neighbor]
        return list(set(neighbors))
    def find_component(self,point_index):
        comp=[]
        addition=[point_index]
        while True:
            comp+=addition
            addition=self.find_same_color_neighbors_of_list(addition,self.vertices_colors[point_index],comp)
            if addition==[]:
                return comp
    def kill(self,color):
        to_kill_list=[0 for _ in range(len(self.vertices))]
        for i in range(len(self.vertices)):
            if (to_kill_list[i]==0) and (self.vertices_colors[i]==color):
                to_kill_comp=True
                comp=self.find_component(i)
                for vert_ind in self.find_neighbors_of_list(comp):
                    to_kill_comp=(to_kill_comp)and(not(self.vertices_colors[vert_ind]=="e"))
                if to_kill_comp:
                    for vert_ind in comp:
                        to_kill_list[vert_ind]=1
                else:
                    for vert_ind in comp:
                        to_kill_list[vert_ind]=2
        for i in range(len(self.vertices)):
            if to_kill_list[i]==1:
                self.vertices_colors[i]="e"
                #pygame.draw.circle(window, (255, 255, 0), [x_w+self.vertices[i][0], y_w+self.vertices[i][1]], r-w, 0)
    def copy_graph(self):
        new_graph=graph("")
        new_graph.vertices=self.vertices
        new_graph.vertices_colors=self.vertices_colors[:]
        new_graph.edges=self.edges
        new_graph.neighbors_list=self.neighbors_list
        new_graph.history=self.history[:]
        return new_graph
def show_map(game_map,window_old,new_window=False):
    if new_window:
        window = pygame.display.set_mode((X, Y))
        pygame.display.set_caption('Go on a graph')
    else:
        window = window_old
    # set the pygame window name
    window.fill((255, 255, 0))
    for edge in game_map.edges:
        pygame.draw.line(window, (0, 0, 255), [x_w+game_map.vertices[edge[0]][0], y_w+game_map.vertices[edge[0]][1]], [x_w+game_map.vertices[edge[1]][0], y_w+game_map.vertices[edge[1]][1]], w_e)
    for i, vert in enumerate(game_map.vertices):
        color = game_map.vertices_colors[i]
        pygame.draw.circle(window, (0, 0, 255), [x_w+vert[0], y_w+vert[1]], r, w_v)
        if color=="e":
            pygame.draw.circle(window, (255, 255, 0), [x_w+vert[0], y_w+vert[1]], r-w_v+1, 0)
        elif color=="b":
            pygame.draw.circle(window, (0, 0, 0), [x_w+vert[0], y_w+vert[1]], r-w_v+1, 0)
        elif color=="w":
            pygame.draw.circle(window, (255, 255, 255), [x_w+vert[0], y_w+vert[1]], r-w_v+1, 0)
    pygame.display.flip()
    if new_window:
        return window
def main(file_name, bot_colors, bot_level, turn_delay, fast_eval=False, smart_pass=False):
    game_map=graph(file_name)
    if game_map.error:
        return
    #pygame.init()
    clock = pygame.time.Clock()

    
    # create the display surface object
    # of specific dimension, i.e. (X, Y).
    #window = pygame.display.set_mode((X, Y))
    window=show_map(game_map,window_old=None, new_window=True)
    # create a surface object, image is drawn on it.
    #imp = pygame.image.load("C:\\Users\\Meir\\Dropbox\\Downloads\\Screenshot_2024-07-21_182250-removebg-preview.png").convert()
    
    # Using blit to copy content from one surface to other
    #scrn.blit(imp, (0, 0))
    
    # paint screen one time
    #pygame.display.flip()
    #delay_time=10
    status = True
    turn="b"
    pas=0
    status_2=True
    #windows = [window]
    window_p = Window.from_display_module()
    pos = window_p.position[:]
    while (status):
        if pos != window_p.position[:]:
            pos = window_p.position[:]
            show_map(game_map,window_old=window)
        for event in pygame.event.get():
            #show_map(game_map)
            if event.type == pygame.QUIT:
                status = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) and status_2:
                for i in range(len(game_map.vertices)):
                    if r*r>((x_w+game_map.vertices[i][0]-event.pos[0])**2+(y_w+game_map.vertices[i][1]-event.pos[1])**2) and (game_map.vertices_colors[i]=="e"):
                        ver2=game_map.vertices_colors[:]
                        game_map.vertices_colors[i]=turn
                        game_map.kill(ops_color(turn))
                        ver=game_map.vertices_colors[:]
                        game_map.kill(turn)
                        if ver==game_map.vertices_colors:
                            if game_map.vertices_colors in game_map.history:
                                message("Ko")
                                game_map.vertices_colors=ver2
                                game_map.vertices_colors[i]="e"
                                window=show_map(game_map, window_old=window, new_window=True)
                            else:
                                pas=0
                                turn=ops_color(turn)
                                game_map.history.append(game_map.vertices_colors[:])
                        else:
                            game_map.vertices_colors=ver
                            game_map.vertices_colors[i]="e"
                            message("suicidal move")
                            window=show_map(game_map, window_old=window, new_window=True)
                        show_map(game_map, window)
            elif (event.type == pygame.KEYUP) and status_2:
                if event.key == pygame.K_p:
                    pas+=1
                    if turn=="w":
                        turn="b"
                        message("white said pass")
                    else:
                        turn="w"
                        message("black said pass")
                    window=show_map(game_map, window_old=window, new_window=True)
        if (pas>1) and (status_2):
            status_2=False
            white=0
            black=0
            count_list=[0 for vert in game_map.vertices]
            for i in range(len(count_list)):
                if (count_list[i]==0):
                    if game_map.vertices_colors[i]=="e":
                        comp=game_map.find_component(i)
                        if game_map.find_neighbors_of_list(comp)==[]:
                            comp_color="e"
                        else:
                            comp_color=game_map.vertices_colors[game_map.find_neighbors_of_list(comp)[0]]
                        for vert_ind in game_map.find_neighbors_of_list(comp):
                            if not(game_map.vertices_colors[vert_ind]==comp_color):
                                comp_color="e"
                        for vert_ind in comp:
                            count_list[vert_ind]=comp_color
                            if True:
                                game_map.vertices_colors[vert_ind]=comp_color
                    else:
                        count_list[i]=game_map.vertices_colors[i]
            for a in count_list:
                if a=="w":
                    white+=1
                elif a=="b":
                    black+=1
            if black>white:
                message("Black won!\nblack:"+str(black)+"  white:"+str(white))
            elif black<white:
                message("White won!\nblack:"+str(black)+"  white:"+str(white))
            else:
                message("Draw!\nBlack:"+str(black)+"  White:"+str(white))
            window=show_map(game_map, window_old=window, new_window=True)
        clock.tick(60)
        if (len(bot_colors)>1) and (status_2):
            time.sleep(turn_delay)
        #show_map(game_map)
        if (turn in bot_colors) and (status_2):
            move = bot.bot_move(game_map, turn, depth=bot_level, fast_eval=fast_eval, smart_pass=smart_pass)
            if move is not None:
                game_map.vertices_colors[move] = turn
                game_map.kill(ops_color(turn))
                game_map.history.append(game_map.vertices_colors[:])
                show_map(game_map, window_old=window)
                pas=0
            else:
                pas+=1
                if turn=="w":
                    #turn="b"
                    message("white said pass")
                else:
                    #turn="w"
                    message("black said pass")
                window=show_map(game_map, window_old=window, new_window=True)
            turn=ops_color(turn)

if __name__ == "__main__":
    sys.path.insert(1, '.')
    pygame.init()
    main("19_19_grid.txt",[],6,1,smart_pass=True)
    pygame.quit()