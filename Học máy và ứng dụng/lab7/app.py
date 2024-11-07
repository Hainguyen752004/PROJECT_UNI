import streamlit as st
import torch
import torchvision
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torch.optim import SGD

# Set device
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Streamlit header
st.title("CIFAR-10 Classification with a Simple MLP")
st.write("This app trains a basic MLP model on the CIFAR-10 dataset and evaluates its performance.")

# Load and preprocess CIFAR-10 data
@st.cache_data
def load_data():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5,), std=(0.5,))
    ])
    trainset = torchvision.datasets.CIFAR10(root='./CIFAR10', train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=1024, num_workers=0, shuffle=True)
    testset = torchvision.datasets.CIFAR10(root='./CIFAR10', train=False, download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=1024, num_workers=0, shuffle=False)
    return trainloader, testloader

trainloader, testloader = load_data()

# Display example images
st.subheader("Example Images from CIFAR-10 Test Set")
def imshow(img):
    img = img * 0.5 + 0.5  # Unnormalize
    np_img = img.numpy()
    plt.imshow(np.transpose(np_img, (1, 2, 0)))
    st.pyplot(plt)

data_iter = iter(testloader)
images, labels = next(data_iter)
imshow(torchvision.utils.make_grid(images[:5]))

# Define the model
def get_model(n_features):
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(n_features, 256),
        nn.ReLU(),
        nn.Linear(256, 10)
    ).to(device)
    return model

# Initialize model, loss function, and optimizer
n_features = 32 * 32 * 3
model = get_model(n_features)
lr = 0.01
optimizer = SGD(params=model.parameters(), lr=lr)
loss_fn = nn.CrossEntropyLoss()

# Evaluation function
def evaluate(model, testloader, criterion):
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            test_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    test_loss /= len(testloader)
    return test_loss, accuracy

# Training loop
@st.cache_resource
def train_model():
    n_epochs = 10
    train_losses = []
    train_accuracies = []
    test_losses = []
    test_accuracies = []

    for epoch in range(n_epochs):
        model.train()
        running_loss = 0.0
        running_correct = 0
        total = 0
        for i, (inputs, labels) in enumerate(trainloader):
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            running_correct += (predicted == labels).sum().item()
            loss.backward()
            optimizer.step()

        epoch_accuracy = 100 * running_correct / total
        epoch_loss = running_loss / len(trainloader)
        test_loss, test_accuracy = evaluate(model, testloader, loss_fn)
        
        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_accuracy)
        test_losses.append(test_loss)
        test_accuracies.append(test_accuracy)
        
        st.write(f"Epoch {epoch+1}/{n_epochs}, Train Loss: {epoch_loss:.4f}, "
                 f"Train Acc: {epoch_accuracy:.2f}%, Test Loss: {test_loss:.4f}, "
                 f"Test Acc: {test_accuracy:.2f}%")
    
    return train_losses, train_accuracies, test_losses, test_accuracies

train_losses, train_accuracies, test_losses, test_accuracies = train_model()

# Plot Loss and Accuracy
st.subheader("Training Progress")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot losses
ax1.plot(train_losses, label='Train Loss')
ax1.plot(test_losses, label='Test Loss')
ax1.set_title("Loss per Epoch")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss")
ax1.legend()

# Plot accuracies
ax2.plot(train_accuracies, label='Train Accuracy')
ax2.plot(test_accuracies, label='Test Accuracy')
ax2.set_title("Accuracy per Epoch")
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Accuracy (%)")
ax2.legend()

st.pyplot(fig)

# Additional custom scaling functions and a simple linear layer for experimentation
import tensorflow as tf

def zScoreScaling(tensor):
    mean, variance = tf.nn.moments(tensor, axes=[0])
    std_dev = tf.sqrt(variance)
    return (tensor - mean) / std_dev

def minMaxScaling(tensor):
    tensor_min = tf.reduce_min(tensor, axis=0)
    tensor_max = tf.reduce_max(tensor, axis=0)
    return (tensor - tensor_min) / (tensor_max - tensor_min)

class Linear:
    def __init__(self, input_dim, output_dim):
        self.weight = torch.randn(output_dim, input_dim)
        self.bias = torch.randn(output_dim)

    def forward(self, x):
        return torch.matmul(x, self.weight.T) + self.bias

st.subheader("Custom Scaling and Linear Layer Example")
tensor_example = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
st.write("Example Tensor:")
st.write(tensor_example.numpy())

zscore = zScoreScaling(tf.convert_to_tensor(tensor_example.numpy()))
min_max = minMaxScaling(tf.convert_to_tensor(tensor_example.numpy()))
st.write("Z-score Scaling:")
st.write(zscore.numpy())
st.write("Min-Max Scaling:")
st.write(min_max.numpy())

tensor_linear = torch.tensor([1.0, 2.0, 3.0])
linear = Linear(3, 2)
output = linear.forward(tensor_linear)
st.write("Output from custom Linear layer:", output)
st.write("Weight:", linear.weight)
st.write("Bias:", linear.bias)
