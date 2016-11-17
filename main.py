from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from math import factorial


def binomial(n, k):
    return factorial(n) / (factorial(k) * factorial(n-k))


def calc_odds(num_dice, win_with):
    win_odds = (7 - win_with) / 6
    lose_odds = 1 - win_odds

    results = []
    for num_wins in range(1, num_dice+1):
        val = binomial(num_dice, num_wins)
        val *= win_odds ** num_wins
        val *= lose_odds ** (num_dice - num_wins)
        results.append(val)

    return results


def expected_kills(odds):
    expect = 0
    for c, odd in enumerate(odds, start=1):
        expect += c * odd
    return expect


def odds_list(odds, crawl):
    cum_prob = [sum(odds[c:])*100 for c in range(len(odds))]
    cum_prob_crawl = [sum(crawl[c:])*100 for c in range(len(crawl))]
    cum_prob_crawl.append(0)

    odds_str = '{} Zombie: {:.1f}%/{:.1f}%\n'.format(1, cum_prob[0], cum_prob_crawl[0])
    for c, (prob, cr) in enumerate(zip(cum_prob[1:], cum_prob_crawl[1:]), start=2):
        odds_str += '{} Zombies: {:.1f}%/{:.1f}%\n'.format(c, prob, cr)

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

    def change_odds(self):
        labels = [['num_1', 'win_1', 'expected_1', 'odds_1'], 
                  ['num_2', 'win_2', 'expected_2', 'odds_2']]

        for l_num, l_win, l_exp, l_odd in labels: 
            dice_num = int(self.ids[l_num].text)
            dice_win = int(self.ids[l_win].text)
            dice_results = calc_odds(dice_num, dice_win)

            if dice_win == 1:
                dice_crawler = calc_odds(dice_num-1, 7)
            else:
                dice_crawler = calc_odds(dice_num-1, 6)

            self.ids[l_exp].text = 'Expect {:.2f} Kills'.format(expected_kills(dice_results))
            self.ids[l_odd].text = odds_list(dice_results, dice_crawler)


class ZombicideDicingApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    ZombicideDicingApp().run()
