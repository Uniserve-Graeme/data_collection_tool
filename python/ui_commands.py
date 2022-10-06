import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime   # For getting time and date info
import pygame
import random
from sys import exit
import os


def run_and_log(command):
    '''
    This function is intended to simplify code writing as it compresses the execution, logging, and decoding of
    all console outputs from given operating system commands into one line, now one function.
    :param command: the input command
    :return: Returns the log
    '''
    result = subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read().decode("utf-8").replace("\r", "")
    return result


def release_and_renew_ip(os):
    '''
    Release and renews DHCP IP, also resets windows sockets. If this is NOT windows, it passes plain text to the log.
    :param os: operating system of the machine currently running the program
    :return: Returns console logs of the commands to be exported into the final log file
    '''
    if os != 'windows':
        release_result = "\nRelease command passed: Unix requires sudo"
        renew_result = "\nRenew command passed: Unix requires sudo"
        netsh_result = "\nNetsh command passed: Unix requires sudo"
    else:
        release_command = ['ipconfig', '/release']  # release current IP
        renew_command = ['ipconfig', '/renew']  # renew DHCP IP lease
        netsh_command = ['netsh', 'winsock', 'reset']   # resets the windows network socket system

        release_result = run_and_log(release_command)  # executes and logs the command to the defined variable
        time.sleep(5)   # wait 5 seconds
        renew_result = run_and_log(renew_command)  # executes and logs the command to the defined variable
        time.sleep(5)   # wait 5 seconds
        netsh_result = run_and_log(netsh_command)  # executes and logs the command to the defined variable
    return release_result, renew_result, netsh_result


def flush_and_register_dns(os):
    '''
    Flushes and registers fresh DNS cache. If this is NOT windows, it passes plain text to the log.
    :param os: operating system of the machine currently running the program
    :return: Returns console logs of the commands to be exported into the final log file
    '''
    if os != 'windows':
        flush_result = "\nDNS flush command passed as system is Unix based and requires sudo"
        register_result = "\nDNS registration command passed as system is Unix based and requires sudo"
    else:
        flush_command = ['ipconfig', '/flushdns']  # flushes current DNS
        register_command = ['ipconfig', '/registerdns']  # requests windows to reapply DNS to all adapters

        flush_result = run_and_log(flush_command)  # executes and logs the command to the defined variable
        time.sleep(5)  # wait 5 seconds
        register_result = run_and_log(register_command)  # executes and logs the command to the defined variable
    return flush_result, register_result


def ping(host, os, testType):
    '''
    Ping test to the defined host for 100 pings at max MTU size.
    :param host: ping test destination
    :param os: operating system of the machine currently running the program
    :param testType: defines weather the test is short or long (10 or 1000 pings)
    :return: string of console logs (decoded from byte to string, removed carriage returns)
    '''
    if debug_mode == True: print("ping test", os)
    
    if os == 'windows':
        param_count_flag, param_MTU = '-n', '-l'
    else:
        param_count_flag, param_MTU = '-c', '-s'
    if testType == 'comprehensive':
        param_count_number = "1000"
    else:
        param_count_number = "10"
        
    if debug_mode == True: print("ping count", param_count_number)
    
    #modified packet size from 1472 to 1400 since command would not run on my pc for sizes above 1419
    command = ['ping', param_count_flag, param_count_number, param_MTU, '1400', host]   # Command itself
    
    ping_result = run_and_log(command)  # executes and logs the command to the defined variable
    return ping_result



def traceroute(host, os):
    '''
    Runs a traceroute to the defined host with max hops of 20 to ensure it does not
    infinitely run and continuously timeout as that can happen if not capped.
    :param host: traceroute destination
    :param os: operating system of the machine currently running the program
    :return: string of console logs (decoded from byte to string, removed carriage returns)
    '''
    if os == 'windows':
        param_command, param_hops = 'tracert', '-h'
    else:
        param_command, param_hops = 'traceroute', '-m'
    command = [param_command, param_hops, "20", host]   # Command itself
    trace_result = run_and_log(command)  # executes and logs the command to the defined variable
    return trace_result


def ipconfig(os):
    '''
    Fetches the IP configuration and hardware ID info for network card MACs, IPs, DNS, Subnets, etc.
    :param os: operating system of the machine currently running the program
    :return: string of ipconfig info console log (decodes from byte to string, removed carriage returns)
    '''
    if os == 'windows':
        param_command, param_flag = 'ipconfig', '/all'
    else:
        param_command, param_flag = 'ifconfig', '-a'
    command = [param_command, param_flag]   # Command itself
    network_config = run_and_log(command)  # executes and logs the command to the defined variable
    return network_config


# def speed_test(server):
#     # This function does not exist as the speed_test api for python is garbage and produces lies
#     return result_string



def Diagnostic(testType):
    # set hostname, gather OS info, set time and date start
    hostname = "google.ca"
    print("running Diagnotic()")

    operating_system = platform.system().lower()
    date_and_time = datetime.now().strftime("%d-%b-%Y_%I.%M.%p")

    # collect data
    ipconfig_output = ipconfig(operating_system)
    test.ipconfig_complete = True
    if debug_mode == True: print("ipconfig complete")
    
    ping_output = ping(hostname, operating_system, testType)
    test.ping_complete = True
    if debug_mode == True: print("ping complete")
    
    traceroute_output = traceroute(hostname, operating_system)
    test.traceroute_complete = True
    if debug_mode == True: print("traceroute complete")
    
    #placeholder
    print(ipconfig_output)
    print(ping_output)
    print(traceroute_output)
    #placeholder
    
    # write data to single output variable and then write to file
    output = date_and_time + "\n\n" + ipconfig_output + "\n" + ping_output + "\n" + traceroute_output
    with open('Uniserve_Diagnostic_' + date_and_time + '.log', 'w') as outfile:
        outfile.write(output)
    display.current_screen = "complete"


# Diagnostic()
#*************************************************************************

startup = True
debug_mode = True #should be set to false when sent to user

def Draw_Text(surface, text, color, rect, font, aa=False, bkg=None):
    y = rect.top
    lineSpacing = 10
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]

    return text

if startup: #load screen
    screen_width = 1280
    screen_height = 720
    centerpoint = ((screen_width)/2, (screen_height)/2)
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Uniserve data collection tool")
    text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    opensans_font = pygame.font.Font("font/OpenSans.ttf", 30)
    text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
    text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)
    clock = pygame.time.Clock()
    icon_surf = pygame.image.load("graphics/uniserve_icon.png").convert_alpha()
    pygame.display.set_icon(icon_surf)

class Test_Progress():
    def __init__(self):
        self.ipconfig_complete = False
        self.ping_complete = False
        self.traceroute_complete = False

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, type):
        super().__init__()
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.type = type
        self.cooldown_max = 20
        self.cooldown = 0
        
        #not hidden by default
        self.status = "default" #statuses are hidden, default, highlighted, clicked
        self.animation_index = 1
        
        #frame 0 is a blank frame used to make sure the button is not visable
        self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
        self.frame_0 = pygame.transform.scale(self.frame_0, (self.width, self.height))
        
        self.frame_1 = pygame.image.load("graphics/button_default.png").convert_alpha()
        self.frame_1 = pygame.transform.scale(self.frame_1, (self.width, self.height))
        self.frame_2 = pygame.image.load("graphics/button_highlighted.png").convert_alpha()
        self.frame_2 = pygame.transform.scale(self.frame_2, (self.width, self.height))
        self.frame_3 = pygame.image.load("graphics/button_pressed.png").convert_alpha()
        self.frame_3 = pygame.transform.scale(self.frame_3, (self.width, self.height))
        self.frames = [self.frame_0, self.frame_1, self.frame_2, self.frame_3]
        
        #use animation index to determine what frame to display from the list of all available frames
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
    
    #handles clicking on the button
    def click_button(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.cooldown == 0: 
                #reset the cooldown
                self.cooldown = self.cooldown_max
                #update status
                self.status = "clicked"
                #placeholder
                print("You clicked on the", self.type, "button")
                display.current_screen = "testing"
                display.update()
                pygame.display.update()
                if self.type == "Quick Test": Diagnostic("basic")
                elif self.type == "Full Test": Diagnostic("comprehensive")
    
    #highlight button on mouseover
    def highlight(self):
        mouse_pos = pygame.mouse.get_pos()
        #check if in bounds
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom: 
            if self.status == "default": self.status = "highlighted"
        else:
            if self.status == "highlighted": self.status = "default"

    def update(self):
        #reduce cooldown
        if self.cooldown > 0: self.cooldown -= 1
    
        #handle button being clicked on
        self.click_button()
        #reset after clicking
        if self.cooldown <= 5 and self.status == "clicked": self.status = "default"
        
        #highlight if mouseover
        self.highlight()
        
        #update animation index based on status
        if display.hide_buttons == True: self.status = "hidden"
        try:
            if self.status == "hidden": self.animation_index = 0
            elif self.status == "default": self.animation_index = 1
            elif self.status == "highlighted": self.animation_index = 2
            elif self.status == "clicked": self.animation_index = 3
        except:
            if debug_mode == True: print("Error: invalid button status visual")
            else: pass
        
        #update visual image
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
     
class Label(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, type, linked_button):
        super().__init__()
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.type = type
        self.linked_button = linked_button
        
        #not hidden by default
        self.hidden = False
        self.animation_index = 1
        
        #frame 0 is a blank frame used to make sure the button is not visable
        self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
        self.frame_0 = pygame.transform.scale(self.frame_0, (self.width, self.height))
        
        self.frame_1 = text_font.render(self.type, True, (250,180,180)) #normal text
        self.frame_2 = text_font.render(self.type, True, (250,250,250)) #highlighted text
        self.frame_3 = text_font.render(self.type, True, (250,250,250)) #highlighted text while button is pressed
        self.frames = [self.frame_0, self.frame_1, self.frame_2, self.frame_3]
        
        self.image = self.frames[self.animation_index]
        # self.rect = pygame.Rect((screen_width*0.1,screen_height*0.25),(screen_width*0.6,screen_height*0.5))
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))

    def update(self):
        #match animation_index with paired button using list index number
        self.animation_index = self.linked_button.animation_index
        #update image and rect
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
     
class Display_Manager:
    def __init__(self):
        self.current_screen = "welcome"
        self.hide_buttons = False
        self.message = " "
        self.message_rect = pygame.Rect((screen_width*0.2,screen_height*0.25),(screen_width*0.6,screen_height*0.5))
    
    def update_message(self):
        #update message based on current_screen
        if self.current_screen == "welcome": self.message = "Welcome to the Uniserve Data Collection Tool"
        if self.current_screen == "testing": self.message = "Currently running tests. This can take up to five minutes for the quick test and up to twenty minutes for the full test, so please do not exit the program even if it appears frozen or unresponsive."
        if self.current_screen == "complete": self.message = "Testing is complete. You can now exit the program and email the file containing the test results to customercare@uniserve.com"
    
    def update(self):
        #fills screen with black to erase previous rendered cycle
        screen.fill((0,0,0))
        
        #update and display current message to the user
        self.update_message()
        Draw_Text(screen, self.message, pygame.Color("coral"), self.message_rect, text_font)
        
        #draw buttons on screen and label them
        buttons.draw(screen)
        labels.draw(screen)

def create_button(pos_x, pos_y, width, height, type):
    button = (Button(pos_x, pos_y, width, height, type))
    buttons.add(button)
    label = (Label(pos_x, pos_y, width, height, type, button))
    labels.add(label)

if startup:
    #create managers
    test = Test_Progress()
    buttons = pygame.sprite.Group()
    button_list = []
    labels = pygame.sprite.Group()
    display = Display_Manager()
    #create buttons
    create_button(screen_width*0.3, screen_height*0.8, screen_width*0.2, screen_height*0.2, "Quick Test")
    create_button(screen_width*0.8, screen_height*0.8, screen_width*0.2, screen_height*0.2, "Full Test")


#game Cycle
while True: 
    for event in pygame.event.get():
        #handles quitting the program
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        #handles keyboard inputs    
        if event.type == pygame.KEYDOWN:
            pass
    
    
    #update buttons (includes clicking on them) and labels
    buttons.update()
    labels.update()
    #update visual display
    display.update()

    #pygame update
    pygame.display.update()
    clock.tick(60)
    