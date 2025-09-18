#import AI/LLM (Ollama?) & Needed libraries

#variables (info is temperorary)
info = {'Name': 'John fitness', 
        'Age': 32,
        'Weight': 243, 
        'Prefered Exercizes': ['push-ups', 'sit-ups'],
        'Excluded Exercizes': ['pull-ups', 'bridges'],
        'Free Time': 1.5}
#Note: Categories are Name, Age, Weight, Free Time, Prefered Exercizes, and Excluded Extercizes


#prompt or the AI
prompt = """Prepare a schedule for ['Name'] using the prefered exercizes 
that can fit in the ['Free Time']"""
#Note: Possibly see about having the user input the rompt


#call to the AI + printing response
AI_Answer = get_llm_answer(prompt)
print(AI_Answer)
