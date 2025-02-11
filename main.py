import pygame
import sys
sys.path.insert(1, '.')
import go
import visoul_editor as v_e
from interactive_things import Button,TextBox,messege,Checkbox,Label
to_show=False
white=(255,255,255)
def main():
    global to_show
    pygame.init()
    screen = pygame.display.set_mode((400, 275))
    pygame.display.set_caption("Go on a graph")
    clock = pygame.time.Clock()

    #text_box = TextBox(50, 100, 400, 50)
    button_go = Button(100, 25, 200, 100, "Play", prep_run_go, 30)
    button_v_e = Button(100, 150, 200, 100, "Create a map", prep_run_v_e,30)

    # Enable key repeat
    #pygame.key.set_repeat(200, 100)  # Delay in ms before repeat, then repeat every 50 ms

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #text_box.handle_event(event)
            button_go.handle_event(event)
            button_v_e.handle_event(event)
        if to_show:
            screen = pygame.display.set_mode((400, 275))
            pygame.display.set_caption("Go on a graph")
            to_show=False

        screen.fill((30, 30, 30))  # Clear the screen with a dark color
        #text_box.draw(screen)
        button_go.draw(screen)
        button_v_e.draw(screen)
        pygame.display.flip()
        clock.tick(30)
def prep_run_go():
    global to_show
    global running
    to_show=True
    #pygame.init()
    messege("Close this window.\nThen enter the path\nof the map.\nThe default is 19X19.")
    screen = pygame.display.set_mode((1000, 200))
    pygame.display.set_caption("Go on a graph")
    clock = pygame.time.Clock()

    #text_box = TextBox(50, 100, 400, 50)
    text_box = TextBox(50, 25, 900, 25)
    button = Button(775, 75, 200, 100, "Play", lambda: play(text_box.text), 30)
    #button_v_e = Button(100, 150, 200, 100, "Create a map", run_v_e,30)

    # Enable key repeat
    pygame.key.set_repeat(400, 100)  # Delay in ms before repeat, then repeat every 50 ms
    running=True
    text_box.text="19_19_grid.txt"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                running=False
            text_box.handle_event(event)
            button.handle_event(event)

        screen.fill((30, 30, 30))  # Clear the screen with a dark color
        text_box.draw(screen)
        button.draw(screen)
        pygame.display.flip()
        clock.tick(30)
def play(path):
    global to_show
    to_show=True
    global running
    running=False
    go.main(path)
def prep_run_v_e():
    global to_show
    global running
    to_show=True
    #pygame.init()
    #messege("Close this window.\nThen enter the path\nof the map.\nThe default is 19X19.")
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption("Go on a graph")
    clock = pygame.time.Clock()

    #text_box = TextBox(50, 100, 400, 50)
    map_file_lb = Label(100, 25, "Enter map name:", 25, white)
    map_file_tb = TextBox(50, 50, 900, 25)
    to_read_lb = Label(160, 100, "Edit an existing map", 25, white)
    to_read_ck = Checkbox(50, 90, 15, 15, white)
    read_file_lb = Label(135, 150, "Enter source map name:", 25, white)
    read_file_tb = TextBox(50, 175, 900, 25)
    to_cre_sizes_lb = Label(510, 225, "Create new setinigs (if you will leave an empty parameter it will be replaced with the parameter from the loaded map)", 25, white)
    to_cre_sizes_ck = Checkbox(10, 215, 15, 15, white)
    width_lb = Label(65, 275, "Width:", 25, white)
    width_tb = TextBox(95, 265, 200, 25)
    width_tb.text="600"
    height_lb = Label(70, 305, "Height:", 25, white)
    height_tb = TextBox(105, 295, 200, 25)
    height_tb.text="600"
    cell_radius_lb = Label(85, 335, "Cell radius:", 25, white)
    cell_radius_tb = TextBox(135, 325, 200, 25)
    cell_radius_tb.text="10"
    cell_boundery_width_lb = Label(125, 365, "Cell boundery width:", 25, white)
    cell_boundery_width_tb = TextBox(215, 355, 200, 25)
    cell_boundery_width_tb.text="3"
    edge_width_lb = Label(85, 395, "Edge width:", 25, white)
    edge_width_tb = TextBox(135, 385, 200, 25)
    edge_width_tb.text="3"
    button = Button(775, 375, 150, 75, "Create map", lambda: run_v_e(to_read_ck.checked,read_file_tb.text,width_tb.text,height_tb.text,cell_radius_tb.text,cell_boundery_width_tb.text,edge_width_tb.text,map_file_tb.text,to_cre_sizes_ck.checked), 25)
    #button_v_e = Button(100, 150, 200, 100, "Create a map", run_v_e,30)

    # Enable key repeat
    pygame.key.set_repeat(400, 50)  # Delay in ms before repeat, then repeat every 50 ms
    running=True
    #text_box.text="19_19_grid.txt"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                running=False
            map_file_tb.handle_event(event)
            to_read_ck.handle_event(event)
            if to_read_ck.checked:
                read_file_tb.handle_event(event)
                to_cre_sizes_ck.handle_event(event)
            if to_cre_sizes_ck.checked or not(to_read_ck.checked):
                width_tb.handle_event(event)
                height_tb.handle_event(event)
                cell_radius_tb.handle_event(event)
                cell_boundery_width_tb.handle_event(event)
                edge_width_tb.handle_event(event)
            button.handle_event(event)

        screen.fill((30, 30, 30))  # Clear the screen with a dark color
        map_file_lb.draw(screen)
        map_file_tb.draw(screen)
        to_read_lb.draw(screen)
        to_read_ck.draw(screen)
        if to_read_ck.checked:
            read_file_lb.draw(screen)
            read_file_tb.draw(screen)
            to_cre_sizes_lb.draw(screen)
            to_cre_sizes_ck.draw(screen)
        if to_cre_sizes_ck.checked or not(to_read_ck.checked):
            width_tb.draw(screen)
            width_lb.draw(screen)
            height_tb.draw(screen)
            height_lb.draw(screen)
            cell_radius_tb.draw(screen)
            cell_radius_lb.draw(screen)
            cell_boundery_width_tb.draw(screen)
            cell_boundery_width_lb.draw(screen)
            edge_width_tb.draw(screen)
            edge_width_lb.draw(screen)
        button.draw(screen)
        pygame.display.flip()
        clock.tick(30)
def run_v_e(to_load:bool,load_file:str,X:str,Y:str,r,w_v:str,w_e:str,file_n:str,to_change:bool)->None:
    if to_load:
        v_e.load(load_file)
        if to_change:
            if X=="":
                X_s=None
            else:
                X_s=int(X)
            if Y=="":
                Y_s=None
            else:
                Y_s=int(Y)
            if r=="":
                r_s=None
            else:
                r_s=int(r)
            if w_v=="":
                w_v_s=None
            else:
                w_v_s=int(w_v)
            if w_e=="":
                w_e_s=None
            else:
                w_e_s=int(w_e)
            v_e.set_attributs(X=X_s,Y=Y_s,r=r_s,w_v=w_v_s,w_e=w_e_s,file_n=file_n)
    else:
        v_e.set_attributs(X=int(X),Y=int(Y),r=int(r),w_v=int(w_v),w_e=int(w_e),vert=[],edg=[],file_n=file_n)
    v_e.main()
    global to_show
    to_show=True
    global running
    running=False
    #not working!!??
if __name__ == "__main__":
    main()