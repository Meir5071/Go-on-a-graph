import pygame
import pyperclip
import sys
def messege(string):
    pygame.init()
    
    width, height = 400, 300
    messege_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('messege')
    
    font = pygame.font.Font(None, 50)
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
class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White background
        self.text_color = (0, 0, 0)    # Black text
        self.font_size = height - 10    # Adjust font size based on height
        self.font = pygame.font.Font(None, self.font_size)
        self.text = ''
        self.cursor_pos = 0  # Cursor position in the text
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.cursor_timer, 500)  # Blink cursor every 500 ms

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.cursor_pos = len(self.text)  # Move cursor to end if activated
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    #print(self.text)  # Or handle text submission
                    #self.text = ''
                    #self.cursor_pos = 0
                    a=1
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                elif event.key in [pygame.K_LEFT, pygame.K_KP4]:
                    if self.cursor_pos > 0:
                        self.cursor_pos -= 1
                elif event.key in [pygame.K_RIGHT, pygame.K_KP6]:
                    if self.cursor_pos < len(self.text):
                        self.cursor_pos += 1
                else:
                    self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
                if (event.key == pygame.K_INSERT or event.key == pygame.K_KP0) and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    clipboard_text = pyperclip.paste()
                    self.text = self.text[:self.cursor_pos] + clipboard_text + self.text[self.cursor_pos:]
                    self.cursor_pos += len(clipboard_text)

        if event.type == self.cursor_timer:
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        # Draw the text box
        pygame.draw.rect(screen, self.color, self.rect)

        # Calculate text surface
        text_surface = self.font.render(self.text, True, self.text_color)

        # Center the text vertically but align it to the left
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        text_rect = text_surface.get_rect(topleft=(self.rect.x + 5, text_y))

        # Draw the cursor if active
        if self.cursor_visible and self.active:
            cursor_x = self.rect.x + 5 + self.font.size(self.text[:self.cursor_pos])[0]
            pygame.draw.line(screen, self.text_color, (cursor_x, self.rect.y + 5), (cursor_x, self.rect.y + self.rect.height - 5), 2)

        # Draw the text
        screen.blit(text_surface, text_rect)

# Example usage
class Button:
    def __init__(self, x, y, width, height, text, callback, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 200, 100)  # Default color (green)
        self.hover_color = (150, 250, 150)  # Color when hovered (light green)
        self.text_color = (0, 0, 0)  # Text color (black)
        self.font = pygame.font.Font(None, font_size)  # Font size
        self.text = text
        self.callback = callback  # Function to call when clicked
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
            else:
                self.is_hovered = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:  # Left mouse button
                self.callback()

    def draw(self, screen):
        # Draw the button
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Checkbox:
    def __init__(self, x, y, width, height, color, checked=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.checked = checked

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if self.checked:
            pygame.draw.rect(screen, self.color, self.rect, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
class Label:
    def __init__(self, x, y, text, font_size, font_color, bg_color=None):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.bg_color = bg_color

        self.font = pygame.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, True, self.font_color, self.bg_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.font_color, self.bg_color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Text Box Example")
    clock = pygame.time.Clock()

    text_box = TextBox(50, 100, 400, 50)
    button = Button(250, 150, 100, 50, "Click Me", button_callback, 36)
    checkbox = Checkbox(200, 220, 20, 20, (255, 255, 255))
    label = Label(300, 230, "Hello, World!", 36, (255, 255, 255))

    # Enable key repeat
    pygame.key.set_repeat(400, 100)  # Delay in ms before repeat, then repeat every 50 ms

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            text_box.handle_event(event)
            button.handle_event(event)
            checkbox.handle_event(event)

        screen.fill((30, 30, 30))  # Clear the screen with a dark color
        text_box.draw(screen)
        button.draw(screen)
        checkbox.draw(screen)
        label.draw(screen)
        pygame.display.flip()
        clock.tick(30)
# Example usage
def button_callback():
    print("Button clicked!")

if __name__ == "__main__":
    main()
