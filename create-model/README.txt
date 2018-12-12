To train our char-RNN:
Note: This step will take you 3-4 hours, depending on your computer, and the notebook was run on a computer with a discrete GPU.

1) Go to https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data and download train.csv, put this files in a directory called "kaggle"
2) Run all the cells in the "build-and-export.ipynb" notebook. You can run this by installing Jyputer, and running the command "$ jupyter notebook" in this directory
3) "build-and-export.ipynb" will export our model into the directory, "ascii-3-model/"


To run our Char-RNN:

Note: this step does not requre you to have trained the model, we have 
1) run the following command in bash,
    $ python make_prediction.py <tweet>
    for instance you could run,
    $ python make_prediction.py "Thats one small step for a man, one giant leap for mankind"
2) The toxicity, along with whether the tweet is obsene, a threat, an insult, or identity hate  will be printed. For each category, the prediction is a number between 0 and 1. Where 0 is not a member of the cateogry, and 1 is likely to be a member of the category
