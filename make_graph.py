import matplotlib.pyplot as pypt

def create_graph(day_temps, night_temps, month, name_city):
    """Создает  график температур за определенный месяц"""
    
    x_data = [str(d + 1) if d >= 9 else '0' + str(d + 1) for d in range(len(day_temps))] # даты всего месяца
    figure, ax = pypt.subplots()

    # Указываем размер графика 
    figure.set_figwidth(9)
    figure.set_figheight(5)

    # Строим график
    ax.set_title(f"Temerature graph for the {month} in {name_city}")
    ax.set_xlabel("Dates")
    ax.set_ylabel("Temperatures")
    ax.plot(x_data, night_temps, label = "Night temeratures", marker = "^")
    ax.plot(x_data, day_temps, label = "Day temeratures", marker = "o")
    ax.legend()

    pypt.show()

