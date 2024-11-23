import asyncio
import time

import torch
import chromadb
import numpy as np

from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
from chromadb.errors import InvalidCollectionException

# Докумантация ChromaDB
# https://docs.trychroma.com/guides#filtering-by-metadata:~:text=You%20can%20query%20by%20a%20set%20of