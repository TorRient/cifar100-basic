import torch
from PIL import Image
from torchvision import models
from backend.transform_utils import transform
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# create a ResNet model
resnet = models.resnet101(pretrained = True)
resnet.eval()

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
    out = resnet(batch_t)
    with open('backend/imagenet_classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]

    # return the top 5 predictions ranked by highest probabilities
    prob = torch.nn.functional.softmax(out, dim = 1)[0] * 100
    _, indices = torch.sort(out, descending = True)
    return {
        "labels":[(classes[idx], prob[idx].item()) for idx in indices[0][:5]]
    }
