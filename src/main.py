# Importing necessary libraries and modules
import UI as inp
import pygame
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

# Initialize tkinter and withdraw its main window (used for file dialog)
Tk().withdraw()

# Encryption function definition
def encrypt(m,n,text):
    # Define lists of consonants and vowels for encryption
    consonants = ["B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Z"]
    vowels = ["A","E","I","O","U","Y"]

    # Initialize encrypted string
    encrypted = ""

    # Convert m and n values to integers
    m = int(m)
    n = int(n)

    # Iterate through each character in the text
    for character in text:
        # Check if the character is uppercase
        if character.isupper():
            upper = True
        else:
            upper = False

        # Encrypt consonants
        if character.upper() in consonants:
            # Find the index of the character in consonants list
            pos = consonants.index(character.upper())
            # Calculate the new position after shifting
            newpos = (pos + n) % len(consonants)
            # Append the encrypted character to the encrypted string
            if upper:
                encrypted += consonants[newpos]
            else:
                encrypted += consonants[newpos].lower()

        # Encrypt vowels
        elif character.upper() in vowels:
            # Find the index of the character in vowels list
            pos = vowels.index(character.upper())
            # Calculate the new position after shifting
            newpos = (pos - m) % len(vowels)
            # Append the encrypted character to the encrypted string
            if upper:
                encrypted += vowels[newpos]
            else:
                encrypted += vowels[newpos].lower()

        # Keep non-alphabet characters as they are
        else:
            encrypted += character

    # Return the encrypted string
    return encrypted

# Decryption function definition (inverse of encryption)
def decrypt(m, n, text):
    return encrypt((int(m)*-1),(int(n)*-1),text)

# Function to prompt user for m and n values
def takeinputs():
    valid = False
    while not valid:
        m = input("Choose an m value > ")
        n = input("Choose an n value > ")
        if m.isnumeric() and n.isnumeric():
            valid = True
        else:
            print("\nPlease choose integer values for both m and n\n")
    return int(m), int(n)

# Menu function for text-based interaction
def menu():
    valid_inputs = ["E", "e", "D", "d"]
    print("Choose an option:")
    print("Encrypt - [e]")
    print("Decrypt - [d]")
    option = input("> ")

    if option in valid_inputs:
        m, n = takeinputs()
        f = open("output.txt", "w")
        if option.upper() == "E":
            f.write(encrypt(m, n, "input.txt"))
            print("\nEncrypted!\n")
        elif option.upper() == "D":
            f.write(decrypt(m, n, "input.txt"))
            print("\nDecrypted!\n")
    else:
        print("\nPlease choose a valid option\n")
        menu()

# Alternate main function for a text-based interface
def main2():
    print("Rob Cipher\n")
    menu()

# Main function for the graphical interface
def main():
  background = (226, 147, 253)
  buttoncol = (0,162,232)
  buttoncol2 = (0,200,232)
  plaintextcol = (0,50,232)
  screen_width = 1200
  screen_height = 750
  infileshow = ""
  intext = ""
  outfile = ""
  outfileshow = ""
  toencrypt = True # encrypt or decrypt
  m = ""
  n = ""
  output = ""

  screen = pygame.display.set_mode((screen_width,screen_height))
  new = True
  pygame.display.set_caption("Rob Cipher")

  title = inp.Text(500,50,None,100,(0,0,0),True,screen)
  mvaltext = inp.Text(320,160,None,70,(0,0,0),True,screen)
  nvaltext = inp.Text(520,160,None,70,(0,0,0),True,screen)
  inpfiletext = inp.Text(300,440,None,40,(0,0,0),False,screen)
  outfiletext = inp.Text(800,440,None,40,(0,0,0),False,screen)

  key1 = inp.Key(50,260,None,80,(0,0,0),True,buttoncol2,screen)

  mbox = inp.Textbox(None,50,"M value",400,180,100,50,buttoncol,buttoncol2,(0,0,0),plaintextcol,10,False,screen)
  nbox = inp.Textbox(None,50,"N value",600,180,100,50,buttoncol,buttoncol2,(0,0,0),plaintextcol,10,False,screen)

  boxes = [mbox,nbox]
  
  down_arrow_img = pygame.image.load("Images\\arrowdown.png").convert_alpha()
  down_arrow1 = inp.image(920,320,down_arrow_img,200,0,screen)
  down_arrow2 = inp.image(50,320,down_arrow_img,200,0,screen)

  downarrows = [down_arrow1,down_arrow2]

  up_arrow_img = pygame.image.load("Images\\arrowup.png").convert_alpha()
  up_arrow1 = inp.image(920,320,up_arrow_img,200,0,screen)
  up_arrow2 = inp.image(50,320,up_arrow_img,200,0,screen)

  uparrows = [up_arrow1,up_arrow2]

  right_arrow_img = pygame.image.load("Images\\arrowright.png").convert_alpha()
  right_arrow = inp.image(500,640,right_arrow_img,60,0,screen)

  write_img_unpressed = pygame.image.load("Images\\Uwrite.png").convert_alpha()
  write_img_pressed = pygame.image.load("Images\\Pwrite.png").convert_alpha()
  write_img_hover = pygame.image.load("Images\\Hwrite.png").convert_alpha()

  encrypt_img_unpressed = pygame.image.load("Images\\Uencrypt.png").convert_alpha()
  encrypt_img_pressed = pygame.image.load("Images\\Pencrypt.png").convert_alpha()
  encrypt_img_hover = pygame.image.load("Images\\Hencrypt.png").convert_alpha()

  decrypt_img_unpressed = pygame.image.load("Images\\Udecrypt.png").convert_alpha()
  decrypt_img_pressed = pygame.image.load("Images\\Pdecrypt.png").convert_alpha()
  decrypt_img_hover = pygame.image.load("Images\\Hdecrypt.png").convert_alpha()

  input_img_unpressed = pygame.image.load("Images\\Uin.png").convert_alpha()
  input_img_hover = pygame.image.load("Images\\Hin.png").convert_alpha()

  output_img_unpressed = pygame.image.load("Images\\Uout.png").convert_alpha()
  output_img_hover = pygame.image.load("Images\\Hout.png").convert_alpha()

  encrypt_button = inp.Button(300,900, encrypt_img_unpressed,encrypt_img_hover,encrypt_img_pressed, 100, True, screen)
  decrypt_button = inp.Button(700,900, decrypt_img_unpressed,decrypt_img_hover,decrypt_img_pressed, 100, False, screen)
  write_button = inp.Button2(500,950, write_img_unpressed,write_img_hover,write_img_pressed, 50, screen)

  inp_file_button = inp.Button2(150,450, input_img_unpressed,input_img_hover,input_img_hover, 80, screen)
  out_file_button = inp.Button2(650,450, output_img_unpressed,output_img_hover,output_img_hover, 80, screen)

  inp_file_display = inp.FileDisplay(None,30,250,650,400,300,(0,0,0),(255,255,255),"Select a text file",screen)
  out_file_display = inp.FileDisplay(None,30,750,650,400,300,(100,100,100),(255,255,255),"",screen)

  fileDisplays = [out_file_display,inp_file_display]

  run = True

  while run:
      screen.fill(background)
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
            run = False

            for box in boxes:
              box.active = False

          for box in boxes:
            box.handle_event(event)
          for window in fileDisplays:
            window.handle_event(event)
          m = mbox.get_text()
          n = nbox.get_text()
          if m != "" and n != "":
            oroutput = output
            if toencrypt:
              output = encrypt(m,n,intext)
              out_file_display.split_text(output)
            else:
              output = decrypt(m,n,intext)
              out_file_display.split_text(output)
            if output != oroutput:
              out_file_display.text_col = (100,100,100)
          else:
            out_file_display.split_text("Choose an n and m value")

          key1.update_key(m,n)
  
      title.draw("Rob's Cipher",screen)
      mvaltext.draw("M:",screen)
      nvaltext.draw("N:",screen)
      inpfiletext.draw(infileshow,screen)
      outfiletext.draw(outfileshow,screen)
      for box in boxes:
        box.draw(screen)

      key1.draw(screen)

      if encrypt_button.draw(screen):
        toencrypt = True
        decrypt_button.deselect()
        if intext != "":
          if m != "" and n != "":
            out_file_display.split_text(encrypt(m,n,intext))
          else:
            out_file_display.split_text("Choose an n and m value")
        else:
          if m != "" and n != "":
            out_file_display.split_text("Select a text file")

      if decrypt_button.draw(screen):
        toencrypt = False
        encrypt_button.deselect()
        if intext != "":
          if m != "" and n != "":
            out_file_display.split_text(decrypt(m,n,intext))
          else:
            out_file_display.split_text("Choose an n and m value")
        else:
          if m != "" and n != "":
            out_file_display.split_text("Select a text file")

      if toencrypt:
        for image in downarrows:
          image.draw(screen)
      else:
        for image in uparrows:
          image.draw(screen)
      
      if inp_file_button.draw(screen):
        chosen = askopenfilename()
        if chosen.endswith(".txt"):
          infile = open(chosen,"r",encoding='UTF8')
          intext = infile.read()
          infile.close()
          inp_file_display.split_text(intext)
          if m != "" and n != "":
            if toencrypt:
              output = encrypt(m,n,intext)
              out_file_display.split_text(output)
            else:
              output = decrypt(m,n,intext)
              out_file_display.split_text(output)
          else:
            out_file_display.split_text("Choose an n and m value")
          infileshow =  os.path.basename(os.path.normpath(chosen))
        else:
          inp_file_display.split_text("Select a text file")
          out_file_display.split_text("Select a text file")


      if out_file_button.draw(screen):
        chosen = askopenfilename()
        if chosen.endswith(".txt"):
          outfile = chosen
          outfileshow =  os.path.basename(os.path.normpath(chosen))
          out_file_display.text_col = (100,100,100)
        else:
          pass

      right_arrow.draw(screen)

      inp_file_display.draw(screen)

      out_file_display.draw(screen)

      if write_button.draw(screen):
        if outfile != "":
          file1 = open(outfile,"w", encoding="UTF8")
          file1.write(output)
          file1.close()
          out_file_display.text_col = (0,0,0)
      pygame.display.update()

main()
