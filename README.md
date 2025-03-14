# Conversational AI BOT

## Project Overview
This project is a Conversational AI bot designed to provide information about historical monuments worldwide. The chatbot can answer user queries related to historical sites and also includes an OTP-based email verification system within the conversation flow.

## Features
- **Conversational AI:** Users can ask about historical monuments, and the bot provides relevant responses.
- **Agentic Workflow:** Implemented using LangGraph to structure the conversation.
- **OTP Verification:** The bot requests and verifies the user’s email via a 6-digit OTP sent using SendGrid.
- **LLM Integration:** Uses Groq's `Gemma2-9b-It` model for response generation.
- **Keyword-Based Email Trigger:** If certain travel-related keywords appear in user queries, the bot prompts for an email to send additional details.

## Tech Stack
- **LLM Framework:** LangGraph + Groq
- **OTP Service:** SendGrid
- **Development Environment:** VS Code
- **Configuration Management:** `config.ini` file to store API keys

## How It Works
1. User starts a conversation and asks about historical monuments.
2. The bot responds with relevant monument details.
3. If the user's query suggests interest in travel recommendations, the bot asks for their email.
4. If the user provides an email, the bot generates a 6-digit OTP and sends it using SendGrid.
5. The user enters the OTP in the chat for verification.
6. Upon successful verification, the bot confirms that details will be sent via email.

## Installation & Setup
### Prerequisites
- Python installed
- API keys for Groq and SendGrid

### Steps
1. Clone the repository:
   ```bash
   git clone <repo-url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `config.ini` with the required API keys:
   ```ini
   [SETTINGS]
   APIKEY = your_sendgrid_api_key
   FROM = your_sender_email
   GROQ_API_KEY = your_groq_api_key
   ```
4. Run the chatbot:
   ```bash
   python main.py
   ```

## Conversation
```
python agent.py       
User: Hey I am travelling to pune can you suggest some places to visit there
Assistant: Of course! Pune is a vibrant city with a lot to offer. ! 

Here are some popular places to get you started:

**Historical & Cultural:**

* **Shaniwar Wada:**  A magnificent 18th-century fort with a rich history.
* **Aga Khan Palace:**  A historical building that served as Mahatma Gandhi's residence during his time in Pune.
* **Parvati Hill:**  A scenic hilltop with ancient temples and panoramic city views.
* **Raja Dinkar Kelkar Museum:**  A unique museum showcasing a vast collection of antiques and artifacts.

**Nature & Outdoors:**

* **Sinhagad Fort:**  A historic fort with stunning views of the surrounding countryside.
* **Lonavala & Khandala:**  Hill stations near Pune known for their scenic beauty and waterfalls.
* **Pawna Lake:**  A picturesque lake perfect for boating and picnicking.


Let me know more about your trip, and I can help you create an unforgettable Pune experience!

Assistant: Would you like more details via email?
User: actual recievers email
Assistant: Thanks! I'll send a verification code to actual recievers email.
Assistant: I have sent a 6-digit code to your email. Please verify it.
Enter OTP: 682328
Assistant: Great, OTP verified! I'll email you soon.
User: ok thanks
Assistant: You're welcome! Is there anything else I can help you with?
```
