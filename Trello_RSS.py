from flask import Flask, request, render_template_string
import os
import feedparser
from dotenv import load_dotenv
from trello import TrelloClient

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        api_secret = request.form.get('api_secret')
        token = request.form.get('token')
        board_id = request.form.get('board_id')
        list_id = request.form.get('list_id')
        feed_url = request.form.get('feed_url')

        # Stocke les valeurs du formulaire en tant que variables d'environnement
        os.environ['TRELLO_API_KEY'] = api_key
        os.environ['TRELLO_API_SECRET'] = api_secret
        os.environ['TRELLO_TOKEN'] = token

        # Charge les variables d'environnement
        load_dotenv()

        # Initialise le client Trello avec les clés d'API stockées dans les variables d'environnement
        trello_client = TrelloClient(
            api_key=os.getenv('TRELLO_API_KEY'),
            api_secret=os.getenv('TRELLO_API_SECRET'),
            token=os.getenv('TRELLO_TOKEN'),
        )

        board = trello_client.get_board(board_id)
        trello_list = board.get_list(list_id)
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            # Crée une carte pour chaque article du flux RSS
            trello_list.add_card(name=entry.title, desc=entry.link)


    return render_template_string("""
    <form method="POST">
      <label for="api_key">Clé API :</label><br>
      <input type="text" id="api_key" name="api_key"><br>
      <label for="api_secret">Secret API :</label><br>
      <input type="text" id="api_secret" name="api_secret"><br>
      <label for="token">Token :</label><br>
      <input type="text" id="token" name="token"><br>
      <label for="board_id">ID du tableau :</label><br>
      <input type="text" id="board_id" name="board_id"><br>
      <label for="list_id">ID de la liste :</label><br>
      <input type="text" id="list_id" name="list_id"><br>
      <label for="feed_url">URL du flux RSS :</label><br>
      <input type="text" id="feed_url" name="feed_url"><br><br>
      <input type="submit" value="Submit">
    </form> 
    """)

if __name__ == '__main__':
    app.run(debug=True)
