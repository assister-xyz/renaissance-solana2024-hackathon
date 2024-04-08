const express = require('express');
const axios = require('axios');
const cors = require('cors');
const cheerio = require('cheerio');
const app = express();
const { MongoClient } = require('mongodb');
const bodyParser = require('body-parser');
const ed25519 = require('@noble/curves/ed25519');
const bs58 = require('bs58');


app.use(cors());
app.use(express.json());

require('dotenv').config();

const MONGO_URI = process.env.MONGODB_URI;
const DB_NAME = process.env.MONGODB_NAME;

const client = new MongoClient(MONGO_URI);

function getUserIdFromLink(link) {
  const regex = /\/users\/(\d+)/;
  
  const matches = regex.exec(link);
  
  if (matches && matches.length > 1) {
      return Number(matches[1]);
  } else {
      return null;
  }
}

async function getUserById(userId) {
  try {
    await client.connect();

    const database = client.db(DB_NAME);
    const collection = database.collection('users');
    const user = await collection.findOne({ user_id: userId });
    return user;
  } finally {
    await client.close();
  }
}

async function updateUserWalletAddress(userId, walletAddress) {
  try {
    await client.connect();
    const database = client.db(DB_NAME);
    const collection = database.collection('users');
    await collection.updateOne(
      { user_id: userId },
      { $set: { wallet_address: walletAddress } }
    );
  }catch (error) {
    console.log(error.message)
  } finally {
    await client.close();
  }
}
app.post('/verify-stackoverflow', async (req, res) => {
  const { link, code } = req.body;
  if (!link || !code) {
    return res.status(400).json({ error: 'Stack Overflow link and unique code are required' });
  }

  try {
    const response = await axios.get(link);
    if (response.status === 200) {
      const $ = cheerio.load(response.data);
      const aboutSection = $('.js-about-me-content').text();
      const codePresent = aboutSection.includes(`Code: ${code}`);
      return res.json({ valid: codePresent });
    } else {
      return res.status(404).json({ error: 'About section not found' });
    }
  } catch (error) {
    return res.status(500).json({ error: 'Failed to fetch the profile page' });
  }
});

app.post('/total-upvotes', async (req, res) => {
  const { user_id} = req.body;
  if (!user_id) {
    return res.status(400).json({ error: 'Missing user_id or tag parameter' });
  }
  
  const user = await getUserById(getUserIdFromLink(user_id));
  return res.json({ total_upvotes: user['up_vote_count'] });
});


app.post('/verify-signature', async (req, res) => {
  try {
      const { signature, message, publicKey, userId } = req.body;
      const decodedMessage = bs58.decode(message);
      const decodedSignature = bs58.decode(signature);
      const decodedPublicKey = bs58.decode(publicKey);

      const isValid = ed25519.ed25519.verify(decodedSignature, decodedMessage, decodedPublicKey)
      if (isValid){
        await updateUserWalletAddress(getUserIdFromLink(userId), publicKey)
        console.log("Success")
      }
      res.json({ valid: isValid });
  } catch (error) {
      res.status(500).json({ error: error.message });
  }
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP' });
});

const port  = 3001;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
