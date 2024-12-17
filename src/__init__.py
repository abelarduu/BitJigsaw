from src.object import Object
import random 

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100

object_selected = False

piece1 = Object(0, 74, 0, 0, 0, 22, 22)
piece2 = Object(0, 74, 0, 22, 0, 18, 18)
piece3 = Object(0, 74, 0,40, 0, 22, 22)
piece4 = Object(0, 74, 0, 0, 22, 18, 18)
piece5 = Object(0, 74, 0, 18, 18, 26, 26)
piece6 = Object(0, 74, 0, 44, 22, 18, 18)
piece7 = Object(0, 74, 0, 0, 40, 22, 22)
piece8 = Object(0, 74, 0, 22, 44, 18, 18)
piece9 = Object(0, 74, 0, 40, 40, 22, 22)

# Peças do game
pieces_list = [piece1, piece2, piece3,
               piece4, piece5, piece6,
               piece7, piece8, piece9]
# Embaralha a lista de peças aleatoriamente
# Adiciona a posição X inicial de cada peça
for index, obj in enumerate(pieces_list):
    obj.index = index
    obj.x = index *10
    
random.shuffle(pieces_list)
               
rects_grid_list = []
CENTER_POSITION_X = SCREEN_WIDTH // 3.8
CENTER_POSITION_Y = SCREEN_HEIGHT // 5
for row_index in range(3):
    for col_index in range(3):
        new_rect = Object(CENTER_POSITION_X + col_index * 16, CENTER_POSITION_Y + row_index * 16, 1, 0, 62, 16, 16)
        new_rect.mov = False
        rects_grid_list.append(new_rect)


for index, rect in enumerate(rects_grid_list):
    rect.index = index
