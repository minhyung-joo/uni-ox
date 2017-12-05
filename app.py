import Tkinter as tk
import ttk
import random
import serial

# For calculating moving average
index = 0
capacity = 15
pm_values = []

thresholds = [80, 90, 700, 40]
style_names = ['temp.Vertical.TProgressbar', 'humid.Vertical.TProgressbar', 'pm.Vertical.TProgressbar', 'co.Vertical.TProgressbar']
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TFrame', background='#66FF66')
ser = serial.Serial('/dev/ttyUSB0', 9600)

class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.initData()
        self.setSize()
        self.grid()
        self.createWidgets()

    def initData(self):
        temp_value = tk.DoubleVar()
        humid_value = tk.DoubleVar()
        pm_value = tk.DoubleVar()
        co_value = tk.DoubleVar()
        temp_str = tk.StringVar()
        temp_str.set(str(temp_value.get()))
        humid_str = tk.StringVar()
        humid_str.set(str(humid_value.get()))
        pm_str = tk.StringVar()
        pm_str.set(str(pm_value.get()))
        co_str = tk.StringVar()
        co_str.set(str(co_value.get()))
        self.data = [temp_value, humid_value, pm_value, co_value]
        self.data_str = [temp_str, humid_str, pm_str, co_str]

    def setSize(self):
        for i in range(4):
            self.columnconfigure(i, minsize=120)
        self.rowconfigure(0, minsize=60)
        self.rowconfigure(1, minsize=120)
        self.rowconfigure(2, minsize=60)

    def createMeterFor(self, name, c):
        self.label = ttk.Label(self, text=name, borderwidth=4, relief=tk.GROOVE, anchor='center')
        self.label.grid(column=c, row=0, padx=8, pady=12, sticky='news')
        self.bar = ttk.Progressbar(self, orient='vertical', length=120, mode='determinate', variable=self.data[c], style=style_names[c])
        self.bar.grid(column=c,row=1)
        self.value = ttk.Label(self, textvariable=self.data_str[c], borderwidth=4, relief=tk.GROOVE, anchor='center')
        self.value.grid(column=c, row=2, padx=25, pady=16, sticky='news')

    def createWidgets(self):
        categories = ['Temperature', 'Humidity', 'PM Level', 'CO Level']
        for i in range(4):
            self.createMeterFor(categories[i], i)

app = Application()
app.master.title('Uni-Ox Air Quality Monitor')

for i in range(4):
    app.data[i].set(40)
    new_value = app.data[i].get()
    app.data_str[i].set(str(new_value))

while True:
    read_serial = ser.readline()
    data = read_serial.split(':')
    if data[0] == 'Temperature':
        temperature = float(data[1])
        if temperature < -40:
            temperature = -40
        if temperature > 100:
            temperature = 100
        app.data[0].set((temperature + 40)/1.4)
        app.data_str[0].set('{0:.2f}'.format(temperature))
        if new_value > thresholds[0]:
            style.configure(style_names[0], background='red')
        else:
            style.configure(style_names[0], background='white')
    elif data[0] == 'Humidity':
        humidity = float(data[1])
        app.data[1].set(humidity)
        app.data_str[1].set('{0:.2f}'.format(humidity))
        if new_value > thresholds[1]:
            style.configure(style_names[1], background='red')
        else:
            style.configure(style_names[1], background='white')
    elif data[0] == 'PM':
        pm = float(data[1])
        if len(pm_values) < capacity:
            pm_values.append(pm)
        else:
            if index >= capacity:
                index = 0
            pm_values[index] = pm
            index = index + 1

        pm = sum(pm_values)/len(pm_values)
        if pm > 1000:
            pm = 1000.00
        app.data[2].set(pm/10)
        app.data_str[2].set('{0:.2f}'.format(pm))
        if pm > thresholds[2]:
            style.configure(style_names[2], background='red')
        else:
            style.configure(style_names[2], background='white')

    random_step = random.randint(-1, 1)
    app.data[3].set(app.data[3].get() + random_step)
    new_value = app.data[3].get()
    app.data_str[3].set(str(new_value))
    if new_value > thresholds[3]:
        style.configure(style_names[3], background='red')
    else:
        style.configure(style_names[3], background='white')

    app.update()
