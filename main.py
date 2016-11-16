from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from math import factorial


def expected_kills(odds):
    expect = 0
    for c, odd in enumerate(odds, start=1):
        expect += c * odd
    return round(expect, 2)


def binomial(n, k):
    return factorial(n) / (factorial(k)*factorial(n-k))


def calc_odds(num_dice, win_with):
    win_odds = ((6 - win_with) + 1) / 6
    lose_odds = (win_with - 1) / 6
    results = []
    for num_wins in range(1, num_dice+1):
        val = win_odds ** num_wins
        val *= lose_odds ** (num_dice - num_wins)
        val *= binomial(num_dice, num_wins)
        results.append(val)
    return results


def odds_list(result_list):
    if len(result_list):
        odds_str = '{} Zombie: {:.1f}%\n'.format(1, round(sum(result_list[0:]) * 100, 1))
    else:
        return ''

    for count in range(1, len(result_list)):
        cum_prob = sum(result_list[count:])
        odds_str += '{} Zombies: {:.1f}%\n'.format(count+1, round(cum_prob*100, 1))

    return odds_str


class MainWidget(BoxLayout):

    @staticmethod
    def decrease_num(current_num):
        if int(current_num) > 1:
            return str(int(current_num) - 1)
        else:
            return str(1)

    @staticmethod
    def increase_num(current_num):
        if int(current_num) < 6:
            return str(int(current_num) + 1)
        else:
            return str(6)

    def change_odds(self, *args):
        # LEFT COLUMN
        dice1_num = int(self.ids.num_1.text)
        dice1_win = int(self.ids.win_1.text)
        dice1_results = calc_odds(dice1_num, dice1_win)

        self.ids.expected_1.text = 'Expect {:.2f} Kills'.format(expected_kills(dice1_results))
        self.ids.odds_1.text = odds_list(dice1_results)

        # RIGHT COLUMN
        dice2_num = int(self.ids.num_2.text)
        dice2_win = int(self.ids.win_2.text)
        dice2_results = calc_odds(dice2_num, dice2_win)

        self.ids.expected_2.text = 'Expect {:.2f} Kills'.format(expected_kills(dice2_results))
        self.ids.odds_2.text = odds_list(dice2_results)


class ZombicideDicingApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    ZombicideDicingApp().run()
