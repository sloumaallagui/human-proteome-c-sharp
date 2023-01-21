import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
import tkinter.scrolledtext as scrolledtext



def read_words(file_name):
    file = open(file_name, 'r')
    words = []
    for line in file:
        line = line.strip()
        if len(line) > 3:
            words.append(line.upper())
    return words

def read_sequences(file_name):
        file = open(file_name, 'r')
        sequences = {}
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                key = line.split('|')[1]
            elif key not in sequences:
                sequences[key] = line
            else:
                sequences[key] = sequences[key] + line
        return sequences


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Mini projet BI')
        self.geometry('450x650')
        self.resizable(False, False)
        self.configure(background='white')
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.Label = ttk.Label(self, text='choisir un fichier fasta et un fichier de mots')
        self.open_fasta_button = ttk.Button(self, text='Ouvrir le fichier fasta ', command=self.open_fasta_file)
        self.open_fasta_button.config(width=25)
        self.open_fasta_button.pack()

        self.open_words_button = ttk.Button(self, text='Ouvrir le fichier des mots', command=self.open_words_file)
        self.open_words_button.config(width=25)
        self.open_words_button.pack()

        self.start_button = ttk.Button(self, text='Commencer', command=self.start)
        self.start_button.config(width=25)
        self.start_button.pack()

        self.label_number_words= ttk.Label(self, text='Nombre des mots :')
        self.label_number_words.config(background='white')
        self.label_number_words.pack()

        self.label_number_occurence_per_seq = ttk.Label(self, text='Nombre d\'occurence de chaque mot dans les sequences')
        self.label_number_occurence_per_seq.configure(background='white')
        self.label_number_occurence_per_seq.pack()

        self.text_nb_occurence = scrolledtext.ScrolledText(self, height=10, width=50)
        self.text_nb_occurence.pack()

        self.label_number_occurence_per_words = ttk.Label(self, text='Nombre d\'occurence de chaque mot par sequence')
        self.label_number_occurence_per_words.configure(background='white')
        self.label_number_occurence_per_words.pack()

        self.text_nb_occurence_per_sequence = scrolledtext.ScrolledText(self, height=10, width=50)
        self.text_nb_occurence_per_sequence.pack()

        self.label_most_frequent = ttk.Label(self, text='Mot le plus frequent')
        self.label_most_frequent.configure(background='white')
        self.label_most_frequent.pack()

        self.text_most_frequent = scrolledtext.ScrolledText(self, height=5, width=50)
        self.text_most_frequent.pack()

        self.label_space = ttk.Label(self, text='')
        self.label_space.configure(background='white')
        self.label_space.pack()





        self.label_info = ttk.Label(self, text='')
        self.label_info.configure(background='white')
        self.label_info.pack()

        self.fasta_file_name = ''
        self.words_file_name = ''




    def open_fasta_file(self):
        self.text_nb_occurence.delete(0.0, tk.END)
        self.text_nb_occurence_per_sequence.delete( 0.0, tk.END)
        self.text_most_frequent.delete( 0.0, tk.END)
        self.fasta_file_name = filedialog.askopenfilename()
        self.label_info['text'] = 'Fichier  : ' + self.fasta_file_name

    def open_words_file(self):
        self.text_nb_occurence.delete(0.0, tk.END)
        self.text_nb_occurence_per_sequence.delete( 0.0, tk.END)
        self.text_most_frequent.delete( 0.0, tk.END)
        self.words_file_name = filedialog.askopenfilename()
        self.label_info['text'] = 'Fichier : ' + self.words_file_name

    def start(self):
        if self.fasta_file_name == '' or self.words_file_name == '':
            messagebox.showerror('Error', 'Entrer les fichier fasta et fichier des mots.')
            return
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        self.start_button.config(state='disabled')

        self.update()
        sequences = read_sequences(self.fasta_file_name)
        words = read_words(self.words_file_name)

        def find_occurrence_per_sequence(sequences, list_of_words):
            occurrence = {}
            for word in list_of_words:
                occurrence[word] = {}
                self.label_info['text'] = 'Mot en cours : ' + word
                self.update()
                for key in sequences:
                    occurrence[word+key] = sequences[key].count(word)
                    if(str(occurrence[word+key]) != "0"):
                        self.text_nb_occurence_per_sequence.insert('end', word + ' found in ' + key + ' : '+ str(occurrence[word+key])  + ' times per sequence \n ')
            return occurrence

        def find_occurrence(sequences, list_of_words):
            occurrence = {}
            self.label_number_words['text'] = 'Nombre des mots : ' + str(len(list_of_words))
            i = 0
            for word in list_of_words:
                occurrence[word] = 0

                self.update()
                
                for key in sequences:
                    i = i + 1
                    occurrence[word] = occurrence[word] + sequences[key].count(word)
                if(str(occurrence[word])!= '0'):
                        self.text_nb_occurence.insert('end', word  + ' found in ' + str(occurrence[word])  + ' sequences \n')    
                self.label_info['text'] = 'Nombre de sequence lue : ' + str(i)
                    
                
            return occurrence

        def find_most_frequent(occurrence):
            max_value = 0
            i = 0
            max_key = ''
            for key in occurrence:



                if occurrence[key] > max_value:
                    max_value = occurrence[key]
                    max_key = key
                    max_percent = max_value / sum(occurrence.values()) * 100
            return (max_key, max_value ,max_percent)

        occurrence = find_occurrence(sequences, words)
        find_occurrence_per_sequence(sequences, words)
        self.update()
        max_key, max_value, max_percent = find_most_frequent(occurrence)
        self.text_most_frequent.insert('end', 'La plus frequent mot est : ' + max_key + ' \n apparait : ' + str(max_value) + " fois \n avec percentage de "+ str(float("{:.2}".format(max_percent))) + ' %')

        self.update()
        self.start_button.config(state='normal')




if __name__ == '__main__':
    app = App()
    app.mainloop()







