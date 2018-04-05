from tkinter import *
from PIL import ImageTk, Image
from random import *
from tkinter import filedialog as fd
from manejo_txt import *
from tkinter import simpledialog, messagebox

users_list = []  # Usada para guardar los usuarios
category_list=['Juegos', 'Musica', 'Herramientas', 'Redes Sociales']  # Usada para asociar los numeros de categoria con
                                                                    # equivalente en palabras.
current_user = 0  # Usada para identificar al actual usuario
current_language = 'esp'  # Usada para identificar el lenguaje actual

bg_color = '#bbb8c1'  # Usada para establecer el color de todas las ventanas.
root = Tk()  # Se crea el root prncipal

# Configuraciones
root.title('Astore')
root.resizable(False, False)


# Dimensiones de la pantalla
win_width, win_height = root.winfo_screenwidth(), root.winfo_screenheight()
win_width = 40*win_width/100
root.geometry('%dx%d+%d+0' % (win_width, win_height*92/100, win_width*80/100))


# Clase que se encarga de la creacion  del menu superior izquierdo, sus atributos estan destinados a la creacion de la
# ventana y sus metodos a el lanzamiento de otras ventanas.
class newMenu:
    def __init__(self, master):

        # Configuraciones principales
        self.bg_color = '#390959'
        self.canvas_menu = Canvas(master, height=win_height * 30 / 100, width=win_width * 25 / 100, bg=self.bg_color,
                                  bd=0, highlightthickness=0, relief='ridge')
        self.canvas_menu.pack()
        self.canvas_menu.place(x=0, y=0)

        self.width = self.canvas_menu.winfo_screenwidth()  # Largo de la ventana
        self.height = self.canvas_menu.winfo_screenheight()  # Alto de la ventana

        self.master = master

        if current_user == -1:  # Caso en el que el usuario es anonimo o invitado.
            self.canvas_menu.bind('<Leave>', self.destroy)  # Destruccion del menu.

            # Cargando la imagen de invitado
            self.load_guest_img = Image.open('../users/guest.gif').resize((50, 50), Image.ANTIALIAS)
            self.user_img = ImageTk.PhotoImage(self.load_guest_img)

            # Posicionando la imagen de invitado.
            self.user_img_label = Label(master, image=self.user_img, bd=0, highlightthickness=0,
                                        relief='ridge', bg=bg_color)
            self.user_img_label.pack()
            self.user_img_label.place(x=5, y=10)

            # Posicionamiento del nombre de usuario
            self.user_name = Label(self.canvas_menu, text='Invitado', font='Times 15', bg=self.bg_color, fg='white')
            self.user_name.pack()
            self.user_name.place(x=70, y=35)

            # Creacion de las banderas de cambio de idioma
            self.esp_flag_load = Image.open('../images/icons/espanna.gif').resize((30,20), Image.ANTIALIAS)
            self.esp_flag_img = ImageTk.PhotoImage(self.esp_flag_load)
            self.esp_flag_label = Label(self.canvas_menu, image=self.esp_flag_img, bg=self.bg_color, cursor='hand2')
            self.esp_flag_label.pack()
            self.esp_flag_label.place(x=win_width*10/100, y=5)
            self.esp_flag_label.bind('<Button-1>', self.change_language_toesp)

            self.eng_flag_load = Image.open('../images/icons/ingles.gif').resize((30, 20), Image.ANTIALIAS)
            self.eng_flag_img = ImageTk.PhotoImage(self.eng_flag_load)
            self.eng_flag_label = Label(self.canvas_menu, image=self.eng_flag_img, bg=self.bg_color, cursor='hand2')
            self.eng_flag_label.pack()
            self.eng_flag_label.place(x=win_width * 18 / 100, y=5)
            self.eng_flag_label.bind('<Button-1>', self.change_language_toeng)

            # Cambiando los labels con texto segun idioma
            if current_language == 'esp':  # Caso del idioma en espannol
                self.login_button = Button(self.canvas_menu, text='Iniciar sesion', bd=0, highlightthickness=0, relief='ridge',
                                           command=self.show_login)
                self.register_button = Button(self.canvas_menu, text='Registrarse', bd=0, highlightthickness=0,
                                              relief='ridge', command=show_register)
                self.home_button = Button(self.canvas_menu, text='Pagina Principal',bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_mainpage)
                self.apps_button = Button(self.canvas_menu, text='Todas las apps', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_search)
            else:  # Caso del idioma en ingles
                self.login_button = Button(self.canvas_menu, text='Login', bd=0, highlightthickness=0,
                                           relief='ridge',
                                           command=self.show_login)
                self.register_button = Button(self.canvas_menu, text='Sign up', bd=0, highlightthickness=0,
                                              relief='ridge', command=show_register)
                self.home_button = Button(self.canvas_menu, text='Home Page', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_mainpage)
                self.apps_button = Button(self.canvas_menu, text='All apps', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_search)

            # Ubicando los botones recien creados
            self.login_button.pack()
            self.register_button.pack()
            self.home_button.pack()
            self.apps_button.pack()
            self.login_button.place(x=0, y=75)
            self.home_button.place(x=0, y=165)

            # Cambiando el tamanno y la ubicacion de los botones segun el idioma
            if current_language == 'esp':  # Caso espannol
                self.register_button.place(x=win_width * 11 / 100, y=120)
                self.apps_button.place(x=win_width*8/100, y=210)
            else:  # Caso ingles
                self.register_button.place(x=win_width * 14 / 100, y=120)
                self.apps_button.place(x=win_width*14/100, y=210)
        else:  # Menu para un usuario registrado.
            try:  # Intenta cargar la imagen de perfil
                self.load_user_img = Image.open(users_list[current_user].perfil).resize((54,50), Image.ANTIALIAS)
            except:  # Si no le es posible, utilizada la imagen por defecto, la de invitado
                self.load_user_img = Image.open('../users/guest.gif').resize((54, 50), Image.ANTIALIAS)
            self.user_img = ImageTk.PhotoImage(self.load_user_img)

            self.canvas_menu.bind('<Leave>', self.destroy)

            self.user_img_label = Label(master, image=self.user_img, bd=0, highlightthickness=0,
                                        relief='ridge', bg=bg_color)
            self.user_img_label.pack()
            self.user_img_label.place(x=5, y=10)

            self.user_name = Label(self.canvas_menu, text='%s' % users_list[current_user].name,
                                   font='Times 15', bg=self.bg_color, fg='white', wraplengt='100') # creando el nombre del usuario
            self.user_name.pack()  # Posicionandolo
            self.user_name.place(x=70, y=35)

            # Creando y posicionando los iconos de cambio de idioma
            self.esp_flag_load = Image.open('../images/icons/espanna.gif').resize((30, 20), Image.ANTIALIAS)
            self.esp_flag_img = ImageTk.PhotoImage(self.esp_flag_load)
            self.esp_flag_label = Label(self.canvas_menu, image=self.esp_flag_img, bg=self.bg_color, cursor='hand2')
            self.esp_flag_label.pack()
            self.esp_flag_label.place(x=win_width * 10 / 100, y=5)
            self.esp_flag_label.bind('<Button-1>', self.change_language_toesp)

            self.eng_flag_load = Image.open('../images/icons/ingles.gif').resize((30, 20), Image.ANTIALIAS)
            self.eng_flag_img = ImageTk.PhotoImage(self.eng_flag_load)
            self.eng_flag_label = Label(self.canvas_menu, image=self.eng_flag_img, bg=self.bg_color, cursor='hand2')
            self.eng_flag_label.pack()
            self.eng_flag_label.place(x=win_width * 18 / 100, y=5)
            self.eng_flag_label.bind('<Button-1>', self.change_language_toeng)

            if users_list[current_user].admin == 'S' or users_list[current_user].admin == 'si':  # Verifica si un usuario es administrador para mostrar el boton de editar la tabla de vendedores
                if current_language == 'esp':  # Crea el boton de admistrar vendedores en espannol
                    self.admin_button = Button(self.canvas_menu, text='Administrar\nVendedores', bd=0, highlightthickness=0,
                                           relief='ridge', command=self.show_admin)
                else:  # En ingles
                    self.admin_button = Button(self.canvas_menu, text='Manage\nSellers', bd=0, highlightthickness=0,
                                               relief='ridge', command=self.show_admin)
                self.admin_button.pack()  # Lo posiciona
                self.admin_button.place(x=0, y=self.height*20/100)
            if current_language == 'esp':  # Cambia el texto de los labels segun el idioma, caso espannol
                self.perfil_button = Button(self.canvas_menu, text='Mi perfil', font='Times 8', bd=0, highlightthickness=0,
                                           relief='ridge', height=1, width=6, command=create_my_profile_page)
                self.register_button = Button(self.canvas_menu, text='Registrarse', bd=0, highlightthickness=0,
                                              relief='ridge', command=show_register)
                self.home_button = Button(self.canvas_menu, text='Pagina Principal', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_mainpage)
                self.apps_button = Button(self.canvas_menu, text='Todas las apps', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_search)
                self.logout_button = Button(self.canvas_menu, text='Cerrar sesion', bd=0, highlightthickness=0,
                                            relief='ridge', command=logout)
            else:  # Caso ingles
                self.perfil_button = Button(self.canvas_menu, text='My profile', font='Times 8', bd=0,
                                            highlightthickness=0,
                                            relief='ridge', command=create_my_profile_page, height=1, width=6)
                self.register_button = Button(self.canvas_menu, text='Sign up', bd=0, highlightthickness=0,
                                              relief='ridge', command=show_register)
                self.home_button = Button(self.canvas_menu, text='Home page', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_mainpage)
                self.apps_button = Button(self.canvas_menu, text='All apps', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_search)
                self.logout_button = Button(self.canvas_menu, text='Log out', bd=0, highlightthickness=0,
                                            relief='ridge', command=logout)

            # Posiciona los botones recien creados
            self.perfil_button.pack()
            self.home_button.pack()
            self.apps_button.pack()
            self.logout_button.pack()

            # Cambia el tamanno de los botones segun idioma, por que algunas palabras son mas largas en un idioma que en otro
            if current_language == 'esp':  # Caso idioma espannol
                self.apps_button.place(x=win_width * 8 / 100, y=140)
                self.logout_button.place(x=win_width * 4 / 100, y=self.height * 26 / 100)
            else:  # Caso idioma ingles
                self.apps_button.place(x=win_width * 14 / 100, y=140)
                self.logout_button.place(x=win_width * 7 / 100, y=self.height * 26 / 100)

            # Posiciona los botones recien creados
            self.perfil_button.place(x=5, y=61)
            self.home_button.place(x=0, y=100)


    # E: Mixtas, ninguna importante.
    # S: Esta funcion no retorna, su unico objetivo es mostrar la ventana de login.
    # R: No hay restricciones para las entradas
    def show_login(self, *args):
        # Intenta aplicar deiconify a login.win_login, si no puede, significa que la ventana esta en withdraw.
        try:
            login.win_login.deiconify()
            login.win_login.lift()  # Levanta la ventana para pasarla al frente
            login.win_login.focus_force()  # Hace un focus forzado a la ventana nueva
            self.destroy()  # Destruye el menu
        except:  # Si el login window no esta en modo withdraw se le hace
            login.win_login.withdraw()
            login.win_login.focus_force()
            self.destroy()  # Desturye el menu

    # E: Mixtas, ninguna importante.
    # S: Esta funcion no retorna, su unico objetivo es mostrar la ventana de administracion.
    # R: No hay restricciones para las entradas
    def show_admin(self, *args):
        global new_manage_win  # Utiliza la variable para sobreescribirla

        # Intenta aplicar deiconify a login.win_login, si no puede, significa que la ventana esta en withdraw.
        try:
            new_manage_win.deiconify()
            new_manage_win.lift()
            new_manage_win.focus_force()
            self.destroy()
        except:
            new_admin_win = Toplevel()  # Crea una nueva ventana
            manageWinVendedores(new_admin_win)  # En base a la ventana recien creada construye la pagina de admisitrar vendedores
            new_admin_win.focus_force()
            self.destroy()  # Destruye el menu

    # E: Mixtas, ninguna importante.
    # S: Esta funcion no retorna, su unico objetivo es mostrar la ventana principal.
    # R: No hay restricciones para las entradas
    def show_mainpage(self, *args):
        global main  # Utiliza la variable global main para destruir el main actual y forzar un random del mainpage

        # Intenta aplicar deiconify a login.win_login, si no puede, significa que la ventana esta en withdraw.
        try:
            self.master.withdraw()  # Esconde la ventana actual
            root.deiconify()
            main.kill()  # Destruye el viejo main
            main = main_window(root, current_language)  # Crea un nuevo main
            root.lift()  # Trae el nuevo main arriba
            root.focus_force()  # Fuerza un focus al nuevo main
            self.destroy()  # Destruye el menu actual
        except:
            root.withdraw()
            main.kill()  # Destruye el viejo main
            main = main_window(root, current_language)  # Crea un nuevo main
            self.master.withdraw()  # Esconde la ventana actual

    # E: Mixtas, ninguna importante o utilizada.
    # S: Esta funcion no retorna, su unico objetivo es mostrar la ventana de busqueda de apps.
    # R: No hay restricciones para las entradas
    def show_search(self, *args):
        try:
            self.master.withdraw()
            search.win.deiconify()
            search.win.lift()
            search.win.focus_force()
            self.destroy()
        except:
            search.win.withdraw()

    # E: Corresponden al evento que llama la funcion, pero no se utilizan.
    # S: No retorna, su funcion es destruir la ventana actual.
    # R: No hay restricciones
    def destroy(self, *args):
        self.canvas_menu.destroy()  # Destruye el canvas sobre el que esta montado todo
        self.user_img_label.destroy()  # Destruye una imagen especifica.

    # E: Corresponden al evento que llama la funcion, no se utilizan.
    # S: No retorna, solo cambia el lenguaje del programa.
    # R: No hay restricciones.
    def change_language_toeng(self, *args):
        global main  # Se utiliza para sobreescribir la informacion del idioma en el main
        global menu  # Se utiliza para sobreescribir la informacion del idioma en el menu
        global current_language  # Se utiliza para guardar la informacion del idioma

        if current_language == 'esp':  # Caso espannol a ingles
            login.change_languagetoeng()  # Llama el metodo para cambiar a idioma ingles de la ventana de login
            adminwin.to_eng()  # Llama el metodo para cambiar a idioma ingles de la ventana de administracion
            current_language = 'eng'  # Cambia la variable global, asi las otras partes del codigo saben que se cambio el idioma
            main.kill()  # Destruye el main viejo
            register.toeng()  # Llama el metodo de cambiar a idioma ingles de la ventana de register
            search.toeng()  # Llama el metodo de cambiar a idioma ingles de la ventana de busqueda
            self.destroy()  # Destruye el menu
            main = main_window(root, current_language)  # Crea un nuevo main
        else:  # Caso espannol a espannol
            # No hace nada, pues ya esta en ingles, solo destruye el menu para tener una efimera retroalimentacion
            self.destroy()

    # E: Corresponden al evento que llama la funcion, no se utilizan.
    # S: No retorna, solo cambia el lenguaje del programa.
    # R: No hay restricciones.
    def change_language_toesp(self, *args):
        global main  # Se utiliza para sobreescribir la informacion del idioma en el main
        global menu  # Se utiliza para sobreescribir la informacion del idioma en el menu
        global current_language  # Se utiliza para guardar la informacion del idioma
        if current_language == 'eng':  # Caso ingles a espannol
            current_language = 'esp'  # Cambia la global a espannol
            login.change_languagetoesp()
            adminwin.to_esp()
            register.toesp()
            search.toesp()
            main.kill()
            self.destroy()
            main = main_window(root, current_language)
        else:  # Espannol a espannol
            # No hace nada, pues ya esta en espannol, solo destruye el menu para tener una efimera retroalimentacion
            self.destroy()

# Clase que define la ventana principal. Sus atributos van orientados a la creacion de la ventana, segun si se trata de un usuario
# o un invitado y sus metodos van destinados a la aleatorizacion de los elementos de la ventana, entre otros
class main_window:
    # Funcion constructor
    def __init__(self, master, language):
        self.language = language
        if current_user == -1 :  # Caso de usuario anonimo o invitado
            self.master = master
            self.random_mainpage()  # Aleatoriza las apps mostradas.
            self.welcome_canvas = Canvas(master, height='200', width='500', bg=bg_color, bd=0, highlightthickness=0,
                                         relief='ridge')  # Crea el canvas superior.
            self.welcome_canvas.pack()  # Lo posiciona
            self.welcome_canvas.place(x=win_width * 10 / 100, y=50)


            if current_language == 'esp':  # Caso de lenguaje espannol
                # Crea unos cuantos labels con textos de bienvenida y los posiciona
                self.welcome_text = Label(self.welcome_canvas, text='Bienvenido, invitado!', font='Times 20', bg=bg_color)
                self.quote = Label(self.welcome_canvas, text='Recuerde que debe\n iniciar sesion para descargar',
                                   font='Times 20 italic', bg=bg_color)
                self.quote.pack()
                self.quote.place(x=0, y=70)
                self.welcome_text.pack()
                self.welcome_text.place(x=0, y=20)
            else:  # Caso de lenguaje ingles
                self.welcome_text = Label(self.welcome_canvas, text='Welcome, guest!', font='Times 20',
                                          bg=bg_color)
                self.quote = Label(self.welcome_canvas, text='Please login in order to\ndownload content',
                                   font='Times 20 italic', bg=bg_color)
                self.quote.pack()
                self.quote.place(x=60, y=70)
                self.welcome_text.pack()
                self.welcome_text.place(x=90, y=20)


            # Carga la imagen de invitado, la renderiza, le cambia el tamanno y la pone en un label
            self.load_guest_img = Image.open('../users/guest.gif').resize((125, 125), Image.ANTIALIAS)
            self.guest_img = ImageTk.PhotoImage(self.load_guest_img)
            self.user_img_label = Label(self.welcome_canvas, image=self.guest_img, bd=0, highlightthickness=0,
                                        relief='ridge')
            # Posiciona el label de la imagen de invitado.
            self.user_img_label.pack()
            self.user_img_label.place(x=350, y=20)

            # carga la imagen que abre el menu, la renderiza, le cambia el tamanno y la pone en un label.
            self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.gif').resize((30, 30), Image.ANTIALIAS)

            self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
            self.hamb_icon_label = Label(root, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                         bg=bg_color, cursor='hand2')  # Para efectos de retroalimentacion se annadio la funcion de cambiar el mouse en label que se pueden presionar

            # Posiciona el label con la imagen.
            self.hamb_icon_label.pack()
            self.hamb_icon_label.place(x=1, y=1)

            self.hamb_icon_label.bind('<Button-1>', self.show_menu)  # Crea el vinculo con la accion de darle click a la image y el metodo show_menu, asi, muestra el menu al darle click
        else:  # Caso de un usuario registrado
            self.master = master
            self.random_mainpage()  # Aleatoriza las apps y sus posiciones

            self.welcome_canvas = Canvas(master, height='200', width='500', bg=bg_color, bd=0, highlightthickness=0,
                                         relief='ridge')  # Crea el canvas superior
            self.welcome_canvas.pack()  # Posiciona dicho canvas
            self.welcome_canvas.place(x=win_width * 10 / 100, y=50)
            if current_language == 'esp':  # Caso de lenguaje espannol
                # Crea el texto de bienvenida
                self.welcome_text = Label(self.welcome_canvas, text='Bienvenido, %s!' % users_list[current_user].name,
                                          font='Times 20', bg=bg_color)  # Toma el nombre del usuario actual para ponerlo en el texto de bienvenida
            else: # Caso de lenguaje ingles
                # Crea el texto de bienvenida
                self.welcome_text = Label(self.welcome_canvas, text='Welcome, %s!' % users_list[current_user].name,
                                          font='Times 20', bg=bg_color)
            # Posiciona el texto de bienvenida
            self.welcome_text.pack()
            self.welcome_text.place(x=0, y=20)

            self.quote_canvas = Canvas(self.welcome_canvas, bg=bg_color, width=349, height =140, bd=0, highlightthickness=0,
                                         relief='ridge')  # Crea el canvas de la frase
            # posiciona dicho canvas
            self.quote_canvas.pack()
            self.quote_canvas.place(x=0,y=50)

            self.randomize_quote()  # Aleatoriza la frase
            try:  # Intenta cargar la imagen del usuario explicita en la tabla.
                self.load_user_img = Image.open(users_list[current_user].perfil).resize((125, 125), Image.ANTIALIAS)
            except:  # Si no existe carga la default
                self.load_user_img = Image.open('../users/guest.gif').resize((125, 125), Image.ANTIALIAS)
            self.user_img = ImageTk.PhotoImage(self.load_user_img)
            self.user_img_label = Label(self.welcome_canvas, image=self.user_img, bd=0, highlightthickness=0,
                                        relief='ridge') # Pone la imagen en un canvas
            self.user_img_label.image = self.user_img  # Reescribe la imagen para no perderla
            # Posiciona la imagen
            self.user_img_label.pack()
            self.user_img_label.place(x=350, y=20)

            # Carga la imagen del menu, la renderiza, cambia el tamanno y la pone en un label.
            self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.gif').resize((30, 30), Image.ANTIALIAS)

            self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
            self.hamb_icon_label = Label(root, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                         bg=bg_color, cursor='hand2')
            # Posiciona el label de la imagen del menu
            self.hamb_icon_label.pack()
            self.hamb_icon_label.place(x=1, y=1)

            self.hamb_icon_label.bind('<Button-1>', self.show_menu)  # Abre el menu al presionar la imagen

    # E: Mixtas, ninguna importante o utilizada.
    # S: Esta funcion no retorna, su unico objetivo es mostrar el menu.
    # R: No hay restricciones para las entradas
    def show_menu(self, *args):
        global menu  # Utilizada para sobreescribir
        menu = newMenu(self.master)

    # E: No tiene entradas
    # S: No retorna, solo aleatoriza las apps y su posicion en la pagina principal
    # R: No hay restricciones, pues no hay entradas
    def random_mainpage(self):
        global category_list

        # Crea el canvas donde se posicionaran las apps
        self.bottom_canvas = Canvas(self.master, height=win_height - 20, width=win_width, bg=bg_color)
        self.bottom_canvas.pack()
        categorias = category_list
        master = self.bottom_canvas
        self.random_mainpage_aux(master, categorias, [], 1)  # Llama una funcion auxiliar

    def random_mainpage_aux(self, master, categorias, used, cont):
        rand = randint(0, 3)  # Crea un numero aleatorio entre 0 y 3
        ini_y = 50  # La pos en y inicial de cada espacio de un app
        com_height = 188  # La altura en comun de cada espacio de un app
        fix = 188  # Constante para arreglar el traslape entre espacios de apps.
        if len(used) == 3:  # Caso base, used es una lista vacia utilizada para guardar las categorias que ya se han puesto para que no repita
            return
        elif not self.is_in(used, categorias[rand], 0):
            if categorias[rand] == 'Juegos':  # Si la lista en el indice rand tiene el elemento 'Juegos'
                categoria_juego = juegos(master, ini_y, fix, com_height, cont)  # Crea una nueva instancia de la clase juegos
                return self.random_mainpage_aux(master, categorias, used + ['Juegos'], cont + 1)
            elif categorias[rand] == 'Musica':# Si la lista en el indice rand tiene el elemento 'Musica'
                categoria_musica = musica(master, ini_y, fix, com_height, cont)  # Crea una nueva instancia de la clase juegos
                return self.random_mainpage_aux(master, categorias, used + ['Musica'], cont + 1)
            elif categorias[rand] == 'Redes Sociales':  # Si la lista en el indice rand tiene el elemento 'Redes'
                categoria_redes = redes(master, ini_y, fix, com_height, cont)  # Crea una nueva instancia de la clase juegos
                return self.random_mainpage_aux(master, categorias, used + ['Redes Sociales'], cont + 1)
            else:  # Si la lista en el indice rand tiene el elemento 'Herramientas'
                categoria_herramientas = herramientas(master, ini_y, fix, com_height, cont)  # Crea una nueva instancia de la clase juegos
                return self.random_mainpage_aux(master, categorias, used + ['Herramientas'], cont + 1)
        else:  # Entra a este caso si se da que ya se uso una de las categorias
            return self.random_mainpage_aux(master, categorias, used, cont)

    # E: Una lista, un elemento y un contador
    # S: True si se da que el elemento esta en la lista, false de lo contrario
    # R: No se pusieron restricciones porque no es algo que introduzca el usuario, es algo bien establecido por el programador
    def is_in(self, list1, ele, cont):
        if len(list1) == cont:  # Caso base, el contador alcanzo la longitud de la lista
            return False
        elif list1[cont] == ele:  # Se encuentra una coincidencia
            return True
        else:  # No se encuentra coincidencia
            return self.is_in(list1, ele, cont + 1)

    # E: No hay entradas, no se necesitan
    # S: La unica funcion del codigo es destruir los widgets de esta clase.
    # R: No hay restricciones, no hay entradas.
    def kill(self):
        self.bottom_canvas.destroy()
        self.welcome_canvas.destroy()
        self.user_img_label.destroy()

    # E: No hay entradas, no son necesarias
    # S: La funcion del codigo es aleatorizar las frases
    # R: No hay restricciones
    def randomize_quote(self):
        try:  # Intenta destruir la quote existente
            self.quote.destroy()
            self.randomize_quote()
        except:  # Si no puede, es porque no existe quote, entonces crea una nueva
            if self.language == 'esp':  # Frases en espannol
                self.quote_text = esp_quotes.get_quote()[0]  # Toma la frase de la clase de frases en espannol
                self.quote_author = esp_quotes.get_quote()[1]  # Toma el autor de la frase de la clase de frases en espannol
            else: # Frases en ingles
                self.quote_text = eng_quotes.get_quote()[0]  # Toma la frase de la clase de frases en ingles
                self.quote_author = eng_quotes.get_quote()[1]  # Toma el autor de la frase de la clase de frases en ingles
            self.quote = Label(self.quote_canvas, font='Times 13 italic', text=self.quote_text, bg=bg_color,
                               wraplengt=330)  # Crea el label de la frase
            # Lo posiciona
            self.quote.pack()
            self.quote.place(x=0, y=20)

            self.quote_author = Label(self.quote_canvas, font='Times 13 italic bold', text='-'+self.quote_author,
                                      bg=bg_color)  # Crea el label del autor
            # Lo posiciona
            self.quote_author.pack()
            self.quote_author.place(x=160, y=100)


# Clase encargada de crear la ventana de login, sus atributos estan dirigidos a la creacion de la ventana, sus metodos
# estan dirigidos, principalmente a la funcion de inicio de sesion.
class newLogin:
    # Funcion constructor
    def __init__(self, master):
        self.master = master
        # Configuracion principal
        self.win_login = Toplevel(bg=bg_color)
        self.win_login.resizable(False, False)
        self.win_login.title('Astore')

        # Dimensiones
        self.win_login_width, self.win_login_height = root.winfo_screenwidth()*20/100, root.winfo_screenheight()*27/100
        self.win_login.geometry('%dx%d+%d+%d' % (self.win_login_width, self.win_login_height,
                                                 self.win_login_width + self.win_login_width,
                                                 self.win_login_height))
        # Creando y posicionando el titulo
        self.title = Label(self.win_login, text='Astore', font='Times 50', bg=bg_color)
        self.title.pack()
        self.title.place(x=self.win_login_width*22/100, y=0)

        # Creando stings variables para los entrys
        self.none1 = StringVar()
        self.none1.set('')   # Setteando un valor inicial
        self.none2 = StringVar()
        self.none2.set('')  # Setteando un valor inicial
        # Creando entrys y labels
        self.user_label = Label(self.win_login, text='Usuario:', font='Times 15', bg=bg_color)
        self.user_entry = Entry(self.win_login, textvariable=self.none1)
        self.pass_label = Label(self.win_login, text='Contraseña:', font='Times 15', bg=bg_color)
        self.pass_entry = Entry(self.win_login, textvariable=self.none2, show='*')

        # Posicionando los entrys y labels recien creados
        self.pass_entry.pack()
        self.pass_label.pack()
        self.user_label.pack()
        self.user_entry.pack()
        self.user_label.place(x=self.win_login_width*14/100, y=self.win_login_height*32/100)
        self.user_entry.place(x=self.win_login_width*38/100, y=self.win_login_height*35/100)
        self.pass_label.place(x=self.win_login_width*6/100, y=self.win_login_height*44/100)
        self.pass_entry.place(x=self.win_login_width*38/100, y=self.win_login_height*47/100)

        # Creando y posicionando botones
        self.login_button = Button(self.win_login, text='Iniciar\nsesion', command=self.login)
        self.register_button = Button(self.win_login, text='Registrarse', command= self.__show_register)
        self.login_button.pack()
        self.register_button.pack()
        self.login_button.place(x=self.win_login_width*23/100, y=self.win_login_height*70/100)
        self.register_button.place(x=self.win_login_width*48/100, y=self.win_login_height*70/100)

        self.win_login.protocol("WM_DELETE_WINDOW", self.win_login.withdraw)  # Vinculando el protocolo de cerrar la ventana a un withdraw, para que no se elimine
                                                                              # todo al cerrar
        self.win_login.bind('<Return>', self.login)  # Vinculando el boton enter con la funcion de login

    # E: Varios, no reelevantes, no utilizados
    # S: No retorna, su unica funcion es mostrar la ventana de registro.
    # R: No hay restricciones para la funcion
    def __show_register(self, *args):
        self.win_login.withdraw()
        show_register()

    # E: No hay, sin embargo, podrian tomarse en cuenta los get a los entrys como entrada, en este caso son un nombre de usuario y una contrasenna
    # S: No retorna, cambia el usuario actual por el usuario escrito en name, si y solo si, la contrasenna de este es la que provee la persona que usa el programa
    def login(self, *args):
        global current_user  # Usada para sobreescribir el usuario actual
        global users_list  # Usada para obtener la contrasenna de el nombre de usuario propuesto por el que usa el programa
        global main  # Usada para sobreescribir el main, hacer uno nuevo.
        global menu  # Usada para hacer un nuevo menu
        global current_language  # Usada para cambiar el idioma, por el preferido del usuario
        # Obteniendo y guardando en variables lo que haya en los entrys.
        login_user = self.user_entry.get()
        login_pass = self.pass_entry.get()
        user_row = users.is_in(login_user, 0, 0)  # False si el usuario propuesto no existe, o si no es el renglon donde esta el usuario propuesto

        # Verifica la validez de la contrasenna
        if user_row and user_row[2].lstrip() == login_pass:  # Si es valida
            current_language = user_row[7]
            self.login_aux(login_user, 0)  # Llamada auxiliar
            main.kill()
            menu.destroy()
            main = main_window(root, current_language)
            menu = newMenu(self.master)
            self.win_login.withdraw()
            self.none1.set('')
            self.none2.set('')
        else: # Si no lo es
            if current_language == 'esp':  # Verifica el lenguaje
                messagebox.showerror(title='Error', message='Usuario o contraseña incorrecta')
            else:
                messagebox.showerror(title='Error', message='Wrong user or password')

    def login_aux(self,login_user, cont):
        global current_user  # Para sobreescribir el usuario actual
        if cont == len(users_list):
            return 'Err'
        elif users_list[cont].username == login_user:
            current_user = cont
            return
        else:
            self.login_aux(login_user, cont+1)

    # E: No hay entradas
    # S: No retorna, solo destruye la ventana actual.
    # R: No hay restricciones
    def destroy(self):
        self.win_login.destroy()

    # E: No hay entradas
    # S: No retorna, solo se encarga de cambiar el lenguaje a ingles
    # R: No hay restricciones.
    def change_languagetoeng(self):
        self.user_label.config(text='   User:')
        self.pass_label.config(text='  Password:')
        self.login_button.config(text='Login')
        self.register_button.config(text='Sign Up')

    # E: No hay entradas
    # S: No retorna, solo se encarga de cambiar el lenguaje a ingles
    # R: No hay restricciones.
    def change_languagetoesp(self):
        self.user_label.config(text='Usuario:')
        self.pass_label.config(text='Contraseña:')
        self.login_button.config(text='Iniciar\nsesion')
        self.register_button.config(text='Registrarse')

# Clase encargada de crear la ventana de registro, sus atributos estan orientados a la creacion de la nueva ventana y sus metodos
# a todo lo relacionado con annadir un nuevo usuario
class newRegister:
    # Funcion constructor
    def __init__(self, master):
        # Configuracion principal
        self.bg_color = '#bbb8c1'
        self.win_register = Toplevel(bg=bg_color)
        self.win_register.title('Registro')
        self.win_register.resizable(False, False)

        # Dimensiones
        self.win_register_width = self.win_register.winfo_screenwidth()*35/100
        self.win_register_height = self.win_register.winfo_screenheight()*95/100
        self.win_register.geometry('%dx%d+%d+0' % (self.win_register_width, self.win_register_height * 89 / 100,
                                                   self.win_register_width * 80 / 100))

        # Creando labels y entrys
        self.descripcion = Label(self.win_register, text='¡Registrese en Astore y sea parte de nuestra\ncomunidad de'+
                                 ' compra y venta!', font='Times 24', bg=self.bg_color)
        self.descripcion.grid()
        self.descripcion.place(x=0, y=0)

        self.name_label = Label(self.win_register, text='Nombre:', font='Times 15', bg=self.bg_color)
        self.name_entry = Entry(self.win_register, width=35)
        self.user_label = Label(self.win_register, text='Usuario:', font='Times 15', bg=self.bg_color)
        self.user_entry = Entry(self.win_register, width=35)
        self.pass_label = Label(self.win_register, text='Contraseña:', font='Times 13', bg=self.bg_color)
        self.pass_entry = Entry(self.win_register, width=35)
        self.repass_label = Label(self.win_register, text='Repetir contraseña:', font='Times 10', bg=self.bg_color)
        self.repass_entry = Entry(self.win_register, width=35)
        self.mail_label = Label(self.win_register, text='Correo:', font='Times 15', bg=self.bg_color)
        self.mail_entry = Entry(self.win_register, width=35)
        self.web_label = Label(self.win_register, text='Pagina web:', font='Times 13', bg=self.bg_color)
        self.web_entry = Entry(self.win_register, width=35)
        self.image_label = Label(self.win_register, text='Imagen de usuario:', font='Times 15', bg=self.bg_color)

        self.img_path = '../images/icons/no_image.png'
        self.load_blank = Image.open(self.img_path).resize((100, 100), Image.ANTIALIAS)
        self.blank_img = ImageTk.PhotoImage(self.load_blank)
        self.image_entry = Label(self.win_register, image=self.blank_img, cursor='hand2')
        self.pais_label = Label(self.win_register, text='Pais:', font='Times 15', bg=self.bg_color)

        self.variable = StringVar(self.win_register)
        self.variable.set('Costa Rica')
        self.pais_entry = OptionMenu(self.win_register, self.variable, 'Costa Rica', 'Otros')

        self.idioma_label = Label(self.win_register, text='Idioma preferido:', font='Times 15', bg=self.bg_color)

        self.esp_flag_load = Image.open('../images/icons/espanna.gif').resize((60, 40), Image.ANTIALIAS)
        self.esp_flag_img = ImageTk.PhotoImage(self.esp_flag_load)
        self.esp_flag_label = Label(self.win_register, image=self.esp_flag_img, bg='red', bd=4, cursor='hand2')
        self.esp_flag_label.bind('<Button-1>', self.espselected)

        self.eng_flag_load = Image.open('../images/icons/ingles.gif').resize((60, 40), Image.ANTIALIAS)
        self.eng_flag_img = ImageTk.PhotoImage(self.eng_flag_load)
        self.eng_flag_label = Label(self.win_register, image=self.eng_flag_img, bg=self.bg_color, cursor='hand2')
        self.eng_flag_label.bind('<Button-1>', self.engselected)

        # Añadiendo al grid
        self.name_label.grid()
        self.name_entry.grid()
        self.user_label.grid()
        self.user_entry.grid()
        self.pass_label.grid()
        self.pass_entry.grid()
        self.repass_label.grid()
        self.repass_entry.grid()
        self.mail_label.grid()
        self.mail_entry.grid()
        self.web_label.grid()
        self.web_entry.grid()
        self.image_label.grid()
        self.image_entry.grid()
        self.pais_label.grid()
        self.pais_entry.grid()
        self.idioma_label.grid()
        self.esp_flag_label.grid()
        self.eng_flag_label.grid()

        # Posicionando
        self.name_label.place(x=self.win_register_width*20/100, y=110)
        self.name_entry.place(x=self.win_register_width*37/100, y=115)
        self.user_label.place(x=self.win_register_width*20/100, y=170)
        self.user_entry.place(x=self.win_register_width*37/100, y=175)
        self.pass_label.place(x=self.win_register_width*20/100, y=233)
        self.pass_entry.place(x=self.win_register_width*37/100, y=235)
        self.repass_label.place(x=self.win_register_width*17/100, y=295)
        self.repass_entry.place(x=self.win_register_width*37/100, y=295)
        self.mail_label.place(x=self.win_register_width*20/100, y=350)
        self.mail_entry.place(x=self.win_register_width*37/100, y=355)
        self.web_label.place(x=self.win_register_width*19/100, y=410)
        self.web_entry.place(x=self.win_register_width*37/100, y=415)
        self.image_label.place(x=self.win_register_width*20/100, y=470)
        self.image_entry.place(x=self.win_register_width*60/100, y=450)
        self.pais_label.place(x=self.win_register_width*25/100, y=585)
        self.pais_entry.place(x=self.win_register_width*45/100, y=585)
        self.idioma_label.place(x=self.win_register_width*20/100, y=645)
        self.esp_flag_label.place(x=self.win_register_width*55/100, y=650)
        self.eng_flag_label.place(x=self.win_register_width*75/100, y=650)

        self.selected_language = 'esp'


        # Botones
        self.ready = Button(self.win_register, text='Listo', font='Times 18', command=self.add_user)
        self.ready.grid()
        self.ready.place(x=self.win_register_width*44/100, y=700)
        self.image_entry.bind('<Button-1>', self.change_img) # Vinculando el presionar el label con el metodo change_img

        self.win_register.protocol("WM_DELETE_WINDOW", self.win_register.withdraw)

    # E: El evento que llama la funcion, no se utiliza.
    # S: No retorna, solo cambia la imagen
    # R: No hay restricciones
    def change_img(self, *args):
        self.win_register.lower()  # Baja la pantalla actual, de otra manera la pantalla de seleccion de imagen quedaria debajo.
        self.img_path = fd.askopenfilename()  # Abre la pantalla de seleccion de archivos.
        try:  # Abre el archivo e intenta procesarlo como una imagen
            load_new_img = Image.open(self.img_path).resize((100,100),Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.image_entry.config(image=new_img)
            self.image_entry.image = new_img
        except:  # Si no puede procesarlo como una imagen carga la imagen de invitado
            if current_language == 'esp':  # verifica el idioma
                messagebox.showwarning(title='Warning', message='El archivo seleccionado no es una imagen procesable')
            else:
                messagebox.showerror(title='Warning', message='Selected archive is not an apropiate image')
            load_new_img = Image.open('../users/guest.gif').resize((100, 100), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.image_entry.config(image=new_img)
            self.image_entry.image = new_img
        self.win_register.lift()  # Devuelve la pantalla actual a su elevacion previa.

    # E: El evento que llama la funcion, no se utiliza.
    # S: No retorna, pero annade el usuario a la tabla de usuarios y todo lo que esto conlleva.
    def add_user(self, *args):
        global main  # Para crear un nuevo main con el nuevo usuario.
        global current_language  # Sobreescribe con el lenguaje preferido del nuevo usuario
        global current_user  # Sobreescribe con el usuario recien creado

        # Toma los valores de los entrys y los guarda en variables
        nombre = self.name_entry.get()
        usuario = self.user_entry.get()
        contra = self.pass_entry.get()
        recontra = self.repass_entry.get()
        correo = self.mail_entry.get()
        seller_id = int(users_list[len(users_list) - 1].seller_id) + 1
        buyer_id = int(users_list[len(users_list) - 1].buyer_id) + 1
        foto = self.img_path
        admin = 'no'
        fondo = 'None'
        pais = self.variable.get()
        language = self.selected_language
        webpage = self.web_entry.get()
        apps_compradas = '0'

        if users.is_in(usuario, 0, 1):  # Caso en el que el nombre de usuario propuesto ya existe
            if current_language == 'esp':  # verifica el idioma
                messagebox.showerror(title='error', message='Ya existe el nombre de usuario')
            else:
                messagebox.showerror(title='error', message='Username already taken')
        else:  # Caso en el que no existe el nombre de usuario
            if nombre.lstrip() != '' or usuario.lstrip() != '' or contra.lstrip() != '' or recontra.lstrip() != '' or correo.lstrip() != '':  # verifica que los campos esten llenos
                if contra.lstrip() == recontra.lstrip():  # Verifica que la contrasenna y la repeticion de la misma sena iguales
                    self.add_touser()
                    self.add_toseller()
                    self.add_tobuyer()
                    create_user(nombre, usuario, contra, str(seller_id), str(buyer_id), correo, webpage,foto,
                                fondo, apps_compradas, admin, pais, language, str(len(users_list))) # Crea el usuario
                    current_user = len(users_list) - 1
                    current_language = language
                    main.kill()
                    main = main_window(root, current_language)
                else:
                    if current_language == 'esp':  # Verifica idioma
                        return messagebox.showerror(title='Error', message='Contrasenas no iguales')
                    else:
                        return messagebox.showerror(title='Error', message='Passwords arent identical')
            else:
                if current_language == 'esp': # Verifica idioma
                    return messagebox.showerror(title='Error', message='Faltan espacios')
                else:
                    return messagebox.showerror(title='Error', message='Missing spaces')

    # E: No hay entradas
    # S: No retorna, solo annade a la tabla de usuarios.
    # R: No hay restricciones
    def add_touser(self):
        # Guarda los datos de los entrys en variables
        nombre = self.name_entry.get()
        usuario = self.user_entry.get()
        contra = self.pass_entry.get()
        foto = self.img_path
        admin = 'no'
        fondo = 'None'
        pais = self.variable.get()
        language = self.selected_language
        # Annade a la tabla de usuarios
        users.add([nombre, usuario, contra, foto, fondo, admin, pais, language, []])
        # Esconde la ventana actual
        self.win_register.withdraw()

    # E: No hay entradas
    # S: No retorna, solo annade a la tabla de sellers
    # R: No hay restricciones
    def add_toseller(self):
        nombre = self.name_entry.get()
        correo = self.mail_entry.get()
        if self.web_entry.get().lstrip() != '':
             webpage = self.web_entry.get()
        else:
            webpage = 'None'
        id = int(users_list[len(users_list)-1].seller_id)+1  # Toma el id del seller anterior y le suma 1
        sellers.add([str(id), nombre, correo, webpage])  # Llama a el metodo de sellersTable de annadir

    # E: No hay entradas
    # S: No retorna, solo annade a la tabla de sellers
    # R: No hay restricciones
    def add_tobuyer(self):
        nombre = self.name_entry.get()
        correo = self.mail_entry.get()
        apps = '0'
        id = int(users_list[len(users_list) - 1].buyer_id) + 1 # Toma el id del buyer anterior y le suma 1

        buyers.add([str(id), nombre, correo, apps])  # Llama al metodo de buyersTable de annadir

    # E: El evento que lo llama
    # S: No retorna, solo se encarga de cambiar los bordes y el color para distinguir banderas
    # R: No hay restricciones
    def engselected(self, *args):
        self.selected_language = 'eng'
        self.eng_flag_label.config(bd=4, bg='red')
        self.esp_flag_label.config(bd=0, bg=bg_color)

    # E: El evento que lo llama
    # S: No retorna, solo se encarga de cambiar los bordes y el color para distinguir banderas
    # R: No hay restricciones
    def espselected(self, *args):
        self.esp_flag_label.config(bd=4, bg='red')
        self.selected_language = 'esp'
        self.eng_flag_label.config(bd=0, bg=bg_color)

    # E: No hay entradas
    # S: No retorna, solo se encarga de cambiar el idioma de los labels a espannol
    # R: No hay restricciones
    def toesp(self):
        self.name_label.config(text='Nombre:')
        self.user_label.config(text='Usuario:')
        self.pass_label.config(text='Contraseña:')
        self.image_label.config(text='Imagen de usuario:')
        self.idioma_label.config(text='Idioma preferido:')
        self.repass_label.config(text='Repetir contraseña:')
        self.mail_label.config(text='Correo:')
        self.web_label.config(text='Pagina web:')
        self.pais_label.config(text='Pais:')
        self.ready.config(text='Listo')

    # E: No hay entradas
    # S: No retorna, solo se encarga de cambiar el idioma de los labels a ingles
    # R: No hay restricciones
    def toeng(self):
        self.name_label.config(text='Name:')
        self.user_label.config(text='User:')
        self.pass_label.config(text='Password:')
        self.image_label.config(text='User image:')
        self.idioma_label.config(text='Prefered language:')
        self.repass_label.config(text='Repeat password:')
        self.mail_label.config(text='Mail:')
        self.web_label.config(text='Web page:')
        self.pais_label.config(text='Country:')
        self.ready.config(text='Ready')


# Clase encargada de crear una nueva ventana de administracion de vendedores, sus atributos estan orientados a
# crear la ventana, mientras sus metodos son meramente de cambio de idioma
class adminWindow:
    # Funcion constructor
    def __init__(self):
        # Configuracion
        self.win = Toplevel()
        self.win.resizable(False, False)

        # Dimensiones
        self.sc_width, self.sc_height = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        self.width = 20 * self.sc_width/100
        self.height = 20 * self.sc_height/100
        self.win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 41 / 100, self.sc_height*30/100))

        # Contenedores
        self.top_canvas = Canvas(self.win, bg=bg_color, width=self.width, height=self.height/2,).grid(row=0, columnspan=2)
        self.bottom_canvas_left = Canvas(self.win, bg=bg_color, width=self.width/2, height=self.height/2,).grid(row=1, column=0)
        self.bottom_canvas_right = Canvas(self.win, bg=bg_color, width=self.width/2, height=self.height/2,).grid(row=1, column=1)

        # Labels
        self.apps_label = Label(self.win, text='Aplicaciones', font='Times 20', bg=bg_color)
        self.vendedores_label = Label(self.win, text='Vendedores', font='Times 20', bg=bg_color)
        self.compradores_label = Label(self.win, text='Compradores', font='Times 20', bg=bg_color)

        # Posicionando los labels
        self.apps_label.grid(row=0, columnspan=2)
        self.vendedores_label.grid(row=1, column=0)
        self.compradores_label.grid(row=1, column=1)

        self.win.protocol("WM_DELETE_WINDOW", self.win.withdraw) # Vinculando el boton cerrar con withdraw para que no se elimine la ventana

    # E: No hay entradas
    # S: No retorna, solo se encarga de cambiar el idioma de los labels a ingles
    # R: No hay restricciones
    def to_eng(self):
        self.apps_label.config(text='Aplications')
        self.vendedores_label.config(text='Sellers')
        self.compradores_label.config(text='Buyers')

    # E: No hay entradas
    # S: No retorna, solo se encarga de cambiar el idioma de los labels a espannol
    # R: No hay restricciones
    def to_esp(self):
        self.apps_label.config(text='Aplicaciones')
        self.vendedores_label.config(text='Vendedores')
        self.compradores_label.config(text='Compradores')

# Clase encargada de la creacion de la ventana de busqueda de apps, sus atributos estan dirigidos a la creacion de la ventana
# mientras sus metodos a la busqueda y posicionamiento de apps.
class searchWin:
    def __init__(self):
        # Configuracion inicial
        self.win = Toplevel()
        self.win.resizable(False, False)

        # Dimensiones
        self.sc_width, self.sc_height = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        self.width = 70 * self.sc_width / 100
        self.height = 80 * self.sc_height / 100
        self.win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 15 / 100, self.sc_height * 10 / 100))

        # Contenedor principal
        self.canvas = Canvas(self.win, width=self.width, height=self.height)
        self.canvas.pack()

        self.title = Label(self.canvas, text='Astore', font='Times 20')
        self.title.pack()
        self.title.place(x=self.width*45/100, y=1)

        if current_language == 'esp':  # Version espannol
            self.entry_label = Label(self.canvas, text='Buscar:', font='Times 13')
        else: # Version ingles
            self.entry_label = Label(self.canvas, text='Search:', font='Times 13')

        # Posiciona
        self.entry_label.pack()
        self.entry_label.place(x=self.width*6/100, y=self.height*8.3/100)
        self.entry = Entry(self.canvas, width=40)
        self.entry.pack()
        self.entry.place(x=self.width*14/100, y=self.height*9/100)
        self.entry.bind('<KeyRelease>', self.start_search)  # Cada vez que se suelta una tecla llama el metodo que busca en todas las apps

        # Configuraciones del boton del menu
        self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.gif').resize((30, 30), Image.ANTIALIAS)

        self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
        self.hamb_icon_label = Label(self.win, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                     cursor='hand2')

        self.hamb_icon_label.pack()
        self.hamb_icon_label.place(x=1, y=1)
        self.hamb_icon_label.bind('<Button-1>', self.show_menu)

        self.app_canvas = Canvas(self.win, width=self.width*89/100, height=self.height*85/100)  # Canvas donde iran las apps encontradas
        self.app_canvas.pack()
        self.app_canvas.place(x=self.width*6/100, y=self.height*13/100)

        # Tamannos comunes para los espacios de las apps
        self.comm_height = self.height*15/100
        self.comm_width = self.width*15/100

        # La ventana aguanta 4 rows y 6 columns
        self.showed_apps=[]  # Lista para las apps mostradas, para no repetir
        self.posicionar_apps(apps.get_list(), 0, 0, 0)

        self.win.protocol('WM_DELETE_WINDOW', root.destroy)

    # E: El evento que la llama, no utilizado
    # S: Retorna el metodo posicionar_apps para acomodar las apps encontradas.
    # R: No hay restricciones
    def start_search(self, *args):
        self.showed_apps = []  # limpieza de la variable self.showed_apps
        self.app_canvas.destroy()  # Destruye el canvas anterior
        self.app_canvas = Canvas(self.win, width=self.width * 89 / 100, height=self.height * 85 / 100)  # Crea uno nuevo
        # Posiciona el canvas
        self.app_canvas.pack()
        self.app_canvas.place(x=self.width * 6 / 100, y=self.height * 13 / 100)
        ele = self.entry.get().lower().replace(' ','') #Toma el elemento del entry y lo normaliza
        if ele != '':  # Verifica si el elemento esta vacio
            return self.posicionar_apps(self.search_nombre_by_letter(apps.get_list(), ele, 0), 0, 0, 0)
        else:
            return self.posicionar_apps(apps.get_list(), 0, 0, 0)

    # E: Lista donde buscar un elemento y un contador.
    # S: Retorna una lista con los elementos de la lista que empiezan con el elemento dado
    # R: No hay restricciones pues todo esta controlado por el programador.
    def search_nombre_by_letter(self, lista, ele, cont):
        global category_list  # Utilizada para buscar por categoria
        if ele != ' ':
            if len(lista) == cont:  # Caso base
                return []
            elif lista[cont][2].lower().replace(' ', '').startswith(ele) or category_list[int(lista[cont][3].lower().replace(' ', ''))] == ele:  # Verifica que empiece con ele o que la busqueda sea igual a ele
                return [lista[cont]] + self.search_nombre_by_letter(lista, ele, cont + 1)
            else:
                return self.search_nombre_by_letter(lista, ele, cont + 1)
        else:
            return []
    # E: Una lista, un contador de columna, un contador de reglon y un contador general
    # S: No retorna, una vez completada la recursividad, solo posiciona los espacios de las apps de una manera ordenada
    # R: No hay restricciones, todo esta bien controlado por codigo.
    def posicionar_apps(self, lista, controw, contcolumn, contgeneral):
        if contgeneral == len(lista): # Caso base
            return
        elif contcolumn < 6:  # Esta dentro del limite de la ventana
            if controw < 4:  # Esta dentro del limite de la ventana
                self.showed_apps = self.showed_apps + ['']
                self.showed_apps[contgeneral] = app(self.app_canvas, controw, contcolumn, lista[contgeneral],
                                                    self.comm_width, self.comm_height)
                return self.posicionar_apps(lista, controw+1, contcolumn, contgeneral+1)
            else:
                self.showed_apps = self.showed_apps + ['']
                self.showed_apps[contgeneral] = app(self.app_canvas, controw, contcolumn, lista[contgeneral],
                                                    self.comm_width, self.comm_height)
                return self.posicionar_apps(lista, 0, contcolumn+1, contgeneral + 1)
        else:
            return self.posicionar_apps(lista, controw+1, 0, contgeneral)

    # Simplemente ensenna el menu
    def show_menu(self, *args):
        return self.__show_menu_aux()

    def __show_menu_aux(self):
        global menu
        menu =newMenu(self.win)

    # E: No hay entradas
    # S: No retorna, solo cambia el texto a ingles
    # R: No hay restricciones
    def toeng(self):
        self.entry_label.config(text='Search:')

    # E: No hay entradas
    # S: No retorna, solo cambia el texto a ingles
    # R: No hay restricciones
    def toesp(self):
        self.entry_label.config(text='Buscar:')


# La siguiente clase es la encargada de la creacion de las paginas de perfil, sus atributos estan orientados a la creacion
# de la misma, mientras sus metodos se utilizan para editar la pagina o mostrar la lista de apps del usuario
class profPage:
    # Funcion constructor
    def __init__(self, info):
        # Configuracion principal
        self.bg_color = '#bbb8c1'
        self.win = Toplevel(bg=self.bg_color)
        self.win.resizable(False, False)

        # Dimensiones
        self.sc_width = self.win.winfo_screenwidth()
        self.sc_height = self.win.winfo_screenheight()
        self.width =  self.sc_width*50/100
        self.height =  self.sc_height*30/100
        self.win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.sc_width*25/100, self.sc_height*15/100))

        # Contenedores principales
        self.canvas_left = Canvas(self.win, bg=self.bg_color, height=self.height, width=self.width*30/100,
                                  bd=0, highlightthickness=0, relief='ridge')
        self.canvas_left.pack()
        self.canvas_left.place(x=0,y=0)

        self.canvas_right = Canvas(self.win, bg=self.bg_color, height=self.height, width=self.width*70/100,
                                   bd=0, highlightthickness=0, relief='ridge')

        self.canvas_right.pack()
        self.canvas_right.place(x=self.width*30/100,y=0)

        # Asignacion de strings variables para los entrys
        self.name = StringVar()
        self.name.set(info.name)  # Setteando el valor inicial
        self.correo = StringVar()
        self.correo.set(info.mail)  # Setteando el valor inicial
        self.webpage = StringVar()
        self.webpage.set(info.webpage)  # Setteando el valor inicial

        # Cargando y redimensionando la imagen del grafico
        self.graphics_img_load = Image.open('../images/icons/graph.gif').resize((50, 50), Image.ANTIALIAS)
        self.graphics_img = ImageTk.PhotoImage(self.graphics_img_load)
        self.graphics_img_label = Label(self.canvas_right, image=self.graphics_img, bg=self.bg_color, cursor='hand2')
        self.graphics_img_label.pack()
        self.graphics_img_label.place(x=self.width*62/100, y=10)
        self.graphics_img_label.image = self.graphics_img
        self.graphics_img_label.bind('<Button-1>', self.show_lista)

        self.name_label = Label(self.canvas_right, textvariable=self.name, font='Times %d bold' % int(self.width*5/100)
                                , bg=self.bg_color, wraplengt=450)
        self.name_label.pack()
        self.name_label.place(x=5, y=0)

        self.correo_label = Label(self.canvas_right, textvariable=self.correo, font='Times 15', bg=self.bg_color)
        self.correo_label.pack()
        self.correo_label.place(x=50, y=80)

        self.webpage_label = Label(self.canvas_right, textvariable=self.webpage, font='Times 15', bg=self.bg_color)
        self.webpage_label.pack()
        self.webpage_label.place(x=50, y=150)

        self.path_user_img = info.perfil
        self.path_user_bg = info.fondo
        self.canvas_left.update()
        try:  # Trata de abrir la imagen especificada por el usuario en la tabla de usuarios
            self.load_user_img = Image.open(self.path_user_img).resize((100,100), Image.ANTIALIAS)
        except FileNotFoundError:  # Si falla carga la imagen de invitado
            self.load_user_img = Image.open('../users/guest.gif').resize((100,100), Image.ANTIALIAS)
        try:  # Trata de abrir la imagen de fondo especificada en la tabla de usuarios
            self.load_user_bg = Image.open(self.path_user_bg).resize((self.canvas_left.winfo_height()
                                                                    , self.canvas_left.winfo_width()), Image.ANTIALIAS)
        except FileNotFoundError: # Si falla abre no_image.png
            self.load_user_bg = Image.open('../images/icons/no_image.png').resize((self.canvas_left.winfo_width()
                                                                                 , self.canvas_left.winfo_height()),
                                                                                   Image.ANTIALIAS)
        # Renderiza y asigna a un label las imagenes, posiciona.
        self.user_bg = ImageTk.PhotoImage(self.load_user_bg)
        self.user_bg_label = Label(self.canvas_left, image=self.user_bg)
        self.user_bg_label.pack()
        self.user_bg_label.place(x=0,y=0)
        self.user_bg_label.image = self.user_bg

        self.user_img = ImageTk.PhotoImage(self.load_user_img)
        self.user_img_label = Label(self.canvas_left, image=self.user_img)
        self.user_img_label.pack()
        self.user_img_label.place(relx=0.3, rely=0.3)
        self.user_img_label.image = self.user_img

        # actualiza el name_label para poder tomar su tamanno
        self.name_label.update()

        # Crea la variable para luego poder reescribirla
        self.lista_root=''

        if info.admin == 'si':  # Caso de admin normal
            self.load_crown = Image.open('../images/icons/mini_crown.gif').resize((50,50), Image.ANTIALIAS)
            self.crown_img = ImageTk.PhotoImage(self.load_crown)
            self.crown_label = Label(self.canvas_right, image=self.crown_img, bg=bg_color)
            self.crown_label.pack()
            self.crown_label.place(x=self.name_label.winfo_width(), y=10)
        elif info.admin == 'S':  # Caso de super admin
            self.load_crown = Image.open('../images/icons/real_crown.gif').resize((50,50), Image.ANTIALIAS)
            self.crown_img = ImageTk.PhotoImage(self.load_crown)
            self.crown_label = Label(self.canvas_right, image=self.crown_img, bg=bg_color)
            self.crown_label.pack()
            self.crown_label.place(x=self.name_label.winfo_width(), y=10)

        if users_list[current_user].name == self.name.get():  # Verifica si el usuario actual es el duenno de la ventana
            # Carga posiciona y renderiza las imagenes.
            self.edit_img_load = Image.open('../images/icons/edit.gif').resize((20,20), Image.ANTIALIAS)
            self.edit_img = ImageTk.PhotoImage(self.edit_img_load)

            self.edit_bg = Label(self.canvas_left, image=self.edit_img, cursor='hand2')
            self.edit_bg.pack()
            self.edit_bg.place(x=0,y=0)
            self.edit_bg.image = self.edit_img
            self.edit_bg.bind('<Button-1>', lambda *args: self.change_img('fondo'))  # Vincula con el metodo que cambia imagenes

            self.edit_profile_img = Label(self.canvas_left, image=self.edit_img, cursor='hand2')
            self.edit_profile_img.pack()
            self.edit_profile_img.place(relx=0.3,rely=0.3)
            self.edit_profile_img.image = self.edit_img
            self.edit_profile_img.bind('<Button-1>', lambda *args: self.change_img('foto')) # Vincula con el metodo que cambia imagenes

            self.edit_mail = Label(self.canvas_right, image=self.edit_img, bg=bg_color, cursor='hand2')
            self.edit_mail.pack()
            self.edit_mail.place(x=self.correo_label.winfo_width()+50, y=90)
            self.edit_mail.bind('<Button-1>', self.change_mail)  # Vincula con el metodo que cambia el email

            self.edit_webpage = Label(self.canvas_right, image=self.edit_img, bg=bg_color, cursor='hand2')
            self.edit_webpage.pack()
            self.edit_webpage.place(x=self.webpage_label.winfo_width()+50, y=160)
            self.edit_webpage.bind('<Button-1>', self.change_page)  # Vincula con el metodo que cambia imagenes

    # E: El evento desde donde se llama, no se utiliza
    # S: No retorna, solo muestra la lista de apps
    # R: No hay restricciones
    def show_lista(self, *args):
        try:
            self.lista_root.deiconify()
            self.lista_root.lift()
            login.win_login.focus_force()
        except:
            self.lista_root = Toplevel()
            self.lista_apps = listaApps(self.lista_root)
            self.lista_root.focus_force()

    # E: String con el espacio de la imagen que debe cambiar
    # S: No retorna, solo cambia la imagen respectiva
    # R: No hay restricciones, se controla muy bien que se envia
    def change_img(self, this):
        global main  # Crear un nuevo main y borrar el anterior
        global current_language  # Pasarlo como argumento al nuevo main
        global current_user  # Usado para modificar o annadir el usuario
        global users_list  # Usado para tomar el objeto respectivo
        global current_user  # Usado para especificar cual indice de users_list utilizar
        self.win.lower()  # Baja la ventana para mostrar la ventana de seleccion de archivos
        self.img_path = fd.askopenfilename()  # Muestra la ventana de seleccion de archivos
        try: # Intenta abrir la imagen especificada
            load_new_img = Image.open(self.img_path).resize((100, 100), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            if this == 'foto':
                self.user_img_label.config(image=new_img)
                self.user_img_label.image = new_img
                users.mod(current_user+1, 3, self.img_path)
                users_list[current_user].perfil = self.img_path
            else:
                self.user_bg_label.config(image=new_img)
                self.user_bg_label.image = new_img
                users.mod(current_user+1, 4, self.img_path)
                users_list[current_user].fondo = self.img_path
        except: # Si no puede abre la imagen de invitado
            load_new_img = Image.open('../users/guest').resize((100, 100), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.user_bg_label.config(image=new_img)
            self.user_bg_label.image = new_img
            users.mod(current_user + 1, 4, self.img_path)
            users_list[current_user].fondo = self.img_path
        self.win.lift()
        main.kill()
        main = main_window(root, current_language)

    # E: El evento desde donde se llama la funcion, no se utiliza
    # S: No retorna, solo cambia el correo del usuario actual
    # R: No hay restricciones
    def change_mail(self, *args):
        new_email = simpledialog.askstring('Input','Introduzca el nuevo e-mail', parent=self.win)  # Tira un popup preguntando por el nuevo valor
        self.correo.set(new_email)
        self.correo_label.update()
        self.edit_mail.place(x=self.correo_label.winfo_width() + 50, y=90)
        users_list[current_user].mod_mail(new_email)

    # E: El evento desde donde se llama la funcion, no se utiliza
    # S: No retorna, solo cambia la pagina del usuario actual
    # R: No hay restricciones
    def change_page(self, *args):
        new_page = simpledialog.askstring('Input', 'Introduzca la nueva pagina web', parent=self.win) # Tira un popup preguntando por el nuevo valor
        self.webpage.set(new_page)
        self.webpage_label.update()
        self.edit_webpage.place(x=self.webpage_label.winfo_width() + 50, y=160)
        users_list[current_user].mod_page(new_page)

# Clase encargada de la construccion de la lista de apps relacionadas a un usuario. Sus atributos son orientados a crear la lista y la ventana
# donde esta esta. Sus metodos son de acomodo de los espacios de las apps y de lanzar una ventana de edicion de apps.
class listaApps:
    # Funcion constructor
    def __init__(self, root):
        # Configuracion inicial
        self.root = root
        self.root.resizable(False, False)
        self.canvas = Canvas(self.root, borderwidth=0, bg=bg_color)
        self.frame = Frame(self.canvas, background=bg_color)
        self.vsby = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.vsbx = Scrollbar(self.root, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsby.set)
        self.canvas.configure(xscrollcommand=self.vsbx.set)

        self.vsby.pack(side="right", fill="y")
        self.vsbx.pack(side='bottom',fill='x')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.lista_apps = [[],[]]  # Se iran guardando labels e imagenes aqui, para luego poder accesarlas mediante un click

        # Dimensiones
        self.sc_width = root.winfo_screenwidth()
        self.sc_height = root.winfo_screenheight()
        self.width = self.sc_width * 60 / 100
        self.height = self.sc_height * 70 / 100
        root.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 25 / 100, self.sc_height * 15 / 100))

        self.populate()

    # E: No recibe entradas
    # S: No retorna, de lo que se encarga es de acomodar las apps de un cierto usuario
    # R: No tiene restricciones
    def populate(self):
        global profile_page  # Usado para comparacion de nombres
        first_lista = find_all(apps.get_list(), users_list[current_user].seller_id, 0, 0)  # Filtro de las apps de un usuario
        last_lista = find_all(first_lista, 'Activo', 6, 0)  # Filtro de las apps no activas
        if users_list[current_user].name == profile_page.name.get():  # Usuario duenno, se muestran todas las apps
            self.__populate_aux(first_lista, 0)

            # Crea el icono de annadir una app
            self.load_plus = Image.open('../images/icons/plus.gif').resize((25, 25), Image.ANTIALIAS)
            self.plus_img = ImageTk.PhotoImage(self.load_plus)
            self.plus = Label(self.frame, image=self.plus_img, bg=bg_color, cursor='hand2')
            self.plus.grid(row=len(first_lista)*2, column=0, columnspan=5)
            self.plus.bind('<Button-1>', lambda event: self.create_edit_win([]))
        else:  # Caso de usuario visitante, no requiere mostrar las apps no activas
            self.__populate_aux(last_lista, 0)



    def __populate_aux(self, lista, cont):
        global profile_page  # Utilizado para comparar el nombre con el usuario actual
        global category_list  # Utilizado para lectura de categorias
        if cont == len(lista):  # Caso base
            return
        else:
            self.lista_apps[0] = self.lista_apps[0] + ['erase']  # Annade un indice para poder escribir en el
            self.img_path = lista[cont][7]
            self.img_load = Image.open(self.img_path).resize((200, 100), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img_load)

            # Se guarda el label en una lista
            self.lista_apps[0][cont] = Label(self.frame, image=self.img, bg=bg_color, cursor='hand2')
            self.lista_apps[0][cont].grid(row=cont*2, column=0, rowspan=2)
            self.lista_apps[0][cont].image = self.img
            self.lista_apps[0][cont].bind('<Button-1>', lambda event: appWindow(lista[cont]))  # abre la ventana de la app al darle click al label

            self.app_name = Label(self.frame, text=lista[cont][2], font='Times 20',
                                  bg=bg_color).grid(row=cont*2, column=1)

            # Evita que s ele ponga un simbolo de moneda a la palabra Free
            if lista[cont][5] != 'Free':
                self.app_cost = Label(self.frame, text='₡'+lista[cont][5], font='Times 20',
                                  bg=bg_color).grid(row=cont*2, column=2)
            else:
                self.app_cost = Label(self.frame, text=lista[cont][5], font='Times 20',
                                      bg=bg_color).grid(row=cont * 2, column=2)

            # Manejo de lenguaje
            if current_language == 'esp':
                self.app_downloads = Label(self.frame, text='Descargas: ' + lista[cont][11],
                                           font='Times 20', bg=bg_color).grid(row=cont*2 + 1, column=1)
                self.app_categoria = Label(self.frame, text='Categoria: '+ category_list[int(lista[cont][3])],
                                           font='Times 20', bg=bg_color).grid(row=cont*2 + 1, column=2)
            else:
                self.app_downloads = Label(self.frame, text='Downloads: ' + lista[cont][11],
                                           font='Times 20', bg=bg_color).grid(row=cont * 2 + 1, column=1)
                self.app_categoria = Label(self.frame, text='Category: ' + category_list[int(lista[cont][3])],
                                           font='Times 20', bg=bg_color).grid(row=cont * 2 + 1, column=2)

            # muestra la ganancia para los duennos
            if users_list[current_user].name == profile_page.name.get():
                if lista[cont][5] == 'Free':
                    # manejo de idioma
                    if current_language == 'esp':
                        self.app_gain = Label(self.frame, text='Ganancia: 0', font='Times 20',
                                              bg=bg_color).grid(row=cont*2, column=3)
                    else:
                        self.app_gain = Label(self.frame, text='Earnings: 0', font='Times 20',
                                              bg=bg_color).grid(row=cont * 2, column=3)
                else:
                    # manejo de idioma
                    if current_language == 'esp':
                        self.app_gain = Label(self.frame, text='Ganancia: %s%d'%(lista[cont][5][0],
                                                                            int(lista[cont][5][1:])*int(lista[cont][11]))
                                              , font='Times 20', bg=bg_color).grid(row=cont * 2, column=3)
                    else:
                        self.app_gain = Label(self.frame, text='Earnings: %s%d' % (lista[cont][5][0],
                                                                                   int(lista[cont][5][1:]) * int(
                                                                                       lista[cont][11]))
                                              , font='Times 20', bg=bg_color).grid(row=cont * 2, column=3)
                # Actualiza el widget para poder usar su tamanno mas adelante
                self.frame.update()

                # Cambia el color dependiendo si es una app activa o inactiva
                if lista[cont][6] == 'Activo':
                    self.app_estado = Canvas(self.frame, bg='green', height=50,
                                             width=200)
                else:
                    self.app_estado = Canvas(self.frame, bg='red', height=50,
                                             width=200)
                self.app_estado.grid(row=cont * 2 + 1, column=3)
                self.app_estado.bind('<Button-1>', lambda event: self.toggle_state(lista[cont][1], lista[cont][6]))
                # mismo procedimiento que con la asignacion de un label a una lista
                self.lista_apps[1] = self.lista_apps[1] + ['erase']
                self.load_edit_img = Image.open('../images/icons/edit.gif').resize((40,80), Image.ANTIALIAS)
                self.edit_img = ImageTk.PhotoImage(self.load_edit_img)
                self.lista_apps[1][cont] = Label(self.frame, image=self.edit_img, bg=bg_color, cursor='hand2')
                self.lista_apps[1][cont].grid(row=cont*2, column=4, rowspan=2)
                self.lista_apps[1][cont].image = self.edit_img
                self.lista_apps[1][cont].bind('<Button-1>', lambda event: self.create_edit_win(lista[cont]))

        # llamada recursiva
        self.__populate_aux(lista, cont + 1)

    # E: Informacion de una app, lista.
    # S: No retorna, solo se encarga de crear una nueva app
    # R: Info no es vacia
    def create_edit_win(self, info):
        if info != []:
            new_edit = editApp()
            new_edit.edit_config(info)
        else:
            new_edit = editApp()

    # E: El id de la app a la cual se le quiere modificar el estado.
    # S: No retorna, solo cambia el estado de una app.
    # R: No hay
    def toggle_state(self, app_id, active):
        if active == 'Activo':
            apps.mod(int(app_id), 6, 'Inactivo')
        else:
            apps.mod(int(app_id), 6, 'Activo')
        self.root.destroy()
        listaApps(Toplevel())


    # Simplemente actualiza el area de visibilidad del scrollbar
    def onFrameConfigure(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

# Clase encargada de la creacion de la ventana de adicion de apps. Sus atributos van orientados a la creacion de la ventana
# y sus metodos a cambiar interactivamente labels de la misma ventana, asi como enviar la informacion de la edicion.
class editApp:
    # Funcion constructor
    def __init__(self):
        # Configuracion principal
        self.bg_color = '#bbb8c1'
        self.win = Toplevel(bg=self.bg_color)
        self.win.resizable(False, False)

        # Dimensiones
        self.sc_width = self.win.winfo_screenwidth()
        self.sc_height = self.win.winfo_screenheight()
        self.width = self.sc_width * 40 / 100
        self.height = self.sc_height * 72 / 100
        self.win.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 25 / 100, self.sc_height * 15 / 100))

        self.frame = Frame(self.win, width=self.width*80/100, height=self.height*90/100)
        self.frame.pack()
        self.frame.place(relx=0.030, rely=0.03)

        # Cargando, renderizando y cambiando el tamanno de imagenes
        self.icon_path = '../images/icons/no_image.png'
        self.load_icon = Image.open(self.icon_path).resize((100,100),Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(self.load_icon)
        self.sc1_path = '../images/icons/no_image.png'
        self.load_sc1 = Image.open(self.sc1_path).resize((300,200), Image.ANTIALIAS)
        self.sc1 = ImageTk.PhotoImage(self.load_sc1)
        self.sc2_path = '../images/icons/no_image.png'
        self.load_sc2 = Image.open(self.sc2_path).resize((300, 200), Image.ANTIALIAS)
        self.sc2 = ImageTk.PhotoImage(self.load_sc2)
        self.banner_path = '../images/icons/no_image.png'
        self.load_banner = Image.open(self.banner_path).resize((600, 200), Image.ANTIALIAS)
        self.banner = ImageTk.PhotoImage(self.load_banner)

        # Creando un string variable para el dropdown menu
        self.variable_categoria = StringVar(self.win)
        self.variable_categoria.set('Seleccionar')

        self.icon_label = Label(self.frame, image=self.icon, cursor='hand2')
        self.icon_label.grid(row=0, column=0, rowspan=2)
        self.app_name = StringVar()  # String variable para el entry
        self.app_name.set('Nombre de la app')  # First set
        self.name_entry = Entry(self.frame, textvariable=self.app_name)
        self.name_entry.grid(row=0, column=1)
        self.app_cost = StringVar()  # String variable para el entry
        self.app_cost.set('₡'+'0')  # First set

        # manejo de idioma
        if current_language == 'esp':
            self.cost_label = Label(self.frame, text='Precio: ₡', font='Times 20').grid(row=0, column=2)
            self.descr_label = Label(self.frame, text='Descripcion:', font='Times 20').grid(row=1, column=1)
            self.categoria_label = Label(self.frame, text='Categoria:', font='Times 20').grid(row=1, column=2)
        else:
            self.cost_label = Label(self.frame, text='Price: ₡', font='Times 20').grid(row=0, column=2)
            self.descr_label = Label(self.frame, text='Descrip$tion:', font='Times 20').grid(row=1, column=1)
            self.categoria_label = Label(self.frame, text='Category:', font='Times 20').grid(row=1, column=2)

        self.categoria_entry = OptionMenu(self.frame, self.variable_categoria, 'Juegos', 'Musica', 'Redes',
                                     'Herramientas')

        # Definienndo entry de precio
        self.cost_entry = Entry(self.frame, textvariable=self.app_cost)
        self.cost_entry.grid(row=0, column=3)
        self.cost_entry.bind('<Button-1>', lambda event: self.app_cost.set(''))  # Borra el entry al presionar sobre el

        self.descr_variable = StringVar()# String variable para el entry
        self.categoria_entry.grid(row=1, column=3)

        #Definiendo el widget texto para la descripcion
        self.descr_entry = Text(self.frame, height=5)
        self.descr_entry.grid(row=2, column=0, columnspan=4, rowspan=2)

        # Asignando label y posicionando
        self.sc1_label = Label(self.frame, image=self.sc1, cursor='hand2')
        self.sc1_label.grid(row=4,column=0, columnspan=2)
        self.sc2_label = Label(self.frame, image=self.sc2, cursor='hand2')
        self.sc2_label.grid(row=4, column=2, columnspan=2)
        self.banner_label = Label(self.frame, image=self.banner, cursor='hand2')
        self.banner_label.grid(row=5, column=0, columnspan=4)

        # Enlaces para el metodo que cambia cada elemento.
        self.icon_label.bind('<Button-1>', self.change_icon)
        self.sc1_label.bind('<Button-1>', self.change_sc1)
        self.sc2_label.bind('<Button-1>', self.change_sc2)
        self.banner_label.bind('<Button-1>', self.change_banner)

        # Manejo de idioma
        if current_language == 'esp':
            self.ready = Button(self.frame, text='Listo', command=lambda: self.send(self.name_entry.get())).grid(row=6, column=1)
            self.cancel = Button(self.frame, text='Cancelar')
        else:
            self.ready = Button(self.frame, text='Ready', command=lambda: self.send(self.name_entry.get())).grid(row=6,
                                                                                                                 column=1)
            self.cancel = Button(self.frame, text='Cancel', command=self.win.destroy)
        self.cancel.grid(row=6, column=2)

    # E: Evento del widget que llama la funcion, no se usa.
    # S: No retorna, unicamente cambia el icono
    # R: No tiene restricciones
    def change_icon(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((100, 100), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.icon_label.config(image=new_img)
            self.icon_label.image = new_img
        except:
            if current_language == 'esp': # Verifica idioma
                messagebox.showwarning(title='Warning', message='Imagen no encontrada')
            else:
                messagebox.showwarning(title='Warning', message='Image not found')
            load_new_img = Image.open('../users/guest.gif').resize((100, 100), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.icon_label.config(image=new_img)
            self.icon_label.image = new_img
        self.win.lift()

    # E: Evento del widget que llama la funcion, no se usa.
    # S: No retorna, unicamente cambia el screenshot 1
    # R: No tiene restricciones
    def change_sc1(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((300, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.sc1_label.config(image=new_img)
            self.sc1_label.image = new_img
        except:
            messagebox.showwarning(title='Warning', message='Imagen no encontrada.')
            load_new_img = Image.open('../images/icons/no_image.png').resize((300, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.sc1_label.config(image=new_img)
            self.sc1_label.image = new_img
        self.win.lift()

    # E: Evento del widget que llama la funcion, no se usa.
    # S: No retorna, unicamente cambia el screenshot2
    # R: No tiene restricciones
    def change_sc2(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((300, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.sc2_label.config(image=new_img)
            self.sc2_label.image = new_img
        except:
            if current_language == 'esp': # Verifica idioma
                messagebox.showwarning(title='Warning', message='Imagen no encontrada')
            else:
                messagebox.showwarning(title='Warning', message='Image not found')
            load_new_img = Image.open('../images/icons/no_image.png').resize((300, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.sc2_label.config(image=new_img)
            self.sc2_label.image = new_img
        self.win.lift()

    # E: Evento del widget que llama la funcion, no se usa.
    # S: No retorna, unicamente cambia el banner
    # R: No tiene restricciones
    def change_banner(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((600, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.banner_label.config(image=new_img)
            self.banner_label.image = new_img
        except:
            if current_language == 'esp': # Verifica idioma
                messagebox.showwarning(title='Warning', message='Imagen no encontrada')
            else:
                messagebox.showwarning(title='Warning', message='Image not found')
            load_new_img = Image.open(self.img_path).resize((600, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.banner_label.config(image=new_img)
            self.banner_label.image = new_img
        self.win.lift()

    # E: Lista de la info de una app
    # S: No retorna, configura la pagina de una app si esta existe
    # R: No hay restricciones
    def edit_config(self, info):
        global category_list
        self.app_name.set(info[2])
        if info[5] != 'Free':
            self.app_cost.set('₡'+info[5])
        else:
            self.app_cost.set(info[5])
        self.descr_entry.insert('1.0', info[4])
        self.variable_categoria.set(category_list[int(info[3])])

        self.icon_path = info[7]
        self.load_icon = Image.open(self.icon_path).resize((100,100), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(self.load_icon)
        self.icon_label.config(image=self.icon)

        self.banner_path = info[8]
        self.load_banner = Image.open(self.banner_path).resize((600, 200), Image.ANTIALIAS)
        self.banner = ImageTk.PhotoImage(self.load_banner)
        self.banner_label.config(image=self.banner)

        self.sc1_path = info[9]
        self.load_sc1 = Image.open(self.sc1_path).resize((300, 200), Image.ANTIALIAS)
        self.sc1 = ImageTk.PhotoImage(self.load_sc1)
        self.sc1_label.config(image=self.sc1)

        self.sc2_path = info[10]
        self.load_sc2 = Image.open(self.sc2_path).resize((300, 200), Image.ANTIALIAS)
        self.sc2 = ImageTk.PhotoImage(self.load_sc2)
        self.sc2_label.config(image=self.sc2)

        self.icon_label.image = self.icon
        self.banner_label.image = self.banner
        self.sc1_label.image = self.sc1
        self.sc2_label.image = self.sc2

    # E: Nombre de la app
    # S: No retorna, la funcion configura un nuevo renglon de la tabla apps a partir de los datos dados en esta ventana.
    def send(self, name):
        global users_list
        global category_list
        if self.name_entry.get().lstrip() != '' or self.name_entry.get().lstrip() != 'Nombre de la app' or self.variable_categoria.get() != 'Seleccionar' or self.cost_entry.get().lstrip() != '':
            num_row_to_update = is_in(apps.get_list(), name, 0, 0)[1]
            row_to_update = is_in(apps.get_list(), name, 0, 0)[0]  # Busca que el nombre exista en la tabla
            new_category = str(lista_isin(category_list, self.variable_categoria.get(), 0)[1])
            cost_entry = self.cost_entry.get()
            if self.cost_entry.get() == 0:
                cost_entry = 'Free'
            if row_to_update:
                new_entry = [users_list[current_user].seller_id, row_to_update[1], self.name_entry.get(),
                             new_category, self.descr_entry.get('1.0', 'end-1c'), cost_entry,
                             'Activo', self.icon_path, self.banner_path, self.sc1_path, self.sc2_path, '0', '0']
                apps.update(num_row_to_update, new_entry)
            else:
                new_entry = [users_list[current_user].seller_id, str(int(apps.get_list()[len(apps.get_list())-1][1])+1), self.name_entry.get(),
                             new_category, self.descr_entry.get('1.0', 'end-1c'), cost_entry,
                             'Activo', self.icon_path, self.banner_path, self.sc1_path, self.sc2_path, '0', '0']
                apps.add(new_entry)
            self.win.destroy()
        else:
            if self.name_entry.get().lstrip() == '' or self.name_entry.get().lstrip == 'Nombre de la app':
                if current_language == 'esp': # Verificar idioma
                    messagebox.showerror(title='Error', message='Favor llenar el espacio de nombre')
                else:
                    messagebox.showerror(title='Error', message='Please fill the name entry')
            elif self.variable_categoria.get() == 'Seleccionar':
                if current_language == 'esp': # Verificar idioma
                    messagebox.showerror(title='Error', message='Favor seleccionar categoria')
                else:
                    messagebox.showerror(title='Error', message='Please select category')
            elif self.cost_entry.get() == '':
                if current_language == 'esp':  # Verificar idioma
                    messagebox.showerror(title='Error', message='Favor ingresar un precio')
                else:
                    messagebox.showerror(title='Error', message='Please insert a price')

# Esta clase esta encargada de la creacion de la ventana de cada app, sus atributos estan dirigidos a la creacion de la ventana
# y sus widgets, sus metodos muestran la pagina del duenno y modifican la cantidad de descargas
class appWindow():
    global category_list
    # Funcion constructor
    def __init__(self, info):
        # Configuracion principal
        self.bg_color = '#bbb8c1'
        self.win = Toplevel(bg=self.bg_color)
        self.win.resizable(False, False)

        # Dimensiones
        self.sc_width = self.win.winfo_screenwidth()
        self.sc_height = self.win.winfo_screenheight()
        self.width = self.sc_width * 52 / 100
        self.height = self.sc_height * 50 / 100
        self.win.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 30 / 100, self.sc_height * 14 / 100))

        self.frame = Frame(self.win)
        self.frame.pack()
        self.frame.place(x=0, y=0)

        self.icon_path = info[7]
        self.sc1_path = info[9]
        self.sc2_path = info[10]
        self.load_icon = Image.open(self.icon_path).resize((100,100), Image.ANTIALIAS)
        self.load_sc1 = Image.open(self.sc1_path).resize((400,160), Image.ANTIALIAS)
        self.load_sc2 = Image.open(self.sc2_path).resize((400,160), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(self.load_icon)
        self.sc1 = ImageTk.PhotoImage(self.load_sc1)
        self.sc2 = ImageTk.PhotoImage(self.load_sc2)

        self.icon_label = Label(self.frame, image=self.icon)
        self.icon_label.grid(row=0, column=0, rowspan=3)
        self.icon_label.image = self.icon

        self.name_label = Label(self.frame, text=info[2])
        self.name_label.grid(row=0, column=1)
        if info[5] == 'Free':
            self.cost_label = Label(self.frame, text=info[5])
        else:
            self.cost_label = Label(self.frame, text='₡'+info[5])
        self.cost_label.grid(row=1, column=1)

        self.categoria_label = Label(self.frame, text=category_list[int(info[3])])
        self.categoria_label.grid(row=2, column=1)

        self.owner_seller_info = sellers.is_in(info[0], 0, 0)

        self.owner_user_info = users.is_in(self.owner_seller_info[1], 0, 0)

        if self.owner_user_info:
            self.owner_img_path = self.owner_user_info[3]
        else:
            self.owner_img_path = '../users/guest.gif'
        self.load_owner_img = Image.open(self.owner_img_path).resize((100,75), Image.ANTIALIAS)
        self.owner_img = ImageTk.PhotoImage(self.load_owner_img)
        self.owner_img_label = Label(self.frame, image=self.owner_img, cursor='hand2')
        self.owner_img_label.grid(row=0, rowspan=2, column=3)

        # manejo de idiomas
        if current_language == 'esp':
            self.owner = Label(self.frame, text='Hecho por: %s' % self.owner_seller_info[1], cursor='hand2')
            self.buy_button = Button(self.frame, text='Comprar', command=self.buy_app)
        else:
            self.owner = Label(self.frame, text='Made by: %s' % self.owner_seller_info[1], cursor='hand2')
            self.buy_button = Button(self.frame, text='Buy', command=self.buy_app)

        self.owner.grid(row=2, column=3)
        self.buy_button.grid(row=1, column=2)

        self.owner_img_label.bind('<Button-1>', lambda event: self.show_profPage(self.owner_seller_info[1]))  # Muestra la pagina de perfil del vendedor
        self.owner.bind('<Button-1>', lambda event: self.show_profPage(self.owner_seller_info[1]))# Muestra la pagina de perfil del vendedor

        self.descr_label = Text(self.frame, width=60)
        self.descr_label.insert('1.0',info[4])
        self.descr_label.grid(row=3, column=0, rowspan=2, columnspan=2)
        self.descr_label.config(state=DISABLED)

        self.sc1_label = Label(self.frame, image=self.sc1)
        self.sc1_label.grid(row=3, column=2, columnspan=2)
        self.sc1_label.image = self.sc1

        self.sc2_label = Label(self.frame, image=self.sc2)
        self.sc2_label.grid(row=4, column=2, columnspan=2)
        self.sc2_label.image = self.sc2

        self.id = info[1]

    # E: No hay entradas
    # S: No retorna, su funcionamiento se basa en actualizar la tabla de apps cada ves que se realiza una compra
    # R: No hay
    def buy_app(self):
        global apps
        global current_user
        apps.mod(int(self.id), 11, str(int(apps.list[int(self.id)][11])+1))
        if current_user != -1:  # Presenta el error de registro a usuarios desconocidos
            if users_list[current_user].country == 'Costa Rica':
                apps.mod(int(self.id), 12, str(int(apps.list[int(self.id)][12]) + 1))
        else:
            if current_language == 'esp':  # verificar idioma
                messagebox.showerror(title='Error', message='Por favor registrese para descargar')
            else:
                messagebox.showerror(title='Error', message='Please login to download content')

    # E: Nombre de usuario del duenno de la pagina a abrir
    # S: No retorna, pero abre la pagina de usuario del username brindado
    # R: No hay restricciones
    def show_profPage(self, username):
        if self.owner_user_info:
            global  profile_page
            user_info = users.is_in(username, 0, 0)
            profile_page = profPage(users_list[int(self.owner_user_info[8])])  # Crea la instancia
            self.win.destroy()
        else:
            if current_language == 'esp':
                messagebox.showinfo(title='Info', message='No hay pagina de usuario asociada a este vendedor')
            else:
                messagebox.showinfo(title='Info', message='There is no user page associated to this seller')

# Clase destinada a la creacion de cada app para la ventana de apps relacionadas a un usuario.
class app:
    def __init__(self, master, row, column,info, width, height):
        self.icon_path = info[7]
        self.load_icon = Image.open(self.icon_path).resize((int(width), int(height)), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(master, image=self.icon_img, cursor='hand2')
        self.icon_label.grid(row=row, column=column)
        self.icon_label.image = self.icon_img
        self.icon_label.bind('<Button-1>', lambda event: appWindow(info))  # Abre la respectiva app al presionar el icono

# Clase destinada a la creacion de label de app en la ventana principal. Sus atributos tienen que ver con este mismo objetivo
# Su metodo randomiza cuales apps son elegidas
class juegos:
    def __init__(self, master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                               bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/juegos.gif').resize((100,100), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(self.canvas, image=self.icon_img, bg=bg_color)
        self.icon_label.pack()
        self.icon_label.place(x=0,y=self.height*3/100)
        self.icon_label.image = self.icon_img

        # Manejo de idioma
        if current_language == 'esp':
            self.title = Label(self.canvas, text='Juegos', bg=bg_color, font='Times 17')
        else:
            self.title = Label(self.canvas, text='Games', bg=bg_color, font='Times 17')
        self.title.pack()
        self.title.place(x=25,y=self.height*15/100)
        self.random()

    # Randomiza cuales apps son mostradas en la pagina principal
    def random(self):
        rand1 = randint(0, len(apps.juegos)-1)
        rand2 = randint(0, len(apps.juegos)-1)
        common_width = 200
        if rand1 == rand2:
            return self.random()
        else:
            subcanvas1 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas1.pack()
            subcanvas1.place(x=102,y=0)
            subcanvas2 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas2.pack()
            subcanvas2.place(x=298,y=0)

            app1 = apps.juegos[rand1]
            app2 = apps.juegos[rand2]

            app1_load_banner = Image.open('%s' %app1[8].lstrip()).resize((200,200),Image.ANTIALIAS)
            app1_banner = ImageTk.PhotoImage(app1_load_banner)
            app1_banner_label = Label(subcanvas1, image=app1_banner, cursor='hand2')
            app1_banner_label.pack()
            app1_banner_label.place(x=0,y=0)
            app1_banner_label.image = app1_banner
            app1_banner_label.bind('<Button-1>', lambda event:appWindow(app1))  #  Abre la app

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event:appWindow(app2))  #  Abre la app


# Clase destinada a la creacion de label de app en la ventana principal. Sus atributos tienen que ver con este mismo objetivo
# Su metodo randomiza cuales apps son elegidas
class herramientas:
    def __init__(self,master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                              bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/tools.png').resize((70, 80), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(self.canvas, image=self.icon_img, bg=bg_color)
        self.icon_label.pack()
        self.icon_label.place(x=15, y=self.height * 3 / 100)
        self.icon_label.image = self.icon_img

        if current_language == 'esp':
            self.title = Label(self.canvas, text='Herramientas', bg=bg_color, font='Times 13')
        else:
            self.title = Label(self.canvas, text='Utilities', bg=bg_color, font='Times 15')
        self.title.pack()
        if current_language == 'esp':
            self.title.place(x=0, y=self.height * 15 / 100)
        else:
            self.title.place(x=20, y=self.height * 15 / 100)
        self.random()

    # Randomiza cuales apps son mostradas en la pagina principal
    def random(self):
        rand1 = randint(0, len(apps.herramientas)-1)
        rand2 = randint(0, len(apps.herramientas)-1)
        common_width = 200
        if rand1 == rand2:
            return self.random()
        else:
            subcanvas1 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas1.pack()
            subcanvas1.place(x=102,y=0)
            subcanvas2 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas2.pack()
            subcanvas2.place(x=298,y=0)

            app1 = apps.herramientas[rand1]
            app2 = apps.herramientas[rand2]

            app1_load_banner = Image.open('%s' %app1[8].lstrip()).resize((200,200),Image.ANTIALIAS)
            app1_banner = ImageTk.PhotoImage(app1_load_banner)
            app1_banner_label = Label(subcanvas1, image=app1_banner, cursor='hand2')
            app1_banner_label.pack()
            app1_banner_label.place(x=0,y=0)
            app1_banner_label.image = app1_banner
            app1_banner_label.bind('<Button-1>', lambda event: appWindow(app1)) #  Abre la app

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event: appWindow(app2))  #  Abre la app


# Clase destinada a la creacion de label de app en la ventana principal. Sus atributos tienen que ver con este mismo objetivo
# Su metodo randomiza cuales apps son elegidas
class musica:
    def __init__(self, master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                               bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/music.gif').resize((100, 100), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(self.canvas, image=self.icon_img, bg=bg_color)
        self.icon_label.pack()
        self.icon_label.place(x=0, y=self.height * 3 / 100)
        self.icon_label.image = self.icon_img

        if current_language == 'esp':
            self.title = Label(self.canvas, text='Musica', bg=bg_color, font='Times 17')
        else:
            self.title = Label(self.canvas, text='Music', bg=bg_color, font='Times 17')
        self.title.pack()
        self.title.place(x=20, y=self.height * 15 / 100)
        self.random()

    # Randomiza cuales apps son mostradas en la pagina principal
    def random(self):
        rand1 = randint(0, len(apps.musica)-1)
        rand2 = randint(0, len(apps.musica)-1)
        common_width = 200
        if rand1 == rand2:
            return self.random()
        else:
            subcanvas1 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas1.pack()
            subcanvas1.place(x=102,y=0)
            subcanvas2 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas2.pack()
            subcanvas2.place(x=298,y=0)

            app1 = apps.musica[rand1]
            app2 = apps.musica[rand2]

            app1_load_banner = Image.open('%s' %app1[8].lstrip()).resize((200,200),Image.ANTIALIAS)
            app1_banner = ImageTk.PhotoImage(app1_load_banner)
            app1_banner_label = Label(subcanvas1, image=app1_banner, cursor='hand2')
            app1_banner_label.pack()
            app1_banner_label.place(x=0,y=0)
            app1_banner_label.image = app1_banner
            app1_banner_label.bind('<Button-1>', lambda event: appWindow(app1))  #  Abre la app

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event: appWindow(app2))  #  Abre la app


# Clase destinada a la creacion de label de app en la ventana principal. Sus atributos tienen que ver con este mismo objetivo
# Su metodo randomiza cuales apps son elegidas
class redes:
    def __init__(self, master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                              bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/social.gif').resize((90, 100), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(self.canvas, image=self.icon_img, bg=bg_color)
        self.icon_label.pack()
        self.icon_label.place(x=8, y=self.height * 3 / 100)
        self.icon_label.image = self.icon_img

        if current_language == 'esp':
            self.title = Label(self.canvas, text='Redes\nsociales', bg=bg_color, font='Times 15')
        else:
            self.title = Label(self.canvas, text='Social \nnetworks', bg=bg_color, font='Times 15')
        self.title.pack()
        if current_language == 'esp':
            self.title.place(x=23, y=self.height * 15 / 100)
        else:
            self.title.place(x=18, y=self.height * 15 / 100)
        self.random()

    # Randomiza cuales apps son mostradas en la pagina principal
    def random(self):
        rand1 = randint(0, len(apps.redes)-1)
        rand2 = randint(0, len(apps.redes)-1)
        common_width = 200
        if rand1 == rand2:
            return self.random()
        else:
            subcanvas1 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas1.pack()
            subcanvas1.place(x=102,y=0)
            subcanvas2 = Canvas(self.canvas, bg=bg_color, height=self.height, width=common_width,
                                bd=0, highlightthickness=0, relief='ridge')
            subcanvas2.pack()
            subcanvas2.place(x=298,y=0)

            app1 = apps.redes[rand1]
            app2 = apps.redes[rand2]

            app1_load_banner = Image.open('%s' %app1[8].lstrip()).resize((200,200),Image.ANTIALIAS)
            app1_banner = ImageTk.PhotoImage(app1_load_banner)
            app1_banner_label = Label(subcanvas1, image=app1_banner, cursor='hand2')
            app1_banner_label.pack()
            app1_banner_label.place(x=0,y=0)
            app1_banner_label.image = app1_banner
            app1_banner_label.bind('<Button-1>', lambda event: appWindow(app1))  #  Abre la app

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event: appWindow(app2))  #  Abre la app


# Clase destinada a la creacion de la tabla de apps. Sus atributos tienen que ver con la tabla en forma de lista
# y otras particularidades. Entre sus metodos se posicionan los metodos get, los metodos de annadir o actualizar la tabla
# entre otros.
class appTable:
    def __init__(self):
        self.file = '../apps/apps.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)  # tabla con espacios
        self.list = normalize_list_table(self.raw_list, 0)  # Matriz de la tabla
        self.close_first_read = self.first_read.close()
        self.musica = self.list_categoria('1', 0)  # lista de apps de musica
        self.juegos = self.list_categoria('0', 0)# lista de apps de juegos
        self.herramientas = self.list_categoria('2', 0)# lista de apps de herramientas
        self.redes = self.list_categoria('3', 0)# lista de apps de redes

    # E: Contador
    # S: Una tabla convertida a lista
    # R: No hay
    def __to_list(self, cont):  # convierte la tabla en lista
        a = self.first_read.readline()
        if a == '':  # Caso base
            return []
        else:
            return [a] + self.__to_list(cont + 1)
    # E: No hay
    # R: No hay
    # S: Retorna los elementos de la tabla
    def get_list(self):
        return self.list[1:]

    # E: No hay
    # R: No hay
    # S: Retorna los encabezados de la tabla
    def get_headers(self):
        return self.list[:1]

    # E: No hay
    # R: No hay
    # S: Retorna los elementos de la tabla categoria musica
    def get_musica(self):
        return self.musica

    # E: No hay
    # R: No hay
    # S: Retorna los elementos de la tabla categoria juegos
    def get_juegos(self):
        return self.juegos

    # E: No hay
    # R: No hay
    # S: Retorna los elementos de la tabla categoria herramientas
    def get_herramientas(self):
        return self.herramientas

    # E: No hay
    # R: No hay
    # S: Retorna los elementos de la tabla categoria redes sociales
    def get_redes(self):
        return self.redes

    # E: Categoria y renglon
    # S: Lista con las apps en cierta categoria
    # R: No hay
    def list_categoria(self, categ, row):
        column_categoria = 3
        if row == len(self.list):
            return []
        elif self.list[row][column_categoria].lstrip() == categ:
            return [self.list[row]] + self.list_categoria(categ, row+1)
        else:
            return [] + self.list_categoria(categ, row+1)

    # E: Lista
    # S: No retorna, solo annade un nuevo renglon con los indices de la lista dada
    # R: No hay
    def add(self, lista):
        global apps
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            apps = appTable()
        else:
            error_handling(0)

    # E: Renglon a modificar de cierta lista
    # S: No retorna, solo modifica un renglon
    # R: No hay
    def update(self, row, lista):
        global apps
        if len(lista) == len(self.list[0]):
            self.list[row+1] = lista
            open_temp_file = open(self.file, 'w')
            create_db(self.list, open_temp_file)
            close_temp_file = open_temp_file.close()
            apps = appTable()
        else:
            error_handling(0)

    # E: renglon, columna y elemento a reemplazar
    # S: No retorna, solo reemplaza un elemento por otro dado
    # R: No hay
    def mod(self, row, column, ele):
        global apps
        open_temp_file = open(self.file, 'w')
        self.list[int(row)][int(column)] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()
        apps = appTable()

# Clase destinada a la creacion de la tabla de compradores. Sus atributos tienen que ver con la tabla en forma de lista
# y otras particularidades. Entre sus metodos se posicionan los metodos get, los metodos de annadir o buscar en la tabla
# entre otros.
class buyersTable:
    def __init__(self):
        self.file = '../users/compradores.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    # E: Contador
    # S: Una tabla convertida a lista
    # R: No hay
    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

    # E: Elemento a buscar en una cierta columna, row es un contador de renglon
    # S: False si el elemento no esta o el renglon si se encuentra una coincidencia
    # R: No hay
    def is_in(self, ele, row, column):
        if row == len(self.list)-1:
            if column == len(self.list[0])-1:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row]
                else:
                    return False
            else:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)
        else:
            if column == len(self.list[0])-1:
                return self.is_in(ele, row+1, 0)
            else:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)

    # E: Lista
    # S: No retorna, solo annade un nuevo renglon con los indices de la lista dada
    # R: No hay
    def add(self, lista):
        global buyers
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            buyers = buyersTable
        else:
            error_handling(0)

    # E: renglon, columna y elemento a reemplazar
    # S: No retorna, solo reemplaza un elemento por otro dado
    # R: No hay
    def mod(self, row, column, ele):
        open_temp_file = open(self.file, 'w')
        self.list[int(row)][int(column)] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()


# Clase destinada a la creacion de la tabla de vendedores. Sus atributos tienen que ver con la tabla en forma de lista
# y otras particularidades. Entre sus metodos se posicionan los metodos get, los metodos de annadir o eliminar de la tabla
# entre otros.
class sellersTable:
    def __init__(self):
        self.file = '../users/vendedores.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    # E: Contador
    # S: Una tabla convertida a lista
    # R: No hay
    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a.lstrip().rstrip('\n')] + self.__to_list(cont + 1)

    # E: Elemento a buscar en una cierta columna, row es un contador de renglon
    # S: False si el elemento no esta o el renglon si se encuentra una coincidencia
    # R: No hay
    def is_in(self, ele, row, column):
        if row == len(self.list)-1:
            if column == len(self.list[0])-1:
                if self.list[row][column].lstrip().lower().replace(' ','') == ele.lower().replace(' ',''):
                    return self.list[row]
                else:
                    return False
            else:
                if self.list[row][column].lstrip().lower().replace(' ','') == ele.lower().replace(' ',''):
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)
        else:
            if column == len(self.list[0])-1:
                return self.is_in(ele, row+1, 0)
            else:
                if self.list[row][column].lstrip().lower().replace(' ','') == ele.lower().replace(' ',''):
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)

    # E: No hay
    # R: No hay
    # S: Retorna los elementos de la tabla
    def get_list(self):
        return self.list[1:]

    # E: Lista
    # S: No retorna, solo annade un nuevo renglon con los indices de la lista dada
    # R: No hay
    def add(self, lista):
        global sellers
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            sellers = sellersTable()
        else:
            error_handling(0)

    # E: renglon, columna y elemento a reemplazar
    # S: No retorna, solo reemplaza un elemento por otro dado
    # R: No hay
    def mod(self, row, column, ele):
        open_temp_file = open(self.file, 'w')
        self.list[int(row)][int(column)] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()

    # E: renglon a eliminar
    # S: No retorna, solamente elimina de la tabla el renglon que se le de
    # R: No hay
    def remove(self, row):
        global sellers
        self.list = self.remove_aux(row, 0)
        open_temp_file = open(self.file, 'w')
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()
        sellers = sellersTable()


    def remove_aux(self, row, cont):
        if cont == len(self.list):
            return []
        elif row == cont:
            return self.remove_aux(row, cont + 1)
        else:
            return [self.list[cont]] + self.remove_aux(row, cont + 1)

# Clase encargada de la creacion de la ventana de administrar vendedores, entre sus atributos se encuntra lo principal para
# crear la ventana, entre sus metodos se encuentra crear una tabla, borrar o annadir renglones
class manageWinVendedores:
    # Funcion constructor
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.config(bg=bg_color)

        # Dimensiones
        self.sc_width = root.winfo_screenwidth()
        self.sc_height = root.winfo_screenheight()
        self.width = self.sc_width * 35 / 100
        self.height = self.sc_height * 50 / 100
        self.root.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 32.5 / 100, self.sc_height * 15 / 100))

        self.canvas = Canvas(self.root, borderwidth=0, bg=bg_color,  bd=0, highlightthickness=0, relief='ridge',
                            width=self.width*80/100, height=self.height*80/100)
        self.frame = Frame(self.canvas, background=bg_color)
        self.vsby = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.vsbx = Scrollbar(self.root, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsby.set)
        self.canvas.configure(xscrollcommand=self.vsbx.set)

        self.vsby.pack(side="right", fill="y")
        self.vsbx.pack(side='bottom',fill='x')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.place(x=50,y=20)

        self.buttons=[]

        self.table()

        self.frame.update()
        self.load_plus = Image.open('../images/icons/plus.gif').resize((20, 20), Image.ANTIALIAS)
        self.plus_img = ImageTk.PhotoImage(self.load_plus)
        self.plus = Label(self.frame, image=self.plus_img, bg=bg_color, cursor='hand2')
        self.plus.grid(row=len(self.buttons)+1, column=0, columnspan=5)
        self.plus.bind('<Button-1>', lambda event: self.add_seller())  # Annade vendedor

        self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.gif').resize((30, 30), Image.ANTIALIAS)

        self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
        self.hamb_icon_label = Label(root, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                     bg=bg_color, cursor='hand2')
        self.hamb_icon_label.pack()
        self.hamb_icon_label.place(x=1, y=1)

        self.hamb_icon_label.bind('<Button-1>', self.show_menu)

    # E: No tiene
    # S: No retorna, crea una tabla en la interfaz
    # R: No hay
    def table(self):
        self.headers = ['ID', 'Nombre', 'Correo', 'Pagina Web']
        Label(self.frame, text=self.headers[0], bg=bg_color, font='Times').grid(row=0, column=0)
        Label(self.frame, text=self.headers[1], bg=bg_color, font='Times').grid(row=0, column=1)
        Label(self.frame, text=self.headers[2], bg=bg_color, font='Times').grid(row=0, column=2)
        Label(self.frame, text=self.headers[3], bg=bg_color, font='Times').grid(row=0, column=3)
        self.__table_aux(sellers.get_list(), 0, 0)

    def __table_aux(self, info, controw, contcolumn):
        if controw == len(info):
            return
        elif contcolumn == len(info[0]):
            load_erase_img = Image.open('../images/icons/red_cross.gif').resize((10,10), Image.ANTIALIAS)
            erase_img = ImageTk.PhotoImage(load_erase_img)
            self.buttons = self.buttons + ['eraseme']
            self.buttons[controw] = Label(self.frame, image=erase_img, bg=bg_color, cursor='hand2')
            self.buttons[controw].grid(row=controw+1, column=contcolumn)
            self.buttons[controw].image = erase_img
            self.buttons[controw].bind('<Button-1>', lambda event: self.erase(controw))
            return self.__table_aux(info, controw + 1, 0)
        else:
            Label(self.frame, text=info[controw][contcolumn], bg=bg_color,
                  font='Times').grid(row=controw+1, column=contcolumn, sticky=W)
            self.__table_aux(info, controw, contcolumn+1)

    # Simplemente actualiza el area de visibilidad del scrollbar
    def onFrameConfigure(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # E: Renglon que se desea eliminar
    # S: No retorna, solo elimina el renglon
    # R: No tiene
    def erase(self, row):
        global new_manage_window
        seller_id = sellers.list[row+1][0]
        isuser = self.isuser(sellers.list[row+1][1])
        if not self.has_active(seller_id, 0):
            sellers.remove(row+1)
            if isuser[0]:
                users.remove_pername(isuser[1][0])
            self.root.destroy()
            new_manage_window = manageWinVendedores(Toplevel())
        else:
            if current_language == 'esp':  # Control de idioma
                messagebox.showerror(title='Error', message='El vendedor tiene aplicaciones activas')
            else:
                messagebox.showerror(title='Error', message='The seller has active apps')

    # E: El id del vendedor del que se quiere saber si tiene apps activas
    # S: True si tiene activas, False de lo contrario.
    # R: No hay restricciones
    def has_active(self, seller_id, cont):
        lista = apps.get_list()
        if cont == len(lista):
            return False
        elif lista[cont][0] == seller_id:
            if lista[cont][6] == 'Activo':
                return True
            else:
                return self.has_active(seller_id, cont+1)
        else:
            return self.has_active(seller_id, cont+1)

    # Simplemente muestra el menu
    def show_menu(self, event):
        global menu
        menu = newMenu(self.root)
    # Simplemente annade un nuevo vendedor a la tabla
    def add_seller(self):
        self.add_seller_aux()

    def add_seller_aux(self):

        new_win = Toplevel()
        main_frame = Frame(new_win)
        main_frame.pack()

        name_label = Label(main_frame, text='Nombre:')
        name_label.grid(row=0, column=0)
        mail_label = Label(main_frame, text='Correo:')
        mail_label.grid(row=1, column=0)
        page_label = Label(main_frame, text='Sitio Web:')
        page_label.grid(row=2, column=0)

        name_entry = Entry(main_frame)
        name_entry.grid(row=0, column=1)
        mail_entry = Entry(main_frame)
        mail_entry.grid(row=1, column=1)
        page_entry = Entry(main_frame)
        page_entry.grid(row=2, column=1)

        # E: No tiene
        # S: No retorna, solamente envia los datos recibidos a sellers.add para que cree un nuevo renglon en la base de datos
        # R: No hay
        def send():
            if name_entry.get() != '' and mail_entry.get() != '' and page_entry.get() != '':
                if not sellers.is_in(name_entry.get(), 0, 1):
                    global new_manage_window
                    sellers.add([str(int(sellers.get_list()[len(sellers.get_list())-1][0])+1), name_entry.get(),
                                 mail_entry.get(), page_entry.get()])
                    self.root.destroy()
                    new_manage_window = manageWinVendedores(Toplevel())
                    new_win.destroy()
                else:
                    if current_language == 'esp':
                        messagebox.showerror(title='Vendedor encontrado',
                                             message='El nombre de vendedor que digito ya existe')
                    else:
                        messagebox.showerror(title='Vendedor encontrado',
                                             message='Seller name already taken')
            elif name_entry.get() == '':
                if current_language == 'esp':
                    messagebox.showerror(title='Error', message='Introduzca un nombre de vendedor')
                else:
                    messagebox.showerror(title='Error', message='Insert the sellers name')
            elif mail_entry.get() == '':
                if current_language == 'esp':
                    messagebox.showerror(title='Error', message='Introduzca un correo')
                else:
                    messagebox.showerror(title='Error', message='Insert an email')
            else:
                if current_language == 'esp':
                    messagebox.showerror(title='Error', message='Introduzca una pagina web')
                else:
                    messagebox.showerror(title='Error', message='Insert a web page')

        ready = Button(main_frame, text='Listo', command=send)
        cancel = Button(main_frame, text='Cancelar', command=new_win.destroy)
        ready.grid(row=3, column=1, sticky=W)
        cancel.grid(row=3, column=0, sticky=E)

    # E: El nombre de un vendedor
    # S: True si el vendedor es un usuario, False si no
    # R: No hay
    def isuser(self, name):
        verify = users.is_in(name, 0, 0)
        if verify:
            return True, verify
        else:
            return False, verify

# Clase destinada a la creacion de la tabla de usuarios. Sus atributos tienen que ver con la tabla en forma de lista
# y otras particularidades. Entre sus metodos se posicionan los metodos get, los metodos de annadir o modificar la tabla
# entre otros.
class usersTable():
    def __init__(self):
        self.file = '../users/usuarios.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    # E: Contador
    # S: Una tabla convertida a lista
    # R: No hay
    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

    # E: Elemento a buscar en una cierta columna, row es un contador de renglon
    # S: False si el elemento no esta o el renglon si se encuentra una coincidencia
    # R: No hay
    def is_in(self, ele, row, column):
        if row == len(self.list)-1:
            if column == len(self.list[0])-1:
                if self.list[row][column].lstrip().lower().replace('', ' ') == ele.lstrip().lower().replace('', ' '):
                    return self.list[row]
                else:
                    return False
            else:
                if self.list[row][column].lstrip().lower().replace('', ' ') == ele.lstrip().lower().replace('', ' '):
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)
        else:
            if column == len(self.list[0]):
                return self.is_in(ele, row+1, 0)
            else:
                if self.list[row][column].lstrip().lower().replace('', ' ') == ele.lstrip().lower().replace('', ' '):
                    return self.list[row]
                else:
                    return self.is_in(ele, row, column+1)

    # E: Lista
    # S: No retorna, solo annade un nuevo renglon con los indices de la lista dada
    # R: No hay
    def add(self, lista):
        global users
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            users = usersTable()
        else:
            error_handling(0)

    # E: renglon, columna y elemento a reemplazar
    # S: No retorna, solo reemplaza un elemento por otro dado
    # R: No hay
    def mod(self, row, column, ele):
        global users
        open_temp_file = open(self.file, 'w')
        self.list[row][column] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()

    # E: Nombre a eliminar
    # S: No retorna, solamente elimina de la tabla el renglon que se le de
    # R: No hay
    def remove_pername(self, name):
        global users
        global users_list
        self.list = self.remove_pername_aux(name, 0)
        open_temp_file = open(self.file, 'w')
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()
        users = usersTable()

    def remove_pername_aux(self, name, cont):
        if cont == len(self.list):
            return []
        elif name == self.list[cont][0]:
            users_list[cont-1] = ''
            return self.remove_pername_aux(name, cont + 1)
        else:
            print(name)
            print(self.list[0])
            return [self.list[cont]] + self.remove_pername_aux(name, cont + 1)

# Clase destinada a la creacion de la tabla de frases. Sus atributos tienen que ver con la tabla en forma de lista
# y otras particularidades. Entre sus metodos se posicionan los metodos get, los metodos de buscar y extraer una frase
# entre otros.
class quoteTable:
    def __init__(self, file):
        self.file = file
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    # E: Contador
    # S: Una tabla convertida a lista
    # R: No hay
    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

    # E: No hay
    # S: Retorna una frase aleatoria de la base de datos de frases.
    # R: No hay
    def get_quote(self):
        quote_number = str(randint(1,20))
        return self.is_in(quote_number, 0, 0)

    # E: Elemento a buscar en una cierta columna, row es un contador de renglon
    # S: False si el elemento no esta o el renglon si se encuentra una coincidencia
    # R: No hay
    def is_in(self, ele, row, column):
        if row == len(self.list)-1:
            if column == len(self.list[0])-1:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row][1:]
                else:
                    return False
            else:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row][1:]
                else:
                    return self.is_in(ele, row, column+1)
        else:
            if column == len(self.list[0]):
                return self.is_in(ele, row+1, 0)
            else:
                if self.list[row][column].lstrip() == ele:
                    return self.list[row][1:]
                else:
                    return self.is_in(ele, row, column+1)

# Clase que modela un usuario, sus atributos se refieren a las columnas de la base de datos de usuarios, sus metodos permiten
# modificar unas cuantas cosas, verificar si existe dentro de la tabla y otros.
class newUser:
    # Funcion constructor
    def __init__(self, name, username, password, seller_id, buyer_id, mail, webpage, perfil, fondo, buys, admin,
                 country, language, user_id):
        self.name = name
        self.username = username.lstrip()
        self.password = password.lstrip()
        self.seller_id = seller_id.lstrip()
        self.buyer_id = buyer_id.lstrip()
        self.mail = mail.lstrip()
        self.webpage = webpage.lstrip()
        self.perfil = perfil.lstrip()
        self.fondo =fondo.lstrip()
        self.buys = buys.lstrip()
        self.admin = admin.lstrip()
        self.country = country.lstrip()
        self.language = language.lstrip()
        self.user_id = user_id.lstrip()
        self.exists = self.__verify()

    # E: No hay
    # S: Retorna True si existe el usuario en la tabla de vendedores o compradores
    # R: No hay
    def __verify(self):
        if buyers.is_in(self.name, 0, 0) or sellers.is_in(self.name, 0, 0):
            self.__retrieve_info(self.name, buyers.is_in(self.name, 0, 0), sellers.is_in(self.name, 0, 0))
            return True
        else:
            return False

    # E : lista de compradores, vendedores y el nombre
    # S: Complementaria de verify, si verify da True, toma los datos de las dos bases de datos y los pone en los campos correspondientes en el objeto
    # R: No hay
    def __retrieve_info(self, name, buyerslist, sellerslist):
        if buyerslist:
            self.buyer_id = buyerslist[0].lstrip()
            self.mail = buyerslist[2].lstrip()
            self.buys = buyerslist[3].lstrip()
        else:
            self.buyer_id = 'None'
            self.mail = 'None'
            self.buys = 'None'
        if sellerslist:
            self.seller_id = sellerslist[0].lstrip()
            self.webpage = sellerslist[3].lstrip()
        else:
            self.seller_id = 'None'
            self.seller_id = 'None'
    # E: valor al que se quiere cambiar el mail
    # S: No retorna, solo cambia el mail en todas las tablas
    # R: No hay
    def mod_mail(self, tothis):
        global buyers
        global sellers

        self.mail = tothis
        buyers.mod(self.buyer_id, 2, tothis)
        sellers.mod(self.seller_id, 2, tothis)

    # E: valor al que se quiere cambiar la webpage
    # S: No retorna, solo cambia el webpage en la tabla de sellers
    # R: No hay
    def mod_page(self, tothis):
        global sellers

        self.webpage = tothis
        sellers.mod(self.seller_id, 3, tothis)

    # E: valor al que se quiere cambiar las compras
    # S: No retorna, solo cambia las compras en la tabla de buyers
    # R: No hay
    def mod_buys(self, tothis):
        global buyers

        self.buys = tothis
        buyers.mod(self.seller_id, 3, tothis)

# Simplemente muestra la ventana de registro
def show_register(*args):
    try:
        register.win_register.deiconify()
        register.win_register.lift()
        register.win_register.focus_force()
    except:
        register.win_register.withdraw()
        register.win_register.focus_force()

# Simplemente cambia el usuario a invitado
def logout(*args):
    global current_user
    global main
    global current_language
    current_user = -1
    main.kill()
    menu.destroy()
    main = main_window(root, current_language)

# E: Todas las columnas de la tabla de usuarios debidamente llenas y separadas.
# S: No retorna, crea un nuevo objeto de usuario en una lista
# R: No hay
def create_user(name, username, password, seller_id, buyer_id, mail, webpage, perfil, fondo, buys, admin,
                country, language, id):
    global users_list
    next_i = len(users_list)
    users_list = users_list + ['delete me']
    users_list[next_i] = newUser(name, username, password, seller_id, buyer_id, mail, webpage, perfil, fondo, buys,
                                 admin, country, language, id)

# E: Contador
# S: No retorna, crea los primeros usuarios.
# R: No hay
def users_list_first_config(cont):
    if cont == len(users.list):
        return
    else:
        create_user(users.list[cont][0], users.list[cont][1], users.list[cont][2], 'None', 'None', 'None', 'None',
                    users.list[cont][3], users.list[cont][4], '0', users.list[cont][5],
                    users.list[cont][6], users.list[cont][7], str(cont))
        users_list_first_config(cont+1)

profile_page=''  # Variable global para el manejo de la pagina de perfil


# Simplemente crea la pagina de perfil propia del current user
def create_my_profile_page(*args):
    global users_list
    global current_user
    global profile_page
    try:
        profile_page.win.deiconify()
        profile_page.win.lift()
        profile_page.win.focus_force()
    except:
        profile_page = profPage(users_list[current_user])

# E: Numero de error
# S: No retorna, tira un pop up con un mensaje de error
# R: No hay
def error_handling(errnum):
    if current_language == 'esp': # Verificar idioma
        err_cases = ['Contacte al administrador\nCodigo de error:1\nNumero de columnas insuficiente',
                     'Contacte al administrador\nHa ocurrido un error inesperado']
        messagebox.showerror(title='Error interno', message=err_cases[errnum])
    else:
        err_cases = ['Contact support\nErr code:1\nColumn number is not enough',
                     'Conctact support\nAn impropted error has ocurred']
        messagebox.showerror(title='Internal error', message=err_cases[errnum])


menu = Label(root)

# Designacion inicial de las clases
apps = appTable()
buyers = buyersTable()
sellers = sellersTable()
users = usersTable()
users_list_first_config(1)
esp_quotes = quoteTable('../misc/quotes/esp.txt')
eng_quotes = quoteTable('../misc/quotes/eng.txt')
main = main_window(root, current_language)
login = newLogin(root)
register = newRegister(root)
adminwin = adminWindow()
search = searchWin()

# Escondiendo las ventanas abiertas
new_manage_window = Toplevel()
new_manage_window.withdraw()
adminwin.win.withdraw()
login.win_login.withdraw()
register.win_register.withdraw()
search.win.withdraw()

# mainloop
mainloop()