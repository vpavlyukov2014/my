import datetime


class ClockText():


    def __init__(self):
        self.refresh_info()


    def refresh_info(self):
        self.text_data = self.get_text_data()


    def get_text_data(self):
        now = datetime.datetime.now()
        return now.strftime("%d %B %Y  %A  %H:%M:%S ")
