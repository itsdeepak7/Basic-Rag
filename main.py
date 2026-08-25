"""command -line demo of the HR POLICY ASSISTANT.
RUN WITH :PYTHON mian.py
"""
from hr_assistant.pipeline import ask,build_hr_assistant

def main():
    print("BUILDING THE HR POLICY ASSISTANT ")
    agent = build_hr_assistant()
    print("ASSISTANT ready!\n")
    demo_questions =[
        "How many  paid annual eave days do i get?",
        "what is the notice period during probation?",
        "can i work from home everyday?",
    ]

    for question in demo_questions:
        print("="*60)
        print("question: ",question)
        print("="*60)
        answer = ask(agent,question)
        print("ANSWER :",answer)
        print("="*60)
        print()

if __name__ == "__main__":
    main()