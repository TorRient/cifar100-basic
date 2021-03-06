import torch
import uvicorn
from PIL import Image
from torchvision import models
from transform_utils import transform
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# create a ResNet model
model = torch.hub.load("chenyaofo/pytorch-cifar-models", "cifar100_mobilenetv2_x1_4", pretrained=True)
model.eval()

@app.post('/predict')
async def predict(image_c: UploadFile=File(...)):
    """Return top 5 predictions ranked by highest probability.

    Parameters
    ----------
    :param image: uploaded image
    :type image: jpg
    :rtype: list
    :return: top 5 predictions ranked by highest probability
    """
    img = Image.open(image_c.file).convert('RGB')
    # load the image, pre-process it, and make predictions
    batch_t = torch.unsqueeze(transform(img), 0)
    out = model(batch_t)
    with open('imagenet_classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]

    # return the top 5 predictions ranked by highest probabilities
    prob = torch.nn.functional.softmax(out, dim = 1)[0] * 100
    _, indices = torch.sort(out, descending = True)
    return {
        "labels":[(classes[idx], prob[idx].item()) for idx in indices[0][:5]]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)