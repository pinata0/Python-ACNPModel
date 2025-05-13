import torch
import torch.nn as nn
from torch_geometric.nn import GATConv

class EventEncoder(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(EventEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU()
        )

    def forward(self, event_features):
        return self.encoder(event_features)  # [num_companies, hidden_dim]

class TemporalEncoder(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(TemporalEncoder, self).__init__()
        self.rnn = nn.GRU(input_dim, hidden_dim, batch_first=True)

    def forward(self, time_series):
        # time_series: [num_companies, time_steps, input_dim]
        _, h_n = self.rnn(time_series)
        return h_n.squeeze(0)  # [num_companies, hidden_dim]

class AgentInteractionLayer(nn.Module):
    def __init__(self, hidden_dim, heads=2):
        super(AgentInteractionLayer, self).__init__()
        self.gat = GATConv(hidden_dim, hidden_dim, heads=heads, concat=False)

    def forward(self, node_features, edge_index):
        return self.gat(node_features, edge_index)  # [num_companies, hidden_dim]

class ImpactPredictor(nn.Module):
    def __init__(self, hidden_dim, output_dim):
        super(ImpactPredictor, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, fused_features):
        return self.fc(fused_features)

class AgentEventImpactModel(nn.Module):
    def __init__(self, event_dim, price_dim, hidden_dim, output_dim):
        super(AgentEventImpactModel, self).__init__()
        self.event_encoder = EventEncoder(event_dim, hidden_dim)
        self.temporal_encoder = TemporalEncoder(price_dim, hidden_dim)
        self.interaction_layer = AgentInteractionLayer(hidden_dim)
        self.predictor = ImpactPredictor(hidden_dim, output_dim)

    def forward(self, event_features, time_series, edge_index):
        # [N, T, D_price], [N, D_event], edge_index [2, E]
        e_encoded = self.event_encoder(event_features)
        t_encoded = self.temporal_encoder(time_series)
        node_features = e_encoded + t_encoded

        interaction_out = self.interaction_layer(node_features, edge_index)
        return self.predictor(interaction_out)
