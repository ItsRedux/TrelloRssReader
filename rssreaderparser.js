const express = require('express');
const Trello = require('node-trello');
const Parser = require('rss-parser');
const dotenv = require('dotenv');

const app = express();
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send(`
    <form method="POST">
      <label for="api_key">Clé API :</label><br>
      <input type="text" id="api_key" name="api_key"><br>
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
  `);
});

app.post('/', async (req, res) => {
  const { api_key, token, board_id, list_id, feed_url } = req.body;

  // Stocke les valeurs du formulaire en tant que variables d'environnement
  process.env.TRELLO_API_KEY = api_key;
  process.env.TRELLO_TOKEN = token;

  // Charge les variables d'environnement
  dotenv.config();

  // Initialise le client Trello avec les clés d'API stockées dans les variables d'environnement
  const trello = new Trello(process.env.TRELLO_API_KEY, process.env.TRELLO_TOKEN);

  const parser = new Parser();
  const feed = await parser.parseURL(feed_url);

  feed.items.forEach(item => {
    // Crée une carte pour chaque article du flux RSS
    trello.post(`/1/lists/${list_id}/cards`, { name: item.title, desc: item.link });
  });

  res.redirect('/');
});

app.listen(3000, () => console.log('App is listening on port 3000'));
