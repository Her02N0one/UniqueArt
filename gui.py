# Program to make a simple
# login screen
import tkinter as tk
import main

root = tk.Tk()
root.wm_title("Personal Abstract Art")
# setting the windows size
root.geometry("300x400")

# declaring string variable 
# for storing name and password 
name_var = tk.StringVar()
age_var = tk.StringVar()
fav_thing_var = tk.StringVar()
fav_color_var = tk.StringVar()



def submit():
	name = name_entry.get()
	age = int(age_entry.get())
	fav_thing = fav_thing_entry.get()
	fav_color = fav_color_entry.get()

	main.main(name, age, fav_thing, fav_color)

name_label = tk.Label(root, text='Name', font=('calibre', 10, 'bold'))
name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))

age_label = tk.Label(root, text='Age', font=('calibre', 10, 'bold'))
age_entry = tk.Entry(root, textvariable=age_var, font=('calibre', 10, 'normal'))

fav_thing_label = tk.Label(root, text='Favorite Thing', font=('calibre', 10, 'bold'))
fav_thing_entry = tk.Entry(root, textvariable=fav_thing_var, font=('calibre', 10, 'normal'))

fav_color_label = tk.Label(root, text='Favorite Color', font=('calibre', 10, 'bold'))
fav_color_entry = tk.Entry(root, textvariable=fav_color_var, font=('calibre', 10, 'normal'))

# creating a button using the widget  
# Button that will call the submit function  
sub_btn = tk.Button(root, text='Submit', command=submit)

# placing the label and entry in 
# the required position using grid 
# method 
name_label.grid(row=0, column=0)
name_entry.grid(row=0, column=1)
age_label.grid(row=1, column=0)
age_entry.grid(row=1, column=1)
fav_thing_label.grid(row=2, column=0)
fav_thing_entry.grid(row=2, column=1)
fav_color_label.grid(row=3, column=0)
fav_color_entry.grid(row=3, column=1)
sub_btn.grid(row=4, column=1)

# performing an infinite loop  
# for the window to display 
root.mainloop()
