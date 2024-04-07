const express = require('express');
const axios = require('axios');
const cors = require('cors');
const cheerio = require('cheerio');
const { ethers } = require('ethers');
const app = express();
const { MongoClient, ObjectId } = require('mongodb');


app.use(cors());
app.use(express.json());

require('dotenv').config();

const STACK_EXCHANGE_API_KEY = process.env.STACK_EXCHANGE_API_KEY;
const contractABI = [
  "function mint(address receiver, uint256 amount)",
];

const MONGO_URI = process.env.MONGODB_URI;
const DB_NAME = process.env.MONGODB_NAME;
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

const PRIVATE_KEY = process.env.PRIVATE_KEY;

const provider = new ethers.providers.JsonRpcProvider("https://polygon-mumbai.infura.io/v3/1573346842fe4ed68384624e8bf48e82"); // Use the appropriate network
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

const contract = new ethers.Contract(CONTRACT_ADDRESS, contractABI, wallet);

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

//
async function mintTokens(receiver, amount) {
  try {
      const tx = await contract.mint(receiver, amount);
      const displayAmount = amount/Math.pow(10, 18);
      await tx.wait();
      console.log(`Successfully minted ${displayAmount} tokens for ${receiver}`);
      return { success: true, message: `Successfully minted ${displayAmount} tokens for ${receiver}`, link: "https://mumbai.polygonscan.com/tx/"+tx["hash"] };
  } catch (error) {
      console.error("Error minting tokens:", error);
      return { success: false, message: "Error minting tokens" };
  }
}

app.post('/get-tokens', async (req, res) => { // add amount 
  const { user_id, signature} = req.body;
  
  if (!user_id || !signature) {
      return res.status(400).json({ error: "User ID, signature are required." });
  }

  try {
      const recoveredAddress = ethers.utils.verifyMessage(user_id, signature);
      const tag = "nearprotocol";
      var amount = (await fetchTotalUpvotes(user_id, tag)).toString();
      if (amount === "0"){
        amount = "1";
      }
      const parsedAmount = ethers.utils.parseUnits(amount, 18);
      const result = await mintTokens(recoveredAddress, parsedAmount);
      
      return res.status(200).json(result);
  } catch (error) {
      console.error(error);
      return res.status(500).json({ error: "Internal server error" });
  }
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP' });
});

const port  = 3001;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
