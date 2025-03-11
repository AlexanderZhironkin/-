import serial
import time
import tkinter
import matplotlib.pyplot as plt

name_fail = 'output_2.txt'     # имя файла хранящего данные эксперемента
def grafik_strou():
    shim = []
    tok = []
    ves = []
    oboroti = []
    napriz = []
    rr = []
    with open(name_fail, "r", encoding="UTF-8") as file_in:
        for line in file_in:
            if line !="\n":
                rr = [x for x in line.split(',')]
                shim.append(int(rr[1])/10)
                tok.append(float(rr[3]))
                ves.append(float(rr[5]))
                oboroti.append(float(rr[7]))
                napriz.append(float(rr[9]))
    plt.figure(1)
    plt.plot(shim, tok, color='green', marker='o')
    plt.title('ГРАФИК ИЗМЕНЕНИЯ ТОКА ОТ ШИМА')
    plt.ylabel('TOK')
    plt.xlabel('ШИМ')

    plt.figure(2)
    plt.plot(shim, ves)
    plt.title('ГРАФИК ИЗМЕНЕНИЯ ТЯГИ ОТ ШИМА')
    plt.xlabel('ШИМ')
    plt.ylabel('СИЛА ТЯГИ')

    plt.figure(3)
    plt.plot(shim, oboroti)
    plt.title('ГРАФИК ОБОРОТОВ В МИНУТУ ОТ ШИМА')
    plt.xlabel('ШИМ')
    plt.ylabel('ОБОРОТЫ')
     
    plt.figure(4)
    plt.plot(shim, napriz)
    plt.title('ГРАФИК ИЗМЕНЕНИЯ НАПРЯЖЕНИЯ ОТ ШИМА')
    plt.xlabel('НАПРЯЖЕНИЕ')
    plt.ylabel('ОБОРОТЫ')
    plt.show()


def zapis_v_fail():
    data_list = []
    ser = serial.Serial("com5", 9600)
    print("Reset Arduino")
    time.sleep(3)
    ser.write(bytes("L", "UTF-8"))
    # Читаем ответ от Arduino через Serial порт
    response = ser.readline()
    decoded_response = response.decode("utf-8") # Декодируем ответ из байтов в строку с использованием UTF-8
    while decoded_response.count("STOP") < 1 :
        print(decoded_response)
        data_list.append(decoded_response)
        response = ser.readline()
        decoded_response = response.decode("utf-8")
    print(decoded_response)
    print(data_list)
    # Закрываем порт
    ser.close()
    print("Запись файла НАЧАЛАСЬ")
    # Записываем данные в файл
    
    with open(name_fail, "w", encoding="UTF-8") as file_out:
        file_out.writelines(data_list)
    print("Запись файла ЗАКОНЧИЛАСЬ")

def quit():
    global tkTop
    ser.write(bytes("L", "UTF-8"))
    tkTop.destroy()


def set_button1_state():
    global b
    b += 1
    varLabel.set("ЗАПУСК ИСПЫТАНИЯ")
    zapis_v_fail()
    varLabel.set(b)
    print(b)
    

def set_button2_state():
    varLabel.set("ВЫЧИСЛЕНИЕ")
    #ser.write(bytes("L", "UTF-8"))
    data_list = []
    grafik_strou()


b = 0


tkTop = tkinter.Tk()
tkTop.geometry("400x500")     #размер окна при запуске приложения
tkTop.title("РЭА и корпорейтед")
tkTop.attributes("-alpha", 0.9)  #прозрачность
tkTop.config(bg="green")
label3 = tkinter.Label(
    text="ИССЛЕДУЙ ВМГ",
    font=("Courier", 12,)
).pack()
tkTop.counter = 0
b = tkTop.counter

varLabel = tkinter.IntVar()
tkLabel = tkinter.Label(
    textvariable=varLabel,
)
tkLabel.pack()

varLabel2 = tkinter.IntVar()
tkLabel2 = tkinter.Label(
    textvariable=varLabel2,
)
tkLabel2.pack()

button1 = tkinter.IntVar()
button1state = tkinter.Button(
    tkTop,
    text="ЗАПУСТИТЬ ИСПЫТАНИЯ",
    command=set_button1_state,
    height=4,
    fg="black",
    width=20,
    background="#A9A9A9",
    activebackground="green",
)
button1state.pack(side="top", ipadx=10, padx=10, pady=15)

button2 = tkinter.IntVar()
button2state = tkinter.Button(
    tkTop,
    text="ВЫВОД ГРАФИКОВ",
    command=set_button2_state,
    height=4,
    fg="black",
    width=16,
    background="#A9A9A9",
    activebackground="green"
)
button2state.pack(side="top", ipadx=10, padx=10, pady=15)

tkButtonQuit = tkinter.Button(
    tkTop, text="ПЕРЕЗАПУСК", command=quit, height=4, fg="black", width=8, background="#A9A9A9", bd=5
)
tkButtonQuit.pack(side="top", ipadx=10, padx=10, pady=15)

tkinter.mainloop()
