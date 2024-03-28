const axios = require('axios');
const fs = require('fs');

const STACK_EXCHANGE_API_KEY = ''; 
const SITE = 'solana.stackexchange'; 


//By reputation

async function fetchTop100ByReputation() {
    const url = `https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=${SITE}&pagesize=100&key=${STACK_EXCHANGE_API_KEY}`;
    try {
        const response = await axios.get(url);
        return response.data.items;
    } catch (error) {
        console.error('Error fetching top 100 by reputation:', error.message);
        return [];
    }
}
  
async function fetchTopAcceptedByAuthor() {
    const url = `https://api.stackexchange.com/2.3/questions/answers?order=desc&sort=votes&site=${SITE}&pagesize=100&key=${STACK_EXCHANGE_API_KEY}`;
    try {
        const response = await axios.get(url);
        return response.data.items.filter(question => question.is_answered && question.accepted_answer_id !== null);
    } catch (error) {
        console.error('Error fetching top accepted by author:', error.message);
        return [];
    }
}
  
async function fetchTop100ByUpvotes() {
    const url = `https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=${SITE}&pagesize=100&filter=withbody&key=${STACK_EXCHANGE_API_KEY}`;
    try {
        const response = await axios.get(url);
        return response.data.items;
    } catch (error) {
        console.error('Error fetching top 100 by upvotes:', error.message);
        return [];
    }
}
  
async function fetchTop100QuestionAskers() {
    const url = `https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=${SITE}&pagesize=100&filter=total&key=${STACK_EXCHANGE_API_KEY}`;
    try {
        const response = await axios.get(url);

        const askerCounts = {};
        //I DON`t KNOW WHY IS IT NOW WORKING T_T
        response.data.items.forEach(question => {
            const askerId = question.owner.user_id;

            if (askerCounts[askerId]) {
                askerCounts[askerId]++;
            } else {
                askerCounts[askerId] = 1;
            }
        });

        const sortedAskers = Object.entries(askerCounts)
            .sort((a, b) => b[1] - a[1]) 
            .slice(0, 100); 
        
        return sortedAskers;
    } catch (error) {
        console.error('Error fetching top 100 question askers:', error.message);
        return [];
    }
}
  
async function fetchPeopleWhoEverAskedQuestion() {
    const url = `https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=${SITE}&pagesize=100&key=${STACK_EXCHANGE_API_KEY}`;
    try {
        const response = await axios.get(url);
        const askers = new Set();
        response.data.items.forEach(question => askers.add(question.owner.user_id));
        return Array.from(askers);
    } catch (error) {
        console.error('Error fetching people who ever asked question:', error.message);
        return [];
    }
}
  
async function fetchPeopleWhoEverResponded() {
    const url = `https://api.stackexchange.com/2.3/answers?order=desc&sort=activity&site=${SITE}&filter=withbody&pagesize=100&key=${STACK_EXCHANGE_API_KEY}`;
    try {
        const response = await axios.get(url);
        const responders = new Set();
        response.data.items.forEach(answer => responders.add(answer.owner.user_id));
        return Array.from(responders);
    } catch (error) {
        console.error('Error fetching people who ever responded:', error.message);
        return [];
    }
}
  
async function main() {
    try {
        const top100ByReputation = await fetchTop100ByReputation();
        console.log('Top 100 by reputation:', top100ByReputation);
  
        const topAcceptedByAuthor = await fetchTopAcceptedByAuthor();
        console.log('Top accepted by author:', topAcceptedByAuthor);
  
        const top100ByUpvotes = await fetchTop100ByUpvotes();
        console.log('Top 100 by upvotes:', top100ByUpvotes);
  
        const top100QuestionAskers = await fetchTop100QuestionAskers();
        console.log('Top 100 question askers:', top100QuestionAskers);
  
        const peopleWhoEverAskedQuestion = await fetchPeopleWhoEverAskedQuestion();
        console.log('People who ever asked question:', peopleWhoEverAskedQuestion);
  
        const peopleWhoEverResponded = await fetchPeopleWhoEverResponded();
        console.log('People who ever responded:', peopleWhoEverResponded);
    } catch (error) {
        console.error('Error in main:', error);
    }
}
  
main();
