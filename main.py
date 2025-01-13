from src import *
from time import time
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
        self.reset()
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="BitJigsaw", fps=60)
        pyxel.load("src/assets/BitJigsaw.pyxres")
        pyxel.run(self.update, self.draw)
        
    def reset(self):
        self.play = False
        self.elapsed_time = None
        self.timer = 0
        self.scores = 0
        object_selected = False
        
        # Limpa as listas de peças e grids
        pieces_list.clear()
        grids_list.clear()
        # Recria as listas
        pieces_list.extend(create_pieces())
        grids_list.extend(create_grids())
            
    def start_timer(self):
        """Inicia o temporizador da partida."""
        self.elapsed_time = int(time())
    
    def update_timer(self):
        """Atualiza o temporizador para o fim da partida."""
        if self.elapsed_time is None:
            self.start_timer()
        else:
            # Timer recebe o tempo corrido (0 - 10)
            # self.Timer recebe o timer na ordem decrescente (10 - 0)
            timer = int(time() - self.elapsed_time)
            if timer <= 10:
                self.timer = 10 - timer
            
    
    def get_pressed_piece(self) -> Object:
        """Retorna a peça que está sendo pressionada no momento."""
        for piece in pieces_list:
            if piece.dragged:
                return piece
            
    def is_piece_correct(self, rect) -> bool:
        """Verifica se a peça está no grid correto."""
        if (not rect.piece is None and
            rect.piece.mov and
            rect.piece.dropped):
            
            if rect.index == rect.piece.index:
                return True
        return False
    
    def align_piece(self, rect):
        """Centraliza a peça ao soltar em um grid."""
        # Centraliza a peça no rect grid
        rect.piece.x = (rect.x + rect.width / 2) - (rect.piece.width / 2)
        rect.piece.y = (rect.y + rect.height / 2) - (rect.piece.width / 2)
        
        match rect.index:
            case 0:
                rect.piece.x += 2
                rect.piece.y += 2
            case 2:
                rect.piece.x -= 2
                rect.piece.y += 2
            case 6:
                rect.piece.x += 2
                rect.piece.y -= 2
            case 8:
                rect.piece.x -= 2
                rect.piece.y -= 2
    
    @handle_error
    def update(self):
        """Método para verificação de interações a cada quadro."""
        if self.play:
            if self.scores == 9:
                # Retorno ao menu inicial
                if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                   self.reset()
                    
            else:
                # Atualiza o Timer a cada quadro
                # Se o Timer zerar: fim da partida 
                self.update_timer()
                if self.timer <= 0:
                    # Retorno ao menu inicial
                    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                        self.reset()
            
            # Verifica e atualiza os grids
            for index, rect in enumerate(grids_list):
                rect.index = index
                rect.update()
                 
                piece = self.get_pressed_piece()
                if not piece is None:
                    if (rect.mouse_up and piece.dragged):
                        rect.piece = piece
                        self.align_piece(rect)

                # Incrementando pontos a cada acerto
                if self.is_piece_correct(rect):
                        self.scores += 1
                        self.align_piece(rect)
                        rect.piece.mov = False
                        
            # Verifica e atualiza as peças
            for obj in pieces_list:
                obj.update()
                
        # Menu Inicial
        else:
            #Verificação para inicialização do game
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.play = True
    
    def HUD(self):
        """Exibe a HUD na interface do game."""
        if self.play:
            CENTER = SCREEN_WIDTH // 2
            ICON_PIECE_POSX = SCREEN_WIDTH // 2 - CENTER // 2 + 1
            ICON_TIMER_POSX = SCREEN_WIDTH // 2 + CENTER // 2 - 20
            pyxel.blt(ICON_PIECE_POSX, 3, 0, 47, 21, 10, 10, 15)
            pyxel.blt(ICON_TIMER_POSX, 3, 0, 58, 21, 10, 10, 15)
        
            padx_scores = len(str(self.scores)) * 4 + 8
            padx_time = len(str(self.timer))/2 * 4 + 10
            pyxel.text(ICON_PIECE_POSX + padx_scores, 5, str(self.scores), 7)
            pyxel.text(ICON_TIMER_POSX + padx_time, 5, str(self.timer), 7)
        
    @handle_error
    def draw(self):
        """Método para atualização da tela a cada quadro."""
        pyxel.cls(12)
        pyxel.mouse(True)
        pyxel.blt(0, 0, 0, 0, 0, 100, 20, 15)
        pyxel.blt(0, SCREEN_HEIGHT - 20, 0, 0, 0, 100, -20, 15)

        if self.play:
            self.HUD()
            # Desenha os grids
            for rect in grids_list:
                rect.draw()
            
            # Desenha as peças
            for obj in pieces_list:
                obj.draw()
                
            if self.scores == 9:
                TXT = "Jigsaw Completed!"
                PADX = len(TXT)/2 * pyxel.FONT_WIDTH
                TXT_POSX = SCREEN_WIDTH/2 - PADX
                TXT_POSY = SCREEN_HEIGHT/2
                pyxel.text( TXT_POSX, 20, str(TXT), pyxel.frame_count % 16)
                
            else:
                if self.timer <= 0:
                    TXT = "Jigsaw Incomplete!"
                    PADX = len(TXT)/2 * pyxel.FONT_WIDTH
                    TXT_POSX = SCREEN_WIDTH/2 - PADX
                    TXT_POSY = SCREEN_HEIGHT/2
                    pyxel.text( TXT_POSX, 20, str(TXT), pyxel.frame_count % 7)
        
        # Menu inicial
        else:
            TXT = "Press Start"
            TXT_CENTER_X = len(TXT)/2 * pyxel.FONT_WIDTH
            ICON_CENTER_Y = SCREEN_HEIGHT/2 - 46/2
            ICON_CENTER_X = SCREEN_WIDTH/2 - 46/2
            pyxel.blt(ICON_CENTER_X, ICON_CENTER_Y, 0, 0, 21, 46, 46, 15)
            pyxel.text(SCREEN_HEIGHT/2 - TXT_CENTER_X +1 , ICON_CENTER_Y + 47, TXT ,pyxel.frame_count % 16)

if __name__ == "__main__":
    Game()