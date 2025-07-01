import { Agent, Doc, Model, Scope, SDKLog } from '@smythos/sdk';
import { create } from 'domain';
import path from 'path';
import {fileURLToPath} from 'url';

import * as readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

const rl = readline.createInterface({
    input,
    output
});

// Create a new agent with a skill that allows it to retrieve information from the vectordb.
async function createAgent() {
    const agent = new Agent({
        id: 'pdf-agent',
        name: 'PDF Agent',
        behavior: 'You are a helpful assistant that responds to user queries, only if you can find the relevant invbvformation in your knowledge base. If your knowledge base does not contain the information, then you cannot answer based on your pretrained data, and say "My knowledge base does nto contain this information.". For every response, you have to provide the document title that you got the information from, and cite the extract of the original text where you got your response from, In the form Title: <title>, Text: <text>, at the end of your response. If you use multiple sources to answer the query, provide the above information for each source. If the knowledge base contains no information that is relevant to the user, then you must not answer the question, and you must tell the user that you cannot answer the question, and then terminate with no additional output. Do not respond with just the cited text, you must also formulate your own response. You can combine knowledge in the document with your pretrained knowledge if this is necessary to answer the user query, such as for background knowledge or how to do specific computations. Be concise yet helpful.',
        model: 'gpt-4o'
    })

    const skill = agent.addSkill({
        name: 'retrieve-info',
        description: 'Use this skill to retrieve information from your knowledge base',
        process: async ({ question }) => {
            const vectordb = agent.vectorDB.RAMVec('ramvec');
            const searchResult = await vectordb.search(question, {topK: 10});
            return `Retrieved Information: \n\n${JSON.stringify(searchResult)}`;
        }
    })

    skill.in({
        question: {
            type: 'Text',
            description: '<Copy here the exact user question> ' + 'Look in your knowledge base.'
        }
    })

    return agent;
}

async function indexDataForAgent(agent: Agent) {
    const filename = fileURLToPath(import.meta.url);
    const dirname = path.dirname(filename);
    const filePath = path.join(dirname, '../files/python_book.pdf');

    const vectordb = agent.vectorDB.RAMVec('ramvec');
    await vectordb.purge();

    const parsedDoc = await Doc.pdf.parse(filePath, {
        title: 'Plan Coverage Information',
        author: 'Blue Cross and Blue Shield of Texas',
        date: '2025-06-10'
    })

    await vectordb.insertDoc(parsedDoc.title, parsedDoc, {myEntry: 'My Metadata'})
}

async function main() {
    const agent = await createAgent();
    await indexDataForAgent(agent);

    while (true) {
        const query = await rl.question('\nEnter your query > ');
        const promptResult = await agent.prompt(query);
        console.log(promptResult);
    }
}

main();
