# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""
# import basics
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen
from better_profanity import profanity
# load up a model from memory. Note you may not need all of these options
'''
tv_summary_ai = aitextgen(model_folder="model/TV Show AI/TV Show Summary/", to_gpu=False)
tv_positive_ai = aitextgen(model_folder="model/TV Show AI/TV Show Positive/", to_gpu=False)
tv_negative_ai = aitextgen(model_folder="model/TV Show AI/TV Show Negative/", to_gpu=False)
movie_summary_ai = aitextgen(model_folder="model/movie models (rori)/movie_synopsis/", to_gpu=False)
movie_positive_ai = aitextgen(model_folder="model/movie models (rori)/positive/", to_gpu=False)
movie_negative_ai = aitextgen(model_folder="model/movie models (rori)/negative/", to_gpu=False)
anime_summary_ai = aitextgen(model_folder="model/Bob AI/Bob synopsis/", to_gpu=False)
anime_positive_ai = aitextgen(model_folder="model/Bob AI/Bob positive/", to_gpu=False)
anime_negative_ai = aitextgen(model_folder="model/Bob AI/Bob negative/", to_gpu=False)
'''


# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

profanity.load_censor_words()


@app.route(f'{base_url}')
def home(): # render hom page 
    return render_template('index.html', generated=None)


# create a function that renders about page
@app.route(f'{base_url}/about/')
def about():
    return render_template('about.html', generated=None)


# create a function that renders team page 
@app.route(f'{base_url}/team/')
def team():
    return render_template('team.html', generated=None)

# render the result page with generated text
@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('generator.html', generated=data)
    else:
        return render_template('generator.html', generated="This is where the description will appear")
    
    
def remove_curse_period(generated):
    for i in generated:
            if generated[-1] not in ['.','!','?']:
                generated=generated[:-1]
    generated = profanity.censor(generated)
    return generated

@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """
    prompt = request.form['prompt'] + " " # user input 

    # check with genre to generate
    if request.form['btn'] == "MOVIE":
        movie_summary_ai = aitextgen(model_folder="model/movie models (rori)/movie_synopsis/", to_gpu=False)
        movie_positive_ai = aitextgen(model_folder="model/movie models (rori)/positive/", to_gpu=False)
        movie_negative_ai = aitextgen(model_folder="model/movie models (rori)/negative/", to_gpu=False)
        generated_movie_summary = movie_summary_ai.generate_one(prompt=str(prompt), min_length=20, max_length=80, temperature = 1, no_repeat_ngram_size= 4)
        generated_movie_summary = remove_curse_period(generated_movie_summary)
        generated_movie_positive = movie_positive_ai.generate_one(prompt=str(prompt), min_length = 20, max_length = 120, temperature = 1, no_repeat_ngram_size = 4)
        generated_movie_positive = remove_curse_period(generated_movie_positive)
        generated_movie_negative = movie_negative_ai.generate_one(prompt=str(prompt), min_length=20, max_length=120, temperature = 1, no_repeat_ngram_size = 4)
        generated_movie_negative = remove_curse_period(generated_movie_negative)


        if request.form.get('positive_comments') and request.form.get('negative_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_movie_summary + "<br><h1>Positive: </h1>" + generated_movie_positive + "<br><h1>Negative: </h1>" + generated_movie_negative
        elif request.form.get('positive_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_movie_summary + "<br><h1>Positive: </h1>" + generated_movie_positive
        elif request.form.get('negative_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_movie_summary + "<br><h1>Negative: </h1>" + generated_movie_negative
        else:
            generated = "<h1>Summary: </h1>" + generated_movie_summary


    if request.form['btn'] == "TV SHOW":
        tv_summary_ai = aitextgen(model_folder="model/TV Show AI/TV Show Summary/", to_gpu=False)
        tv_positive_ai = aitextgen(model_folder="model/TV Show AI/TV Show Positive/", to_gpu=False)
        tv_negative_ai = aitextgen(model_folder="model/TV Show AI/TV Show Negative/", to_gpu=False)
        generated_tv_summary = tv_summary_ai.generate_one(prompt=str(prompt), min_length = 20, max_length = 50, temperature = 1, no_repeat_ngram_size = 4)
        generated_tv_summary = remove_curse_period(generated_tv_summary)
        generated_tv_positive = tv_positive_ai.generate_one(prompt=str(prompt), min_length = 20, max_length = 80, temperature = 1, no_repeat_ngram_size = 4)
        generated_tv_positive = remove_curse_period(generated_tv_positive)
        generated_tv_negative = tv_negative_ai.generate_one(prompt=str(prompt), min_length=20, max_length = 80, temperature = 1, no_repeat_ngram_size = 4)
        generated_tv_negative = remove_curse_period(generated_tv_negative)

        if request.form.get('positive_comments') and request.form.get('negative_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_tv_summary + "<br><h1>Positive: </h1>" + generated_tv_positive + "<br><h1>Negative: </h1>" + generated_tv_negative
        elif request.form.get('positive_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_tv_summary + "<br><h1>Positive: </h1>" + generated_tv_positive
        elif request.form.get('negative_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_tv_summary + "<br><h1>Negative: </h1>" + generated_tv_negative
        else:
            generated = "<h1>Summary: </h1>" + generated_tv_summary



    if request.form['btn'] == "ANIME":
        anime_summary_ai = aitextgen(model_folder="model/Bob AI/Bob synopsis/", to_gpu=False)
        anime_positive_ai = aitextgen(model_folder="model/Bob AI/Bob positive/", to_gpu=False)
        anime_negative_ai = aitextgen(model_folder="model/Bob AI/Bob negative/", to_gpu=False)
        generated_anime_summary =anime_summary_ai.generate_one(prompt=str(prompt), min_length = 30, max_length = 90, temperature = 1, no_repeat_ngram_size = 4)
        generated_anime_summary = remove_curse_period(generated_anime_summary)
        generated_anime_positive = anime_positive_ai.generate_one(prompt=str(prompt), min_length = 70, max_length = 120, temperature = 1, no_repeat_ngram_size = 4)
        generated_anime_positive = remove_curse_period(generated_anime_positive)
        generated_anime_negative = anime_negative_ai.generate_one(prompt=str(prompt), min_length=70, max_length=120, temperature = 1, no_repeat_ngram_size = 4)
        generated_anime_negative = remove_curse_period(generated_anime_negative)

        if request.form.get('positive_comments') and request.form.get('negative_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_anime_summary + "<br><h1>Positive: </h1>" + generated_anime_positive + "<br><h1>Negative: </h1>" + generated_anime_negative
        elif request.form.get('positive_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_anime_summary + "<br><h1>Positive: </h1>" + generated_anime_positive
        elif request.form.get('negative_comments'): # check sentiment
            generated = "<h1>Summary: </h1>" + generated_anime_summary + "<br><h1>Negative: </h1>" + generated_anime_negative
        else:
            generated = "<h1>Summary: </h1>" + generated_anime_summary


    data = {'generated_ls': generated}
    session['data'] = generated
    return redirect(url_for('results'))


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc6.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
