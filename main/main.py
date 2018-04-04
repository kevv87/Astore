from tkinter import *
from PIL import ImageTk, Image
from random import *
from tkinter import filedialog as fd
from manejo_txt import *
from tkinter import simpledialog

users_list = []
current_user = 1
current_language = 'esp'

bg_color = '#bbb8c1'
root = Tk()
root.title('Astore')
root.resizable(False, False)


# Dimensiones de la pantalla
win_width, win_height = root.winfo_screenwidth(), root.winfo_screenheight()
win_width = 40*win_width/100

root.geometry('%dx%d+%d+0' % (win_width, win_height*92/100, win_width*80/100))


class newMenu:
    def __init__(self, master):
        self.bg_color = '#390959'
        self.canvas_menu = Canvas(master, height=win_height * 30 / 100, width=win_width * 25 / 100, bg=self.bg_color,
                                  bd=0, highlightthickness=0, relief='ridge')
        self.canvas_menu.pack()
        self.canvas_menu.place(x=0, y=0)

        self.width = self.canvas_menu.winfo_screenwidth()
        self.height = self.canvas_menu.winfo_screenheight()

        self.master = master

        if current_user == -1:
            self.load_guest_img = Image.open('../users/guest.png').resize((50, 50), Image.ANTIALIAS)
            self.user_img = ImageTk.PhotoImage(self.load_guest_img)

            self.canvas_menu.bind('<Leave>', self.destroy)

            self.user_img_label = Label(master, image=self.user_img, bd=0, highlightthickness=0,
                                        relief='ridge', bg=bg_color)
            self.user_img_label.pack()
            self.user_img_label.place(x=5, y=10)

            self.user_name = Label(self.canvas_menu, text='Invitado', font='Times 15', bg=self.bg_color, fg='white')
            self.user_name.pack()
            self.user_name.place(x=70, y=35)

            self.esp_flag_load = Image.open('../images/icons/espanna.png').resize((30,20), Image.ANTIALIAS)
            self.esp_flag_img = ImageTk.PhotoImage(self.esp_flag_load)
            self.esp_flag_label = Label(self.canvas_menu, image=self.esp_flag_img, bg=self.bg_color, cursor='hand2')
            self.esp_flag_label.pack()
            self.esp_flag_label.place(x=win_width*10/100, y=5)
            self.esp_flag_label.bind('<Button-1>', self.change_language_toesp)

            self.eng_flag_load = Image.open('../images/icons/ingles.png').resize((30, 20), Image.ANTIALIAS)
            self.eng_flag_img = ImageTk.PhotoImage(self.eng_flag_load)
            self.eng_flag_label = Label(self.canvas_menu, image=self.eng_flag_img, bg=self.bg_color, cursor='hand2')
            self.eng_flag_label.pack()
            self.eng_flag_label.place(x=win_width * 18 / 100, y=5)
            self.eng_flag_label.bind('<Button-1>', self.change_language_toeng)

            if current_language == 'esp':
                self.login_button = Button(self.canvas_menu, text='Iniciar sesion', bd=0, highlightthickness=0, relief='ridge',
                                           command=self.show_login)
                self.register_button = Button(self.canvas_menu, text='Registrarse', bd=0, highlightthickness=0,
                                              relief='ridge', command=show_register)
                self.home_button = Button(self.canvas_menu, text='Pagina Principal',bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_mainpage)
                self.apps_button = Button(self.canvas_menu, text='Todas las apps', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_search)
            else:
                self.login_button = Button(self.canvas_menu, text='Login', bd=0, highlightthickness=0,
                                           relief='ridge',
                                           command=self.show_login)
                self.register_button = Button(self.canvas_menu, text='Sign up', bd=0, highlightthickness=0,
                                              relief='ridge', command=show_register)
                self.home_button = Button(self.canvas_menu, text='Home Page', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_mainpage)
                self.apps_button = Button(self.canvas_menu, text='All apps', bd=0, highlightthickness=0,
                                          relief='ridge', command=self.show_search)
            self.login_button.pack()
            self.register_button.pack()
            self.home_button.pack()
            self.apps_button.pack()
            self.login_button.place(x=0, y=75)
            self.home_button.place(x=0, y=165)
            if current_language == 'esp':
                self.register_button.place(x=win_width * 11 / 100, y=120)
                self.apps_button.place(x=win_width*8/100, y=210)
            else:
                self.register_button.place(x=win_width * 14 / 100, y=120)
                self.apps_button.place(x=win_width*14/100, y=210)
        else:
            try:
                self.load_user_img = Image.open(users_list[current_user].perfil).resize((54,50), Image.ANTIALIAS)
            except:
                self.load_user_img = Image.open('../users/guest.png').resize((54, 50), Image.ANTIALIAS)
            self.user_img = ImageTk.PhotoImage(self.load_user_img)

            self.canvas_menu.bind('<Leave>', self.destroy)

            self.user_img_label = Label(master, image=self.user_img, bd=0, highlightthickness=0,
                                        relief='ridge', bg=bg_color)
            self.user_img_label.pack()
            self.user_img_label.place(x=5, y=10)
            if len(users_list[current_user].name) < 8:
                self.user_name = Label(self.canvas_menu, text='%s' % users_list[current_user].name,
                                   font='Times 15', bg=self.bg_color, fg='white')
            else:
                self.user_name = Label(self.canvas_menu, text='%s' % users_list[current_user].name,
                                       font='Times 10', bg=self.bg_color, fg='white')
            self.user_name.pack()
            self.user_name.place(x=70, y=35)

            self.esp_flag_load = Image.open('../images/icons/espanna.png').resize((30, 20), Image.ANTIALIAS)
            self.esp_flag_img = ImageTk.PhotoImage(self.esp_flag_load)
            self.esp_flag_label = Label(self.canvas_menu, image=self.esp_flag_img, bg=self.bg_color, cursor='hand2')
            self.esp_flag_label.pack()
            self.esp_flag_label.place(x=win_width * 10 / 100, y=5)
            self.esp_flag_label.bind('<Button-1>', self.change_language_toesp)

            self.eng_flag_load = Image.open('../images/icons/ingles.png').resize((30, 20), Image.ANTIALIAS)
            self.eng_flag_img = ImageTk.PhotoImage(self.eng_flag_load)
            self.eng_flag_label = Label(self.canvas_menu, image=self.eng_flag_img, bg=self.bg_color, cursor='hand2')
            self.eng_flag_label.pack()
            self.eng_flag_label.place(x=win_width * 18 / 100, y=5)
            self.eng_flag_label.bind('<Button-1>', self.change_language_toeng)

            if users_list[current_user].admin == 'S' or users_list[current_user].admin == 'si':
                if current_language == 'esp':
                    self.admin_button = Button(self.canvas_menu, text='Administrar\nVendedores', bd=0, highlightthickness=0,
                                           relief='ridge', command=self.show_admin)
                else:
                    self.admin_button = Button(self.canvas_menu, text='Manage\nSellers', bd=0, highlightthickness=0,
                                               relief='ridge', command=self.show_admin)
                self.admin_button.pack()
                self.admin_button.place(x=0, y=self.height*20/100)
            if current_language == 'esp':
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
            else:
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
            self.perfil_button.pack()
            self.home_button.pack()
            self.apps_button.pack()
            self.logout_button.pack()
            if current_language == 'esp':
                self.apps_button.place(x=win_width * 8 / 100, y=140)
                self.logout_button.place(x=win_width * 4 / 100, y=self.height * 26 / 100)
            else:
                self.apps_button.place(x=win_width * 14 / 100, y=140)
                self.logout_button.place(x=win_width * 7 / 100, y=self.height * 26 / 100)
            self.perfil_button.place(x=5, y=61)
            self.home_button.place(x=0, y=100)



    def show_login(self, *args):
        try:
            login.win_login.deiconify()
            login.win_login.lift()
            login.win_login.focus_force()
            self.destroy()
        except:
            login.win_login.withdraw()
            login.win_login.focus_force()
            self.destroy()

    def show_admin(self, *args):
        global new_manage_win
        try:
            new_manage_win.deiconify()
            new_manage_win.lift()
            new_manage_win.focus_force()
            self.destroy()
        except:
            new_admin_win = Toplevel()
            manageWinVendedores(new_admin_win)
            new_admin_win.focus_force()
            self.destroy()

    def show_mainpage(self, *args):
        global main
        try:
            self.master.withdraw()
            root.deiconify()
            main.kill()
            main = main_window(root, current_language, current_language)
            root.lift()
            root.focus_force()
            self.destroy()
        except:
            root.withdraw()
            main.kill()
            main = main_window(root, current_language, current_user)
            self.master.withdraw()
            root.focus_force()

    def show_search(self, *args):
        try:
            self.master.withdraw()
            search.win.deiconify()
            search.win.lift()
            search.win.focus_force()
            self.destroy()
        except:
            search.win.withdraw()
            search.win.focus_force()

    def destroy(self, *args):
        self.canvas_menu.destroy()
        self.user_img_label.destroy()


    def change_language_toeng(self, *args):
        global main
        global menu
        global current_language
        if current_language == 'esp':
            login.change_languagetoeng()
            adminwin.to_eng()
            current_language = 'eng'
            main.kill()
            register.toeng()
            search.toeng()
            self.destroy()
            main = main_window(root, current_language, current_user)
        else:
            self.destroy()

    def change_language_toesp(self, *args):
        global main
        global menu
        global login
        global current_language
        if current_language == 'eng':
            current_language = 'esp'
            login.change_languagetoesp()
            adminwin.to_esp()
            register.toesp()
            search.toesp()
            main.kill()
            self.destroy()
            main = main_window(root, current_language, current_user)
        else:
            self.destroy()


class main_window:

    def __init__(self, master, language, user):
        self.language = language
        if current_user == -1 :
            self.master = master
            self.random_mainpage()
            self.welcome_canvas = Canvas(master, height='200', width='500', bg=bg_color, bd=0, highlightthickness=0,
                                         relief='ridge')
            self.welcome_canvas.pack()
            self.welcome_canvas.place(x=win_width * 10 / 100, y=50)


            if current_language == 'esp':
                self.welcome_text = Label(self.welcome_canvas, text='Bienvenido, invitado!', font='Times 20', bg=bg_color)
                self.quote = Label(self.welcome_canvas, text='Recuerde que debe\n iniciar sesion para descargar',
                                   font='Times 20 italic', bg=bg_color)
                self.quote.pack()
                self.quote.place(x=0, y=70)
                self.welcome_text.pack()
                self.welcome_text.place(x=0, y=20)
            else:
                self.welcome_text = Label(self.welcome_canvas, text='Welcome, guest!', font='Times 20',
                                          bg=bg_color)
                self.quote = Label(self.welcome_canvas, text='Please login in order to\ndownload content',
                                   font='Times 20 italic', bg=bg_color)
                self.quote.pack()
                self.quote.place(x=60, y=70)
                self.welcome_text.pack()
                self.welcome_text.place(x=90, y=20)


            self.load_guest_img = Image.open('../users/guest.png').resize((125, 125), Image.ANTIALIAS)
            self.guest_img = ImageTk.PhotoImage(self.load_guest_img)
            self.user_img_label = Label(self.welcome_canvas, image=self.guest_img, bd=0, highlightthickness=0,
                                        relief='ridge')
            self.user_img_label.pack()
            self.user_img_label.place(x=350, y=20)

            self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.png').resize((30, 30), Image.ANTIALIAS)

            self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
            self.hamb_icon_label = Label(root, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                         bg=bg_color, cursor='hand2')
            self.hamb_icon_label.pack()
            self.hamb_icon_label.place(x=1, y=1)

            self.hamb_icon_label.bind('<Button-1>', self.show_menu)
        else:
            self.master = master
            self.random_mainpage()

            self.welcome_canvas = Canvas(master, height='200', width='500', bg=bg_color, bd=0, highlightthickness=0,
                                         relief='ridge')
            self.welcome_canvas.pack()
            self.welcome_canvas.place(x=win_width * 10 / 100, y=50)
            if current_language == 'esp':
                self.welcome_text = Label(self.welcome_canvas, text='Bienvenido, %s!' % users_list[current_user].name,
                                          font='Times 20', bg=bg_color)
            else:
                self.welcome_text = Label(self.welcome_canvas, text='Welcome, %s!' % users_list[current_user].name,
                                          font='Times 20', bg=bg_color)
            self.welcome_text.pack()
            self.welcome_text.place(x=0, y=20)

            self.quote_canvas = Canvas(self.welcome_canvas, bg=bg_color, width=349, height =140, bd=0, highlightthickness=0,
                                         relief='ridge')
            self.quote_canvas.pack()
            self.quote_canvas.place(x=0,y=50)

            self.randomize_quote()
            try:
                self.load_user_img = Image.open(users_list[current_user].perfil).resize((125, 125), Image.ANTIALIAS)
            except:
                self.load_user_img = Image.open('../users/guest.png').resize((125, 125), Image.ANTIALIAS)
            self.user_img = ImageTk.PhotoImage(self.load_user_img)
            self.user_img_label = Label(self.welcome_canvas, image=self.user_img, bd=0, highlightthickness=0,
                                        relief='ridge')
            self.user_img_label.image = self.user_img
            self.user_img_label.pack()
            self.user_img_label.place(x=350, y=20)
            self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.png').resize((30, 30), Image.ANTIALIAS)

            self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
            self.hamb_icon_label = Label(root, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                         bg=bg_color, cursor='hand2')
            self.hamb_icon_label.pack()
            self.hamb_icon_label.place(x=1, y=1)

            self.hamb_icon_label.bind('<Button-1>', self.show_menu)


    def show_menu(self, *args):
        return self.__show_menu_aux()

    def __show_menu_aux(self):
        global menu
        menu = newMenu(self.master)

    def random_mainpage(self):
        self.bottom_canvas = Canvas(self.master, height=win_height - 20, width=win_width, bg=bg_color)
        self.bottom_canvas.pack()
        categorias = ['Juegos', 'Musica', 'Redes sociales', 'Herramientas']
        master = self.bottom_canvas
        self.random_mainpage_aux(master, categorias, [], 1)

    def is_in(self, list1, ele, cont):
        if len(list1) == cont:
            return False
        elif list1[cont] == ele:
            return True
        else:
            return self.is_in(list1, ele, cont + 1)

    def random_mainpage_aux(self, master, categorias, used, cont):
        rand = randint(0, 3)
        ini_y = 50
        com_height = 188
        fix = 188
        if len(used) == 3:
            return
        elif not self.is_in(used, categorias[rand], 0):
            if categorias[rand] == 'Juegos':
                categoria_juego = juegos(master, ini_y, fix, com_height, cont)
                return self.random_mainpage_aux(master, categorias, used + ['Juegos'], cont + 1)
            elif categorias[rand] == 'Musica':
                categoria_musica = musica(master, ini_y, fix, com_height, cont)
                return self.random_mainpage_aux(master, categorias, used + ['Musica'], cont + 1)
            elif categorias[rand] == 'Redes sociales':
                categoria_redes = redes(master, ini_y, fix, com_height, cont)
                return self.random_mainpage_aux(master, categorias, used + ['Redes sociales'], cont + 1)
            else:
                categoria_herramientas = herramientas(master, ini_y, fix, com_height, cont)
                return self.random_mainpage_aux(master, categorias, used + ['Herramientas'], cont + 1)
        else:
            return self.random_mainpage_aux(master, categorias, used, cont)

    def kill(self):
        self.bottom_canvas.destroy()
        self.welcome_canvas.destroy()
        self.user_img_label.destroy()

    def randomize_quote(self):
        try:
            self.quote.destroy()
            self.randomize_quote()
        except:
            if self.language == 'esp':
                self.quote_text = esp_quotes.get_quote()[0]
                self.quote_author = esp_quotes.get_quote()[1]

            else:
                self.quote_text = eng_quotes.get_quote()[0]
                self.quote_author = eng_quotes.get_quote()[1]
            self.quote = Label(self.quote_canvas, font='Times 13 italic', text=self.quote_text, bg=bg_color,
                               wraplengt=330)
            self.quote.pack()
            self.quote.place(x=0, y=20)
            self.quote_author = Label(self.quote_canvas, font='Times 13 italic bold', text='-'+self.quote_author,
                                      bg=bg_color)
            self.quote_author.pack()
            self.quote_author.place(x=160, y=100)

    def change_languagetoesp(self):
        global current_language
        if current_language == 'eng':
            self.randomize_quote()


class newLogin:
    def __init__(self, master):
        self.master = master
        self.bg = '#bbb8c1'
        # Configuracion principal
        self.win_login = Toplevel(bg=self.bg)
        self.win_login.resizable(False, False)
        self.win_login.title('Astore')

        # Dimensiones
        self.win_login_width, self.win_login_height = root.winfo_screenwidth()*20/100, root.winfo_screenheight()*27/100
        self.win_login.geometry('%dx%d+%d+%d' % (self.win_login_width, self.win_login_height,
                                                 self.win_login_width + self.win_login_width,
                                                 self.win_login_height))

        self.title = Label(self.win_login, text='Astore', font='Times 50', bg=self.bg)
        self.title.pack()
        self.title.place(x=self.win_login_width*22/100, y=0)

        self.none1 = StringVar()
        self.none1.set('')
        self.none2 = StringVar()
        self.none2.set('')
        self.user_label = Label(self.win_login, text='Usuario:', font='Times 15', bg=self.bg)
        self.user_entry = Entry(self.win_login, textvariable=self.none1)
        self.pass_label = Label(self.win_login, text='Contraseña:', font='Times 15', bg=self.bg)
        self.pass_entry = Entry(self.win_login, textvariable=self.none2)

        self.pass_entry.pack()
        self.pass_label.pack()
        self.user_label.pack()
        self.user_entry.pack()
        self.user_label.place(x=self.win_login_width*14/100, y=self.win_login_height*32/100)
        self.user_entry.place(x=self.win_login_width*38/100, y=self.win_login_height*35/100)
        self.pass_label.place(x=self.win_login_width*6/100, y=self.win_login_height*44/100)
        self.pass_entry.place(x=self.win_login_width*38/100, y=self.win_login_height*47/100)

        self.login_button = Button(self.win_login, text='Iniciar\nsesion', command=self.login)
        self.register_button = Button(self.win_login, text='Registrarse', command= self.__show_register)
        self.login_button.pack()
        self.register_button.pack()
        self.login_button.place(x=self.win_login_width*23/100, y=self.win_login_height*70/100)
        self.register_button.place(x=self.win_login_width*48/100, y=self.win_login_height*70/100)

        self.win_login.protocol("WM_DELETE_WINDOW", self.win_login.withdraw)
        self.win_login.bind('<Return>', self.login)

    def __show_register(self, *args):
        self.win_login.withdraw()
        show_register()

    def login(self, *args):
        global current_user
        global users_list
        global main
        global menu
        global current_language
        login_user = self.user_entry.get()
        login_pass = self.pass_entry.get()
        user_row = users.is_in(login_user, 0, 0)
        if user_row and user_row[2].lstrip() == login_pass:
            current_language = user_row[7]
            self.login_aux(login_user, 0)
            main.kill()
            menu.destroy()
            main = main_window(root, current_language, current_user)
            menu = newMenu(self.master)
            self.win_login.withdraw()
            self.none1.set('')
            self.none2.set('')
        else:
            print('Contrasena incorrecta o no usuario')

    def login_aux(self,login_user, cont):
        global current_user
        if cont == len(users_list):
            return 'Err'
        elif users_list[cont].username == login_user:
            current_user = cont
            return
        else:
            self.login_aux(login_user, cont+1)

    def destroy(self):
        self.win_login.destroy()

    def change_languagetoeng(self):
        self.user_label.config(text='   User:')
        self.pass_label.config(text='  Password:')
        self.login_button.config(text='Login')
        self.register_button.config(text='Sign Up')

    def change_languagetoesp(self):
        self.user_label.config(text='Usuario:')
        self.pass_label.config(text='Contraseña:')
        self.login_button.config(text='Iniciar\nsesion')
        self.register_button.config(text='Registrarse')

class newRegister:
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

        self.esp_flag_load = Image.open('../images/icons/espanna.png').resize((60, 40), Image.ANTIALIAS)
        self.esp_flag_img = ImageTk.PhotoImage(self.esp_flag_load)
        self.esp_flag_label = Label(self.win_register, image=self.esp_flag_img, bg=self.bg_color)
        self.esp_flag_label.bind('<Button-1>', self.espselected)

        self.eng_flag_load = Image.open('../images/icons/ingles.png').resize((60, 40), Image.ANTIALIAS)
        self.eng_flag_img = ImageTk.PhotoImage(self.eng_flag_load)
        self.eng_flag_label = Label(self.win_register, image=self.eng_flag_img, bg=self.bg_color)
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
        self.image_entry.bind('<Button-1>', self.change_img)

        self.win_register.protocol("WM_DELETE_WINDOW", self.win_register.withdraw)

    def change_img(self, *args):
        self.win_register.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((100,100),Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.image_entry.config(image=new_img)
            self.image_entry.image = new_img
        except:
            print('No image')
        self.win_register.lift()

    def add_user(self, *args):
        global main
        global current_language
        global current_user

        print('callback')
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

        if users.is_in(usuario, 0, 1):
            print('Ya existe el nombre de usuario')
        else:
            if nombre.lstrip() != '' and usuario.lstrip() != '' and contra.lstrip() != '' and recontra.lstrip() != '' and correo.lstrip() != '':
                if contra.lstrip() == recontra.lstrip():
                    self.add_touser()
                    self.add_toseller()
                    self.add_tobuyer()
                    create_user(nombre, usuario, contra, str(seller_id), str(buyer_id), correo, webpage,foto, fondo, apps_compradas, admin, pais, language)
                    current_user = len(users_list) - 1
                    current_language = language
                    main.kill()
                    main = main_window(root, current_language, current_user)
                else:
                    return print('Contrasenas no iguales')
            else:
                return print('Faltan espacios')

    def add_touser(self):

        nombre = self.name_entry.get()
        usuario = self.user_entry.get()
        contra = self.pass_entry.get()
        foto = self.img_path
        admin = 'no'
        fondo = 'None'
        pais = self.variable.get()
        language = self.selected_language
        users.add([nombre, usuario, contra, foto, fondo, admin, pais, language, []])
        self.win_register.withdraw()


    def add_toseller(self):
        nombre = self.name_entry.get()
        correo = self.mail_entry.get()
        if self.web_entry.get().lstrip() != '':
             webpage = self.web_entry.get()
        else:
            webpage = 'None'
        id = int(users_list[len(users_list)-1].seller_id)+1

        sellers.add([str(id), nombre, correo, webpage])

    def add_tobuyer(self):
        nombre = self.name_entry.get()
        correo = self.mail_entry.get()
        apps = '0'
        id = int(users_list[len(users_list) - 1].buyer_id) + 1

        buyers.add([str(id), nombre, correo, apps])

    def engselected(self, *args):
        self.selected_language = 'eng'

    def espselected(self, *args):
        self.selected_language = 'esp'

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


class adminWindow:
    def __init__(self):
        self.win = Toplevel()
        self.win.resizable(False, False)

        self.sc_width, self.sc_height = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        self.width = 20 * self.sc_width/100
        self.height = 20 * self.sc_height/100
        self.win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 41 / 100, self.sc_height*30/100))

        self.top_canvas = Canvas(self.win, bg=bg_color, width=self.width, height=self.height/2,).grid(row=0, columnspan=2)
        self.bottom_canvas_left = Canvas(self.win, bg=bg_color, width=self.width/2, height=self.height/2,).grid(row=1, column=0)
        self.bottom_canvas_right = Canvas(self.win, bg=bg_color, width=self.width/2, height=self.height/2,).grid(row=1, column=1)

        self.apps_label = Label(self.win, text='Aplicaciones', font='Times 20', bg=bg_color)
        self.vendedores_label = Label(self.win, text='Vendedores', font='Times 20', bg=bg_color)
        self.compradores_label = Label(self.win, text='Compradores', font='Times 20', bg=bg_color)

        self.apps_label.grid(row=0, columnspan=2)
        self.vendedores_label.grid(row=1, column=0)
        self.compradores_label.grid(row=1, column=1)

        self.win.protocol("WM_DELETE_WINDOW", self.win.withdraw)

    def to_eng(self):
        self.apps_label.config(text='Aplications')
        self.vendedores_label.config(text='Sellers')
        self.compradores_label.config(text='Buyers')

    def to_esp(self):
        self.apps_label.config(text='Aplicaciones')
        self.vendedores_label.config(text='Vendedores')
        self.compradores_label.config(text='Compradores')


class searchWin:
    def __init__(self):
        self.win = Toplevel()
        self.win.resizable(False, False)

        self.sc_width, self.sc_height = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        self.width = 70 * self.sc_width / 100
        self.height = 80 * self.sc_height / 100
        self.win.geometry('%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 15 / 100, self.sc_height * 10 / 100))

        self.canvas = Canvas(self.win, width=self.width, height=self.height)
        self.canvas.pack()

        self.title = Label(self.canvas, text='Astore', font='Times 20')
        self.title.pack()
        self.title.place(x=self.width*45/100, y=1)

        if current_language == 'esp':
            self.entry_label = Label(self.canvas, text='Buscar:', font='Times 13')
        else:
            self.entry_label = Label(self.canvas, text='Search:', font='Times 13')

        self.entry_label.pack()
        self.entry_label.place(x=self.width*6/100, y=self.height*8.3/100)
        self.entry = Entry(self.canvas, width=40)
        self.entry.pack()
        self.entry.place(x=self.width*14/100, y=self.height*9/100)
        self.entry.bind('<KeyRelease>', self.start_search)

        self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.png').resize((30, 30), Image.ANTIALIAS)

        self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
        self.hamb_icon_label = Label(self.win, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                     cursor = 'hand2')

        self.hamb_icon_label.pack()
        self.hamb_icon_label.place(x=1, y=1)
        self.hamb_icon_label.bind('<Button-1>', self.show_menu)

        self.app_canvas = Canvas(self.win, width=self.width*89/100, height=self.height*85/100)
        self.app_canvas.pack()
        self.app_canvas.place(x=self.width*6/100, y=self.height*13/100)

        self.comm_height = self.height*15/100
        self.comm_width = self.width*15/100
        # La ventana aguanta 4 rows y 6 columns
        self.showed_apps=[]
        self.posicionar_apps(apps.get_list(), 0, 0, 0)

        self.win.protocol('WM_DELETE_WINDOW', root.destroy)



    def start_search(self, *args):
        self.showed_apps = []
        self.app_canvas.destroy()
        self.app_canvas = Canvas(self.win, width=self.width * 89 / 100, height=self.height * 85 / 100)
        self.app_canvas.pack()
        self.app_canvas.place(x=self.width * 6 / 100, y=self.height * 13 / 100)
        ele = self.entry.get().lower().replace(' ','')
        if ele != '':
            return self.posicionar_apps(self.search_nombre_by_letter(apps.get_list(), ele, 0), 0, 0, 0)
        else:
            return self.posicionar_apps(apps.get_list(), 0, 0, 0)

    def search_nombre_by_letter(self, lista, ele, cont):
        if ele != ' ':
            if len(lista) == cont:
                return []
            elif lista[cont][2].lower().replace(' ', '').startswith(ele) or lista[cont][3].lower().replace(' ', '') == ele:
                return [lista[cont]] + self.search_nombre_by_letter(lista, ele, cont + 1)
            else:
                return self.search_nombre_by_letter(lista, ele, cont + 1)
        else:
            return []


    def posicionar_apps(self, lista, controw, contcolumn, contgeneral):
        if contgeneral == len(lista):
            return
        elif contcolumn<6:
            if controw<4:
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

    def show_menu(self, *args):
        return self.__show_menu_aux()

    def __show_menu_aux(self):
        global menu
        menu =newMenu(self.win)

    def toeng(self):
        self.entry_label.config(text='Search:')

    def toesp(self):
        self.entry_label.config(text='Buscar:')

class profPage:
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

        self.canvas_left = Canvas(self.win, bg=self.bg_color, height=self.height, width=self.width*30/100,
                                  bd=0, highlightthickness=0, relief='ridge')
        self.canvas_left.pack()
        self.canvas_left.place(x=0,y=0)

        self.canvas_right = Canvas(self.win, bg=self.bg_color, height=self.height, width=self.width*70/100,
                                   bd=0, highlightthickness=0, relief='ridge')

        self.canvas_right.pack()
        self.canvas_right.place(x=self.width*30/100,y=0)

        self.name = StringVar()
        self.name.set(info.name)
        self.correo = StringVar()
        self.correo.set(info.mail)
        self.webpage = StringVar()
        self.webpage.set(info.webpage)

        self.graphics_img_load = Image.open('../images/icons/graph.png').resize((50, 50), Image.ANTIALIAS)
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
        try:
            self.load_user_img = Image.open(self.path_user_img).resize((100,100), Image.ANTIALIAS)
        except FileNotFoundError:
            self.load_user_img = Image.open('../users/guest.png').resize((100,100), Image.ANTIALIAS)
        try:
            self.load_user_bg = Image.open(self.path_user_bg).resize((self.canvas_left.winfo_height()
                                                                      ,self.canvas_left.winfo_width()), Image.ANTIALIAS)
        except FileNotFoundError:
            self.load_user_bg = Image.open('../images/icons/no_image.png').resize((self.canvas_left.winfo_width()
                                                                      ,self.canvas_left.winfo_height()), Image.ANTIALIAS)

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

        self.name_label.update()

        self.lista_root=''

        if info.admin == 'si':
            self.load_crown = Image.open('../images/icons/mini_crown.png').resize((50,50), Image.ANTIALIAS)
            self.crown_img = ImageTk.PhotoImage(self.load_crown)
            self.crown_label = Label(self.canvas_right, image=self.crown_img, bg=bg_color)
            self.crown_label.pack()
            self.crown_label.place(x=self.name_label.winfo_width(), y=10)
        elif info.admin == 'S':
            self.load_crown = Image.open('../images/icons/real_crown.png').resize((50,50), Image.ANTIALIAS)
            self.crown_img = ImageTk.PhotoImage(self.load_crown)
            self.crown_label = Label(self.canvas_right, image=self.crown_img, bg=bg_color)
            self.crown_label.pack()
            self.crown_label.place(x=self.name_label.winfo_width(), y=10)

        if users_list[current_user].name == self.name.get():
            self.edit_img_load = Image.open('../images/icons/edit.png').resize((20,20), Image.ANTIALIAS)
            self.edit_img = ImageTk.PhotoImage(self.edit_img_load)

            self.edit_bg = Label(self.canvas_left, image=self.edit_img, cursor='hand2')
            self.edit_bg.pack()
            self.edit_bg.place(x=0,y=0)
            self.edit_bg.image = self.edit_img
            self.edit_bg.bind('<Button-1>', lambda *args: self.change_img('fondo'))

            self.edit_profile_img = Label(self.canvas_left, image=self.edit_img, cursor='hand2')
            self.edit_profile_img.pack()
            self.edit_profile_img.place(relx=0.3,rely=0.3)
            self.edit_profile_img.image = self.edit_img
            self.edit_profile_img.bind('<Button-1>', lambda *args: self.change_img('foto'))

            self.edit_mail = Label(self.canvas_right, image=self.edit_img, bg=bg_color, cursor='hand2')
            self.edit_mail.pack()
            self.edit_mail.place(x=self.correo_label.winfo_width()+50, y=90)
            self.edit_mail.bind('<Button-1>', self.change_mail)

            self.edit_webpage = Label(self.canvas_right, image=self.edit_img, bg=bg_color, cursor='hand2')
            self.edit_webpage.pack()
            self.edit_webpage.place(x=self.webpage_label.winfo_width()+50, y=160)
            self.edit_webpage.bind('<Button-1>', self.change_page)


    def show_lista(self, *args):
        try:
            self.lista_root.deiconify()
            self.lista_root.lift()
            login.win_login.focus_force()
        except:
            self.lista_root = Toplevel()
            self.lista_apps = listaApps(self.lista_root)
            self.lista_root.focus_force()

    def change_img(self, this):
        global main
        global current_language
        global current_user
        global users_list
        global current_user
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
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
        except:
            print('No image')
        self.win.lift()
        main.kill()
        main = main_window(root, current_language, current_user)

    def change_mail(self, *args):
        new_email = simpledialog.askstring('Input','Introduzca el nuevo e-mail', parent=self.win)
        self.correo.set(new_email)
        self.correo_label.update()
        self.edit_mail.place(x=self.correo_label.winfo_width() + 50, y=90)
        users_list[current_user].mod_mail(new_email)

    def change_page(self, *args):
        new_page = simpledialog.askstring('Input','Introduzca la nueva pagina web', parent=self.win)
        self.webpage.set(new_page)
        self.webpage_label.update()
        self.edit_webpage.place(x=self.webpage_label.winfo_width() + 50, y=160)
        users_list[current_user].mod_page(new_page)


class listaApps:
    def __init__(self, root):
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

        self.lista_apps = [[],[]]

        # Dimensiones
        self.sc_width = root.winfo_screenwidth()
        self.sc_height = root.winfo_screenheight()
        self.width = self.sc_width * 60 / 100
        self.height = self.sc_height * 70 / 100
        root.geometry(
            '%dx%d+%d+%d' % (self.width, self.height, self.sc_width * 25 / 100, self.sc_height * 15 / 100))

        self.populate()


    def populate(self, *args):
        global profile_page
        first_lista = find_all(apps.get_list(), users_list[current_user].seller_id, 0, 0)
        last_lista = find_all(first_lista, 'Activo', 6, 0)
        if users_list[current_user].name == profile_page.name.get():
            self.__populate_aux(first_lista, 0)
            if users_list[current_user].name == profile_page.name.get():
                self.load_plus = Image.open('../images/icons/plus.png').resize((25, 25), Image.ANTIALIAS)
                self.plus_img = ImageTk.PhotoImage(self.load_plus)
                self.plus = Label(self.frame, image=self.plus_img, bg=bg_color, cursor='hand2')
                self.plus.grid(row=len(first_lista)*2, column=0, columnspan=5)
                self.plus.bind('<Button-1>', lambda event: self.create_edit_win([]))
        else:
            self.__populate_aux(last_lista, 0)



    def __populate_aux(self, lista, cont):
        global profile_page
        if cont == len(lista):
            return
        else:
            self.lista_apps[0] = self.lista_apps[0] + ['']
            self.img_path = lista[cont][7]
            self.img_load = Image.open(self.img_path).resize((200,100),Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img_load)
            self.lista_apps[0][cont] = Label(self.frame, image=self.img, bg=bg_color)
            self.lista_apps[0][cont].grid(row=cont*2, column=0, rowspan=2)
            self.lista_apps[0][cont].image = self.img

            self.app_name = Label(self.frame, text=lista[cont][2], font='Times 20',
                                  bg=bg_color).grid(row=cont*2, column=1)
            self.app_cost = Label(self.frame, text=lista[cont][5], font='Times 20',
                                  bg=bg_color).grid(row=cont*2, column=2)
            if current_language == 'esp':
                self.app_downloads = Label(self.frame, text='Descargas: ' + lista[cont][11],
                                           font='Times 20', bg=bg_color).grid(row=cont*2 + 1, column=1)
                self.app_categoria = Label(self.frame, text='Categoria: '+lista[cont][3],
                                           font='Times 20', bg=bg_color).grid(row=cont*2 + 1, column=2)
            else:
                self.app_downloads = Label(self.frame, text='Downloads: ' + lista[cont][11],
                                           font='Times 20', bg=bg_color).grid(row=cont * 2 + 1, column=1)
                self.app_categoria = Label(self.frame, text='Category: ' + lista[cont][3],
                                           font='Times 20', bg=bg_color).grid(row=cont * 2 + 1, column=2)
            if users_list[current_user].name == profile_page.name.get():
                if lista[cont][5] == 'Free':
                    if current_language == 'esp':
                        self.app_gain = Label(self.frame, text='Ganancia: 0', font='Times 20',
                                              bg=bg_color).grid(row=cont*2, column=3)
                    else:
                        self.app_gain = Label(self.frame, text='Earnings: 0', font='Times 20',
                                              bg=bg_color).grid(row=cont * 2, column=3)
                else:
                    if current_language == 'esp':
                        self.app_gain = Label(self.frame, text='Ganancia: %s%d'%(lista[cont][5][0],
                                                                            int(lista[cont][5][1:])*int(lista[cont][11]))
                                              , font='Times 20', bg=bg_color).grid(row=cont * 2, column=3)
                    else:
                        self.app_gain = Label(self.frame, text='Earnings: %s%d' % (lista[cont][5][0],
                                                                                   int(lista[cont][5][1:]) * int(
                                                                                       lista[cont][11]))
                                              , font='Times 20', bg=bg_color).grid(row=cont * 2, column=3)
                self.frame.update()
                if lista[cont][6] == 'Activo':
                    self.app_estado = Canvas(self.frame, bg='green', height=50,
                                             width=200).grid(row=cont*2 + 1, column=3)
                else:
                    self.app_estado = Canvas(self.frame, bg='red', height=50,
                                             width=200).grid(row=cont * 2 + 1, column=3)

                self.lista_apps[1] = self.lista_apps[1] + ['erase']
                self.load_edit_img = Image.open('../images/icons/edit.png').resize((40,80), Image.ANTIALIAS)
                self.edit_img = ImageTk.PhotoImage(self.load_edit_img)
                self.lista_apps[1][cont] = Label(self.frame, image=self.edit_img, bg=bg_color, cursor='hand2')
                self.lista_apps[1][cont].grid(row=cont*2, column=4, rowspan=2)
                self.lista_apps[1][cont].image = self.edit_img
                self.lista_apps[1][cont].bind('<Button-1>', lambda event: self.create_edit_win(lista[cont]))

        self.__populate_aux(lista, cont + 1)

    def create_edit_win(self, info):
        if info != []:
            new_edit = editApp()
            new_edit.edit_config(info)
        else:
            new_edit = editApp()

    def onFrameConfigure(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class editApp:
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

        self.variable_categoria = StringVar(self.win)
        self.variable_categoria.set('Seleccionar')

        self.icon_label = Label(self.frame, image=self.icon, cursor='hand2')
        self.icon_label.grid(row=0, column=0, rowspan=2)
        self.app_name = StringVar()
        self.app_name.set('Nombre de la app')
        self.name_entry = Entry(self.frame, textvariable=self.app_name)
        self.name_entry.grid(row=0, column=1)
        self.app_cost = StringVar()
        self.app_cost.set('$'+'0')
        if current_language == 'esp':
            self.cost_label = Label(self.frame, text='Precio:', font='Times 20').grid(row=0, column=2)
            self.descr_label = Label(self.frame, text='Descripcion:', font='Times 20').grid(row=1, column=1)
            self.categoria_label = Label(self.frame, text='Categoria:', font='Times 20').grid(row=1, column=2)
        else:
            self.cost_label = Label(self.frame, text='Price:', font='Times 20').grid(row=0, column=2)
            self.descr_label = Label(self.frame, text='Description:', font='Times 20').grid(row=1, column=1)
            self.categoria_label = Label(self.frame, text='Category:', font='Times 20').grid(row=1, column=2)

        self.categoria_entry = OptionMenu(self.frame, self.variable_categoria, 'Juegos', 'Musica', 'Redes',
                                     'Herramientas')
        self.cost_entry = Entry(self.frame, textvariable=self.app_cost)
        self.cost_entry.grid(row=0, column=3)
        self.descr_variable = StringVar()
        self.categoria_entry.grid(row=1, column=3)
        self.descr_entry = Text(self.frame, height=5)
        self.descr_entry.grid(row=2, column=0, columnspan=4, rowspan=2)
        self.sc1_label = Label(self.frame, image=self.sc1, cursor='hand2')
        self.sc1_label.grid(row=4,column=0, columnspan=2)
        self.sc2_label = Label(self.frame, image=self.sc2, cursor='hand2')
        self.sc2_label.grid(row=4, column=2, columnspan=2)
        self.banner_label = Label(self.frame, image=self.banner, cursor='hand2')
        self.banner_label.grid(row=5, column=0, columnspan=4)
        self.icon_label.bind('<Button-1>', self.change_icon)
        self.sc1_label.bind('<Button-1>', self.change_sc1)
        self.sc2_label.bind('<Button-1>', self.change_sc2)
        self.banner_label.bind('<Button-1>', self.change_banner)

        if current_language == 'esp':
            self.ready = Button(self.frame, text='Listo', command=lambda: self.send(self.name_entry.get())).grid(row=6, column=1)
            self.cancel = Button(self.frame, text='Cancelar')
        else:
            self.ready = Button(self.frame, text='Ready', command=lambda: self.send(self.name_entry.get())).grid(row=6,
                                                                                                                 column=1)
            self.cancel = Button(self.frame, text='Cancel', command=self.win.destroy)
        self.cancel.grid(row=6, column=2)

    def change_icon(self, *args):
        print('a')
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((100, 100), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.icon_label.config(image=new_img)
            self.icon_label.image = new_img
        except:
            print('No image')
        self.win.lift()

    def change_sc1(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((300, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.sc1_label.config(image=new_img)
            self.sc1_label.image = new_img
        except:
            print('No image')
        self.win.lift()

    def change_sc2(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((300, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.sc2_label.config(image=new_img)
            self.sc2_label.image = new_img
        except:
            print('No image')
        self.win.lift()

    def change_banner(self, *args):
        self.win.lower()
        self.img_path = fd.askopenfilename()
        try:
            load_new_img = Image.open(self.img_path).resize((600, 200), Image.ANTIALIAS)
            new_img = ImageTk.PhotoImage(load_new_img)
            self.banner_label.config(image=new_img)
            self.banner_label.image = new_img
        except:
            print('No image')
        self.win.lift()

    def edit_config(self, info):
        self.app_name.set(info[2])
        self.app_cost.set(info[5])
        self.descr_entry.insert('1.0', info[4])
        self.variable_categoria.set(info[3])

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

    def send(self, name):
        global users_list
        if self.name_entry.get().lstrip() != '' and self.name_entry.get().lstrip() != 'Nombre de la app' and self.variable_categoria.get() != 'Seleccionar' and self.cost_entry.get().lstrip() != '':
            num_row_to_update = is_in(apps.get_list(), name, 0, 0)[1]
            row_to_update = is_in(apps.get_list(), name, 0, 0)[0]
            if row_to_update:
                new_entry = [users_list[current_user].seller_id, row_to_update[1], self.name_entry.get(),
                             self.variable_categoria.get(), self.descr_entry.get('1.0', 'end-1c'), self.cost_entry.get(),
                             'Activo', self.icon_path, self.banner_path, self.sc1_path, self.sc2_path, '0', '0']
                apps.update(num_row_to_update, new_entry)
            else:
                new_entry = [users_list[current_user].seller_id, str(int(apps.get_list()[len(apps.get_list())-1][1])+1), self.name_entry.get(),
                             self.variable_categoria.get(), self.descr_entry.get('1.0', 'end-1c'), self.cost_entry.get(),
                             'Activo', self.icon_path, self.banner_path, self.sc1_path, self.sc2_path, '0', '0']
                apps.add(new_entry)
            self.win.destroy()
        else:
            print('Faltan espacios')


class appWindow():
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

        self.cost_label = Label(self.frame, text=info[5])
        self.cost_label.grid(row=1, column=1)

        self.categoria_label = Label(self.frame, text=info[3])
        self.categoria_label.grid(row=2, column=1)

        self.owner_seller_info = sellers.is_in(info[0], 0, 0)

        self.owner_user_info = users.is_in(self.owner_seller_info[1], 0, 0)

        if self.owner_user_info:
            print(self.owner_user_info)
            self.owner_img_path = self.owner_user_info[3]
        else:
            self.owner_img_path = '../users/guest.png'
        self.load_owner_img = Image.open(self.owner_img_path).resize((100,75), Image.ANTIALIAS)
        self.owner_img = ImageTk.PhotoImage(self.load_owner_img)
        self.owner_img_label = Label(self.frame, image=self.owner_img, cursor='hand2')
        self.owner_img_label.grid(row=0, rowspan=2, column=3)


        if current_language == 'esp':
            self.owner = Label(self.frame, text='Hecho por: %s' % self.owner_seller_info[1], cursor='hand2')
            self.buy_button = Button(self.frame, text='Comprar', command=self.buy_app)
        else:
            self.owner = Label(self.frame, text='Made by: %s' % self.owner_seller_info[1], cursor='hand2')
            self.buy_button = Button(self.frame, text='Buy', command=self.buy_app)

        self.owner.grid(row=2, column=3)
        self.buy_button.grid(row=1, column=2)

        self.owner_img_label.bind('<Button-1>', lambda event: self.show_profPage(self.owner_seller_info[1]))
        self.owner.bind('<Button-1>', lambda event: self.show_profPage(self.owner_seller_info[1]))

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


    def buy_app(self):
        global apps
        global current_user
        apps.mod(int(self.id), 11, str(int(apps.list[int(self.id)][11])+1))
        if current_user != -1:
            if users_list[current_user].country == 'Costa Rica':
                apps.mod(int(self.id), 12, str(int(apps.list[int(self.id)][12]) + 1))
        else:
            print('Registrese')

    def show_profPage(self, username):
        if self.owner_user_info:
            global  profile_page
            user_info = users.is_in(username, 0, 0)
            profile_page = profPage(users_list[int(self.owner_user_info[8])])
            self.win.destroy()
        else:
            print('No hay pagina registrada')

class app:
    def __init__(self, master, row, column,info, width, height):
        self.icon_path = info[7]
        self.load_icon = Image.open(self.icon_path).resize((int(width), int(height)), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(master, image=self.icon_img, cursor='hand2')
        self.icon_label.grid(row=row, column=column)
        self.icon_label.image = self.icon_img
        self.icon_label.bind('<Button-1>', lambda event: appWindow(info))

class juegos:
    def __init__(self, master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                               bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/juegos.png').resize((100,100), Image.ANTIALIAS)
        self.icon_img = ImageTk.PhotoImage(self.load_icon)
        self.icon_label = Label(self.canvas, image=self.icon_img, bg=bg_color)
        self.icon_label.pack()
        self.icon_label.place(x=0,y=self.height*3/100)
        self.icon_label.image = self.icon_img

        if current_language == 'esp':
            self.title = Label(self.canvas, text='Juegos', bg=bg_color, font='Times 17')
        else:
            self.title = Label(self.canvas, text='Games', bg=bg_color, font='Times 17')
        self.title.pack()
        self.title.place(x=25,y=self.height*15/100)
        self.random()

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
            app1_banner_label.bind('<Button-1>', lambda event:appWindow(app1))

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event:appWindow(app2))


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
            app1_banner_label.bind('<Button-1>', lambda event: appWindow(app1))

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event: appWindow(app2))


class musica:
    def __init__(self, master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                               bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/music.png').resize((100, 100), Image.ANTIALIAS)
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
            app1_banner_label.bind('<Button-1>', lambda event: appWindow(app1))

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event: appWindow(app2))


class redes:
    def __init__(self, master, ini_y, fix, com_height, cont):
        self.canvas = Canvas(master, width=500, height=com_height, bg=bg_color,
                              bd=0, highlightthickness=0, relief='ridge')
        self.width = self.canvas.winfo_screenwidth()
        self.height = self.canvas.winfo_screenheight()
        self.canvas.pack()
        self.canvas.place(x=10 * win_width / 100, y=ini_y + fix * cont)

        self.load_icon = Image.open('../images/icons/social.png').resize((90, 100), Image.ANTIALIAS)
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
            app1_banner_label.bind('<Button-1>', lambda event: appWindow(app1))

            app2_load_banner = Image.open('%s' % app2[8].lstrip()).resize((200, 200), Image.ANTIALIAS)
            app2_banner = ImageTk.PhotoImage(app2_load_banner)
            app2_banner_label = Label(subcanvas2, image=app2_banner, cursor='hand2')
            app2_banner_label.pack()
            app2_banner_label.place(x=0, y=0)
            app2_banner_label.image = app2_banner
            app2_banner_label.bind('<Button-1>', lambda event: appWindow(app2))


class appTable:
    def __init__(self):
        self.file = '../apps/apps.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()
        self.musica = self.list_categoria('Musica', 0)
        self.juegos = self.list_categoria('Juegos', 0)
        self.herramientas = self.list_categoria('Herramientas', 0)
        self.redes = self.list_categoria('Redes', 0)

    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

    def get_list(self):
        return self.list[1:]

    def get_headers(self):
        return self.list[:1]

    def get_musica(self):
        return self.musica

    def get_juegos(self):
        return self.juegos

    def get_herramientas(self):
        return self.herramientas

    def get_redes(self):
        return self.redes

    def list_categoria(self, categ, row):
        column_categoria = 3
        if row == len(self.list):
            return []
        elif self.list[row][column_categoria].lstrip() == categ:
            return [self.list[row]] + self.list_categoria(categ, row+1)
        else:
            return [] + self.list_categoria(categ, row+1)

    def add(self, lista):
        global apps
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            print(lista)
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            apps = appTable()
        else:
            print('Faltan columnas')

    def update(self, row, lista):
        global apps
        if len(lista) == len(self.list[0]):
            self.list[row+1] = lista
            open_temp_file = open(self.file, 'w')
            create_db(self.list, open_temp_file)
            close_temp_file = open_temp_file.close()
            apps = appTable()
        else:
            print(lista)
            print(len(lista[0]))
            print(len(self.list[0]))

    def mod(self, row, column, ele):
        global apps
        open_temp_file = open(self.file, 'w')
        self.list[int(row)][int(column)] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()
        apps = appTable()

class buyersTable:
    def __init__(self):
        self.file = '../users/compradores.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

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

    def add(self, lista):
        global buyers
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            buyers = buyersTable
        else:
            print('Faltan columnas')

    def mod(self, row, column, ele):
        open_temp_file = open(self.file, 'w')
        self.list[int(row)][int(column)] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()



class sellersTable:
    def __init__(self):
        self.file = '../users/vendedores.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()
        print(self.list)

    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a.lstrip().rstrip('\n')] + self.__to_list(cont + 1)

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

    def raw_table(self):
        open_temp_file = open(self.file, 'r')
        table = self.__raw_table_aux(open_temp_file)
        close_temp_file = open_temp_file.close()
        return table

    def __raw_table_aux(self, file):
        row = file.readline()
        if row == '':
            return []
        else:
            return [row[:len(row)-2]] + self.__raw_table_aux(file)

    def get_list(self):
        return self.list[1:]

    def add(self, lista):
        global sellers
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            sellers = sellersTable()
        else:
            print('Faltan columnas')

    def mod(self, row, column, ele):
        open_temp_file = open(self.file, 'w')
        self.list[int(row)][int(column)] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()

    def remove(self, row):
        global sellers
        self.list = self.remove_aux(row, 0, False)
        open_temp_file = open(self.file, 'w')
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()
        sellers = sellersTable()


    def remove_aux(self, row, cont, deleted):
        if cont == len(self.list):
            return []
        elif row == cont:
            return self.remove_aux(row, cont + 1, True)
        else:
            if deleted:
                self.list[cont][0] = str(int(self.list[cont][0])-1)
                return [self.list[cont]] + self.remove_aux(row, cont + 1, deleted)
            else:
                return [self.list[cont]] + self.remove_aux(row, cont+1, deleted)


class manageWinVendedores:
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
        self.load_plus = Image.open('../images/icons/plus.png').resize((20, 20), Image.ANTIALIAS)
        self.plus_img = ImageTk.PhotoImage(self.load_plus)
        self.plus = Label(self.frame, image=self.plus_img, bg=bg_color, cursor='hand2')
        self.plus.grid(row=len(self.buttons)+1, column=0, columnspan=5)
        self.plus.bind('<Button-1>', lambda event: self.add_seller())

        self.load_hamb_icon = Image.open('../images/icons/hamburguer_icon.png').resize((30, 30), Image.ANTIALIAS)

        self.hamb_icon = ImageTk.PhotoImage(self.load_hamb_icon)
        self.hamb_icon_label = Label(root, image=self.hamb_icon, bd=0, highlightthickness=0, relief='ridge',
                                     bg=bg_color, cursor='hand2')
        self.hamb_icon_label.pack()
        self.hamb_icon_label.place(x=1, y=1)

        self.hamb_icon_label.bind('<Button-1>', self.show_menu)


    def table(self, *args):
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
            load_erase_img = Image.open('../images/icons/red_cross.png').resize((10,10), Image.ANTIALIAS)
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


    def onFrameConfigure(self, *args):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def erase(self, row):
        global new_manage_window
        sellers.remove(row+1)
        self.root.destroy()
        new_manage_window = manageWinVendedores(Toplevel())

    def show_menu(self, event):
        global menu
        menu = newMenu(self.root)

    def add_seller(self):
        self.add_seller_aux()

    def add_seller_aux(self):
        def send():
            if name_entry.get() != '' and mail_entry.get() != '' and page_entry.get() != '':
                global new_manage_window
                sellers.add([str(int(sellers.get_list()[len(sellers.get_list())-1][0])+1), name_entry.get(),
                             mail_entry.get(), page_entry.get()])
                self.root.destroy()
                new_manage_window = manageWinVendedores(Toplevel())

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

        ready = Button(main_frame, text='Listo', command=send)
        cancel = Button(main_frame, text='Cancelar')
        ready.grid(row=3, column=0, sticky=E)
        cancel.grid(row=3, column=1, sticky=W)




class usersTable():
    def __init__(self):
        self.file = '../users/usuarios.txt'
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)

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

    def add(self, lista):
        global users
        if len(lista) == len(self.list[0]):
            open_temp_file = open(self.file, 'w')
            create_db(self.list + [lista], open_temp_file)
            close_temp_file = open_temp_file.close()
            users = usersTable()
        else:
            print('Faltan columnas')

    def mod(self, row, column, ele):
        global users
        open_temp_file = open(self.file, 'w')
        self.list[row][column] = ele
        create_db(self.list, open_temp_file)
        close_temp_file = open_temp_file.close()


class quoteTable:
    def __init__(self, file):
        self.file = file
        self.first_read = open(self.file)
        self.raw_list = self.__to_list(0)
        self.list = normalize_list_table(self.raw_list, 0)
        self.close_first_read = self.first_read.close()

    def __to_list(self, cont):
        a = self.first_read.readline()
        if a == '':
            return []
        else:
            return [a] + self.__to_list(cont + 1)


    def get_quote(self):
        quote_number = str(randint(1,20))
        return self.is_in(quote_number, 0, 0)

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


class newUser:
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


    def __verify(self):
        if buyers.is_in(self.name, 0, 0) or sellers.is_in(self.name, 0, 0):
            self.__retrieve_info(self.name, buyers.is_in(self.name, 0, 0), sellers.is_in(self.name, 0, 0))
            return True
        else:
            return False

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

    def mod_mail(self, tothis):
        global buyers
        global sellers

        self.mail = tothis
        buyers.mod(self.buyer_id, 2, tothis)
        sellers.mod(self.seller_id, 2, tothis)

    def mod_page(self, tothis):
        global sellers

        self.webpage = tothis
        sellers.mod(self.seller_id, 3, tothis)

    def mod_buys(self, tothis):
        global buyers

        self.buys = tothis
        buyers.mod(self.seller_id, 3, tothis)


def show_register(*args):
    try:
        register.win_register.deiconify()
        register.win_register.lift()
        register.win_register.focus_force()
    except:
        register.win_register.withdraw()
        register.win_register.focus_force()


def logout(*args):
    global current_user
    global main
    global current_language
    current_user = -1
    main.kill()
    menu.destroy()
    main = main_window(root, current_language, current_user)


def create_user(name, username, password, seller_id, buyer_id, mail, webpage, perfil, fondo, buys, admin,
                country, language, id):
    global users_list
    next_i = len(users_list)
    users_list = users_list + ['delete me']
    users_list[next_i] = newUser(name, username, password, seller_id, buyer_id, mail, webpage, perfil, fondo, buys,
                                 admin, country, language, id)


def users_list_first_config(cont):
    if cont == len(users.list):
        return
    else:
        create_user(users.list[cont][0], users.list[cont][1], users.list[cont][2], 'None', 'None', 'None', 'None',
                    users.list[cont][3], users.list[cont][4], '0', users.list[cont][5],
                    users.list[cont][6], users.list[cont][7], str(cont))
        users_list_first_config(cont+1)

profile_page=''

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

menu = Label(root)

apps = appTable()
buyers = buyersTable()
sellers = sellersTable()
users = usersTable()
users_list_first_config(1)
esp_quotes = quoteTable('../misc/quotes/esp.txt')
eng_quotes = quoteTable('../misc/quotes/eng.txt')


main = main_window(root, current_language, current_user)
login = newLogin(root)
register = newRegister(root)
adminwin = adminWindow()
search = searchWin()

new_manage_window = Toplevel()
new_manage_window.withdraw()

adminwin.win.withdraw()
login.win_login.withdraw()
register.win_register.withdraw()
search.win.withdraw()


mainloop()