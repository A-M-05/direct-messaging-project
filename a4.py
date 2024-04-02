import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import time
from ds_messenger import DirectMessenger, DirectMessage
import ds_client
import ds_protocol
import DataStorage


SERVER = "168.235.86.101"
PORT = 3021

class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        temp = self.message_editor.get('1.0', 'end').rstrip()
        return temp

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview",
                             background="AntiqueWhite3",
                             foreground="Black",
                             bordercolor='AntiqueWhite1')
        self.style.configure('Treeview.Heading',
                             background='AntiqueWhite3',
                             foreground='Black',
                             borderwidth=5,
                             bordercolor='Black')
        self.style.map('Treeview.Heading',
                       background=[('selected', '!focus', 'Black')])

        self.posts_tree = ttk.Treeview(posts_frame, height = 4)
        self.posts_tree.heading('#0', text = 'Contacts')
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH,
                             side=tk.TOP,
                             expand=True,
                             padx=5,
                             pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH,
                         side=tk.TOP,
                         expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="AntiqueWhite2", bd = 5)
        editor_frame.pack(fill=tk.BOTH,
                          side=tk.LEFT,
                          expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="AntiqueWhite2", width=5)
        scroll_frame.pack(fill=tk.BOTH,
                          side=tk.LEFT,
                          expand=False)

        message_frame = tk.Frame(master=self,
                                 bg="AntiqueWhite2",
                                 bd = 5)
        message_frame.pack(fill=tk.BOTH,
                           side=tk.TOP,
                           expand=False)

        self.message_editor = tk.Text(message_frame,
                                      width=0,
                                      height=2,
                                      bg = 'AntiqueWhite4',
                                      font = ('Helvetica', 20),
                                      borderwidth = 2)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True,
                                 padx=0,
                                 pady=0)

        self.entry_editor = tk.Text(editor_frame,
                                    width=0,
                                    height=8,
                                    bg = 'AntiqueWhite4',
                                    font = ('Helvetica', 20))
        self.entry_editor.tag_configure('entry-right',
                                        justify='right',
                                        foreground = 'white',
                                        spacing2 = 4)
        self.entry_editor.tag_configure('entry-left',
                                        justify='left',
                                        foreground = 'black',
                                        background = "white",
                                        spacing2 = 4)
        self.entry_editor.pack(fill=tk.BOTH,
                               side=tk.LEFT,
                               expand=True,
                               padx=0,
                               pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y,
                                    side=tk.LEFT,
                                    expand=False,
                                    padx=0,
                                    pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command = self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH,
                         side=tk.RIGHT,
                         padx=5,
                         pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH,
                               side=tk.LEFT,
                               padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame,
                                     width=30,
                                     text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame,
                                     width=30,
                                     bg = 'AntiqueWhite1',
                                     fg = 'black',
                                     insertbackground= 'black')
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame,
                                       width=30,
                                       text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame,
                                       width=30,
                                       bg = 'AntiqueWhite1',
                                       fg = 'black',
                                       insertbackground = 'black')
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        #self.password...

        self.password_label = tk.Label(frame,
                                       width=30,
                                       text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame,
                                       width = 30,
                                       bg = 'AntiqueWhite1',
                                       fg = 'black',
                                       insertbackground= 'black')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry['show'] = '*'
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.data_storage = DataStorage.DataStorage()
        self.all_contacts = set()
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!

        self.direct_messenger = DirectMessenger()

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def send_message(self):
        # You must implement this!
        if self.direct_messenger.token is None:
            messagebox.showinfo("ALERT", "No token given by server!")
        else:
            recipient = self.recipient

            d_m = DirectMessage(message = str(self.body.get_text_entry()),
                            recipient = str(recipient),
                            timestamp = str(time.time()),
                            sender = str(self.username))
            temp = self.direct_messenger.send(d_m)
            if temp:
                self.body.insert_user_message(str(self.body.get_text_entry()))
                self.body.set_text_entry("")
                self.data_storage.add_dm(d_m)
            else:
                messagebox.showinfo("ALERT", "Message was not sent!")


    def add_contact(self):
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        new_contact = tk.simpledialog.askstring("New Contact", "Enter contact name: ")
        self.body.insert_contact(new_contact)
        self.all_contacts.add(new_contact)

    def recipient_selected(self, recipient):
        self.recipient = recipient

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username,
                              self.password,
                              self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

        profile_path = Path.cwd()/Path(f'{self.username}.dsu')
        if profile_path.exists():
            try:
                self.data_storage.load_profile(profile_path)
            except:
                pass
        else:
            Path.touch(profile_path)

        self.data_storage.dsuserver = self.server
        self.data_storage.username = self.username
        self.data_storage.password = self.password
        self.path = profile_path

        self.direct_messenger.dsuserver = self.server
        self.direct_messenger.username = self.username
        self.direct_messenger.password = self.password

        self.display_messages()

    def join_server(self):
        try:
            response = ds_client.send(self.direct_messenger.dsuserver,
                                      PORT,
                                      self.direct_messenger.username,
                                      self.direct_messenger.password,
                                      message = "join")
        except:
            messagebox.showerror("ERROR", "Could not join server.")

        data_tuple = ds_protocol.extract_json(response)

        if data_tuple[0] == "error":
            messagebox.showerror("ERROR", data_tuple[1])
        elif data_tuple[0] == "ok":
            self.user_token = data_tuple[2]
            self.direct_messenger.token = self.user_token

    def check_new(self):
        # You must implement this!

        if self.direct_messenger.token is None:
            self.after(1000, self.check_new)
        else:
            new_dms = self.direct_messenger.retrieve_new()
            for d_m in new_dms:
                self.data_storage.add_dm(d_m)

            self.display_messages()
            self.after(1000, self.check_new)

    def display_messages(self):
        temp = []
        for recipient in self.data_storage.dm_dictionary.values():
                for dm in recipient:
                    if dm.get_recipient() != self.username and not dm.get_recipient() in self.all_contacts:
                        self.body.insert_contact(dm.get_recipient())
                        self.all_contacts.add(dm.get_recipient())
                    elif dm.get_recipient() == self.username and not dm.get_sender() in self.all_contacts:
                        self.body.insert_contact(dm.get_sender())
                        self.all_contacts.add(dm.get_sender())

                    if dm.get_recipient() == self.recipient or dm.get_sender() == self.recipient:
                        temp.append(dm)
        temp.sort(key = lambda x: x.timestamp)

        self.body.entry_editor.delete(1.0, tk.END)

        for d_m in temp:
            if d_m.get_recipient() == self.recipient:
                self.body.insert_user_message(d_m.get_message())
            else:
                self.body.insert_contact_message(d_m.get_message())
        
        self.after(1000, self.display_messages)

    def save(self):
        try:
            self.data_storage.convert_dms_to_tuples()
            self.data_storage.save_profile(self.path)
        except:
            pass

    def save_and_quit(self):
        try:
            self.save()
        except:
            pass
        finally:
            self.root.destroy()

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Save', command = self.save)
        menu_file.add_command(label='Close', command = self.save_and_quit)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        settings_file.add_command(label = 'Join DS Server', command = self.join_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def main():
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.after(1000, app.check_new)

    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.protocol("WM_DELETE_WINDOW", app.save_and_quit)
    main.mainloop()

main()
