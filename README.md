# ⚡ Web3Bridge Cohort XIII AI Assistant

An intelligent **AI-powered learning assistant** that helps **upcoming Web3Bridge participants** explore, study, and understand materials from **past cohorts**.  
Built with **Pydantic AI**, **Streamlit**, and **Groq LLMs**, it provides instant, accurate answers about Web3, Solidity, Hardhat, and smart contract development all based on real content from the Web3Bridge Cohort XIII GitHub repository.

---

## 🧭 OVERVIEW

Preparing for Web3Bridge can be challenging especially with the vast amount of learning materials spread across GitHub folders and markdown files.  
This project solves that by giving learners an **interactive AI assistant** that can:

- Retrieve information directly from the **Web3Bridge Cohort XIII GitHub repo**
- Explain key **Solidity and blockchain concepts** in simple language  
- Provide **citations and file links** for deeper exploration  

This assistant makes it easier for **new students** to get ready for the next cohort by learning from **previous lessons and assignments** without having to dig through raw code or documentation.
<img width="1920" height="1020" alt="Screenshot 2025-10-22 193037" src="https://github.com/user-attachments/assets/9624a660-b010-4d61-be05-8c9737fbb7e5" />

---

## ⚙️ Installation
Requirements:
- Python 3.9+
- [UV](https://github.com/astral-sh/uv)


### 1. Clone the repository
```
git clone https://github.com/igbokwewinnie/web3bridge-ai-agent.git
cd web3bridge-ai-agent
```

### 2. Sync dependencies with `uv`
```
uv sync
```

### 3. Add your environment variable

Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🚀 Usage

Run the Streamlit app:
```
uv run streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

You can now ask:
> *“What topics were covered in Week 4 of Web3Bridge Cohort XIII?”*  
> *“Explain Solidity visibility specifiers like in the course.”*  
> *“What was taught about Hardhat or smart contracts?”*

The AI will stream the answer in real-time, citing the exact GitHub files where the content came from.


https://github.com/user-attachments/assets/122c10e3-2fde-47f8-83d5-110c047afdf5


---

## ✨ Features

✅ Built for **Web3Bridge learners** study past cohorts easily 
✅ **Real-time streaming answers** using Groq LLMs  
✅ **Retrieval-based AI** — uses Cohort XIII materials for context  
✅ **Citations** linking directly to GitHub files  
✅ Local **logging system** for interaction history  

**Planned updates:**
- Add topic filtering by “Week” or “Module”  
- Multi-cohort support (XII, XIII, XIV, etc.)
- Add solidity official docs
- Integration with a vector database for faster searches  

---

## Evaluations

We evaluate the agent using the following criteria:

- instructions_follow: The agent followed the user's instructions
- instructions_avoid: The agent avoided doing things it was told not to do
- answer_relevant: The response directly addresses the user's question
- answer_clear: The answer is clear and correct
- answer_citations: The response includes proper citations or sources when required
- completeness: The response is complete and covers all key aspects of the request
- tool_call_search: Is the search tool invoked?

Current evaluation metrics: 
```
instructions_follow    0.771429
instructions_avoid     1.000000
answer_relevant        0.857143
answer_clear           0.842857
answer_citations       0.642857
completeness           0.714286
tool_call_search       0.971429
```
The most important metric for this project is answer_relevant. This measures whether the system's answer is relevant to the user. It's currently 85%.
Improvements: Our evaluation is currently based on only 7 questions. We need to collect more data for a more comprehensive evaluation set.

## 🧩 Project Structure

```
app/
 ┣ ingest.py          # Downloads, reads, and chunks GitHub markdown files
 ┣ search_agent.py    # Sets up the AI agent with prompt and Groq model
 ┣ search_tools.py    # Handles search across indexed documents
 ┣ logs.py            # Logs user-agent interactions
 ┗ app.py             # Streamlit web interface
```

---

## 🤝 Contributing

Contributions are welcome!  
If you’d like to improve the assistant or extend it to other cohorts:

1. Fork this repository  
2. Create a new branch (`feature/add-x`)  
3. Commit your changes  
4. Submit a pull request  

Follow standard Python style (PEP 8) and ensure your code is tested.

---

## 🧪 Tests

Run tests with:
```
uv run pytest
```

To test the Streamlit app in headless mode:
```
uv run streamlit run app.py --server.headless true
```

---

## ☁️ Deployment

To deploy on **Streamlit Cloud**:
Generate a requirement.txt file from your uv environment:
```
uv export > requirements.txt
```

1. Push your repo to GitHub  
2. Go to [Streamlit Cloud](https://share.streamlit.io) → **“New App”**  
3. Connect your repo and deploy  
4. In your app settings → **Secrets**, add:
   ```
   GROQ_API_KEY="your_groq_api_key_here"
   ```
Once saved, your app redeploys automatically.

---

## 🧠 FAQ / Troubleshooting

**Q:** The app says `GROQ_API_KEY not found`  
**A:** Add it to your `.env` file locally or under “Secrets” in Streamlit Cloud.

**Q:** It shows `'Agent' object has no attribute 'toolsets'`  
**A:** That’s a harmless warning from an internal dependency. You can ignore it safely.

---

## 🙏 Credits / Acknowledgments

- [Web3Bridge](https://web3bridge.com/) — original training content and resources
- [Alexy Grigorev](https://www.linkedin.com/in/agrigorev) for the [AI Agents Crash Course](https://alexeygrigorev.com/aihero/)
- [Groq](https://groq.com/) — ultra-fast Llama-3 inference backend  
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) — agent framework  
- [Streamlit](https://streamlit.io/) — frontend for AI interactions  

---
This project was developed as part of the AI Agent Crash Course, where I learned how to build an intelligent retrieval-based agent that can chunk data, index it, and answer questions contextually.
