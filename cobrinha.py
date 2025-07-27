from tkinter import *
import random

LARGURA=1000
ALTURA=700
VELOCIDADE=50
ESPAÇO=20
PARTES_CORPO=3
COR_COBRA="#32a852"
COR_COMIDA="#f2403a"
COR_FUNDO="#000000"
class Cobra:
    def __init__(self):
        self.tamanho_corpo=PARTES_CORPO
        self.coordinates=[]
        self.squares=[]
        for i in range(0,PARTES_CORPO):
            self.coordinates.append([0,0])

        for x,y in self.coordinates:
            square=canvas.create_rectangle(x,y,x+ESPAÇO,y+ESPAÇO,fill=COR_COBRA,tag="cobra")
            self.squares.append(square)


class Comida:
    def __init__(self):
        x = random.randint(0, (LARGURA // ESPAÇO) - 1) * ESPAÇO
        y = random.randint(0, (ALTURA // ESPAÇO) - 1) * ESPAÇO
        self.coordinates=[x,y]
        canvas.create_oval(x,y,x+ESPAÇO,y+ESPAÇO,fill=COR_COMIDA,tag="Comida")

def next_turn(cobra ,comida):
    x , y =cobra.coordinates[0]
    if direção =="up":
        y-=ESPAÇO

    elif direção == "down":
        y += ESPAÇO

    elif direção == "left":
        x -= ESPAÇO

    elif direção == "right":
        x += ESPAÇO

    cobra.coordinates.insert(0, (x , y))
    square=canvas.create_rectangle(x,y,x+ESPAÇO,y+ESPAÇO,fill=COR_COBRA)
    cobra.squares.insert(0,square)

    if x==comida.coordinates[0] and y==comida.coordinates[1]:
        global pontuação
        pontuação+=1
        label.config(text="Pontuação:{}".format(pontuação))
        canvas.delete("Comida")
        comida=Comida()
    else:
        del cobra.coordinates[-1]
        canvas.delete(cobra.squares[-1])
        del cobra.squares[-1]

    if check_collisions(cobra):
        game_over()

    else:
        janela.after(VELOCIDADE,next_turn,cobra,comida)

def change_direction(new_direction):
    global direção

    if new_direction=='left':
        if direção!='right':
            direção=new_direction

    elif new_direction=='right':
        if direção!='left':
            direção=new_direction

    elif new_direction=='up':
        if direção!='down':
            direção=new_direction

    elif new_direction=='down':
        if direção!='up':
            direção=new_direction
def check_collisions(cobra):
    x,y=cobra.coordinates[0]
    if x<0 or x>=LARGURA:
        return True
    elif y < 0 or y >= ALTURA:
        return True

    for body_part in cobra.coordinates[1:]:
        if x ==body_part[0] and y== body_part[1]:
            return True

    return False
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=("Arial",70),text="Fim de jogo",fill="red",tag="gameover")
janela=Tk()
janela.title("Jogo da cobrinha")
janela.resizable(False,False)
pontuação=0
direção="down"
label=Label(janela,text="Pontuação:{}".format(pontuação),font=("Arial",30))
label.pack()
canvas=Canvas(janela,bg=COR_FUNDO,height=ALTURA,width=LARGURA)
canvas.pack()
janela.update()
janela_largura=janela.winfo_width()
janela_altura=janela.winfo_height()
largura_tela=janela.winfo_screenwidth()
altura_tela=janela.winfo_screenheight()
x=int((largura_tela/2)-(janela_largura/2))
y=int((altura_tela/2)-(janela_altura/2))
janela.geometry(f"{janela_largura}x{janela_largura}+{x}+{y}")

janela.bind("<w>",lambda vent:change_direction('up'))
janela.bind("<a>",lambda vent:change_direction('left'))
janela.bind("<s>",lambda vent:change_direction('down'))
janela.bind("<d>",lambda vent:change_direction('right'))
cobra =Cobra()
comida =Comida()

next_turn(cobra, comida)
janela.mainloop()