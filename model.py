# can choose to just import mesa or to do these and streamline code a little
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from agents import SegAgent
import numpy as np


# set up the model and initialize the world
class SegModel(Model):
    height = 16
    width = height

    # adding agents to the world
    def __init__(self, width, height, num_agents, minority_pc_1, minority_pc_2, intolerance_1, intolerance_2, stopping_level):
        self.num_agents = num_agents  # we're allowing these values to be set at each run
        self.minority_pc_1 = minority_pc_1
        self.minority_pc_2 = minority_pc_2
        self.intolerance_1 = intolerance_1
        self.intolerance_2 = intolerance_2
        self.width = width
        self.height = height
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.stopping_level = stopping_level

        # global measures for how agents are doing overall
        self.happy = 0
        self.happy_dim1_0 = 0
        self.happy_dim1_1 = 0
        self.happy_dim2_0 = 0
        self.happy_dim2_1 = 0
        
        # number of agents in each groups
        self.num_agents_dim1_1 = 0
        self.num_agents_dim1_0  = 0
        self.num_agents_dim2 = 0
        self.num_agents_dim2_d11 = 0
        self.num_agents_dim2_d10  = 0

        # similarity measures
        self.similar_dim1_g = 0  
        self.similar_dim1_g0 = 0  
        self.similar_dim1_g1 = 0  
        self.similar_dim2_g = 0  
        self.similar_dim2_g0 = 0  
        self.similar_dim2_g1 = 0  
        self.neighbors_g = 0
        self.neighbors_dim1_g0 = 0
        self.neighbors_dim1_g1 = 0
        self.neighbors_dim2_g0 = 0
        self.neighbors_dim2_g1 = 0

        # percent of similar neighbors
        self.pct_neighbors_dim1_0 = 0
        self.pct_neighbors_dim1_1 = 0
        self.pct_neighbors_dim2_0 = 0
        self.pct_neighbors_dim2_1 = 0


        # placing agents at random in the world
        # setting finite number of each agent type
        self.num_agents_dim1_1 = round(self.num_agents * self.minority_pc_1)
        self.num_agents_dim1_0 = self.num_agents - self.num_agents_dim1_1

        # get the total number of agents in the minority of dimension 2
        self.num_agents_dim2 = round(self.num_agents * self.minority_pc_2)
        # split it so half of them are in group 1 of dimension 1, and half on group 0 of dimension 1
        self.num_agents_dim2_d11 = round(self.num_agents_dim2/2)
        self.num_agents_dim2_d10 = self.num_agents_dim2 - self.num_agents_dim2_d11

        range_d20 = [*range(self.num_agents_dim1_1, self.num_agents_dim1_1 + self.num_agents_dim2_d10)]

        #setting agent types based on the numbers above
        for i in range(self.num_agents):
            if i < self.num_agents_dim1_1:
                self.agent_type_1 = 1
            else:
                self.agent_type_1 = 0

            if i < self.num_agents_dim2_d11 or i in range_d20:
                self.agent_type_2 = 1
            else:
                self.agent_type_2 = 0
            
            # setting agent's grid position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            agent = SegAgent(i, self, self.agent_type_1, self.agent_type_2)
            self.schedule.add(agent)
            self.grid.position_agent(agent, (x, y))

        self.running = True  # need this for batch runner

        # somewhat extensive data collection
        self.datacollector = DataCollector(
            model_reporters={"Pct Happy": lambda m: round(100 * m.happy / m.num_agents, 1),
                             "Pct Happy Group A dim 1": lambda m: round(100 * m.happy_dim1_0 / m.num_agents_dim1_0, 1),
                             "Pct Happy Group B dim 1": lambda m: round(100 * m.happy_dim1_1 / m.num_agents_dim1_1, 1),
                             "Pct Happy Group A dim 2": lambda m: round(100 * m.happy_dim2_0 / (m.num_agents - m.num_agents_dim2), 1),
                             "Pct Happy Group B dim 2": lambda m: round(100 * m.happy_dim2_1 / m.num_agents_dim2, 1),
                             "Avg pct similar neighbors (A) dim 1": lambda m: m.pct_neighbors_dim1_0,
                             "Avg pct similar neighbors (B) dim 1": lambda m: m.pct_neighbors_dim1_1,
                             "Avg pct similar neighbors (A) dim 2": lambda m: m.pct_neighbors_dim2_0,
                             "Avg pct similar neighbors (B) dim 2": lambda m: m.pct_neighbors_dim2_1,
                             "Num Agents": lambda m: m.num_agents,
                             "Num Agents (A) dim 1": lambda m: m.num_agents_dim1_0,
                             "Num Agents (B) dim 1": lambda m: m.num_agents_dim1_1,
                             "Num Agents (A) dim 2": lambda m: m.num_agents - m.num_agents_dim2,
                             "Num Agents (B) dim 2": lambda m: m.num_agents_dim2,
                             "Pct group B dim 1": lambda m: m.minority_pc_1,
                             "Intolerance_1": lambda m: m.intolerance_1,
                             "Pct group B dim 2": lambda m: m.minority_pc_2,
                             "Intolerance_2": lambda m: m.intolerance_2}
        )
        

    # define what happens in one step of the model
    # model stopped when all agents are happy
    def step(self):
        self.happy = 0  # Reset counter of happy agents
        self.happy_dim1_0 = 0  # Reset counter of happy agents
        self.happy_dim1_1 = 0  # Reset counter of happy agents
        self.happy_dim2_0 = 0  # Reset counter of happy agents
        self.happy_dim2_1 = 0  # Reset counter of happy agents
        self.similar_dim1_g = 0  # Reset counter of similar agents
        self.similar_dim1_g0 = 0  # Reset counter of similar agents
        self.similar_dim1_g1 = 0  # Reset counter of similar agents
        self.similar_dim2_g = 0  # Reset counter of similar agents
        self.similar_dim2_g0 = 0  # Reset counter of similar agents
        self.similar_dim2_g1 = 0  # Reset counter of similar agents
        self.neighbors_g = 0
        self.neighbors_dim1_g0 = 0
        self.neighbors_dim1_g1 = 0
        self.neighbors_dim2_g0 = 0
        self.neighbors_dim2_g1 = 0

 

        for agent in self.schedule.agents:
            self.neighbors_g += agent.neighbors_a
            self.similar_dim1_g += agent.similar_dim_1
            self.similar_dim2_g += agent.similar_dim_2

            if agent.type_1 == 0:
                self.neighbors_dim1_g0 += agent.neighbors_a
                self.similar_dim1_g0 += agent.similar_dim1_0
            else:
                self.neighbors_dim1_g1 += agent.neighbors_a
                self.similar_dim1_g1 += agent.similar_dim1_1

            if agent.type_2 == 0:
                self.neighbors_dim2_g0 += agent.neighbors_a
                self.similar_dim2_g0 += agent.similar_dim2_0
            else:
                self.neighbors_dim2_g1 += agent.neighbors_a
                self.similar_dim2_g1 += agent.similar_dim2_1
            

        self.schedule.step()
        self.datacollector.collect(self)

        # solves division by zero issue
        if self.neighbors_g == 0:
            self.pct_neighbors = 0
        else:
            #self.pct_neighbors = round(100 * self.similar_g / self.neighbors_g, 1)
            self.pct_neighbors_dim1_0 = round(100 * self.neighbors_dim1_g0 / self.neighbors_dim1_g0, 1)
            self.pct_neighbors_dim1_1 = round(100 * self.similar_dim1_g1 / self.neighbors_dim1_g1, 1)
            self.pct_neighbors_dim2_0 = round(100 * self.similar_dim2_g0 / self.neighbors_dim2_g0, 1)
            self.pct_neighbors_dim2_1 = round(100 * self.similar_dim2_g1 / self.neighbors_dim2_g1, 1)

        # stops the model when everyone is happy
        if self.happy >= self.stopping_level * self.schedule.get_agent_count():
            self.running = False


