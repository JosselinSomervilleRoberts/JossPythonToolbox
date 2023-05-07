from toolbox.log import Logger
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

l = Logger(verbose=True, save=True, tensorboard=True, save_path="logs")
l.log("Hello world!")
l.log("Damn, this is cool!", "red")

# Small pytorch example
class Net(nn.Module):
    def __init__(self) -> None:
        super(Net, self).__init__()
        self.fc1 = nn.Linear(1, 1)
        self.fc2 = nn.Linear(1, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        l.debug(x, verbose=False)
        x1 = self.fc1(x)
        l.debug(x1, verbose=False)
        x2 = F.relu(x1)
        l.debug(x2, verbose=False)
        x3 = self.fc2(x2)
        l.debug(x3, verbose=False)
        return x3
    
net = Net()
optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)
criterion = nn.MSELoss()

for i in range(100):
    optimizer.zero_grad()
    output = net(torch.ones(1,1))
    loss = criterion(output, torch.ones(1,1)*2)
    loss.backward()
    optimizer.step()
    l.log_value("loss", loss.item())

# Log graph
l.log_graph(net, input_size=(1,1))

# Image example
# Generate a random image
img_HWC = np.zeros((100, 100, 3))
img_HWC[:, :, 0] = np.arange(0, 10000).reshape(100, 100) / 10000
img_HWC[:, :, 1] = 1 - np.arange(0, 10000).reshape(100, 100) / 10000
l.log_image("random_image", img_HWC)

# Histogram example
# Generate a random histogram
hist = np.random.randint(0, 100, (100, 100))
l.log_histogram("random_histogram", hist)

# Save model
l.save_model(net, "best")