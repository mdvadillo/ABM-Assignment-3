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

# difference in dimension 1 are portrayed by color -- purples are majority, blues are minority 
# difference in dimension 2 are protrayed by shape -- circle is majority, square in minority 
    if agent.type_1 == 1 and agent.type_2 == 0:
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.5"
        portrayal["Color"] = "steelblue"
    elif agent.type_1 == 0 and agent.type_2 == 0:
        portrayal["Shape"] = "circle"
        portrayal["r"] = "0.5"
        portrayal["Color"] = "darkmagenta"
    elif agent.type_1 == 1 and agent.type_2 == 1:
        portrayal["Shape"] = "rect"
        portrayal["w"] = "0.3"
        portrayal["h"] = "0.3"
        portrayal["Color"] = "lightskyblue"
    elif agent.type_1 == 0 and agent.type_2 == 1:
        portrayal["Color"] = "orchid"
        portrayal["Shape"] = "rect"
        portrayal["w"] = "0.3"
        portrayal["h"] = "0.3"
    

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
    "num_agents": UserSettableParameter('slider', "Number of Agents", 
                                      int(0.8 * SegModel.height ** 2), 10, 
                                      SegModel.height * SegModel.width, 10),
    "minority_pc_1": UserSettableParameter('slider', "% Minority group in 1st dimension", 0.35, 0.00, 1.0, 0.05),
    "minority_pc_2": UserSettableParameter('slider', "% Minority group in 2nd dimension", 0.35, 0.00, 1.0, 0.05),
    "intolerance_1": UserSettableParameter('slider', "Intolerance on 1st dimension: (Minimum % of matching neighbors)",
                                          0.375, 0, 1, 0.125),
    "intolerance_2": UserSettableParameter('slider', "Intolerance on 2nd dimension: (Minimum % of matching neighbors)" ,
                                          0.375, 0, 1, 0.125),
    "stopping_level": UserSettableParameter('slider', "Porportion of happy agents at which simulation stops" ,
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
