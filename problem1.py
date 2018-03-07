import numpy as np
import scr.StatisticalClasses as Stat



class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, id, prob_head, n_games):
        self._id = id
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameLoss = [] # create an empty list where losses will be stored


        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=self._id*1000+n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)


    def get_games(self):
        return(self._gameRewards)


# probability of lose money in games
    def get_prob_lose(self):
        losetime = 0
        for k in self._gameRewards:
            if k < 0:
                losetime += 1
                self._gameLoss.append(1)
            else:
                self._gameLoss.append(0)
        return losetime / len(self._gameRewards)

class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_sizes):

        self._ids = ids
        self._popsizes = pop_sizes
        self._get_all_rewards =[]

    def simulate(self):
        """ simulates all cohorts """
        for i in range(len(self._ids)):
            cohort = SetOfGames(i, 0.5, self._popsizes)
            self._get_all_rewards.append(cohort.get_ave_reward())


# run trail of 1000 games to calculate expected reward
games = SetOfGames(1, 0.5, 1000)


# print the average reward
print('Expected reward when the probability of head is 0.5:', games.get_ave_reward())

Stat_sumStat_reward = Stat.SummaryStat('Game Rewards', games.get_games())
CI_Expected = Stat_sumStat_reward.get_t_CI(0.05)

games.get_prob_lose()
a = games._gameLoss
Stat_sumStat_loss = Stat.SummaryStat('Game Loss', a)
CI_Loss = Stat_sumStat_loss.get_t_CI(0.05)

# problem 1: print the CI of the expected reward and the probability of loss
print("the 95% t-based confidence intervals for the expected reward is", CI_Expected)
print("the 95% t-based confidence intervals for the probability of loss", CI_Loss)

# problem 2:  interpret the confidence intervals reported in Problem 1
print("95% CI of expected rewards means: if we repeat many times of 1000 games and get a confidence interval in each time, 95% of the intervals will cover true mean of expected rewards.")
print("95% CI of the probability of loss means: if we repeat many times of 1000 games and get a confidence interval in each time, 95% of the intervals will cover true probability of loss.")

# problem 3: Analyze this game

simulation_N = 1000
gamblesize =10
gambles = MultiCohort(range(simulation_N), gamblesize)
gambles.simulate()
units = gambles._get_all_rewards
Stat_sum = Stat.SummaryStat('Game Gambler', units)
CI_Gambler = Stat_sum.get_PI(0.05)
print("the 95% confidence interval for the expected reward for a gambler is", CI_Gambler)

print("It means if a gambler repeats 10 times of 1000 games and get a confidence interval in each time, 95% of the intervals will cover true mean of expected rewards."
      "The interval is ", CI_Gambler,
      "For a casino, the 95% confidence interval is ", CI_Expected, ", all negative. So the more you play the more you lose. ")




