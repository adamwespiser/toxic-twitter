# Overview
`python make_predictions.py "tweet text"`    
This will load a keras model, and run it against the first argument.    
This will work without training the model, and you just need the contents of, "ascii-3-model", which contains the saved model and its weights.    


To train the model, look into `char-cnn-one-shot-ipynb`, which contains the model code to train against the kaggle dataset. Before you do that, you have to first download 'train.csv'  and 'test.csv' from here:    
https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge





