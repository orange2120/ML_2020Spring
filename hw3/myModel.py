
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset

class ImgDataset(Dataset):
    def __init__(self, x, y=None, transform=None):
        self.x = x
        # label is required to be a LongTensor
        self.y = y
        if y is not None:
            self.y = torch.LongTensor(y)
        self.transform = transform
    def __len__(self):
        return len(self.x)
    def __getitem__(self, index):
        X = self.x[index]
        if self.transform is not None:
            X = self.transform(X)
        if self.y is not None:
            Y = self.y[index]
            return X, Y
        else:
            return X

# my best model

class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        #torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        #torch.nn.MaxPool2d(kernel_size, stride, padding)
        #input 維度 [3, 128, 128]
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, 3, 1, 1),  # [64, 128, 128]
            nn.BatchNorm2d(64),
            nn.ReLU(),
            # nn.Conv2d(64, 64, 3, 1, 1),  # [64, 128, 128]
            # nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [64, 64, 64]

            # nn.Dropout(0.2),

            nn.Conv2d(64, 128, 3, 1, 1), # [128, 64, 64]
            nn.BatchNorm2d(128),
            nn.ReLU(),
            # nn.Conv2d(128, 128, 3, 1, 1), # [128, 64, 64]
            # nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [128, 32, 32]

            # nn.Dropout(0.2),

            nn.Conv2d(128, 256, 3, 1, 1), # [256, 32, 32]
            nn.BatchNorm2d(256),
            nn.ReLU(),
            # nn.Conv2d(256, 256, 3, 1, 1), # [256, 32, 32]
            # nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),      # [256, 16, 16]

            # nn.Dropout(0.2),

            nn.Conv2d(256, 512, 3, 1, 1), # [512, 16, 16]
            nn.ReLU(),
            # nn.Conv2d(512, 512, 3, 1, 1), # [512, 16, 16]
            # nn.ReLU(),
            nn.BatchNorm2d(512),
            nn.MaxPool2d(2, 2, 0),       # [512, 8, 8]

            # nn.Dropout(0.2),
            
            nn.Conv2d(512, 512, 3, 1, 1), # [512, 8, 8]
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [512, 4, 4]
        )
        self.fc = nn.Sequential(
            # nn.Linear(512*4*4, 1024),
            nn.Linear(512*4*4, 5120),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(5120, 2048),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(2048, 512),
            # nn.Linear(1024, 256),
            # nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(512, 11),
            # nn.Linear(512, 11),
            # nn.Softmax(dim=1)
        )
        
    def forward(self, x):
        out = self.cnn(x)
        out = out.view(out.size()[0], -1)
        return self.fc(out)

'''
# my model 2 : add more conv2d layer
class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        #torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        #torch.nn.MaxPool2d(kernel_size, stride, padding)
        #input 維度 [3, 128, 128]
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 64, 3, 1, 1),  # [64, 128, 128]
            nn.BatchNorm2d(64),
            nn.ReLU(),

            # nn.Conv2d(64, 64, 3, 1, 1),  # [64, 128, 128]
            # nn.BatchNorm2d(64),
            # nn.ReLU(),

            nn.MaxPool2d(2, 2, 0),      # [64, 64, 64]

            # nn.Dropout(0.2),

            nn.Conv2d(64, 128, 3, 1, 1), # [128, 64, 64]
            nn.BatchNorm2d(128),
            nn.ReLU(),

            nn.Conv2d(128, 128, 3, 1, 1), # added layer
            nn.BatchNorm2d(128),
            nn.ReLU(),
            
            nn.MaxPool2d(2, 2, 0),      # [128, 32, 32]
            # nn.Dropout(0.2),

            nn.Conv2d(128, 256, 3, 1, 1), # [256, 32, 32]
            nn.BatchNorm2d(256),
            nn.ReLU(),

            nn.Conv2d(256, 256, 3, 1, 1), # added layer
            nn.BatchNorm2d(256),
            nn.ReLU(),
            
            nn.MaxPool2d(2, 2, 0),      # [256, 16, 16]

            # nn.Dropout(0.2),

            nn.Conv2d(256, 512, 3, 1, 1), # [512, 16, 16]
            nn.BatchNorm2d(512),
            nn.ReLU(),

            # nn.Conv2d(512, 512, 3, 1, 1), # # added layer
            # nn.ReLU(),
            # nn.BatchNorm2d(512),

            nn.MaxPool2d(2, 2, 0),       # [512, 8, 8]

            # nn.Dropout(0.2),
            
            nn.Conv2d(512, 512, 3, 1, 1), # [512, 8, 8]
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),       # [512, 4, 4]
        )
        self.fc = nn.Sequential(
            # nn.Linear(512*4*4, 1024),
            nn.Linear(512*4*4, 5120),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(5120, 2048),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(1024, 512),
            # nn.Linear(1024, 256),
            # nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(512, 11),
            # nn.Linear(512, 11),
            # nn.Softmax(dim=1)
        )
'''


