import Head from "next/head";
import { useState } from "react";
import styles from "./index.module.css";
const { Configuration, OpenAIApi } = require("openai");
const dotenv = require('dotenv');
dotenv.config(); 

const configuration = new Configuration({
  // TODO figure out how to serve this up properly
  apiKey: "FILL IN",
});
const openai = new OpenAIApi(configuration);

export default function Home() {
  const [animalInput, setAnimalInput] = useState("");
  const [contextInput, setContextInput] = useState("");
  const [result, setResult] = useState();
  const [userResponse, setUserResponse] = useState();

  async function onSubmit(event) {
    event.preventDefault();
    try {
      const completion = await openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        messages: [{"role": "user", "content": contextInput}, {"role": "user", "content": animalInput}],
      });
  
      setUserResponse(completion.data.choices[0].message.role);
      setResult(completion.data.choices[0].message.content);
    } catch(error) {
      console.error(error);
      alert(error.message);
    }
  }

  return (
    <div>
      <Head>
        <title>OpenAI Quickstart</title>
        <link rel="icon" href="/dog.png" />
      </Head>

      <main className={styles.main}>
        <img src="/dog.png" className={styles.icon} />
        <h3>What do you want to ask ChatGPT?</h3>
        <form onSubmit={onSubmit}>
          <input 
            type="text"
            name="context"
            placeholder="Context for each individual prompt"
            value={contextInput}
            onChange={(e) => setContextInput(e.target.value)}
          />
          <input
            type="text"
            name="animal"
            placeholder="Enter an animal"
            value={animalInput}
            onChange={(e) => setAnimalInput(e.target.value)}
          />
          <input type="submit" value="Generate names" />
        </form>
        <div className={styles.result}>{userResponse}</div>
        <div className={styles.result}>{result}</div>
      </main>
    </div>
  );
}
