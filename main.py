from src import *
import pyxel

def handle_error(func):
    """Método para tratamento de erros."""
    def wrapper(self):
        try:
            func(self)
        except Exception as err:
            print(f"Erro na execução de {func.__name__}: {err}")
    return wrapper

class Game:
    def __init__(self):
        self.scores = 0
        self.time = 30
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="BitJigsaw", fps=60)
        pyxel.load("src/assets/BitJigsaw.pyxres")
        pyxel.run(self.update, self.draw)
    
    def get_pressed_piece(self) -> Object:
        """Retorna a peça que está sendo pressionada no momento."""
        for piece in pieces_list:
            if piece.dragged:
                return piece
            
    def is_piece_correct(self, rect) -> bool:
        if (not rect.piece is None and
            rect.piece.mov and
            rect.piece.dropped):
                    
            if rect.index == rect.piece.index:
                return True
        return False
        
    def align_piece(self, rect):
        # Centraliza a peça no rect grid
        rect.piece.x = (rect.x + rect.width / 2) - (rect.piece.width / 2)
        rect.piece.y = (rect.y + rect.height / 2) - (rect.piece.width / 2)
        
        match rect.index:
            case 0:
                rect.piece.x +=2
                rect.piece.y +=2
            case 2:
                rect.piece.x -=2
                rect.piece.y +=2
            case 6:
                rect.piece.x +=2
                rect.piece.y -=2
            case 8:
                rect.piece.x -=2
                rect.piece.y -=2
    
    @handle_error
    def update(self):
        """Método para verificação de interações a cada quadro."""
        # Verifica e atualiza os grids
        
        for index, rect in enumerate(rects_grid_list):
            rect.index = index
            rect.update()
            
            piece = self.get_pressed_piece()
            if not piece is None:
                if (rect.mouse_up and piece.dragged):
                    rect.piece = piece
                    self.align_piece(rect)

                
            # encrementando pontos a cada acerto
            if self.is_piece_correct(rect):
                    self.scores += 1
                    self.align_piece(rect)
                    rect.piece.mov = False

        # Verifica e atualiza as peças
        for obj in pieces_list:
            obj.update()
            
    def HUD(self):
        """Exibe a HUD na interface do game."""
        pyxel.rect(0, 0, SCREEN_WIDTH, 16, 12)
        pyxel.rect(0, 72, SCREEN_WIDTH, 28, 12)
        
        CENTER = SCREEN_WIDTH //2
        ICON_PIECE_POSX = SCREEN_WIDTH //2 - CENTER //2 + 1
        ICON_TIMER_POSX = SCREEN_WIDTH //2 + CENTER //2 - 20
        pyxel.blt(ICON_PIECE_POSX, 1, 0, 0, 0, 10, 10, 12)
        pyxel.blt(ICON_TIMER_POSX, 1, 0, 10, 0, 10, 10, 12)
        
        
        padx_scores = len(str(self.scores)) * 4 + 8
        padx_time = len(str(self.time)) * 4 + 4
        pyxel.text(ICON_PIECE_POSX + padx_scores, 4, str(self.scores), 7)
        pyxel.text(ICON_TIMER_POSX + padx_time, 4, str(self.time), 7)

    @handle_error
    def draw(self):
        """Método para atualização da tela a cada quadro."""
        pyxel.cls(6)
        pyxel.mouse(True)
        self.HUD()
        
        # Desenha os grids
        for rect in rects_grid_list:
            rect.draw()
        
        # Desenha as peças
        for obj in pieces_list:
            obj.draw()

if __name__ == "__main__":
    Game()