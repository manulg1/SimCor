# SimCor
# non-correlated and correlated (Cholesky transformation) price/value simulation

1
The first function of this package allow user to simulate the evolution of the price/value of an index or asset. It can be made applying two different techniques:
- Monte carlo simulation: MC only uses the asset’s daily volatility to make X simulations of the Y following values.
- Brownian motion simulation: GBM uses the concept of Geometric Brownian Motion to make X simulations of the Y following values

2
However, we need to simulate the evolution of different assets or indexes that are highly correlated. In this cases, it is necesary to follow 3 different steps:
- First, the variance-covariance matrix is used to measure the linear relationships between them.
- Then, the evolution is simulated for each asset independently.
- Finally, Cholesky transformation is used to transform the set of uncorrelated variables into variables with given covariances [1]. (This shoul be done by correlating the expected evolution and applying it to the previous value consecutively)


There are several examples of easy transformations [2] but this package allows users to correlate a big number of simulation one by one, for all the correlated assets.
