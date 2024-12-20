from src.object import Object
import random

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100

def update_index(objs_list):
    """Enumera cada index de cada objeto da lista."""
    for index, obj in enumerate(objs_list):
        obj.index = index

def create_pieces() -> list:
    """ Gera e retorna uma lista de peças embaralhadas."""
    pieces = [
        Object(0, 74, 0, 0, 0, 22, 22),
        Object(0, 74, 0, 22, 0, 18, 18),
        Object(0, 74, 0,40, 0, 22, 22),
        Object(0, 74, 0, 0, 22, 18, 18),
        Object(0, 74, 0, 18, 18, 26, 26),
        Object(0, 74, 0, 44, 22, 18, 18),
        Object(0, 74, 0, 0, 40, 22, 22),
        Object(0, 74, 0, 22, 44, 18, 18),
        Object(0, 74, 0, 40, 40, 22, 22)]
              
    # Adicionando index de cada peça
    # Embaralha a lista de peças
    update_index(pieces)
    random.shuffle(pieces)
    # Adiciona a posição X inicial de cada peça
    for index, piece in enumerate(pieces):
        piece.x = index *10
        
    return pieces
        
def create_grids() -> list:
    """ Gera e retorna uma lista de grids."""
    CENTER_POSITION_X = SCREEN_WIDTH // 3.8
    CENTER_POSITION_Y = SCREEN_HEIGHT // 5
    
    grids = []
    # Gerando Grid 3x3
    for row_index in range(3):
        for col_index in range(3):
            new_rect = Object(CENTER_POSITION_X + col_index * 16, CENTER_POSITION_Y + row_index * 16, 1, 0, 62, 16, 16)
            new_rect.mov = False
            grids.append(new_rect)

        # Adicionando index de cada peça
        update_index(grids)
    
    return grids