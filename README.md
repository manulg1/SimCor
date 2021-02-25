# SimCor
### From non-correlated to correlated (Cholesky transformation) time-series simulation

1
The first function of this package allows users to simulate the evolution of, for example, a price time-series. It can be made by applying two different techniques:
- Monte Carlo simulation: It only uses the asset’s daily volatility to make X simulations of the Y following values.
- Brownian motion simulation: It uses the concept of Geometric Brownian Motion to make X simulations of the Y following values

2
However, sometimes it is necessary to simulate the evolution of different values that are highly correlated. In this case, it is necessary to follow 3 different steps:
- Firstly, we have to calculate the variance-covariance matrix, which is used to measure the linear relationships between them.
- Then, the evolution is simulated for each asset independently, as in the previous function.
- Lastly, the Cholesky transformation is used to transform the set of uncorrelated simulations to present a given relation [1]. (This should be done by correlating the expected evolution and applying it to the estimated values consecutively)


There are several examples of easy transformations [2] but this package allows users to correlate a big number of simulations one by one.
