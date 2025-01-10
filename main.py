from src import *
from time import *
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
            self.timer = 10 - timer
            
            # Timer zerado / fim da partida 
            if self.timer <= 0:
                self.reset()
    
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
            self.update_timer()
            
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
            pyxel.blt(ICON_PIECE_POSX, 1, 0, 48, 0, 10, 10, 15)
            pyxel.blt(ICON_TIMER_POSX, 1, 0, 58, 0, 10, 10, 15)
        
            padx_scores = len(str(self.scores)) * 4 + 8
            padx_time = len(str(self.timer))/2 * 4 + 8
            pyxel.text(ICON_PIECE_POSX + padx_scores, 4, str(self.scores), 7)
            pyxel.text(ICON_TIMER_POSX + padx_time, 4, str(self.timer), 7)
        
    @handle_error
    def draw(self):
        """Método para atualização da tela a cada quadro."""
        pyxel.cls(6)
        pyxel.mouse(True)
        pyxel.rect(0, 0, SCREEN_WIDTH, 16, 2)
        pyxel.rect(0, 72, SCREEN_WIDTH, 28, 3)

        if self.play:
            self.HUD()
            # Desenha os grids
            for rect in grids_list:
                rect.draw() 
            
            # Desenha as peças
            for obj in pieces_list:
                obj.draw()
        
        # Menu inicial
        else:
            TXT = "Press Start"
            TXT_CENTER_X = len(TXT)/2 * pyxel.FONT_WIDTH
            ICON_CENTER_Y = SCREEN_HEIGHT/2 - 48/2
            ICON_CENTER_X = SCREEN_WIDTH/2 - 48/2
            pyxel.blt(ICON_CENTER_X, ICON_CENTER_Y -6, 0, 0, 0, 48, 48, 15)
            pyxel.text(SCREEN_HEIGHT/2 - TXT_CENTER_X +1 , SCREEN_HEIGHT - 17, TXT ,pyxel.frame_count % 16)

if __name__ == "__main__":
    Game()