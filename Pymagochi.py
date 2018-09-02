import pygame
from pygame.locals import *
from configparser import ConfigParser
from ast import literal_eval
from Pymagochi_class import Pymagotchi
from Timer import Timer

def get_config(filename='config.ini'):
    try :
        config = ConfigParser()
        config.read(filename)
        params = { 'screen': {}, 'color': {} }
        for param in config['screen']:
            params['screen'][param] = int(config['screen'][param])
        for param in config['color']:
            params['color'][param] = literal_eval(config['color'][param])
        return params
    except :
        print('Can\'t read config file {} '.format(filename))
        exit(1)
        
def read_hex_image(filename):
    try :
        with open(filename, 'r') as fic:
            data = fic.read()
    except:
        print('Can\'t read hex image file {}'.format(filename))
        exit(1)
    return tuple(data.split('0x')[1:])

def get_bits(number, num_bits):
    return [(number >> bit) & 1 for bit in range(num_bits - 1, -1, -1)]

def render_display(screen, image_data, params):
    for y in range(32):
        bits = get_bits(int(image_data[y], 16),32)
        bits.reverse()
        for x in range(0, 32):
            color = params['color']['pixel_off']
            if x in range(len(bits)):
                if bits[x]:
                    color = params['color']['pixel_on']
            pygame.draw.rect(screen, color, (x * 10 + 32, y * 10 +64, 8, 8))

def read_sprites(screen, params):
    data = {
        'screen': screen,
        'params': params,
        'active': 'pymagotchi',
        'state': 0
    }
    
    data['pymagotchi'] = [
        read_hex_image('sprites/pymagotchi_face.hex'),
        read_hex_image('sprites/pymagotchi_wait.hex')
    ]
    
    data['eat'] = [
        read_hex_image('sprites/eat1.hex'),
        read_hex_image('sprites/eat2.hex'),
        read_hex_image('sprites/eat3.hex')
    ]
    
    data['dead'] = [
        read_hex_image('sprites/dead1.hex'),
        read_hex_image('sprites/dead2.hex')
    ]
    
    return data

def animation(sprite_name, data):
    if data['active'] != sprite_name:
        data['active'] = sprite_name
        data['state'] = 0
    else:
        data['state'] = (data['state'] + 1) % 2
    
    render_display(data['screen'], data[sprite_name][data['state']], data['params'])

def statistics(screen, font, pymagotchi):
    surf = font.render('-' * 27, True, params['color']['pixel_on'])
    screen.blit(surf, (360, 60))
    surf = font.render('--STAT--', True, params['color']['pixel_on'])
        
    screen.blit(surf, (360, 70))
    surf = font.render('-' * 27, True, params['color']['pixel_on'])
    screen.blit(surf, (360, 80))
    stats = ('NOM', 'AGE', 'FAIM', 'FORCE')
    for pos, y in enumerate(i for i in range(100, 140, 10)):
        surf = font.render(stats[pos], True, params['color']['pixel_on'])
        screen.blit(surf, (360, y))
        surf = font.render(':', True, params['color']['pixel_on'])
        screen.blit(surf, (420, y))
        surf = font.render(pymagotchi.get(stats[pos]), True, params['color']['pixel_on'])
        screen.blit(surf, (430, y))
    surf = font.render('-' * 27, True, params['color']['pixel_on'])
    screen.blit(surf, (360, 160))
    
    
def start_game(params):
    pygame.init()
    pymagotchi = Pymagotchi('name')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((params['screen']['width'], params['screen']['heigth']), 0, 32)
    pygame.display.set_caption('Pymagotchi')
    font = pygame.font.SysFont('Calibri', 12)
    
    sprites = read_sprites(screen, params)
    timer = Timer(pygame.time.get_ticks())
    
    while True:
        screen.fill(params['color']['background'])
        
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                exit(0)
        
        if timer.isDuration(1, pygame.time.get_ticks()):
            pymagotchi.events()
        
        pygame.time.wait(100)
        animation(pymagotchi.get_state(), sprites)
        
        statistics(screen, font, pymagotchi)
       
        pygame.display.update()
        clock.tick(params['screen']['fps'])
        
        
if __name__ == '__main__':
    params = get_config()
    start_game(params)