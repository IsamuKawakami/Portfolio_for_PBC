from tkinter import *
from tkinter import messagebox as msbox
from tkinter import ttk
from PIL import ImageTk, Image
import json
import random
import pandas as pd
import numpy as np



# To do list:
  # Quit button macro?
  # indice for questions (in order of apperance)
  # letter of options (a., b. c. d.)
  # function to show the answer key



#___________Config______________:

source_dt_file='Q_Bank.json'
fgr="DAMA-logoS.png"
title_font_colour="#003469"
letra="arial"
num_opt=4 #temporary definition of number of answer options...


global target
target=60
global x_pivot_com_btn
x_pivot_com_btn=385
global delta_x_pivot_com_btn
delta_x_pivot_com_btn=150
global y_pivot_com_btn
y_pivot_com_btn=525
global delta_y_pivot_com_btn
delta_y_pivot_com_btn=275


#_____________Creating a class to structure the app!:_________________
class Quiz_GI:
    def __init__(self):
       self.marked=[]
       self.ql=[]
       self.qn = 0
       self.ques = self.question(self.qn)
       self.opt_selected=IntVar()
       self.opts=self.radiobtns()
       self.show_options(self.qn)
       self.commands()
       self.correct_answer=0

    def question(self, qn):
        #t = Label(root, text="QUIZ Practice for the DAMA Certification", width=32, fg=title_font_colour, font=('Helvetica 15 underline'))
        #t = Label(root, text="QUIZ Practice for the DAMA Certification", width=32, fg=title_font_colour, font=(letra,20,"bold", "underline"))
        #t.place(x=250, y=35)
        global qun
        qun = Label(root, text=q[qn], width=50, font=(letra, 16, "bold"), anchor="w")
        qun.place(x=70, y=120)
        return qun

    def radiobtns(self):
        n=0
        b=[]
        yp=170
        
        while n < num_opt:
            global btn
            
            btn=Radiobutton(root, text=" ", cursor="hand2", justify="left", wraplength=830, indicatoron=1, variable=self.opt_selected, value=n+1, font=(letra, 14))
            btn.grid(row = n, column=0, columnspan = 2,padx=25,sticky=W,)
            b.append(btn)
            btn.place (x=100, y=yp)
            n += 1
            yp += 80
            
        return b    
    
    def show_options(self, qn):
        i=0
        index=["a) ","b) ","c) ","d) "]
        self.opt_selected.set(0)
        self.ques['text']="Q."+str(qn+1)+": "+q[qn]
        self.ql.append(self.ques['text'])
        for ops in op[qn]:
            self.opts[i]['text']=index[i]+ops
            i +=1

    
       
    def show_stats(self):
        score=int(self.correct_answer/len(q)*100)
        result_str="Score: " + str(score) + "%"
        wrg=len(q)-self.correct_answer
        result_cor="Number of correct answers: " + str(self.correct_answer)
        result_wrg="Number of missed answers: " + str(wrg)
        
        if score>=target:
            clrfg="green"
        else:
            clrfg="red"    
        
        clear_window()
          
        resulta = Label(root, text=result_str, width=50, font=(letra, 16, "bold"), fg=clrfg, anchor="w")
        resulta.place(x=70, y=120)

        resultb = Label(root, text=result_cor, width=50, font=(letra, 14, "bold"), anchor="w")
        resultb.place(x=100, y=170)

        resultc = Label(root, text=result_wrg, width=50, font=(letra, 14, "bold"), anchor="w")
        resultc.place(x=100, y=250)
       
        self.stats_screen_commands()
   
    def commands(self):
        nxtcommand=Button(root, text="Next", cursor="hand2", command=self.next_button_macro, width=10, bg="green", fg="white",font=(letra, 16,"bold"))
        nxtcommand.place(x=x_pivot_com_btn,y=y_pivot_com_btn)
        quitcommand=Button(root, text="Quit", cursor="hand2", command=root.destroy, width=10, bg="red", fg="white",font=(letra, 16,"bold"))
        quitcommand.place (x=x_pivot_com_btn + delta_x_pivot_com_btn, y=y_pivot_com_btn)

    def question_keys_commands(self):
        clscommand=Button(answer_key_window, text="Close", cursor="hand2", command=self.cls_button_macro, width=10, bg="red", fg="white",font=(letra, 16,"bold"))
        clscommand.place(x=385,y=525)

    def stats_screen_commands(self):
        # macro for the following button must be created!!!! - DONE!!!
        show_anskey_command=Button(root, text="Show Session Details", cursor="hand2", command=self.show_session_details_button_macro, width=21, bg="red", fg="white",font=(letra, 16,"bold"))
        show_anskey_command.place(x=x_pivot_com_btn,y=y_pivot_com_btn-(delta_y_pivot_com_btn/3))
        
        play_again_command=Button(root, text="Play Again", cursor="hand2", command=self.play_again_macro, width=10, bg="green", fg="white",font=(letra, 16,"bold"))
        play_again_command.place(x=x_pivot_com_btn,y=y_pivot_com_btn)
        
        quitcommand=Button(root, text="Quit", cursor="hand2", command=root.destroy, width=10, bg="red", fg="white",font=(letra, 16,"bold"))
        quitcommand.place (x=x_pivot_com_btn + delta_x_pivot_com_btn, y=y_pivot_com_btn)


    def check_answer(self, qn):
        if self.opt_selected.get()==gabarito[qn]:
             
           return True
        
    
    # Not using this function, may be deleted...
    def show_result(self):
        score=int(self.correct_answer/len(q)*100)
        result_str="Score: " + str(score) + "%"
        wrg=len(q)-self.correct_answer
        result_cor="Number of correct answers: " + str(self.correct_answer)
        result_wrg="Number of missed answers: " + str(wrg)
        msbox.showinfo("Your Results:", "\n".join([result_str,result_cor,result_wrg]))
        peta=msbox.askquestion("Thanks for Playing!","Would you like to play again?")
        if peta == 'no':
          root.destroy()
        else:
          peta=msbox.askquestion("Awesome!","Would you like to start a new session?")
          if peta=='no':
              quiz=Quiz_GI()
          else:
              Generate_Question_Session(df_q_bank)
              Generate_Content(df_q_bank)    
              quiz=Quiz_GI()
    
    def next_button_macro(self):
        if self.check_answer(self.qn):
            self.correct_answer +=1
            self.marked.append("correct")
        else:
            self.marked.append("incorrect")    
        self.qn +=1
        if self.qn==len(q):
           self.show_stats()
           #self.show_result()
        else:    
           self.show_options(self.qn) 

    def quit_button_macro(self):  #work here later and substitute on command for quit button.
        root.destroy       
    
    def cls_button_macro(self):  
        answer_key_window.destroy       
    
    
    #Work on this...
    def show_session_details_button_macro(self):
                
        dic_details = {'Question':self.ql,
        'Answer':anw,
        'Your Choice':self.marked,
        'DMBOK Chapter': ch,
        'DMBOK Page':pg}
        
        df_details = pd.DataFrame(dic_details)

        top=Toplevel(root)
        top.title=("Your Latest session")
        

        frame_details=Frame(top)
        frame_details.pack(pady=10)
        t_details=ttk.Treeview(top)
        
        t_details["column"]=list(df_details)
        t_details["show"]="headings"

        for column in t_details["column"]:
            t_details.heading(column, text=column)

        df_rows=df_details.to_numpy().tolist()
        
        for row in df_rows:
            t_details.insert("","end",values=row)
        
        t_details.pack()
        #top.iconbitmap("icon")
        btn_cls_anwrkey=Button(top, text="Close", cursor="hand2", command=top.destroy, width=10, bg="red", fg="white",font=(letra, 16,"bold")).pack()
        #answer_key_window=Tk().Toplevel(root)
        #canvas=Canvas(answer_key_window, 500, 500)
        #canvas.pack()
        
        
        




    def play_again_macro(self):
        peta=msbox.askquestion("Let's do it again!","Would you like restart from a new session?")
        if peta=='no':
            clear_window()
            quiz=Quiz_GI()
        else:
            clear_window()
            Generate_Question_Session(df_q_bank)
            Generate_Content(df_q_bank)    
            quiz=Quiz_GI()
    

        


# Below, are the general functions:

def Generate_Question_Session(df_q_bank):
    # Shuffles the question bank to reorder how questions will appear. May also add filter for chapters and number of questios in the session!
    
    df_q_bank=df_q_bank.sample(frac=1)
    

def Generate_Content(df_q_bank):
  # Creates shuffled answer options for each question in the session and also its proper answer key. 
  # shuffleing dataframe rows so questions won't appear always in the same order...
  #df_q_bank=df_q_bank.sample(frac=1)

  # Loading the questions and asnwers from the dataframe into lists to be handle by the UI class defined above ...
  global q
  q=df_q_bank["questions"].to_list()
  global anw
  anw=df_q_bank["answr"].to_list()
  global pg
  pg=df_q_bank["page"].to_list()
  global ch
  ch=df_q_bank["chptr"].to_list()
  

  # Creating shuffles options and proper answer keys!!!
  global op
  op=[]
  global gabarito
  gabarito=[]

  for p in range(len(anw)):
     temp_op=[]
     temp_to_shff_op=anw.copy()
     temp_op.append(anw[p])
     temp_to_shff_op.remove(anw[p])
     random.shuffle(temp_to_shff_op)
     #temp_to_shff_op.append(anw[p])
     temp_op.append(temp_to_shff_op[0])
     temp_op.append(temp_to_shff_op[1])
     temp_op.append(temp_to_shff_op[2])
     random.shuffle(temp_op)
     gabarito.append(temp_op.index(anw[p])+1)
     op.append(temp_op)

  




def clear_window():
    n=2 # index that will refer to the itens that will remain in the screen (i.e: Top label and DAMA logo). 
    all_wid=root.winfo_children()
    out_wid=all_wid[2:len(all_wid)]

    for widget in out_wid:
       widget.destroy()



# ---------NOW WE START RUNNING THINGS!!!!----------

# Creating the backgroung instance for the GI
root=Tk()
root.geometry("1050x660")
root.title('Dama Quiz - by DAMA Vancouver Chapter')


# Adding and handling DAMA logo ...
img = PhotoImage(file=fgr)
label = Label(root, image=img)
label.place(x=850, y=10)

# adding top label ...
t = Label(root, text="QUIZ Practice for the DAMA Certification", width=32, fg=title_font_colour, font=(letra,20,"bold", "underline"))
t.place(x=250, y=35)

#importing jason info into a data frame...

df_q_bank = pd.read_json(source_dt_file)


# Generating content by calling function ...

Generate_Question_Session(df_q_bank)
Generate_Content(df_q_bank)

# Calling the UI...
quiz=Quiz_GI()



root.mainloop()