# ABM-Assignment-1

The [agents.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/agents.py) contains code for agents' behavior. We have 4 types of agents overall. Each agent gets assigned one of two groups in each dimension, in a model with two dimensions total. For explanation purposes, below we call the agents in the minority "In", and the agents not in the minority (in the majority) "Out". With this convention, agents can have the following types:

Dimension 1\2 | In | Out 
--- | --- | --- 
In | (1,1) | (0,1) 
Out | (1,0) | (0,0) 

[model.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/model.py) constains the model, takes in model parameters and creates the agents. Here, we added a way to specify the agents' type in the second dimension: we draw from a bernoulli distribution with probability p = probability of being in group A (user-settable parameter). We also added a (user-settable) model parameter for a "stopping point", that allows the simulation to end before 100% happiness is reached -- user can set what proportion of agents needs to be happy in order to stop the simulation. 

[server.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/server.py)  creates the visualization. We added some slider user-settable parameters (proportion that belongs to group A in second dimension, intolerance level for the second dimension, and simulation stopping point).

[run.py](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/model.py)  runs the model.

in [Assignment_1_Write_Up.pdf](https://github.com/mdvadillo/ABM-Assignment-1/blob/main/Assignment_1_Write_Up.pdf) you will find the paper we wrote explaining our changes to the model and a brief look at some results. 
