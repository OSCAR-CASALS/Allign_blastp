import os
import tkinter as tk
from tkinter import filedialog
from Functions import Explore_alignment
from functools import partial

class MyApp():
    def __init__(self):
        #Temporal file that will be deleted once the aplication is closed
        os.system('mkdir TEMPORAL_FILE')
        #Variables that must be set at the begining
        self.file_1 = ''
        self.database = ''
        #Create window
        self.root = tk.Tk()
        self.root.title('Blast result observer')
        self.root.geometry('900x700')
        self.root.minsize(900, 700)
        self.root.maxsize(900, 700)
        #Main frame
        self.Frame = tk.Frame(self.root, bg = 'beige', width = 900, height = 700)
        self.Frame.pack(fill='both', expand = 1)
        #Text
        tk.Label(self.Frame, text = 'SIMPLE INTEFACE', font = 'Arial 40 bold', bg = 'beige', fg = 'orange').place(x = 180, y = 100)
        database_text = tk.Label(self.Frame, text='Select the sequences that your query will be alligned to', bg = 'beige', font = 'Arial 16').place(x = 60, y = 260)
        query_text = tk.Label(self.Frame, text = 'Query sequence', bg = 'beige', font = 'Arial 16').place(x = 390, y = 400)
        self.Err_message = tk.Label(self.Frame, text = 'Database or Query missing', fg = 'red', font = 'Arial 12 bold', bg = 'beige')
        #Buttons
        Database_button = tk.Button(self.Frame, text = 'Database', fg = 'red', width = 20, height = 2, command = self.Database_clicked, font = 'Arial 16')
        Database_button.place(x = 320, y = 300)
        File_button = tk.Button(self.Frame, text = 'Query', fg = 'red', width = 20, height = 2, command = self.Query_clicked, font = 'Arial 16')
        File_button.place(x=320, y = 440)

        Start_button = tk.Button(self.Frame, text='Continue', fg = 'black', width = 20, height = 2, font = 'Arial 20 bold', command = self.Continue_clicked)
        Start_button.place(x=260, y=600)
        #Text for selected options
        self.Database_selected = tk.Label(self.Frame, text='None selected', bg = 'white')
        self.Database_selected.place(x=640, y=340)
        self.Query_selected = tk.Label(self.Frame, text='None selected', bg = 'white')
        self.Query_selected.place(x=640, y=480)
        #main loop
        self.Err_message.place(x=1000,y=800)
        self.root.mainloop()
    
    def allign(self):
        print(self.file_1)
        os.system('mkdir TEMPORAL_FILE/Blast_database')
        os.system('makeblastdb -in ' + self.database + ' -out TEMPORAL_FILE/Blast_database/Dat -dbtype prot')
        self.al_obj = Explore_alignment(self.file_1, 'TEMPORAL_FILE/Blast_database/Dat', 'TEMPORAL_FILE/al.txt')

    def Database_clicked(self):
        self.database = filedialog.askopenfile(title='Select file', initialdir=os.getcwd()).name
        self.Database_selected.config(text=self.database.split('/')[-1])
        #Creating a blast database with the given fasta
        if 'Blast_database' in os.listdir('TEMPORAL_FILE'):
            os.system('rm -r TEMPORAL_FILE/Blast_database')

    def Query_clicked(self):
        self.file_1 = filedialog.askopenfile(title='Select file', initialdir=os.getcwd()).name
        self.Query_selected.config(text=self.file_1.split('/')[-1])
    
    def create_frame_for_res(self):
        self.star_res = 0
        self.end_res = 10
        self.Frame_2 = tk.Frame(self.root, bg = 'beige')
        tk.Button(self.Frame_2, text = 'back', command=self.back_clicked).place(x=10, y=10)
        tk.Button(self.Frame_2, text = 'Next', command=partial(self.Next_or_prev_clicked, 10)).place(x=800, y = 660)
        tk.Button(self.Frame_2, text = 'Previous', command=partial(self.Next_or_prev_clicked, -10)).place(x=10, y = 660)
        self.Frame_2.pack(fill='both', expand = 1)
        self.alligned_sequences = self.al_obj.extract_entries()
        n = 110
        tk.Label(self.Frame_2, text = 'qseqID', bg = 'red', fg = 'white').place(x=(n*0.6)-30, y = 180)
        tk.Label(self.Frame_2, text = 'sseqID', bg = 'red', fg = 'white').place(x=(n*2.6)-140, y = 180)
        tk.Label(self.Frame_2, text = 'qstart', bg = 'red', fg = 'white').place(x=(n*3.6)-140, y = 180)
        tk.Label(self.Frame_2, text = 'qend', bg = 'red', fg = 'white').place(x=(n*4.6)-140, y = 180)
        tk.Label(self.Frame_2, text = 'sstart', bg = 'red', fg = 'white').place(x=(n*5.6)-140, y = 180)
        tk.Label(self.Frame_2, text = 'ssend', bg = 'red', fg = 'white').place(x=(n*6.6)-140, y = 180)
        tk.Label(self.Frame_2, text = 'E-value', bg = 'red', fg = 'white').place(x=(n*7.6)-140, y = 180)
        tk.Label(self.Frame_2, text = 'Perc.Id', bg = 'red', fg = 'white').place(x=(n*8.6)-140, y = 180)
        self.res_frame = tk.Frame(self.Frame_2, width=900, height=360)
        self.res_frame.pack(padx=30, pady=200)
        self.display_res()
    
    def display_res(self):
        count = 0
        labels_res = []
        if self.star_res < 0:
            self.star_res = 0
            self.end_res = 10
        if self.end_res > len(self.alligned_sequences) or self.star_res > len(self.alligned_sequences):
            self.star_res = len(self.alligned_sequences) - 10
            self.end_res = len(self.alligned_sequences) 
        for i in range(self.star_res, self.end_res):
            seq = self.alligned_sequences[i]
            labels_res.append([tk.Label(self.res_frame, text = seq[0], bg = 'white'),
                               tk.Label(self.res_frame, text = seq[1], bg='white'),
                               tk.Label(self.res_frame, text = seq[2], bg='white'),
                               tk.Label(self.res_frame, text = seq[3], bg='white'),
                               tk.Label(self.res_frame, text = seq[4], bg='white'),
                               tk.Label(self.res_frame, text = seq[5], bg='white'),
                               tk.Label(self.res_frame, text = seq[6], bg='white'),
                               tk.Label(self.res_frame, text = seq[7], bg='white')])
            for number in range(0, 8):
                labels_res[count][number].place(x=((number+0.6)*110)-60, y = 20*(count + 0.6))
            count += 1

    def Continue_clicked(self):
        if self.database != '' and self.file_1 != '':
            self.Err_message.place(x=1000, y=800)
            self.Frame.pack_forget()
            self.allign()
            self.create_frame_for_res()
        else:
            self.Err_message.place(x=320, y=560)
    
    def back_clicked(self):
        self.Frame.pack(fill='both', expand = 1)
        self.Frame_2.destroy()

    def Next_or_prev_clicked(self, direction):
        self.star_res += direction
        self.end_res += direction
        self.res_frame.destroy()
        self.res_frame = tk.Frame(self.Frame_2, width=900, height=360)
        self.res_frame.pack(padx=30, pady=200)
        self.display_res()

myApp = MyApp()
#Removing temporal file
os.system('rm -r TEMPORAL_FILE')
        





