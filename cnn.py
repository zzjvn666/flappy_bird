import os
import torch
from torchvision import transforms, models
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from torch import nn, optim
import torch.nn.functional as F
from tqdm import tqdm


class CustomDataset(Dataset):
    def __init__(self, img_dir, pos_file, transform=None):
        self.img_dir = img_dir
        self.pos_file = pos_file
        self.transform = transform
        self.img_files = sorted(os.listdir(img_dir))
        self.pos_data = pd.read_csv(pos_file, header=None).values

    def __len__(self):
        return len(self.img_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_files[idx])
        from PIL import Image
        try:
            image = Image.open(img_path)
        except Exception:
            image = torch.load(img_path)

        pos = torch.tensor(self.pos_data[idx], dtype=torch.float32)

        if self.transform:
            if isinstance(image, torch.Tensor):
                image = self.transform.transforms[1:](image)
            else:
                image = self.transform(image)

        return image, pos


img_dir = 'imgs'
pos_file = 'pos.txt'
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # ResNet 输入通常为 224x224
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
dataset = CustomDataset(img_dir, pos_file, transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 使用预训练的 ResNet18 模型
model = models.resnet18(pretrained=True)
# 修改最后一层全连接层以适应回归任务
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    # 使用 tqdm 显示进度条
    with tqdm(dataloader, unit="batch") as tepoch:
        for inputs, labels in tepoch:
            tepoch.set_description(f"Epoch {epoch + 1}")
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            tepoch.set_postfix(loss=loss.item())

    print(f'Epoch {epoch + 1}, Loss: {running_loss / len(dataloader)}')

# 保存模型参数
torch.save(model.state_dict(), 'trained_model.pth')

# 模型评价
model.eval()
total_mae = 0.0
total_mse = 0.0
num_samples = 0

with torch.no_grad():
    with tqdm(dataloader, unit="batch") as tepoch:
        for inputs, labels in tepoch:
            tepoch.set_description("Evaluating")
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)

            mse = criterion(outputs, labels)
            mae = nn.L1Loss()(outputs, labels)

            total_mse += mse.item()
            total_mae += mae.item()
            num_samples += inputs.size(0)
            tepoch.set_postfix(mse=mse.item(), mae=mae.item())

print(f'Average MSE: {total_mse / num_samples}')
print(f'Average MAE: {total_mae / num_samples}')