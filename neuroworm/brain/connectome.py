from brain.neuron import Neuron


neurons = {

    # sensory

    "AWA": Neuron(threshold=1),
    "AWB": Neuron(threshold=1),

    # integration

    "AIB": Neuron(threshold=1),

    # behaviours

    "AVA": Neuron(threshold=1),  # avoid

    "AVB": Neuron(threshold=1),  # explore

    "RIM": Neuron(threshold=1),  # escape
}


connections = [

    {
        "from": "AWA",
        "to": "AIB",
        "weight": 2
    },

    {
        "from": "AWB",
        "to": "AIB",
        "weight": 1
    },

    {
        "from": "AIB",
        "to": "AVA",
        "weight": 2
    },

    {
        "from": "AIB",
        "to": "RIM",
        "weight": 2
    },

    {
        "from": "AWA",
        "to": "AVB",
        "weight": -1
    }
]