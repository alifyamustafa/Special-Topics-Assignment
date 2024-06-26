# -*- coding: utf-8 -*-
"""Special Topics Assignment-Alifya Mustafa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/183Nb8IEnqfPl3HUp_XZzSYvdosGADTbe
"""

pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sentence_transformers.quantization import quantize_embeddings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
from sklearn.linear_model import LogisticRegression

# 1. Specify preffered dimensions
dimensions = 512

# 2. load model
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", truncate_dim=dimensions)

# For retrieval you need to pass this prompt.
query = 'Represent this sentence for searching relevant passages: A man is eating a piece of bread'

df = pd.read_csv('dataset.csv')
print(df)

# Missing Values drop
df = df.dropna(subset=['text'])
# Convert into strings
df['text'] = df['text'].astype(str)

# 2. Encode
embeddings = model.encode(df['text'].tolist())

similarities = cos_sim(embeddings[0], embeddings[1:])
print('similarities:', similarities)

# Prepare the data
labels = df['sentiment'].values
binary_embeddings = quantize_embeddings(embeddings, precision="ubinary")
X = np.array(binary_embeddings)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Create classifier
classifier = LogisticRegression()

# Train the classifier on the training data
classifier.fit(X_train, y_train)

# Predict the sentiments for the testing set
y_pred = classifier.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Print the evaluation metrics
print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1 Score: {f1}')