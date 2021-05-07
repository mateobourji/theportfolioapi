import numpy as np
import pandas as pd
from scipy.optimize import minimize, Bounds


class Portfolio:
    risk_free_rate = np.power((1 + 0.017260), (1 / 365)) - 1
    # TODO: implement function to pull latest rf rate data from yahoo finance

    def __init__(self, hist_data):
        self.hist_data = hist_data

    # implemented using np.dot not pd.dot to avoid issues with column names not matching indices names
    @staticmethod
    def _portfolio_returns(weights, security_returns):
        return np.dot(weights.T, security_returns)

    @staticmethod
    def _portfolio_std(weights, security_cov):
        return np.sqrt(np.dot(np.dot(weights.T, security_cov), weights))

    @classmethod
    def _return_over_risk(cls, weights, security_returns, security_cov):
        return cls._portfolio_returns(weights, security_returns) / cls._portfolio_std(weights, security_cov)

    @classmethod
    def _sharpe_ratio(cls, weights, security_returns, security_cov):
        return (cls._portfolio_returns(weights, security_returns) - cls.risk_free_rate) \
               / cls._portfolio_std(weights, security_cov)

    def _equal_weighted_portfolio(self):
        portfolio_weights = np.ones(len(self.hist_data.securities))
        portfolio_weights /= sum(portfolio_weights)
        return portfolio_weights

    def _random_weighted_portfolio(self):
        portfolio_weights = np.random.rand(len(self.hist_data.securities))
        portfolio_weights /= sum(portfolio_weights)
        return portfolio_weights

    def _optimal_weights_SQP(self, optimization):

        weights = self._equal_weighted_portfolio()  # initial guess of equal weighted portfolio

        if optimization == 'equal-weighted':
            return weights

        else:
            optimization_funcs = {'min-variance': {'func': self._portfolio_std,
                                                   'args': (self.hist_data.cov)},
                                  'return-over-risk': {'func': self.reverse(self._return_over_risk),
                                                       'args': (self.hist_data.mean,
                                                                self.hist_data.cov)},
                                  'sharpe-ratio': {'func': self.reverse(self._sharpe_ratio),
                                                   'args': (self.hist_data.mean,
                                                            self.hist_data.cov)}}
            #using reverse wrapper (* -1) with functions to maximize optimization below
            return minimize(fun=optimization_funcs[optimization]['func'], x0=weights,
                            args=optimization_funcs[optimization]['args'],
                            method='SLSQP',
                            bounds=Bounds(0, 1),
                            constraints=({'type': 'eq',
                                          'fun': lambda weights: 1.0 - np.sum(weights)}),
                            options={'maxiter': 1000})['x']

    def _optimal_weights_monte_carlo(self, optimization, simulations=10000):

        if optimization == 'equal-weighted':
            return self._equal_weighted_portfolio()

        else:
            simulated_portfolios = self._monte_carlo_simulation(simulations=simulations)
            """Need to split df in two: one with id + weights and one with id + stats because 'weights' is object 
            dtype and cannot apply idxmin/idxmax to df that includes object type """

            portfolio_stats = simulated_portfolios.drop(['weights'], axis=1)
            portfolio_weights = simulated_portfolios.drop(['returns', 'std', 'return_over_risk', 'sharpe_ratio'],
                                                          axis=1)
            simulated_portfolios.drop(['weights'], axis=1, inplace=True)
            optimization_funcs = {'min-variance': {'func': 'idxmin',
                                                   'col': 'std'},
                                  'return-over-risk': {'func': 'idxmax',
                                                       'col': 'return_over_risk'},
                                  'sharpe-ratio': {'func': 'idxmax',
                                                   'col': 'sharpe_ratio'}}

            optimal_portfolio_index = getattr(portfolio_stats, optimization_funcs[optimization]['func'])()[
                optimization_funcs[optimization]['col']]

            return portfolio_weights.iloc[optimal_portfolio_index-1, :][0]

    def _monte_carlo_simulation(self, simulations=10000):
        portfolio_list = []

        for i in range(simulations):
            id = i + 1
            weights = self._random_weighted_portfolio()
            returns = self._portfolio_returns(weights, self.hist_data.mean)
            std = self._portfolio_std(weights, self.hist_data.cov)
            return_over_risk = self._return_over_risk(weights, self.hist_data.mean, self.hist_data.cov)
            sharpe_ratio = self._sharpe_ratio(weights, self.hist_data.mean, self.hist_data.cov)
            portfolio_list.append([id, weights, returns, std, return_over_risk, sharpe_ratio])

        return pd.DataFrame(portfolio_list,
                            columns=['id', 'weights', 'returns', 'std', 'return_over_risk', 'sharpe_ratio']) \
            .set_index('id')

    def optimal_portfolio(self, method="monte-carlo", optimization="sharpe-ratio", simulations=20000):
        #TODO: 
        if method == 'monte-carlo':
            optimal_weights = self._optimal_weights_monte_carlo(optimization=optimization, simulations=simulations)
        elif method == 'SQP':
            optimal_weights = self._optimal_weights_SQP(optimization=optimization)
        else:
            raise Exception('Please choose a valid method')

        returns = self._portfolio_returns(optimal_weights, self.hist_data.mean)
        std = self._portfolio_std(optimal_weights, self.hist_data.cov)
        return_over_risk = self._return_over_risk(optimal_weights, self.hist_data.mean, self.hist_data.cov)
        sharpe_ratio = self._sharpe_ratio(optimal_weights, self.hist_data.mean, self.hist_data.cov)

        return {'optimal weights': list(optimal_weights), 'returns': returns, 'std': std,
                'return_over_risk': return_over_risk, 'sharpe_ratio': sharpe_ratio}

    @staticmethod
    def reverse(func):
        def wrapper_reverse(*args, **kwargs):
            return -1 * func(*args, **kwargs)
        return wrapper_reverse
    # wrapper in order to maximize sharpe ratio in SQP optimization function
