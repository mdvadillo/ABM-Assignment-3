from model import SegModel

# Set your parameter values for one run
# Reminder that the model takes on these parameter values:
# width, height, num_agents, minority_pc, intolerance

#making them very intolerant
model = SegModel(16, 16, 200, 0.4, 0.4, 0.75, 0.75, 1)
for t in range(200):
    model.step()

# extract data as a pandas Data Frame
model_df = model.datacollector.get_model_vars_dataframe()

## NOTE: to do data collection, you need to be sure your pathway is correct to save this!
# export the data to a csv file for graphing/analysis
model_df.to_csv("seg_model_single_run_very_intolerant_data.csv")