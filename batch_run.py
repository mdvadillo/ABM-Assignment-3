from model import SegModel
from mesa.batchrunner import FixedBatchRunner
import json 
import pandas as pd
from itertools import product
import numpy as np

# parameters that will remain constant
fixed_parameters = {
    "height": 16,
    "width": 16,
    "num_agents": 200,
    "minority_pc_1": 0.4, 
    "minority_pc_2": 0.4, 
    "stopping_level":1
}

# parameters you want to vary
# can also include combinations here
params = {"intolerance_1": [*np.arange(0.125, 1, 0.125)],
            "intolerance_2": [*np.arange(0.125, 1, 0.125)]}


# combine all the parameters you want to combine using this function
def dict_product(dicts): #could just use the below but it's cleaner this way
    """
    >>> list(dict_product(dict(number=[1,2], character='ab')))
    [{'character': 'a', 'number': 1},
     {'character': 'a', 'number': 2},
     {'character': 'b', 'number': 1},
     {'character': 'b', 'number': 2}]
    """
    return (dict(zip(dicts, x)) for x in product(*dicts.values()))

parameters_list = [*dict_product(params)]

# what to run and what to collect
# iterations is how many runs per parameter value
# max_steps is how long to run the model
batch_run = FixedBatchRunner(SegModel, parameters_list,
                             fixed_parameters, iterations=10,
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
                                            "Intolerance_2": lambda m: m.intolerance_2},
                             max_steps=50)

# run the batches of your model with the specified variations
batch_run.run_all()


## NOTE: to do data collection, you need to be sure your pathway is correct to save this!
# Data collection
# extract data as a pandas Data Frame
batch_df = batch_run.get_model_vars_dataframe()

# export the data to a csv file for graphing/analysis
batch_df.to_csv("seg_model_batch_run_data.csv")