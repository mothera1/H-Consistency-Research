import torch
import torch.nn as nn
import torch.optim as optim

from load_blob_pets import *
from blob_nn import Blob
from limited_nn import limited

def train(criterion, optimizer, model, epochs = 25):
    model.train()
    train_loss = []
    
    for epoch in range(epochs):
        tracking = []
        for i in trainloader:
            inputs, labels = map_labels(i)
            inputs, labels = inputs.to(device, non_blocking=True), labels.to(device, non_blocking=True)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            tracking.append(loss.item())
        
        train_loss.append(sum(tracking)/len(tracking))
        print(f'Epoch # {epoch+1} is complete!')
       
            
    return train_loss



device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

#model = Blob()
#model = CNN()
model = limited()
model.to(device)
class_weights = class_weights_dataloader.to(device)
#criterion = nn.CrossEntropyLoss()
criterion = nn.MultiMarginLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

history = train(criterion, optimizer, model)

PATH = './limited_Hinge.pth'
torch.save(model.state_dict(), PATH)

plt.plot(history, color='blue', marker='o')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.show()
