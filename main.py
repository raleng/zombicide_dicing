from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from math import factorial


def binomial(n, k):
    """ Calculates the binomial coefficient (n over k). """
    return factorial(n) / (factorial(k) * factorial(n-k))


def calc_odds(num_dice, win_with):
    """ Computes the probabilities for killing any number of zombies.

    The formula is:
    (n over k) * (p)^k * (1-p)^(n-k)
    """
    win_odds = (7 - win_with) / 6
    lose_odds = 1 - win_odds

    for num_wins in range(1, num_dice+1):
        val = binomial(num_dice, num_wins)
        val *= win_odds ** num_wins
        val *= lose_odds ** (num_dice - num_wins)
        yield val


def calc_crawl(num_dice):
    """ Computes the probability for generating at least one crawler.

    The formula is:
    1 - (5/6)^num_dice
    """
    for num in range(num_dice, 0, -1):
        yield (1 - (5/6) ** num) * 100
    yield 0  # last entry is always 0, because all dice kill


def expected_kills(odds):
    """ Computes the expected value of zombie kills. """
    expect = 0
    for c, odd in enumerate(odds, start=1):
        expect += c * odd
    return expect


def odds_list(odds, crawl):
    """ Yields tuple (N, P, C) with

    N = Number of killed zombies,
    P = Probability killing N zombies,
    C = Probability generating a crawler while killing N zombies.
    """
    cum_prob = [sum(odds[c:])*100 for c in range(len(odds))]

    for c, (prob, cr) in enumerate(zip(cum_prob, crawl), start=1):
        yield (c, prob, cr)


class DiceLayout(FloatLayout):

    def __init__(self, **kwargs):
        """ Initializes odds for default values after building widget. """
        super(DiceLayout, self).__init__(**kwargs)
        # Make sure the widget init is done
        Clock.schedule_once(self._finish_init, 0)

    def _finish_init(self, dt=0):
        self.change_odds()

    @staticmethod
    def decrease_num(current_num):
        """ Decreases number by one. Dose not decrease below 1. """
        if int(current_num) > 1:
            return str(int(current_num) - 1)
        else:
            return str(1)

    @staticmethod
    def increase_num(current_num):
        """ Increases number by one. Dose not increase over 6. """
        if int(current_num) < 6:
            return str(int(current_num) + 1)
        else:
            return str(6)

    def change_odds(self):
        """ Sets the text labels according to the current probabilities. """

        # Getting input values and calculating odds
        dice_num = int(self.ids['num'].text)
        dice_win = int(self.ids['win'].text)
        dice_results = list(calc_odds(dice_num, dice_win))

        # If dice win with 1 or better (i.e. always), no crawler is being created.
        if dice_win == 1:
            dice_crawler = [0 for _ in range(dice_num)]
        else:
            dice_crawler = list(calc_crawl(dice_num-1))

        # Setting output
        self.ids['exp'].text = 'Avg: {:.2f}'.format(expected_kills(dice_results))

        grid_odds = self.ids['odd']
        grid_odds.bind(minimum_height=grid_odds.setter('height'))
        grid_odds.clear_widgets()
        for odds in list(odds_list(dice_results, dice_crawler)):
            grid_odds.add_widget(Label(text='{}'.format(odds[0]),
                                       font_size='25dp',
                                       bold=True,
                                       size_hint_x=0.3,
                                       ))
            grid_odds.add_widget(Label(text='{:.1f}%'.format(odds[1]),
                                       font_size='25dp',
                                       size_hint_x=0.4,
                                       ))
            grid_odds.add_widget(Label(text='{:.1f}%'.format(odds[2]),
                                       font_size='15dp',
                                       size_hint_x=0.3,
                                       ))


class MainWidget(BoxLayout):
    pass


class ZomDieApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    ZomDieApp().run()
