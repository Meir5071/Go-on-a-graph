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
                pygame.quit()
                pygame.init()
                screen = pygame.display.set_mode((400, 275))
                pygame.display.set_caption("Go on a graph")
                button_go = Button(100, 25, 200, 100, "Play", prep_run_go, 30)
                button_v_e = Button(100, 150, 200, 100, "Create a map", prep_run_v_e,30)
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
    #pygame.quit()
    #pygame.init()
    messege("Close this window. Then enter the path of the map. The default is 19X19.")
    screen = pygame.display.set_mode((1000, 200))
    pygame.display.set_caption("Go on a graph")
    clock = pygame.time.Clock()

    #text_box = TextBox(50, 100, 400, 50)
    text_box = TextBox(50, 25, 900, 25)
    button = Button(775, 75, 200, 100, "Play", lambda: play(text_box.text, bot_ck.checked, bot_color_tb.text, bot_difficulty_tb.text,turn_delay_tb.text,smart_pass=smart_pass_ck.checked), 30)
    bot_ck=Checkbox(50,55,15,15, white)
    bot_lb=Label(175, 63, "Play against the computer", 25, white)
    bot_color_lb = Label(240, 85, "Computer color (black, white or both):", 25, white)
    bot_color_tb = TextBox(400, 72, 40, 25)
    bot_difficulty_lb = Label(167, 110, "Computer difficulty:", 25, white)
    bot_difficulty_tb = TextBox(254, 99, 40, 25)
    turn_delay_lb = Label(170, 160, "Turn delay (seconds):", 25, white)
    turn_delay_tb = TextBox(260, 150, 40, 25)
    smart_pass_ck=Checkbox(85,126,15,15, white)
    smart_pass_lb=Label(390, 135, "The computer will try to win and not get the maximal score difference", 25, white)
    #button_v_e = Button(100, 150, 200, 100, "Create a map", run_v_e,30)

    # Enable key repeat
    pygame.key.set_repeat(400, 100)  # Delay in ms before repeat, then repeat every 50 ms
    running=True
    text_box.text="19_19_grid.txt"
    bot_difficulty_tb.text="2"
    bot_color_tb.text="white"
    turn_delay_tb.text="2"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                running=False
            text_box.handle_event(event)
            button.handle_event(event)
            if not running:
                return
            bot_ck.handle_event(event)
            if bot_ck.checked:
                bot_color_tb.handle_event(event)
                bot_difficulty_tb.handle_event(event)
                smart_pass_ck.handle_event(event)
                if bot_color_tb.text=="both":
                    turn_delay_tb.handle_event(event)
        screen.fill((30, 30, 30))  # Clear the screen with a dark color
        text_box.draw(screen)
        button.draw(screen)
        bot_ck.draw(screen)
        bot_lb.draw(screen)
        if bot_ck.checked:
            bot_color_lb.draw(screen)
            bot_color_tb.draw(screen)
            bot_difficulty_lb.draw(screen)
            bot_difficulty_tb.draw(screen)
            smart_pass_ck.draw(screen)
            smart_pass_lb.draw(screen)
            if bot_color_tb.text=="both":
                turn_delay_lb.draw(screen)
                turn_delay_tb.draw(screen)

        pygame.display.flip()
        clock.tick(30)
def play(path,bot_exists,bot_colors_str,bot_level,turn_delay,smart_pass):
    global to_show
    to_show=True
    global running
    running=False
    #pygame.quit()
    #pygame.init()
    if bot_exists:
        if bot_colors_str=="black":
            bot_colors=["b"]
        elif bot_colors_str=="white":
            bot_colors=["w"]
        elif  bot_colors_str=="both":
            bot_colors=["b","w"]
        else:
            bot_colors=[]
        go.main(path,bot_colors,int(bot_level),int(turn_delay),smart_pass=smart_pass)
    else:
        go.main(path,[],0,0)
    #pygame.quit()
    #pygame.init()
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
            if not running:
                return

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
    #pygame.quit()
    #pygame.init()
    if to_load:
        m=v_e.load(load_file)
        if m=="error":
            return
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
    #pygame.quit()
    #pygame.init()
    #not working!!??
if __name__ == "__main__":
    main()