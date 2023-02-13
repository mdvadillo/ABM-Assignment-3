from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import SegModel



# define and set up agent visualization
def schelling_draw(agent):
    if agent is None:
        return
    portrayal = {"Filled": "true", "Layer": 0}

    if agent.type_1 == 0 and agent.type_2 == 1:
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.5"
        portrayal["Color"] = "steelblue"
    elif agent.type_1 == 1 and agent.type_2 == 1:
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.5"
        portrayal["Color"] = "darkmagenta"
    elif agent.type_1 == 0 and agent.type_2 == 0:
        portrayal["Shape"] = "rect"
        portrayal["w"] = "0.3"
        portrayal["h"] = "0.3"
        portrayal["Color"] = "steelblue"
    elif agent.type_1 == 1 and agent.type_2 == 0:
        portrayal["Color"] = "darkmagenta"
        portrayal["Shape"] = "rect"
        portrayal["w"] = "0.3"
        portrayal["h"] = "0.3"

    if agent.type_2 == 1:
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.5"
    #else:
        #portrayal["Shape"] = "circle"
        #portrayal["r"] = "0.5"
    #elif agent.type_1 == 0 and agent.type_2 == 1:
        #portrayal["Color"] = "mediumseagreen"
    #elif agent.type_1 == 1 and agent.type_2 == 1:
        #portrayal["Color"] = "Black"

    return portrayal


# text elements we're calling
# these next portions allow for the values
# to appear in the gui for the model
class HappyElement(TextElement):

    def render(self, model):
        return "% Happy agents: " + str(round(
            (model.happy / model.num_agents) * 100, 1)) + "%"




# set up how and what we're calling for the gui
# canvas itself
canvas_element = CanvasGrid(schelling_draw, SegModel.height, SegModel.width, 500, 500)

# text elements
happy_element = HappyElement()

# various charts / reporting options
happy_chart = ChartModule([{"Label": "Pct Happy", "Color": "Black"}])


# set up how the visualization will look
model_params = {
    "height": SegModel.height,
    "width": SegModel.width,
    "num_agents": UserSettableParameter('slider', "Number Agents", 
                                      int(0.8 * SegModel.height ** 2), 10, 
                                      SegModel.height * SegModel.width, 10),
    "minority_pc_1": UserSettableParameter('slider', "% group B (first dimension)", 0.35, 0.00, 1.0, 0.05),
    "minority_pc_2": UserSettableParameter('slider', "Probability of being in group A in second dimension", 0.35, 0.00, 1.0, 0.05),
    "intolerance_1": UserSettableParameter('slider', "Intolerance on first dimension: (Desired % of matching neighbors)",
                                          0.375, 0, 1, 0.125),
    "intolerance_2": UserSettableParameter('slider', "Intolerance on second dimension: (Desired % of matching neighbors)" ,
                                          0.375, 0, 1, 0.125),
    "stopping_level": UserSettableParameter('slider', "Fraction of happy agents required to stop simulation" ,
                                          1, 0, 1, 0.1),
}

# this is where we call the different elements we're going to be visualizing
# it includes the model, the graph/grid/world, and our various charts
# it also features a name for the model and our relevant parameter values
server = ModularServer(
    SegModel,
    [canvas_element, happy_element,
     happy_chart],
    "Schelling's Segregation Model",
    model_params
)
