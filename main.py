from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request


app = Flask(__name__,static_folder='templates/assets',)
def get_details(movieid, year, poster, title):
    def process(n):
        try:
            arr = n.split("\n")
            arr2 = []
            for i in range(len(arr)):
                arr[i] = arr[i].strip()
                if arr[i]!="" and arr[i]!="Edit":
                    arr2.append(arr[i]) 
            #print(arr)
            return arr2[:-1]
        except:
            return "None"
    def op(req):
        try:
            arr = process(req[0].text)
            rating = arr[2].split(" ")
            actual_votes = rating[0]
            total_votes = rating[2]
            percentage = int((int(actual_votes)/int(total_votes))*100)
            result_single = {"category":arr[0], "type":arr[1], "actual_votes":actual_votes, "total_votes":total_votes,"percentage":percentage, "details":arr[13:]}
            return result_single
        except:
            return "None"
        
    req = requests.get(f"https://www.imdb.com/title/{movieid}/parentalguide")

    #print(req.text)
    bs1 = BeautifulSoup(req.text, 'html.parser')
    nudity = bs1.find_all("section", id='advisory-nudity')
    voilence = bs1.find_all("section", id='advisory-violence')
    profanity = bs1.find_all("section", id='advisory-profanity')
    alcohol = bs1.find_all("section", id='advisory-alcohol')
    frightening = bs1.find_all("section", id='advisory-frightening')
    nudity_dict = op(nudity)
    voilence_dict = op(voilence)
    profanity_dict = op(profanity)
    alcohol_dict = op(alcohol)
    frightening_dict = op(frightening)
    result = {"nudity":nudity_dict, "voilence":voilence_dict, "profanity":profanity_dict, "alcohol":alcohol_dict, "frightening":frightening_dict, "poster":poster, "year":year, "title":title, "movieid":movieid}
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=="POST":
        name = request.form['query']
        req = requests.get("https://virajapi.herokuapp.com/movie/?query="+name).json()
        if req["Response"]=="False":
            return "No movies found :("
        return render_template("results.html", para=req["Search"])
    return render_template("index.html")

@app.route("/movie")
def movie():
    movieid = request.args.get("id")
    year = request.args.get("year")
    poster = request.args.get("poster")
    title = request.args.get("title")
    result = get_details(movieid, year, poster, title)
    return render_template("movie.html", result=result)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
