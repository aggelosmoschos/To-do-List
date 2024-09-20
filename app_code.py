from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

task_file = "tasks.txt" #μεταβλητή που ορίζει το αρχείο txt που θα χρησιμοποιηθεί
weekdays=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] #η λίστα που αντιπροσωπεύει τις 7 ημέρες της εβδομάδας

def read_my_tasks():
    tasks_in_day={day: [] for day in weekdays} #Δημιουργώ το λεξικό tasks_in_day όπου κάθε ημέρα είναι κλειδί, μέσα στο οποίο δημιουργείται μία κενή λίστα όπου βρίσκονται οι εργασίες της συγκεκριμένης μέρας
    try:
        with open(task_file, "r") as file:  #Με δομή try-except ανοίγω το αρχείο σε read mode και χωρίζω σε γραμμή-γραμμή εργασίες και ημέρες με το "/" ως διαχωριστικό
            for line in file:
                task, day = line.strip().split("/")
                tasks_in_day[day].append(task)
    except FileNotFoundError:
        pass
    return tasks_in_day

def write_tasks(tasks_in_day):  #Ανοίγω το αρχείο σε write mode και γράφω καινούριο task για οποιαδήποτε μέρα της εβδομάδας(έγινε χρήση f-string για να καθαρίσει ο κώδικας, ιδέα από ChatGPT)
    with open(task_file, "w")as file:
        for day, tasks in tasks_in_day.items():
            for task in tasks:
                file.write(f"{task}/{day}\n")

@app.route("/") #Κώδικας Flask, είναι ο κώδικασ που ορίζει το home screen και συνδέεται άμεσα με τον html κώδικα
def home():
    tasks_in_day=read_my_tasks()
    return render_template("home.html", tasks_in_day=tasks_in_day, days=weekdays)

@app.route("/add_tasks", methods=["POST"]) #Συνέχεια του Flask κώδικα, το συγκεκριμένω fuction προσθέτει μέσω form τα καινούρια tasks και έπειτα επιστρέφει τον χρήστη στο home screen
def add_tasks():
    day=request.form.get("day")
    task=request.form.get("task")
    if day and task and day in weekdays:
        tasks_in_day=read_my_tasks()
        tasks_in_day[day].append(task)
        write_tasks(tasks_in_day)
    return redirect(url_for("home"))

@app.route("/delete_tasks/<day>/<int:task_num>") #Το fuction δίνει τη δυνατότητα στον χρήστη να πατήσει ένα link το οποίο διαγράφει συγκεκριμένο task και επιστρέφει τον χρήστη στο home screen
def delete_tasks(day, task_num):
    tasks_in_day=read_my_tasks()
    if day in tasks_in_day and 0<=task_num<len(tasks_in_day[day]): #Η ιδέα για την χρήση του int:task_num ως "διεύθυνση" για την εύκολη εύρεση των tasks δώθηκε απο το chatgpt, απλούστευσε και έκανε πιο άμεσο τον κώδικα και ήταν κάτι που δεν είχα συναντήσει στην έρευνα μου σχετικά με το flask
        tasks_in_day[day].pop(task_num)
        write_tasks(tasks_in_day)
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run()        
