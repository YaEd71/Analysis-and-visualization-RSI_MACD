import data_download as dd
import data_plotting as dplt

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров: AAPL (Apple Inc), GOOGL (Alphabet Inc), "
        "MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    try:
        ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")

        # Получение данных об акциях
        stock_data = dd.fetch_stock_data(ticker, period)

        if stock_data is None:
            print("Не удалось получить данные. Завершение программы.")
            return

        # Добавление скользящего среднего
        stock_data = dd.add_moving_average(stock_data)

        # Добавление технических индикаторов
        stock_data = dd.add_technical_indicators(stock_data)

        # Проверка сильных колебаний
        dd.notify_if_strong_fluctuations(stock_data, ticker, threshold=3)

        # Расчет и вывод средней цены
        dd.calculate_average_price(stock_data)

        # Выбор типа графика
        print("\nВыберите тип графика:")
        print("1. По умолчанию (цена и скользящее среднее)")
        print("2. RSI")
        print("3. MACD")
        print("4. Все индикаторы")

        plot_choice = input("Введите номер варианта (1-4): ")
        plot_types = {
            '1': 'default',
            '2': 'rsi',
            '3': 'macd',
            '4': 'all'
        }
        plot_type = plot_types.get(plot_choice, 'default')

        # Построение графика с выбранным типом
        dplt.create_and_save_plot(stock_data, ticker, period, plot_type=plot_type)

        # Запрос на экспорт данных
        export_choice = input("Хотите экспортировать данные в CSV? (да/нет): ").lower()
        if export_choice in ['да', 'yes', 'y']:
            filename = f"{ticker}_{period}_stock_data.csv"
            dd.export_data_to_csv(stock_data, filename)

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()