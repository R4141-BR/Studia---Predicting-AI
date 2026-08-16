import subprocess
import os
import winsound
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import questionary
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

option = 0

X_train = [
    #mat
    [1, 1.0], [1, 2.5], [1, 4.0], [1, 6.0], [1, 7.5], [1, 9.0], [1, 10.0],
    #ing
    [2, 1.0], [2, 2.0], [2, 3.5], [2, 5.0], [2, 7.0], [2, 8.5], [2, 10.0],
    #cn
    [3, 1.0], [3, 3.0], [3, 4.5], [3, 6.0], [3, 7.5], [3, 9.0],
    #hist
    [4, 1.5], [4, 3.0], [4, 5.0], [4, 6.5], [4, 8.0], [4, 10.0],
    #quim
    [5, 1.0], [5, 2.5], [5, 4.0], [5, 6.0], [5, 8.0], [5, 9.5]
]

y_train = [
    3.0, 4.8, 6.2, 7.8, 8.9, 9.5, 9.8, #mat

    4.5, 6.0, 7.5, 8.7, 9.2, 9.7, 10.0, #ing
    
    3.8, 5.8, 7.0, 8.2, 9.0, 9.6, #cn
    
    3.5, 5.2, 7.2, 8.3, 9.1, 9.8, #hist
    
    3.2, 5.0, 6.5, 8.0, 9.0, 9.7 #quim
]

recomendation = {
    1: "As you got a grade below 70% on Mathematics, focus on reviewing the main concepts and practicing more exercises.",
    2: "As you got a grade below 70% on English, focus on reviewing the main concepts and practicing more exercises.",
    3: "As you got a grade below 70% on Science, focus on reviewing the main concepts and practicing more exercises.",
    4: "As you got a grade below 70% on History, focus on reviewing the main concepts and practicing more exercises.",
    5: "As you got a grade below 70% on Chemistry, focus on reviewing the main concepts and practicing more exercises.",

    6: "As you got a grade bigger than 70% on Mathematics, keep up the good work and continue practicing to maintain your performance.",
    7: "As you got a grade bigger than 70% on English, keep up the good work and continue practicing to maintain your performance.",
    8: "As you got a grade bigger than 70% on Science, keep up the good work and continue practicing to maintain your performance.",
    9: "As you got a grade bigger than 70% on History, keep up the good work and continue practicing to maintain your performance.",
    10: "As you got a grade bigger than 70% on Chemistry, keep up the good work and continue practicing to maintain your performance.",
}

typesofstudy = {
    1: "Mathematics",
    2: "English",
    3: "Science",
    4: "History",
    5: "Chemistry",
}

recommendationforstudying = {
        1: "Remember to take breaks during your study sessions to improve focus and retention.",
        2: "Try to study in a quiet environment to minimize distractions and enhance concentration.",
        3: "Use active learning techniques, such as summarizing information in your own words, to reinforce understanding.",
        4: "Practice with past exams or quizzes to familiarize yourself with the format and types of questions you may encounter.",
}

preprocess = ColumnTransformer(
    transformers=[
        ("subject", OneHotEncoder(handle_unknown="ignore"), [0]),
        ("hours", StandardScaler(), [1]),
    ]
)

pipe = Pipeline([
    ("preprocess", preprocess),
    ("regressor", LinearRegression()),
])

pipe.fit(X_train, y_train)

def cleanfds():
    os.system('cls' if os.name == 'nt' else 'clear')

def salvar_blocodedados(texto):
    import datetime
    name_arq = "Study_Records.txt"
    with open("Study_Records.txt", "a") as arquivo:
        arquivo.write(f"--[{datetime.datetime.now()}], This is a note: {texto}\n")
    print("Data saved successfully to 'Study_Records.txt'.")

    try:
        os.startfile(name_arq)
    except AttributeError:
        import subprocess , platform
        if platform.system() == "Darwin":
            subprocess.call(["open", name_arq])
        else:
            subprocess.call(["xdg-open", name_arq])


def tocar_alarme_e_popup(materia='Estudos'):
    import subprocess
    import winsound

    try:
        winsound.Beep(1000, 1500)
    except Exception:
        pass

    mensagem = f'Your session in {materia} has finished! Time to take a break.'
    titulo = '🔔 Time for a Break!'

    ps_script = f'Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show("{mensagem}", "{titulo}")'
    subprocess.run(['powershell', '-Command', ps_script])


def createalarm(howmanydays, howmuchperday, materia="Estudos"):
    import time
    console.print(Panel(
        f"[bold cyan]Alarm Configured for {materia}[/bold cyan]\n"
        f"Target: [yellow]{howmanydays} days/week[/yellow], [yellow]{howmuchperday} hours/day[/yellow]",
        title="⏰ Study Alarm Set",
        style="blue"
    ))
  
    minutos_totais = howmuchperday * 60
    segundos_espera = minutos_totais * 60

    with Progress(
        SpinnerColumn(),
        TextColumn(f"[bold green]Session active ({minutos_totais:.0f} mins)... Studying {materia}![/bold green]"),
        transient=True
    ) as progress:
        progress.add_task("waiting", total=None)
        time.sleep(segundos_espera)

    tocar_alarme_e_popup(materia)

def createtimetostudy(whentostudy,howmuchperday,materia="Estudos"):
    cleanfds()
    while True:
        try:
    
            print(f"\n According to your input, this week you will study {whentostudy*howmuchperday}. That means you will study {whentostudy} days a week, and {howmuchperday} hours per day. According to the program, you will get a {pipe.predict([[materia, howmuchperday]])[0]:.2f}/10 in {typesofstudy[materia]}.\n.")
            choice = input("Would you like me to set up an Alarm to remind you to study? (y/n): ")

            if choice.lower() == 'y':
                createalarm(whentostudy, howmuchperday, materia)
            elif choice.lower() == 'n':
                print("No alarm will be set. Remember to study regularly!")
            else:
                print("Invalid choice. No alarm will be set.")
        except ValueError:
            print("\n[ERROR] Invalid input. Please enter valid numbers.")
            continue

            
def notaporhora(materiasid,horas):
    cleanfds()

    dados_entrada = [[materiasid, horas]]
    predicao = pipe.predict(dados_entrada)[0]
    score = max(0, min(10, predicao))

    if score < 7:
        whattohelp = recommendationforstudying.get(materiasid, "Keep studying consistently to improve your performance.")
    else:
        whattohelp = recomendation[materiasid + 5]

    print(f"\nPredicted score for {typesofstudy[materiasid]} with {horas} hours studied: {score:.2f}/10.\nTip: {whattohelp}")
    salvar_blocodedados(f"Subject: {typesofstudy[materiasid]}, Hours: {horas}, Predicted Score: {score:.2f}/10, Tip: {whattohelp}")

#
def quantoestudar(materiasid, nota_desejada):
    cleanfds()
    

    nota_0h = pipe.predict([[materiasid, 0]])[0]
    nota_1h = pipe.predict([[materiasid, 1]])[0]
    multiplier = nota_1h - nota_0h
    horasnecessarias = (nota_desejada - nota_0h) / multiplier if multiplier != 0 else float('inf')
    h_min = max(0, horasnecessarias)
    
    horas_necessarias = max(0, h_min)
    if nota_desejada < 0 or nota_desejada > 10:
        print("\n[ERROR] Desired score must be between 0 and 10.")
        return


    print(f"\nTo achieve a score of {nota_desejada:.2f}/10 in subject {typesofstudy[materiasid]}, you need to study approximately {horas_necessarias:.2f} hours. Tip: {recommendationforstudying.get(materiasid, 'Keep studying consistently to improve your performance.')}")
    salvar_blocodedados(f"Subject: {typesofstudy[materiasid]}, Desired Score: {nota_desejada:.2f}/10, Required Hours: {horas_necessarias:.2f}")


def criar_grafico(materiasid):
    cleanfds()
    import matplotlib.pyplot as plt

    x_reais = [ponto[1] for ponto in X_train if ponto[0] == materiasid]
    y_reais = [y_train[i] for i in range(len(X_train)) if X_train[i][0] == materiasid]

    horas = np.linspace(0, 10, 100)
    dados_entrada = [[materiasid, float(h)] for h in horas]
    predicoes = pipe.predict(dados_entrada)
    plt.figure(figsize=(8, 5))
    plt.scatter(x_reais, y_reais, color='red', label='Training Data',zorder=5)
    plt.plot(horas, predicoes , color = 'blue', label='Predicted Score by AI', linewidth=2)
    plt.title(f"Predicted Score vs Hours Studied for Subject {typesofstudy[materiasid]}")
    plt.xlabel("Hours Studied")
    plt.ylabel("Predicted Score")
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.legend()
    plt.grid(True)
    plt.show()

def começarprograma ():
    os.system('cls' if os.name == 'nt' else 'clear')

    console.print(
        Panel.fit(
            "[bold cyan]STUDIA[/bold cyan] - [dim]Smart Grade Predictor & Study Assistant[/dim]",
            border_style="magenta"
        )
    )

    while True:
        action = questionary.select(
            """()()()()()()()()()()()()()()()()()()
# ()   _____ __            ___      ()
# ()  / ___// /___  ______/ (_____ _()
# ()  \__ \/ __/ / / / __  / / __ `/()
# () ___/ / /_/ /_/ / /_/ / / /_/ / ()
# ()/____/\__/\__,_/\__,_/_/\__,_/  ()
# ()()()()()()()()()()()()()()()()()()
# \n--- Predictions Start ---
# Choose an option:""",
            choices=[
                "1. Predict score based on hours studied",
                "2. Calculate hours needed for a desired score",
                "3. View Study Graph",
                "4. Create a Study Alarm",
                "Exit"
            ]
        ).ask()

        if action is None or action == "Exit":
            console.print("[bold red]Exiting application. Happy studying![/bold red]")
            break

        if action.startswith("1"):
            materiasid = int(Prompt.ask("Enter subject ID (1-Mat, 2-Eng, 3-Sci, 4-His, 5-Qui):", default="1"))
            horas = float(Prompt.ask("Enter hours studied", default="2.0"))
            console.print(f"[bold green]✓ Processing request for {typesofstudy[materiasid]} ({horas} hrs)...[/bold green]")
            notaporhora(materiasid, horas)

        if action.startswith("2"):
            materiasid = int(Prompt.ask("Enter subject ID (1-Mat, 2-Eng, 3-Sci, 4-His, 5-Qui):", default="1"))
            nota_desejada = float(Prompt.ask("Enter desired score (0-10)", default="7.0"))
            console.print(f"[bold green]✓ Processing request for {typesofstudy[materiasid]} to achieve a score of {nota_desejada}...[/bold green]")
            quantoestudar(materiasid, nota_desejada)

        if action.startswith("3"):
            materiasid = int(Prompt.ask("Enter subject ID (1-Mat, 2-Eng, 3-Sci, 4-His, 5-Qui):", default="1"))
            console.print(f"[bold green]✓ Generating study graph for {typesofstudy[materiasid]}...[/bold green]")
            criar_grafico(materiasid)

        elif action.startswith("4"):
            howmuchperweek = int(Prompt.ask("Days per week", default="5"))
            howmanyhourperday = float(Prompt.ask("Hours per day", default="1.5"))
            materiasid = int(Prompt.ask("Enter subject ID (1-Mat, 2-Eng, 3-Sci, 4-His, 5-Qui):", default="1"))

            if Confirm.ask("Start timer now?"):
                createalarm(howmuchperweek, howmanyhourperday, materiasid)

começarprograma()