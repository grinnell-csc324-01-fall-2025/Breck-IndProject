# Necessary libraries for image and data translation and manipulation
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import os
from PIL import Image



# File that will create a database for the game's data to be input into
# Then it will be manipulated and turned into understandable data for pytorch

