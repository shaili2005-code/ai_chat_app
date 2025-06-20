import requests

def test_pdf_chat(question):
    url = "http://localhost:5000/api/ask"
    headers = {"Content-Type": "application/json"}
    data = {"question": question}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise error for bad status
        answer = response.json().get("answer", "No answer found")
        print(f"Q: {question}\nA: {answer}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    test_pdf_chat(user_question)
