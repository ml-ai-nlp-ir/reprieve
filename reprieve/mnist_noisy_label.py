import torch
import torchvision
from torchvision import transforms
from torch.utils.data import Dataset

import numpy as np
import numpy.random as npr

from . dataset_wrappers import DatasetCache

FLAG = "[MNIST_NOISYGT]"

old_print = print
def print(*args, **kwargs):  # noqa: E302
    return old_print(FLAG, *args, **kwargs)


class MNISTNoisyLabelDataset(Dataset):
    def __init__(self, train=True, p_corrupt=0.1):
        self.p_corrupt = p_corrupt

        self.data = torchvision.datasets.MNIST(
            './data', train=train, download=True,
            transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))]))
        self.data = DatasetCache(self.data)

    def __getitem__(self, index):
        x, y = self.data[index]
        y_fake_probs = np.zeros((10,)) + self.p_corrupt / 9.
        y_fake_probs[int(y)] = 1 - self.p_corrupt
        # w/ prob 1 - p_corrupt, use right label,
        # else uniform over wrong labels
        y_fake = npr.choice(range(10), p=y_fake_probs)

        # make every 10th element a 1, starting at the sampled y_fake
        # i.e. make a tiled one-hot vector
        x_fake = torch.zeros_like(x).flatten()
        x_fake[y_fake::10] = 1
        return x_fake, y

    def __len__(self):
        return len(self.data)


if __name__ == "__main__":
    dataset = MNISTNoisyLabelDataset()
    import ipdb; ipdb.set_trace()
