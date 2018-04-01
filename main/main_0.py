from tkinter import *
from PIL import ImageTk, Image
from random import *


def callback(*args):
    print('You called the callback!')


# Primera configuracion
win = Tk()
win.resizable(False, False)
win.title('Astore')
bg_color = '#bbb8c1'
yscrollbar = Scrollbar(win)
yscrollbar.pack(side=RIGHT, fill=Y)

# Dimensiones de la pantalla
win_width, win_height = win.winfo_screenwidth(), win.winfo_screenheight()
win_width = 40*win_width/100

win.geometry('%dx%d+%d+0' % (win_width, win_height*89/100, win_width*80/100))


# Contenedores
main_frame = Frame()
bottom_canvas = Canvas(win, height=win_height, width=win_width, bg=bg_color, scrollregion=(0, 0, win_width, 1000),
                       yscrollcommand=yscrollbar.set)
bottom_canvas.pack()
yscrollbar.config(command=bottom_canvas.yview)

welcome_canvas = Canvas(win, height='200', width='500', bg=bg_color, bd=0, highlightthickness=0, relief='ridge')
welcome_canvas.pack()
welcome_canvas.place(x=win_width*10/100, y=50)


# Texto
welcome_text = Label(welcome_canvas, text='Bienvenido, invitado!', font='Times 20', bg=bg_color)
quote = Label(welcome_canvas, text='Recuerde que debe\n iniciar sesion para descargar', font='Times 20 italic',
              bg =bg_color)
quote.pack()
quote.place(x=0, y=70)
welcome_text.pack()
welcome_text.place(x=0, y=20)


# Imagenes
load_guest_img = Image.open('../images/profile/guest.png').resize((125, 125), Image.ANTIALIAS)

guest_img = ImageTk.PhotoImage(load_guest_img)
user_img_label = Label(welcome_canvas, image=guest_img, bd=0, highlightthickness=0, relief='ridge')
user_img_label.pack()
user_img_label.place(x=350, y=20)

load_hamb_icon = Image.open('../images/icons/hamburguer_icon.png').resize((30, 30), Image.ANTIALIAS)

hamb_icon = ImageTk.PhotoImage(load_hamb_icon)
hamb_icon_label = Label(win, image=hamb_icon, bd=0, highlightthickness=0, relief='ridge', bg=bg_color)
hamb_icon_label.pack()
hamb_icon_label.place(x=1, y=1)


# Botones


def random_mainpage():
    categorias = ['Juegos', 'Musica', 'Redes sociales', 'Herramientas']
    random_mainpage_aux(categorias, [], 1)


def is_in(list1, ele, cont):
    if len(list1) == cont:
        return False
    elif list1[cont] == ele:
        return True
    else:
        return is_in(list1, ele, cont+1)


def random_mainpage_aux(categorias, used, cont):
    rand = randint(0,3)
    ini_y = 50
    if len(used) == 4:
        return
    elif not is_in(used, categorias[rand], 0):
        if categorias[rand] == 'Juegos':
            canvas_juegos = Canvas(bottom_canvas, width=500, height=200, bg='black')
            canvas_juegos.pack()
            canvas_juegos.place(x=10*win_width/100, y=ini_y + 200*cont)
            print('Juegos')
            return random_mainpage_aux(categorias, used+['Juegos'], cont+1)
        elif categorias[rand] == 'Musica':
            canvas_musica = Canvas(bottom_canvas, width=500, height=200, bg='green')
            canvas_musica.pack()
            canvas_musica.place(x=10 * win_width / 100, y=ini_y + 200 * cont)
            print('Musica')
            return random_mainpage_aux(categorias, used + ['Musica'], cont+1)
        elif categorias[rand] == 'Redes sociales':
            canvas_redes = Canvas(bottom_canvas, width=500, height=200, bg='red')
            canvas_redes.pack()
            canvas_redes.place(x=10 * win_width / 100, y=ini_y + 200 * cont)
            print('Redes sociales')
            return random_mainpage_aux(categorias, used + ['Redes sociales'], cont + 1)
        else:
            canvas_herramientas = Canvas(bottom_canvas, width=500, height=200, bg='white')
            canvas_herramientas.pack()
            canvas_herramientas.place(x=10 * win_width / 100, y=ini_y + 200 * cont)
            print('Herramientas')
            return random_mainpage_aux(categorias, used + ['Herramientas'], cont + 1)
    else:
        return random_mainpage_aux(categorias, used, cont)

def show_menu(*args):
    canvas_menu = Canvas(win, height=win_height, width=win_width*20/100)
    canvas_menu.pack()
    canvas_menu.place(x=0, y=0)

    destroy = lambda a : canvas_menu.destroy()
    canvas_menu.bind('<Leave>', destroy)

    test_label = Label(canvas_menu, text='Invitado')
    test_label.pack()
    test_label.place(x=win_width*10/100, y=50)

    idiom_button = Button(canvas_menu)
    idiom_button.pack()
    idiom_button.place(x=0, y=0)


random_mainpage()


hamb_icon_label.bind('<Button-1>', show_menu)
mainloop()
