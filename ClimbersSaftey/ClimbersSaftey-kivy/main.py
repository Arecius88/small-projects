from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class BoxLayout(BoxLayout):
    pass


class MainWidget(BoxLayout):
    belayer_input = StringProperty("0")
    climber_input = StringProperty("0")
    sandbag_weight = 15
    amount_sandbags = 0
    sandbags = StringProperty("Sandbags needed")

    def belayer_validate(self, widget):
        self.belayer_input = widget.text

    def climber_validate(self, widget):
        self.climber_input = widget.text


    def cal_weight_diff(self):
        #print(f"Belayer: {self.belayer_input}")
        #print(f"Climber: {self.climber_input}")
        self.belayer_input_int = int(self.belayer_input)
        self.climber_input_int = int(self.climber_input)

        if self.belayer_input_int > 0 and self.climber_input_int > 0:
            self.weight_diff = self.climber_input_int / self.belayer_input_int

            if self.weight_diff > 1.2:
                self.amount_sandbags = round((self.climber_input_int - self.belayer_input_int)/self.sandbag_weight)
                self.sandbags = str(f'You need: {self.amount_sandbags} sandbags')
                print(self.sandbags)

            else:
                self.sandbags = "You don't need sandbags"

        else:
            self.sandbags = "Error: Insert numbers above 0"

class ClimbersSafetyApp(App):
    pass


ClimbersSafetyApp().run()
