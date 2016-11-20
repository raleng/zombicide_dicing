from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

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


def expected_kills(odds):
    """ Computes the expected value of zombie kills. """
    expect = 0
    for c, odd in enumerate(odds, start=1):
        expect += c * odd
    return expect


def odds_list(odds, crawl):
    """ Generates a string, listing the cumulative probabilities for killing any
    number of zombies.
    """
    cum_prob = [sum(odds[c:])*100 for c in range(len(odds))]
    cum_prob_crawl = [sum(crawl[c:])*100 for c in range(len(crawl))]
    cum_prob_crawl.append(0)  # last entry is always 0, because all dice kill

    odds_str = ''
    for c, (prob, cr) in enumerate(zip(cum_prob, cum_prob_crawl), start=1):
        odds_str += '{} -- {:.1f}%/{:.1f}%\n'.format(c, prob, cr)

    return odds_str


class MainWidget(BoxLayout):

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
        labels = [['num_1', 'win_1', 'expected_1', 'odds_1'], 
                  ['num_2', 'win_2', 'expected_2', 'odds_2']]

        for l_num, l_win, l_exp, l_odd in labels:
            # Getting input values and calculating odds
            dice_num = int(self.ids[l_num].text)
            dice_win = int(self.ids[l_win].text)
            dice_results = list(calc_odds(dice_num, dice_win))

            # If dice win with 1 or better (i.e. always), no crawler is being created.
            # Calling 'calc_odds(_, 7)' returns list of zeros
            if dice_win == 1:
                dice_crawler = list(calc_odds(dice_num-1, 7))
            else:
                dice_crawler = list(calc_odds(dice_num-1, 6))

            # Setting output
            self.ids[l_exp].text = 'Expect {:.2f} Kills'.format(expected_kills(dice_results))
            self.ids[l_odd].text = odds_list(dice_results, dice_crawler)


class ZombicideDicingApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    ZombicideDicingApp().run()
