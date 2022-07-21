from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#A4B787"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
check = ""
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(time_text, text="00:00")
    check_label.config(text="")
    title_label.config(text="Timer", font=(FONT_NAME, 50), bg=YELLOW, fg=GREEN, pady=10)
    global reps
    reps = 0
    global check
    check = ""
    start_button.config(state=NORMAL)


# ---------------------------- TIMER MECHANISM ------------------------------- #
# todo: after click, disable the start button temporarily
def start_timer():
    # tracking reps
    global reps
    reps += 1

    # disable the start button until reset
    start_button.config(state=DISABLED)

    # turn min to total sec
    work_sec = WORK_MIN * 60
    s_break_sec = SHORT_BREAK_MIN * 60
    l_break_sec = LONG_BREAK_MIN * 60

    # determine how much time to count down depending on which reps now is
    if reps % 8 == 0:
        count_down(l_break_sec)
        title_label.config(text="Break!", fg=RED, font=(FONT_NAME, 50))
    elif reps % 2 == 0:
        count_down(s_break_sec)
        title_label.config(text="Break!", fg=PINK, font=(FONT_NAME, 50))
    elif reps % 2 != 0:
        count_down(work_sec)
        title_label.config(text="Work..", fg=GREEN, font=(FONT_NAME, 50))


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(total_sec):
    # show 2 digits instead of only 1. ex: 08:03 not 8:3
    count_min = math.floor(total_sec / 60)
    count_sec = total_sec % 60

    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(time_text, text=f"{count_min}:{count_sec}")

    # make sure the total sec is not going to be less than 0
    if total_sec >= 0:
        global timer  # in order to cancel the countdown in reset_timer()
        timer = window.after(1000, count_down, total_sec - 1)

    # when the countdown is over, start countdown again without click the button and lead to the next rep
    else:
        start_timer()
        if reps % 2 == 0:
            global check
            check += "✔︎"
            check_label.config(text=check)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=30, bg=YELLOW)
window.title("Pomodoro")

canvas = Canvas(width=205, height=223, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(102, 110, image=tomato_img)
time_text = canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

title_label = Label(text="Timer", font=(FONT_NAME, 50), bg=YELLOW, fg=GREEN, pady=10)
title_label.grid(column=1, row=0)
check_label = Label(font=(FONT_NAME, 30), bg=YELLOW, fg=GREEN, pady=10)
check_label.grid(column=1, row=3)

start_button = Button(text="Start", font=(FONT_NAME, 16), highlightthickness=0, command=start_timer)
reset_button = Button(text="Reset", font=(FONT_NAME, 16), highlightthickness=0, command=reset_timer)
start_button.grid(column=0, row=2)
reset_button.grid(column=2, row=2)

window.mainloop()
