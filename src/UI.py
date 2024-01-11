import pygame
import string
from time import sleep
import threading
pygame.init()

class Button():
    # Initialize button with position, images for different states, scale, selection state, and screen
    def __init__(self, x, y, image, image_hover, image_selected, scale, selected, screen):
        # Screen dimensions and scaling factors
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.domsc = min(self.sheight, self.swidth)

        # Scale images for button states
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        self.image_hover = pygame.transform.scale(image_hover, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        self.image_select = pygame.transform.scale(image_selected, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))

        # Adjust size and position
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (((x * self.swidth / 1000) - (self.width / 2)), ((y * self.sheight / 1000) - (self.height / 2)))

        # Button state variables
        self.clicked = False
        self.selected = selected

    # Draw button on screen and handle click events
    def draw(self, surface):
        image = self.image
        action = False
        pos = pygame.mouse.get_pos()

        # Change image on hover and handle click
        if self.rect.collidepoint(pos):
            image = self.image_hover
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                self.selected = True

        # Change image if button is selected
        if self.selected:
            image = self.image_select

        # Reset click state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button image
        surface.blit(image, (self.rect.x, self.rect.y))
        return action

    # Deselect the button
    def deselect(self):
        self.selected = False


class Button2():
    # Button2 is similar to Button but without a selected state
    def __init__(self, x, y, image, image_hover, image_selected, scale, screen):
        # Initialization similar to Button class
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.domsc = min(self.sheight, self.swidth)
        # Scaling of images
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        self.image_hover = pygame.transform.scale(image_hover, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        self.image_select = pygame.transform.scale(image_selected, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        # Adjusting position and size
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (((x * self.swidth / 1000) - (self.width / 2)), ((y * self.sheight / 1000) - (self.height / 2)))
        # State variable for click detection
        self.clicked = False

    # Draw the button and handle interactions
    def draw(self, surface):
        image = self.image
        action = False
        pos = pygame.mouse.get_pos()

        # Handle hover and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.clicked:
                    self.clicked = True
                    action = True
                    image = self.image_select
            else:
                image = self.image_hover

        # Reset click state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button image
        surface.blit(image, (self.rect.x, self.rect.y))
        return action

class Textbox:
    # Textbox for user input
    def __init__(self, font, font_size, empty_text, x, y, width, height, active_colour, passive_colour, active_text, inactive_text, buffer, hidden, screen):
        # Initializing textbox properties
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.base_font = pygame.font.Font(font, font_size * self.sheight // 1000)
        self.default = empty_text
        self.rect = pygame.Rect((x - (width / 2)) * self.swidth / 1000, (y - (height / 2)) * self.sheight / 1000, width * self.swidth / 1000, height * self.sheight / 1000)
        self.end_buffer = pygame.Rect(((x + width - buffer) - (width / 2)) * self.swidth / 1000, (y - (height / 2)) * self.sheight / 1000, buffer, height * self.sheight / 1000)
        self.active_colour = active_colour
        self.passive_colour = passive_colour
        self.usertext = ""
        self.active = False
        self.active_text = active_text
        self.inactive_text = inactive_text
        self.hidden = hidden
        # Cursor setup
        self.cursor = pygame.Rect((self.rect.topright), (3, self.rect.height - 10))
        self.cursorposition = 0
        self.cursorshow = True
        self.thread_running = False

    # Handle keyboard and mouse events
    def handle_event(self, event):
        # Keyboard events for text manipulation
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    # Backspace handling
                    self.usertext = self.usertext[:(max(0, self.cursorposition - 1))] + self.usertext[self.cursorposition:]
                    self.cursorposition = max(0, self.cursorposition - 1)
                elif event.key == pygame.K_DELETE:
                    # Delete key handling
                    self.usertext = self.usertext[:self.cursorposition] + self.usertext[(min(len(self.usertext), self.cursorposition + 1)):]
                elif event.key == pygame.K_LEFT:
                    # Move cursor left
                    self.cursorposition = max(0, self.cursorposition - 1)
                elif event.key == pygame.K_RIGHT:
                    # Move cursor right
                    self.cursorposition = min(len(self.usertext), self.cursorposition + 1)
                else:
                    # Add typed character
                    if event.unicode.isnumeric() and len(self.usertext) < 6:
                        self.usertext = (self.usertext[:self.cursorposition] + event.unicode + self.usertext[self.cursorposition:])
                        self.cursorposition = min(len(self.usertext), self.cursorposition + 1)

        # Mouse event for textbox focus
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if self.rect.collidepoint(pos):
                self.active = True
            else:
                self.active = False
            self.cursorposition = len(self.usertext)

    # Draw the textbox on the screen
    def draw(self, screen):
        if self.active:
            # Start cursor flicker thread if not already running
            cursorflicker = threading.Thread(target=self.cursorflicker, args=(0.5,))
            if not self.thread_running:
                cursorflicker.start()
            colour = self.active_colour
            text_colour = self.active_text
            active_text = "".join(["*" if self.hidden else char for char in self.usertext[:self.cursorposition]])
        else:
            colour = self.passive_colour
            text_colour = self.inactive_text
            active_text = self.default if self.usertext == "" else "".join(["*" if self.hidden else char for char in self.usertext])

        # Render text and cursor
        text_surfacel = self.base_font.render(active_text, True, text_colour)
        pygame.draw.rect(screen, colour, self.rect)
        screen.blit(text_surfacel, (self.rect.x + 5, self.rect.y + 5))
        split = text_surfacel.get_rect(topleft=(self.rect.x + 3, self.rect.y + 5))
        self.cursor.midleft = split.midright
        if self.cursorshow and self.active:
            pygame.draw.rect(screen, self.active_text, self.cursor)
        pygame.draw.rect(screen, colour, self.end_buffer)

    # Thread for cursor flickering effect
    def cursorflicker(self, secs):
        self.thread_running = True
        while self.active:
            sleep(secs)
            self.cursorshow = not self.cursorshow
        self.thread_running = False

    # Return the current text in the textbox
    def get_text(self):
        return str(self.usertext)

    # Clear the textbox content
    def clear(self):
        self.usertext = ""
        self.cursorposition = 0

class image():
    # Image class for displaying static images
    def __init__(self, x, y, image, scale, scaley, screen):
        # Screen dimensions and scaling factors
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.width = image.get_width()
        self.height = image.get_height()
        self.domscale = min(self.sheight,self.swidth)
        

        # Scale the image
        if scaley == 0:
            self.image = pygame.transform.scale(image, (int(self.width * scale * self.domscale / 100000), int(self.height * scale * self.domscale / 100000)))
        else:
            self.image = pygame.transform.scale(image, (int(self.swidth * scale / 1000), int(self.sheight * scaley / 1000)))

        # Adjust size and position
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (((x * self.swidth / 1000) - (self.width / 2)), ((y * self.sheight / 1000) - (self.height / 2)))

    # Draw the image on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

"""class image():
    def __init__(self,x,y,image,scale,scaley,screen):
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.width = image.get_width()
        self.height = image.get_height()
        self.domscale = min(self.sheight,self.swidth)
        if scaley == 0:
            self.image = pygame.transform.scale(image,(int(self.width*scale*self.domscale/100000),int(self.height*scale*self.domscale/100000)))
        else:
            self.image = pygame.transform.scale(image,(int(self.swidth*scale/1000),int(self.sheight*scaley/1000)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (((x*self.swidth/1000)-(self.width/2)),((y*self.sheight/1000)-(self.height/2)))
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))
"""
class background:
    # Background class for setting the background image
    def __init__(self, image, screen):
        # Scale the image to fit the screen
        self.image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))

    # Draw the background image
    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Key:
    # Key class for displaying a dynamic keyboard layout
    def __init__(self, x, y, font, size, colour, mid, rectcol, screen):
        # Initialize key properties
        self.mid = mid
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.base_font = pygame.font.Font(font, size * self.sheight // 1000)
        self.colour = colour
        self.x = x * self.swidth / 1000
        self.y = y * self.sheight / 1000
        self.key = []
        self.rectcol = rectcol
        self.rect = pygame.Rect(80 * self.swidth / 1000, 250 * self.sheight / 1000, (810 * self.swidth) / 1000, 150 * self.sheight / 1000)

    # Draw the keyboard layout
    def draw(self, screen):
        # Draw rectangle for key background
        pygame.draw.rect(screen, self.rectcol, self.rect)
        # Render each key
        for i in range(26):
            pos = i - 13
            # Render the mapped key
            text_surfacekey = self.base_font.render(self.key[i], True, self.colour)
            widthkey = text_surfacekey.get_width()
            screen.blit(text_surfacekey, (((600 - (widthkey / 2)) + (31 * pos) * self.swidth / 1000), self.y + 50))
            # Render the actual key
            text_surfacealpha = self.base_font.render(list(string.ascii_uppercase)[i], True, self.colour)
            widthalpha = text_surfacealpha.get_width()
            screen.blit(text_surfacealpha, (((600 - (widthalpha / 2)) + (31 * pos) * self.swidth / 1000), self.y))

    # Update the keys based on encryption settings
    def update_key(self, m, n):
        consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Z"]  # list of consonants
        vowels = ["A", "E", "I", "O", "U", "Y"]  # list of vowels
        alphabet = list(string.ascii_uppercase)
        self.key = []
        if m != "" and n != "":
            m = int(m)
            n = int(n)
            # Map each letter based on cipher rules
            for character in alphabet:
                if character in consonants:
                    pos = consonants.index(character)
                    newpos = (pos + n) % len(consonants)
                    self.key += consonants[newpos]
                elif character in vowels:
                    pos = vowels.index(character)
                    newpos = (pos - m) % len(vowels)
                    self.key += vowels[newpos]
        else:
            self.key = alphabet

class Text:
    # Text class for displaying static text
    def __init__(self, x, y, font, size, colour, mid, screen):
        # Initialize text properties
        self.mid = mid
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.base_font = pygame.font.Font(font, size * self.sheight // 1000)
        self.colour = colour
        self.x = x * self.swidth / 1000
        self.y = y * self.sheight / 1000

    # Draw the text on the screen
    def draw(self, text, screen):
        # Render the text
        text_surface = self.base_font.render(text, True, self.colour)
        if self.mid:
            # Center text if mid flag is set
            width = text_surface.get_width()
            screen.blit(text_surface, (self.x - (width / 2), self.y))
        else:
            screen.blit(text_surface, (self.x, self.y))

class FileDisplay:
    # FileDisplay class for showing file content or messages
    def __init__(self, font, font_size, x, y, width, height, text_col, back_col, text, screen):
        # Initialize file display properties
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.height = height
        self.width = width
        self.base_font = pygame.font.Font(font,font_size*self.sheight//1000)
        self.rect=pygame.Rect((x-(width/2))*self.swidth/1000,(y-(height/2))*self.sheight/1000,width*self.swidth/1000,height*self.sheight/1000)
        self.outrect=pygame.Rect(((x-(width/2))*self.swidth/1000)-(self.base_font.get_height()),((y-(height/2))*self.sheight/1000)-(self.base_font.get_height()),(width*self.swidth/1000)+(2*self.base_font.get_height()),(height*self.sheight/1000)+(2*self.base_font.get_height()))
        self.width = self.rect.width
        self.active = False
        self.back_col = back_col
        self.text_col = text_col
        self.y_offset = 0
        self.running = True
        
        self.lines = []
        self.split_text(text)
        self.scrolled = len(self.lines)#-4

    # Handle keyboard and mouse events for scrolling
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            # Scroll up or down
            if event.key == pygame.K_UP and self.scrolled > 0:
                self.y_offset += self.base_font.get_height()
                self.scrolled -= 1
            elif event.key == pygame.K_DOWN and self.scrolled < len(self.lines) - 3:
                self.y_offset -= self.base_font.get_height()
                self.scrolled += 1

        # Activate or deactivate on mouse click
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            self.active = self.rect.collidepoint(pos)

    # Split input text into lines for display
    def split_text(self, text):
        self.lines = []
        words = text.split()
        while words:
            line_words = []
            while words:
                line_words.append(words.pop(0))
                fw, fh = self.base_font.size(' '.join(line_words + words[:1]))
                if fw > self.width:
                    break
            line = ' '.join(line_words)
            self.lines.append(line)

    # Draw the file content or message
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        fw,fh = self.base_font.size("line")
        y_off = 0 #(max(0,((len(self.lines)-4)*fh)))*-1
        for line in self.lines:
            ty = self.rect.y + self.y_offset + y_off + 10
            tx = self.rect.x + 3
            font_surface = self.base_font.render(line,True,self.text_col)
            line = font_surface.get_rect(topleft = (tx,ty))
            linetop = line.top
            linebot = line.bottom
            if linebot < self.rect.bottom and linetop > self.rect.top - 5:
                screen.blit(font_surface,(tx,ty))
            y_off+=fh