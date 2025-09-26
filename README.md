create a virtual env
```
python -m venv venv
```

install requirements.txt
```
pip install -r requirements.txt
```

make sure to have the tweets data set from https://www.kaggle.com/datasets/kazanova/sentiment140 and change the `DATA_PATH` var in `app.py` according to where your `.csv` file is.

and run the flask app
```
flask --app app run
```