#from time import wait
import pygame
import pygame.locals
from pygame._sdl2 import Window
import sys
#sys.path.insert(1, '.')
def ops_color(color):
    if color=="w":
        return("b")
    else:
        return("w")

class graph:
    def __init__(self,file_path):
        file=open(file_path)
        global X
        global Y
        global x_w
        global y_w
        global r
        global w_v
        global w_e
        X=int(file.readline()[:-1])
        Y=int(file.readline()[:-1])
        x_w=int(file.readline()[:-1])
        y_w=int(file.readline()[:-1])
        r=int(file.readline()[:-1])
        w_v=int(file.readline()[:-1])
        w_e=int(file.readline()[:-1])
        file.readline()
        file_str=file.read()
        file.close()
        vert_spl=file_str.split("\nedges\n")[0].split("\n")
        edge_spl=file_str.split("\nedges\n")[1].split("\n")
        self.vertices=[]
        self.edges=[]
        for vert in vert_spl:
            self.vertices+=[[int(vert.split(",")[0]),int(vert.split(",")[1]),"e"]]
        for edge in edge_spl:
            self.edges+=[[int(edge.split(",")[0]),int(edge.split(",")[1])]]
        #self.vertices=[[0,0,"e"],[0,100,"e"],[0,200,"e"],[100,0,"e"],[100,100,"e"],[100,200,"e"],[200,0,"e"],[200,100,"e"],[200,200,"e"]]
        #self.edges=[[0,1],[1,2],[0,3],[3,4],[4,5],[1,4],[2,5],[3,6],[6,7],[7,8],[4,7],[5,8]]
        self.negihbors_list=[self.find_negihbors(i) for i in range(len(self.vertices))]
    def find_negihbors(self,point_index):
        negihbors=[]
        for edge in self.edges:
            if edge[0]==point_index:
                negihbors+=[edge[1]]
            elif edge[1]==point_index:
                negihbors+=[edge[0]]
        return list(set(negihbors))
    def find_negihbors_of_list(self,point_indexs):
        negihbors=[]
        for point_index in point_indexs:
            for negihbor in self.negihbors_list[point_index]:
                    if (not(negihbor in point_indexs)):
                        negihbors+=[negihbor]
        return list(set(negihbors))
    def find_same_color_negihbors_of_list(self,point_indexs,color,found_points):
        negihbors=[]
        for point_index in point_indexs:
            for negihbor in self.negihbors_list[point_index]:
                    if (self.vertices[negihbor][2]==color) and (not(negihbor in found_points)):
                        negihbors+=[negihbor]
        return list(set(negihbors))
    def find_componnent(self,point_index):
        comp=[]
        addition=[point_index]
        while True:
            comp+=addition
            addition=self.find_same_color_negihbors_of_list(addition,self.vertices[point_index][2],comp)
            if addition==[]:
                return comp
    def kill(self,color):
        to_kill_list=[0 for _ in range(len(self.vertices))]
        for i in range(len(self.vertices)):
            if (to_kill_list[i]==0) and (self.vertices[i][2]==color):
                to_kill_comp=True
                comp=self.find_componnent(i)
                for vert_ind in self.find_negihbors_of_list(comp):
                    to_kill_comp=(to_kill_comp)and(not(self.vertices[vert_ind][2]=="e"))
                if to_kill_comp:
                    for vert_ind in comp:
                        to_kill_list[vert_ind]=1
                else:
                    for vert_ind in comp:
                        to_kill_list[vert_ind]=2
        for i in range(len(self.vertices)):
            if to_kill_list[i]==1:
                self.vertices[i]=self.vertices[i][0:2]+["e"]
                #pygame.draw.circle(window, (255, 255, 0), [x_w+self.vertices[i][0], y_w+self.vertices[i][1]], r-w, 0)
def show_map(game_map):
    window = pygame.display.set_mode((X, Y))
    # set the pygame window name
    pygame.display.set_caption('Go on a graph')
    window.fill((255, 255, 0))
    for edge in game_map.edges:
        pygame.draw.line(window, (0, 0, 255), [x_w+game_map.vertices[edge[0]][0], y_w+game_map.vertices[edge[0]][1]], [x_w+game_map.vertices[edge[1]][0], y_w+game_map.vertices[edge[1]][1]], w_e)
    for vert in game_map.vertices:
        pygame.draw.circle(window, (0, 0, 255), [x_w+vert[0], y_w+vert[1]], r, w_v)
        if vert[2]=="e":
            pygame.draw.circle(window, (255, 255, 0), [x_w+vert[0], y_w+vert[1]], r-w_v+1, 0)
        elif vert[2]=="b":
            pygame.draw.circle(window, (0, 0, 0), [x_w+vert[0], y_w+vert[1]], r-w_v+1, 0)
        elif vert[2]=="w":
            pygame.draw.circle(window, (255, 255, 255), [x_w+vert[0], y_w+vert[1]], r-w_v+1, 0)
    pygame.display.flip()
    return window
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
    status_2=False
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
    status_2=True
    #show_map()
    #pygame.quit()
def main(file_name):
    game_map=graph(file_name)
    pygame.init()
    clock = pygame.time.Clock()

    
    # create the display surface object
    # of specific dimension..e(X, Y).
    #window = pygame.display.set_mode((X, Y))
    window=show_map(game_map)
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
    windows = [window]
    window_p = Window.from_display_module()
    pos = window_p.position[:]
    history=[str(game_map.vertices)]
    while (status):
        if pos != window_p.position[:]:
            pos = window_p.position[:]
            show_map(game_map)
        for event in pygame.event.get():
            #show_map(game_map)
            if event.type == pygame.QUIT:
                status = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) and status_2:
                for i in range(len(game_map.vertices)):
                    if r*r>((x_w+game_map.vertices[i][0]-event.pos[0])**2+(y_w+game_map.vertices[i][1]-event.pos[1])**2) and (game_map.vertices[i][2]=="e"):
                        ver2=game_map.vertices[:]
                        game_map.vertices[i][2]=turn
                        game_map.kill(ops_color(turn))
                        ver=game_map.vertices[:]
                        game_map.kill(turn)
                        if ver==game_map.vertices:
                            if str(game_map.vertices) in history:
                                messege("Ko")
                                game_map.vertices=ver2
                                game_map.vertices[i][2]="e"
                            else:
                                pas=0
                                turn=ops_color(turn)
                                history.append(str(game_map.vertices))
                        else:
                            game_map.vertices=ver
                            game_map.vertices[i][2]="e"
                            messege("suicidal move")
                        show_map(game_map)
            elif (event.type == pygame.KEYUP) and status_2:
                if event.key == pygame.K_p:
                    pas+=1
                    if turn=="w":
                        turn="b"
                        messege("white said pass")
                    else:
                        turn="w"
                        messege("black said pass")
                    show_map(game_map)
        if (pas>1) and (status_2):
            status_2=False
            white=0
            black=0
            count_list=[0 for vert in game_map.vertices]
            for i in range(len(count_list)):
                if (count_list[i]==0):
                    if game_map.vertices[i][2]=="e":
                        comp=game_map.find_componnent(i)
                        comp_color=game_map.vertices[game_map.find_negihbors_of_list(comp)[0]][2]
                        for vert_ind in game_map.find_negihbors_of_list(comp):
                            if not(game_map.vertices[vert_ind][2]==comp_color):
                                comp_color="e"
                        for vert_ind in comp:
                            count_list[vert_ind]=comp_color
                            if True:
                                game_map.vertices[vert_ind][2]=comp_color
                    else:
                        count_list[i]=game_map.vertices[i][2]
            for a in count_list:
                if a=="w":
                    white+=1
                elif a=="b":
                    black+=1
            if black>white:
                messege("Black won!\nblack:"+str(black)+"  white:"+str(white))
            elif black<white:
                messege("White won!\nblack:"+str(black)+"  white:"+str(white))
            else:
                messege("Draw!\nBlack:"+str(black)+"  White:"+str(white))
            show_map(game_map)
        clock.tick(60)
if __name__ == "__main__":
    sys.path.insert(1, '.')
    main("19_19_grid.txt")