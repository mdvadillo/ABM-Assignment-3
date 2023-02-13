# can choose to just import mesa or to do these and streamline code a little
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


# set up and initialize the agents
class SegAgent(Agent):
    def __init__(self, pos, model, agent_type_1, agent_type_2):  # agents and their characteristics
        super().__init__(pos, model)
        self.pos = pos
        self.type_1 = agent_type_1
        self.type_2 = agent_type_2
        self.similar_dim_1 = 0  # agent-specific measures of neighbor similarity
        self.similar_dim_2 = 0
        self.total_similar = 0
        self.similar_dim1_0 = 0
        self.similar_dim1_1 = 0
        self.similar_dim2_0 = 0
        self.similar_dim2_1 = 0
        self.neighbors_a = 0  # count of neighbors for each agent (ignore empty squares)
        self.a_pct_similar_dim1 = 0 # calculate neighbor percents
        self.a_pct_similar_dim2 = 0  

    # describe what happens in each step for the agents
    # agents check surroundings and count neighbors of the same type, by dimension
    def step(self):
        self.similar_dim_1 = 0  # reset these counters each time step
        self.similar_dim_2 = 0
        self.total_similar = 0    # haven't used this yet
        self.similar_dim1_0 = 0
        self.similar_dim1_1 = 0
        self.similar_dim2_0 = 0
        self.similar_dim2_1 = 0
        self.neighbors_a = 0
        self.a_pct_similar_dim1 = 0
        self.a_pct_similar_dim2 = 0

        # get neighbors and determine if your intolerance threshold is met
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            self.neighbors_a += 1

            if neighbor.type_1 == self.type_1:
                self.similar_dim_1 += 1      # counting those with equal attributed in dim 1

                if self.type_1 == 0:
                    self.similar_dim1_0 += 1

                elif self.type_1 == 1:
                    self.similar_dim1_1 += 1
                
            if neighbor.type_2 == self.type_2: # look at second dimension of similarity
                self.similar_dim_2 += 1      # counting those with equal attributed in dim 2

                if self.type_2 == 0:
                    self.similar_dim2_0 += 1

                elif self.type_2 == 1:
                    self.similar_dim2_1 += 1  

        # If unhappy in either category, move to an empty space on the grip:
        if self.similar_dim_1 < 8*(self.model.intolerance_1) or self.similar_dim_2 < 8*(self.model.intolerance_2):
            self.model.grid.move_to_empty(self) 
        
        # if happy, stay. Calculate happiness measurements for tracking
        else:
            self.model.happy += 1
            # happiness model trackers in the first dimension
            if self.type_1 == 0:
                self.model.happy_dim1_0 += 1
            else: 
                self.model.happy_dim1_1 += 1
            
            #happiness model trackers in the second dimension
            if self.type_2 == 0:
                self.model.happy_dim2_0 += 1
            else: 
                self.model.happy_dim2_1 += 1

# still need to fix this
        if self.neighbors_a > 0:
            self.a_pct_similar_dim1 = round(100 * self.similar_dim_1 / self.neighbors_a, 1)
            self.a_pct_similar_dim2 = round(100 * self.similar_dim_2 / self.neighbors_a, 1)
        else:
            self.a_pct_similar_dim1 = 0
            self.a_pct_similar_dim2 = 0


