import torch
import torch.nn as nn

class Estimator():
    @abstractmethod
    def returnShadeValue(self, *args):
        pass

class AlgorithmicEstimatedReach(Estimator):
    pass


'''
Recurrent network implementation. The idea of this is to utilize deep learning to
gain a meaning representation of previous states to yield a shading value. This value
is then multiplied to the bid to determine how much we should pay for any given
moment. 

This was to be trained in recurrent.ipynb, but idea was not implemented because
of concerns of the objective function. 
'''
class RecurrentEstimator(Estimator):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(RecurrentEstimator, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.gru_layer = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True)
        self.hidden_state = torch.zeros(self.num_layers, 1, self.hidden_dim)
        self.output_layer = nn.Linear(hidden_dim, output_dim)    
        
    def reset(self):
        self.hidden_state = torch.zeros(self.num_layers, 1, self.hidden_dim)

    def forward(self, x):
        out, self.hidden_state = self.gru_layer(x, self.hidden_state.detach())  # Using the internal state
        out = self.output_layer(out[:, -1, :]) 
        return out

    @staticmethod
    def returnShadeValue(self, *args):
        return self.forward(args)

        