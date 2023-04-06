from flask import Flask, render_template
from csv_read import combined_list
import random
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = 'gpt-3.5-turbo'

app = Flask(__name__)

# Returns a list of ID,Name, and room, given number of intentional interactions desired


def choose_interactions(num_interactions, combined_list):
    list_of_rows = []
    for i in range(num_interactions):
        random_row = random.choice(combined_list)
        list_of_rows.append(random_row)
    return list_of_rows


interactions = choose_interactions(6, combined_list)
print("############################")
print(interactions)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    output, total_output = [], []
    for i in range(0, len(interactions)):
        first_name = interactions[i][1]
        last_name = interactions[i][2]
        id_number = interactions[i][0]
        room_number = interactions[i][3]

        user_input = "I am a residential assistant at Arizona State University, Barrett Honors College. I have to interact with residents on a daily basis. Write a summary of an interaction that I might have with a student named " + \
            first_name+". Use gender neutral pronouns. Tell the story from my point of view. Make it two sentences or shorter. Make it different than the last story."

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{user_input}"}
        ]

        response = openai.ChatCompletion.create(
            model=model_id,
            messages=messages
        )

        output = response.choices[0].message.content
        print("----------------------------------------------------------------")
        print(f"RESIDENT INTERACTION {i+1}\n")
        # print(f"User Input: {user_input}\n")
        print(f"EMPLID: {id_number}\n")
        print(f"Name: {first_name} {last_name}\n")
        # print(f"{last_name}\n")
        print(f"ROOM#: {room_number}\n")
        print(f"INTERACTION: {output}\n")
        total_output.append(
            f"RESIDENT INTERACTION {i}\nEMPLID: {id_number}\nName: {first_name} {last_name}\nROOM#: {room_number}\nINTERACTION: {output}\n")
        print("----------------------------------------------------------------")
    return render_template('index.html', total_output=total_output)


if __name__ == '__main__':
    app.run(debug=True)
