#!/usr/bin/env python3
import argparse, os, torch, torchvision
from torchvision import transforms, datasets
from torch import nn, optim
from torch.utils.data import DataLoader

class SimpleFireCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3,16,3,2,1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16,32,3,2,1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32*8*8, 64), nn.ReLU(),
            nn.Linear(64, 2)
        )
    def forward(self, x): return self.net(x)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="dataset root with train/ and val/")
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--out", default="fire_cnn.pt")
    args = ap.parse_args()

    tfm = transforms.Compose([
        transforms.Resize((128,128)),
        transforms.ToTensor(),
    ])
    train_ds = datasets.ImageFolder(os.path.join(args.data,"train"), transform=tfm)
    val_ds   = datasets.ImageFolder(os.path.join(args.data,"val"), transform=tfm)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True)
    val_dl   = DataLoader(val_ds, batch_size=args.batch)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleFireCNN().to(device)
    opt = optim.Adam(model.parameters(), lr=args.lr)
    crit = nn.CrossEntropyLoss()

    for epoch in range(args.epochs):
        model.train()
        total, correct, loss_sum = 0, 0, 0.0
        for x,y in train_dl:
            x,y = x.to(device), y.to(device)
            opt.zero_grad()
            logits = model(x)
            loss = crit(logits, y)
            loss.backward()
            opt.step()
            loss_sum += float(loss)*x.size(0)
            pred = logits.argmax(1)
            correct += (pred==y).sum().item()
            total += x.size(0)
        train_acc = correct/total if total else 0.0
        model.eval()
        vtotal,vcorrect,vloss_sum=0,0,0.0
        with torch.no_grad():
            for x,y in val_dl:
                x,y = x.to(device), y.to(device)
                logits = model(x)
                loss = crit(logits, y)
                vloss_sum += float(loss)*x.size(0)
                pred = logits.argmax(1)
                vcorrect += (pred==y).sum().item()
                vtotal += x.size(0)
        val_acc = vcorrect/vtotal if vtotal else 0.0
        print(f"Epoch {epoch+1}/{args.epochs} | train_acc={train_acc:.3f} val_acc={val_acc:.3f}")
    torch.save(model.state_dict(), args.out)
    print("Saved:", args.out)

if __name__ == "__main__":
    main()
