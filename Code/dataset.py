import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np


class CancerDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.trasnform = transform
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        img_path = os.path.join(self.image_dir, self.images[index])
        mask_path = os.path.join(
            self.mask_dir, self.images[index].replace(".tif", ".png"))
        image = np.array(Image.open(img_path).convert("RGB"))
        mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
        # because we use sigmoid in our last activation
        mask[mask == 255.0] = 1.0

        if self.trasnform is not None:
            augmentation = self.trasnform(image=image, mask=mask)
            image = augmentation["image"]
            mask = augmentation["mask"]

        return image, mask
