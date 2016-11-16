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


def crawler_chance(num_dice):
    crawler = []
    if not num_dice == 1:
        for die in range(1, num_dice):
            crawler.append(sum(calc_odds(die, 6)))

    crawler.append(0)
    return crawler


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
        # LEFT COLUMN
        dice1_num = int(self.ids.num_1.text)
        dice1_win = int(self.ids.win_1.text)
        dice1_results = calc_odds(dice1_num, dice1_win)

        # If every die wins, the crawler chance is 0
        # calc_odds(X, 7) returns list of zeros
        if dice1_win == 1:
            dice1_crawler = calc_odds(dice1_num-1, 7)
        else:
            dice1_crawler = calc_odds(dice1_num-1, 6)

        self.ids.expected_1.text = 'Expect {:.2f} Kills'.format(expected_kills(dice1_results))
        self.ids.odds_1.text = odds_list(dice1_results, dice1_crawler)

        # RIGHT COLUMN
        dice2_num = int(self.ids.num_2.text)
        dice2_win = int(self.ids.win_2.text)
        dice2_results = calc_odds(dice2_num, dice2_win)

        # If every die wins, the crawler chance is 0
        # calc_odds(X, 7) returns list of zeros
        if dice2_win == 1:
            dice2_crawler = calc_odds(dice2_num-1, 7)
        else:
            dice2_crawler = calc_odds(dice2_num-1, 6)

        self.ids.expected_2.text = 'Expect {:.2f} Kills'.format(expected_kills(dice2_results))
        self.ids.odds_2.text = odds_list(dice2_results, dice2_crawler)


class ZombicideDicingApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    ZombicideDicingApp().run()
