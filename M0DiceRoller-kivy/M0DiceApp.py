from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from random import randint


class GidLayoutMain(GridLayout):
    amount_of_dices_konv = StringProperty("0 dices")
    fails_konv = StringProperty("0 fails")
    succs_konv = StringProperty("0 succsesses")
    other_value_konv = StringProperty("0 other")
    avail_dice = StringProperty("0 other")
    amount_of_dices_press_konv = StringProperty("Press")
    underscore = "_" * 10
    function_test_start = f"\n{underscore} Start of function test {underscore}"
    function_test_end = f"{underscore} End of funtion test {underscore}\n"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.amount_of_dices = 0
        self.fails = 0
        self.succs = 0
        self.other_value = 0
        self.other_value = 0

    def dice(self):
        self.minimum = 1
        self.maximum = 6


    def add_dice(self):
        self.amount_of_dices += 1
        print(f"{self.amount_of_dices} dices in dicepool")
        self.amount_of_dices_konv = f"{self.amount_of_dices} dices"

    def remove_dice(self):
        self.amount_of_dices -= 1
        if self.amount_of_dices >= 0:
            print(f"{self.amount_of_dices} dices is in dicepool")
            self.amount_of_dices_konv = f"{self.amount_of_dices} dices"
        else:
            self.amount_of_dices = 0
            print(f"{self.underscore} No more Dices {self.underscore}")

    def roll_dices(self):
        print(f"{self.underscore} Roll_dice was Clicked {self.underscore}")
        self.dice()
        while self.amount_of_dices != 0:
            self.result = randint(self.minimum, self.maximum)

            if self.result == 1:
                self.fails += 1
                self.fails_konv = f"{self.fails} fails"

            elif self.result == 6:
                self.succs += 1
                self.succs_konv = f"{self.succs} succsesses"

            else:
                self.other_value += 1
                self.other_value_konv = f"{self.other_value} other"


            #print(f"{self.result} VÄRDE PÅ TÄRNING")
            self.amount_of_dices -= 1
        self.other_value = self.other_value
        self.amount_of_dices_press_konv = f"Press {self.other_value} dices"

        #if self.amount_of_dices >= 0:
        #    self.amount_of_dices_konv = f"{self.amount_of_dices} dices"

    def press_dice(self):
        print(f"{self.underscore} press_dice was Clicked {self.underscore}\n")
        #self.other_value = self.other_value
        self.amount_of_dices_press_konv = f"Press {self.other_value} dices"

        while self.other_value != 0:
            self.result_press = randint(1, 6)
            print(f"{self.result_press} PRESS VALUE")
            if self.result_press == 1:
                self.fails += 1
                self.fails_konv = f"{self.fails} fails"

            elif self.result_press == 6:
                self.succs += 1
                self.succs_konv = f"{self.succs} succsesses"

            else:
                pass

            self.other_value -= 1

        if self.other_value >= 0:
            self.amount_of_dices_press_konv = f"Press {self.other_value} dices"

    def reset_dice(self):
        self.amount_of_dices_konv = f"{self.amount_of_dices} dices"

        self.other_value = 0
        self.other_value_konv = str(self.other_value) + " other"
        self.succs = 0
        self.succs_konv = str(self.succs) + " succsesses"
        self.fails = 0
        self.fails_konv = str(self.fails) + " fails"
        self.other_value = 0
        #self.amount_of_dices_press_konv = f"Press {self.other_value}"
        print(f"{self.underscore} Reset was clicked {self.underscore}")

    def reset_check_button(self):
        print(self.function_test_start)
        print(f"{self.other_value} D6 to press")
        print(f"{self.succs} SUCs")
        print(f"{self.fails} FAILs")
        print(f"{self.other_value} OTHERs ")
        print(self.function_test_end)


class MainWidget(Widget):
    pass

class M0DiceRollerApp(App):
    pass


M0DiceRollerApp().run()