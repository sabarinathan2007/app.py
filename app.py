from flask import Flask,request,render_template #lightweight Framework
import pandas as pd #dataFram work readinfo csv rowcol
import google.generativeai as genai
from dotenv import load_dotenv
import os


#Step call api key model
load_dotenv()

app=Flask(__name__)

#configure model 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash")

df=pd.read_csv("qa_data (1).csv")

#csv into context text
context_text=""

for _,row in df.iterrows():
    context_text +=f"Q: {row['question']}\nA: {row['answer']}\n\n"

def ask_gemini(query):
    prompt=f"""
you are a Q&A assistant.

Answer ONLY using the context below.
If the answer is not present, say: No rlevant Q&A found.

Context:
{context_text}

Question: {query}
"""
    response=model.generate_content(prompt)
    return response.text.strip()

'''print("RAG custome Q&A ChatBot")
print("Enter exit come outside or terminate")

while True:
    user_input=input("you: ")
    if user_input.lower()=="exit":
        print("Goodbye!")
        break
    answer=ask_gemini(user_input)
    print(f"{answer}\n")'''

#connecting html and app.py

@app.route("/",methods=["GET","POST"])
def home():
    answer=""
    if request.method=="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=answer)

#running app
if __name__=="__main__":
    app.run()
    