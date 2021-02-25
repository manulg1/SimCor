# -*- coding: utf-8 -*-
"""
@author: Manuel Luna
"""

import numpy as np
import math
import pandas as pd
import scipy


'''
Simulation process - 1 index

Based on: https://programmingforfinance.com/2017/11/monte-carlo-simulations-of-future-stock-prices-in-python/
'''  

# Init data: price or value evolution serie of one index and the returns
class random_simulation:
    def __init__(self, returns, prices):
        self.returns = returns.values
        self.prices = prices.values

    # Only uses the asset’s daily volatility to make X simulations of the Y following values
    def monte_carlo(self, num_simulations, predicted_days):
        returns = self.returns
        prices = self.prices
        
        last_price = prices[-1]
        
        simulation_df = pd.DataFrame()

        #Create Each Simulation as a Column in df
        for x in range(num_simulations):
            count = 0
            daily_vol = np.nanstd(returns)
            
            price_series = []
            
            #Append Start Value
            price = last_price
            price_series.append(price)
            
            #Series for Predicted Days
            for i in range(predicted_days):
                if count == 251:
                    break
                price = price_series[count] * math.exp(np.random.normal(0, daily_vol))
                price_series.append(price)
                count += 1
        
            simulation_df[x] = price_series
            self.simulation_df = simulation_df
            self.predicted_days = predicted_days


    # gbm uses the concept of Geometric Brownian Motion to make X simulations of the Y following values
    def brownian_motion(self, num_simulations, predicted_days):
        returns = self.returns
        prices = self.prices

        last_price = prices[-1]

        #Note we are assuming drift here
        simulation_df = pd.DataFrame()
        
        #Create Each Simulation as a Column in df
        for x in range(num_simulations):
            
            #Inputs
            count = 0
            avg_daily_ret = np.nanmean(returns)
            variance = np.nanvar(returns)
            
            daily_vol = np.nanstd(returns)
            daily_drift = avg_daily_ret - (variance/2)
            drift = daily_drift - 0.5 * daily_vol ** 2
            
            #Append Start Value    
            prices = []
            
            shock = drift + daily_vol * np.random.normal()
            prices.append(last_price)
            
            for i in range(predicted_days):
                if count == 251:
                    break
                shock = drift + daily_vol * np.random.normal()
                price = prices[count] * math.exp(shock)
                prices.append(price)
                
        
                count += 1
            simulation_df[x] = prices
            self.simulation_df = simulation_df
            self.predicted_days = predicted_days

'''
Correlated simulations - multi index

Applying Cholesky: https://quantcorner.wordpress.com/2018/02/09/generation-of-correlated-random-numbers-using-python/
'''

# Now the the init data is a dataframe with the price evolution of all the correlated index and another one with their respective returns. Furthermore we have to specify the number of observations to calculate the correlation.
# Then to apply monte carlo or gbm correlated simulation the correlation matrix will be needed
class cor_simulation:
    def __init__(self, returns, prices, cor_days):
        self.returns = returns
        self.prices = prices
        self.cordays = cor_days

    # Uses the asset’s daily volatility to make X simulations of the Y following values.
    def monte_carlo_cor_sim(self, num_simulations, predicted_days,  corm=0):
        results=[]
        
        if corm == 0:
            cor_m = self.prices.tail(self.cordays).corr()
        else:
            cor_m = corm
        
        # Simulate prices for each class
        for i in range(len(self.returns.columns)):
            returns1 = self.returns.iloc[:,i]
            prices1 = self.prices.iloc[:,i]
            
            # Simulation
            sim = random_simulation(returns1,prices1)
            sim.monte_carlo(num_simulations, predicted_days)
            # Save results
            results.append(sim.simulation_df)

        # Correlate each simulation applying cholesky to their returns
        # We take the X index for each simulation. Example: simualtion 32 take index 1,2,3..X
        for i in range(num_simulations):
            df_c = pd.DataFrame()
            # take each class in the selected simulation 
            for j in range(len(self.returns.columns)):
                df_c[j]=results[j].iloc[:,i]
            # values to returns 
            df_c1 = np.log(df_c) - np.log(df_c.shift(1))
            df_c1 = df_c1.replace([np.inf, -np.inf], np.nan)
            # Apply Cholesky
            U= np.asmatrix(scipy.linalg.cholesky(cor_m))
            cU= df_c1 @ U
            cU= pd.DataFrame(cU)
            # Convert in values again
            cU.iloc[0,:]=df_c.iloc[0,:]
            for j in range(1, predicted_days+1):
                cU.iloc[j,:] = np.exp(cU.iloc[j,:]+np.log(cU.iloc[(j-1),:]))
            # Save new cor simulation values in the place of no-correlated ones 
            for j in range(len(self.returns.columns)):
                results[j].iloc[:,i]=cU[j]

        self.results_mc = results

    # gbm uses the concept of Geometric Brownian Motion to make X simulations of the Y following values
    def brownian_motion_cor_sim(self, num_simulations, predicted_days,  corm=0):
        results=[]
        
        if corm == 0:
            cor_m = self.prices.tail(self.cordays).corr()
        else:
            cor_m = corm
        
        # Simulate prices for each class
        for i in range(len(self.returns.columns)):
            returns1 = self.returns.iloc[:,i]
            prices1 = self.prices.iloc[:,i]
            
            # Simulation
            sim = random_simulation(returns1,prices1)
            sim.brownian_motion(num_simulations, predicted_days)
            # Save results
            results.append(sim.simulation_df)

        # Correlate each simulation applying cholesky to their returns
        # We take the X index for each simulation. Example: simualtion 32 take index 1,2,3..X
        for i in range(num_simulations):
            df_c = pd.DataFrame()
            # take each class in the selected simulation 
            for j in range(len(self.returns.columns)):
                df_c[j]=results[j].iloc[:,i]
            # Values to returns 
            df_c1 = np.log(df_c) - np.log(df_c.shift(1))
            df_c1 = df_c1.replace([np.inf, -np.inf], np.nan)
            # Apply Cholesky
            U= np.asmatrix(scipy.linalg.cholesky(cor_m))
            cU= df_c1 @ U
            cU= pd.DataFrame(cU)
            # Convert in values again
            cU.iloc[0,:]=df_c.iloc[0,:]
            for j in range(1, predicted_days+1):
                cU.iloc[j,:] = np.exp(cU.iloc[j,:]+np.log(cU.iloc[(j-1),:]))
            # Save new cor simulation values in the place of no-correlated ones 
            for j in range(len(self.returns.columns)):
                results[j].iloc[:,i]=cU[j]

        self.results_gbm = results
