import pyxel

class Object:
    def __init__(self, x, y, img, img_x, img_y, width, height):
        """Inicializa o objeto com as suas propriedades."""
        self.x = x
        self.y = y
        self.img = img
        self.img_x = img_x
        self.img_y = img_y
        self.width = width
        self.height = height
        self.mov = True
        self.mouse_up = False
        self.mouse_pressed = False
        self.mouse_released = False
        self.dragged = False
        self.dropped = False
        self.piece = None
        self.index = None
        
    def check_click(self):
        """Verifica se o mouse está clicando no objeto."""
        # VERIFICAÇÃO DO MOUSE
        # Verifica a posição do mouse nos eixos X e Y
        if (pyxel.mouse_x >= self.x and
            pyxel.mouse_x <= self.x + self.width and 
            pyxel.mouse_y >= self.y and
            pyxel.mouse_y <= self.y + self.height):
                self.mouse_up = True
        else:
            self.mouse_up = False
                
        # VERIFICAÇÃO DO CLIQUE DO MOUSE
        # Verifica se o botão do mouse foi pressionado ou liberado
        if self.mouse_up:
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.mouse_pressed = True
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.mouse_released = True
                self.mouse_pressed = False
            self.mouse_released = False
            
    def drag(self):
        """Ativa o arrasto do objeto com o mouse."""
        self.dragged = True
        self.dropped = False
        self.x = pyxel.mouse_x - self.width / 2
        self.y = pyxel.mouse_y - self.height / 2

    def drop(self):
        """Desativa o arrasto e marca o objeto como solto."""
        self.dragged = False
        self.dropped = True

    def update(self):
        """Atualiza o estado do objeto, verificando cliques e movimento."""
        self.check_click()
                    
        if self.mov:
            # Sistema de arrastar e soltar
            if (self.mouse_up and
                self.mouse_pressed):
                    self.drag()
            else: 
                self.drop()
        
    def draw(self):
        """Desenha o objeto na tela."""
        pyxel.blt(self.x, self.y, self.img, self.img_x, self.img_y, self.width, self.height, 12)
        
        # Adiciona uma borda no objeto selecionado
        if (self.mouse_up and self.mov):
            self.img = 2
        else:
            self.img = 1