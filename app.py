from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)


# Sample questions for the quiz
questions = [
    {
        "question": "In Catalonia, Spain, what is Tió de Nadal?",
        "options": [
            """a) A log that is fed and cared for, then beaten so it "defecates" presents.""",
            "b) A traditional Catalan sport where competitors race to decorate the largest Christmas tree.",
            "c) An annual festival where people build elaborate gingerbread log cabins.",
            "d) Tió de Nadal is rumored to be Santa's secret workshop located deep within the Catalonian forests."
        ],
        "correctAnswer": """a) A log that is fed and cared for, then beaten so it "defecates" presents.""",
        "image": "static/images/tio_de_nadal.jpg"
    },
    {
        "question": "In Japan, what unusual tradition is popular on Christmas Day?",
        "options": [
            "a) Eating Kentucky Fried Chicken as a festive meal.",
            "b) Decorating bamboo trees with origami cranes.",
            "c) Dressing up as sumo wrestlers and exchanging gifts.",
            "d) Hosting silent meditation retreats in honor of the New Year."
        ],
        "correctAnswer": "a) Eating Kentucky Fried Chicken as a festive meal.",
        "image": "static/images/kfc.jpg"
    },
    {
        "question": "In Austria, what is Krampus in their Christmas folklore?",
        "options": [
            "a) A festive goat that delivers presents.",
            "b) A giant snowman built in every town square.",
            "c) A horned creature who punishes naughty children.",
            "d) A traditional pastry eaten on Christmas morning."
        ],
        "correctAnswer": "c) A horned creature who punishes naughty children.",
        "image": "static/images/krampus.jpg"
    },
    {
        "question": "In Ukraine, why do people decorate their Christmas trees with spider webs?",
        "options": [
            "a) To ward off evil spirits during the winter solstice.",
            "b) To attract prosperity and good luck in the New Year",
            "c) To symbolize the interconnectedness of life",
            "d) To honor a legend where spiders decorated a poor family's tree."
        ],
        "correctAnswer": "d) To honor a legend where spiders decorated a poor family's tree.",
        "image": "static/images/ukraine.jpg"
    },
    {
        "question": "In Norway, what unique tradition is observed on Christmas Eve?",
        "options": [
            "a) Leaving out a plate of lutefisk for Santa.",
            "b) Lighting bonfires to guide the return of the sun",
            "c) Hiding all the brooms to prevent witches from stealing them",
            "d) Dressing up in Viking costumes and reenacting battles."
        ],
        "correctAnswer": "c) Hiding all the brooms to prevent witches from stealing them",
        "image": "static/images/norway.jpg"
    },
    {
        "question": "In Venezuela, how do people commonly travel to early morning mass during the Christmas season?",
        "options": [
            "a) By roller-skating through the streets.",
            "b) By horse-drawn sleighs decorated with lights.",
            "c) By swimming across the Guaire River.",
            "d) By riding bicycles adorned with poinsettias."
        ],
        "correctAnswer": "a) By roller-skating through the streets.",
        "image": "static/images/venezuela.jpg"
    },
    {
        "question": "In Wales, what is the Mari Lwyd tradition?",
        "options": [
            "a) A festival where people wear sheep costumes and dance.",
            "b) Parading with a horse's skull on a pole, going door to door singing.",
            "c) A competition to build the tallest snowman in town.",
            "d) A communal feast featuring leeks and dragon-shaped bread."
        ],
        "correctAnswer": "b) Parading with a horse's skull on a pole, going door to door singing.",
        "image": "static/images/wales.jpg"
    },
    {
        "question": "In Iceland, what are the Yule Lads known for?",
        "options": [
            "a) Thirteen mischievous trolls who visit children during the 13 nights before Christmas.",
            "b) A group of elves who bring snow to the mountains.",
            "c) Musicians who perform traditional songs in town squares.",
            "d) A team of reindeer that guide Santa's sleigh."
        ],
        "correctAnswer": "a) Thirteen mischievous trolls who visit children during the 13 nights before Christmas.",
        "image": "static/images/iceland.jpg"
    },
    {
        "question": "In the Czech Republic, what do unmarried women do on Christmas Eve to predict their marital status?",
        "options": [
            "a) Bake a special cake and see if it rises.",
            "b) Walk backward around a church three times.",
            "c) Look into a mirror at midnight to see their future spouse.",
            "d) Throw a shoe over their shoulder towards the door."
        ],
        "correctAnswer": "d) Throw a shoe over their shoulder towards the door.",
        "image": "static/images/czech.jpg"
    },
    {
        "question": "In Finland, what is a common Christmas Eve tradition?",
        "options": [
            "a) Swimming in ice-cold lakes to welcome the New Year.",
            "b) Building snow forts to ward off evil spirits.",
            "c) Planting a fir tree to symbolize new beginnings.",
            "d) Visiting a sauna to cleanse the body and mind."
        ],
        "correctAnswer": "d) Visiting a sauna to cleanse the body and mind.",
        "image": "static/images/finland.jpg"
    },

    {
        "question": """In Oaxaca, Mexico, what are people doing during the "Noche de Rábanos" (Night of the Radishes)?""",
        "options": [
            "a) Watching a nighttime parade featuring giant illuminated radish floats.",
            "b) Carving radishes into intricate sculptures and displays.",
            "c) Eating a communal feast where only radish-based dishes are served.",
            "d) Playing a traditional game of radish tossing to predict the year's harvest."
        ],
        "correctAnswer": "b) Carving radishes into intricate sculptures and displays.",
        "image": "static/images/mexico.jpg"
    },
    {
        "question": "In South Africa, what unusual food is sometimes eaten on Christmas Day?",
        "options": [
            "a) Fried caterpillars of the Emperor Moth.",
            "b) Grilled kangaroo steaks.",
            "c) Fermented shark meat.",
            "d) Roasted guinea pigs."
        ],
        "correctAnswer": "a) Fried caterpillars of the Emperor Moth.",
        "image": "static/images/sa.jpg"
    },
    {
        "question": """In Greenland, what is a traditional winter food named "Kiviak"?""",
        "options": [
            "a) A stew made from reindeer organs.",
            "b) Dried fish mixed with berries.",
            "c) A seal skin stuffed with 500 auks and left to ferment.",
            "d) A dish made from whale blubber and seaweed."
        ],
        "correctAnswer": "c) A seal skin stuffed with 500 auks and left to ferment.",
        "image": "static/images/greenland.jpeg"
    },
    {
        "question": "In Slovakia, what does the head of the family do with a spoonful of Loksa (pudding) during Christmas dinner?",
        "options": [
            "a) Buries it in the yard to honor ancestors.",
            "b) Feeds it to the family pet for good luck.",
            "c) Throws it at the ceiling to predict the next year's harvest.",
            "d) Places it under the tablecloth for prosperity."
        ],
        "correctAnswer": "c) Throws it at the ceiling to predict the next year's harvest.",
        "image": "static/images/slovakia.jpg"
    },
    {
        "question": "In the Philippines, what is the Giant Lantern Festival?",
        "options": [
            "a) A night where people release thousands of lanterns into the sky.",
            "b) A festival featuring massive, elaborate lanterns made from bamboo and paper.",
            "c) A competition to build the largest Christmas tree out of lanterns.",
            "d) A parade where floats are illuminated entirely by lanterns."
        ],
        "correctAnswer": "b) A festival featuring massive, elaborate lanterns made from bamboo and paper.",
        "image": "static/images/philippines.jpeg"
    },
    {
        "question": """In Germany, who is "Belsnickel" in Christmas folklore?""",
        "options": [
            "a) A man who visits children dressed in rags, carrying a switch to punish the naughty.",
            "b) A festive gnome who leaves gifts in children's shoes.",
            "c) A magical deer that guides Santa's sleigh.",
            "d) A snow fairy who brings the first snowfall."
        ],
        "correctAnswer": "a) A man who visits children dressed in rags, carrying a switch to punish the naughty.",
        "image": "static/images/belsnickel.jpeg"
    },
    {
        "question": """In Portugal, what is "Consoda," a tradition observed on Christmas morning?""",
        "options": [
            "a) Baking bread with hidden coins inside.",
            "b) Lighting candles in windows to guide lost souls.",
            "c) Exchanging gifts of salt and olive oil.",
            "d) Setting extra places at the table for deceased relatives."
        ],
        "correctAnswer": "d) Setting extra places at the table for deceased relatives.",
        "image": "static/images/portugal.jpg"
    },
    {
        "question": """In Italy, who is "La Befana"?""",
        "options": [
            "a) A fairy who turns snow into sweets.",
            "b) A kind witch who delivers gifts to children on Epiphany Eve.",
            "c) A talking donkey that predicts the future.",
            "d) A giant cat that brings good luck."
        ],
        "correctAnswer": "b) A kind witch who delivers gifts to children on Epiphany Eve.",
        "image": "static/images/italy.jpg"
    },
    {
        "question": """In Guatemala, what is "La Quema del Diablo"?""",
        "options": [
            "a) A festival where fireworks are used to chase away spirits.",
            "b) A cleansing ritual where people burn effigies of the devil to rid homes of evil.",
            "c) A dance where participants wear devil masks and costumes.",
            "d) A cooking contest featuring spicy dishes."
        ],
        "correctAnswer": "b) A cleansing ritual where people burn effigies of the devil to rid homes of evil.",
        "image": "static/images/guatemala.jpeg"
    },
    {
        "question": "In Germany, what vegetable ornament is hidden in the Christmas tree?",
        "options": [
            "a) A cabbage.",
            "b) A potato.",
            "c) A pickle.",
            "d) A carrot."
        ],
        "correctAnswer": "c) A pickle.",
        "image": "static/images/gurke.jpeg"
    }
]


users = {}
moderator_username = "Marie"  # Pre-defined moderator username for simplicity
current_question_index = 0  # Track current question index for all users
show_correct_answer = False  # Track if the correct answer should be displayed

@app.route('/current_question_index')
def get_current_question_index():
    return {"current_question_index": current_question_index}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
    username = request.form['username']
    if username not in users:
        users[username] = {"score": 0, "answers": []}
    if username == moderator_username:
        return redirect(url_for('moderator'))
    return redirect(url_for('quiz', username=username))

@app.route('/quiz/<username>')
def quiz(username):
    print(f"Current Question Index: {len(users[username]['answers'])}")
    print(f"User Answers: {users[username]['answers']}")
    if username == moderator_username:
        return redirect(url_for('moderator'))

    if len(users[username]["answers"]) >= len(questions):
        print("Redirecting to leaderboard")
        return redirect(url_for('leaderboard'))

    current_question_index = len(users[username]["answers"])
    question = questions[current_question_index]
    return render_template(
        'quiz.html',
        username=username,
        question=question,
        current_question_index=current_question_index,
        show_correct_answer=False
    )



@app.route('/answer', methods=['POST'])
def answer():
    username = request.form['username']
    question_index = int(request.form['question_index'])
    answer = request.form.get('answer')  # Use .get() to avoid KeyError

    # Ensure the user exists in the dictionary
    if username not in users:
        return redirect(url_for('index'))

    # Check if an answer was submitted
    if not answer:
        # Redirect back to the quiz with an error message
        error_message = "Please select an answer before submitting."
        question = questions[question_index]
        return render_template(
            'quiz.html',
            username=username,
            question=question,
            current_question_index=question_index,
            show_correct_answer=False,
            error_message=error_message
        )

    # Record the user's answer
    if len(users[username]["answers"]) <= question_index:
        users[username]["answers"].append({"question_index": question_index, "answer": answer})

        # Update the score if the answer is correct
        if questions[question_index]["correctAnswer"] == answer:
            users[username]["score"] += 1

    # Redirect back to the quiz to show the next question
    return redirect(url_for('quiz', username=username))


@app.route('/moderator', methods=['GET', 'POST'])
def moderator():
    global current_question_index, show_correct_answer

    if current_question_index < len(questions):
        question = questions[current_question_index]
        correct_image = None

        if request.method == 'POST' and 'reveal_answer' in request.form:
            show_correct_answer = True
            correct_image = question["image"]  # Retrieve the image of the correct answer

        return render_template(
            'moderator.html',
            question=question,
            show_correct_answer=show_correct_answer,
            correct_image=correct_image,
            current_question_index=current_question_index
        )
    else:
        return redirect(url_for('leaderboard'))


@app.route('/reveal_answer', methods=['POST'])
def reveal_answer():
    global show_correct_answer
    show_correct_answer = True
    return redirect(url_for('moderator'))

@app.route('/next_question', methods=['POST'])
def next_question():
    global current_question_index, show_correct_answer
    show_correct_answer = False
    current_question_index += 1
    return redirect(url_for('moderator'))

@app.route('/leaderboard')
def leaderboard():
    # Ensure users dictionary is not empty
    if not users:
        return render_template('leaderboard.html', leaderboard=[])

    # Sort users by score in descending order
    try:
        sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)
        leaderboard_data = [{"username": user, "score": data["score"]} for user, data in sorted_users]
    except Exception as e:
        print(f"Error processing leaderboard: {e}")
        leaderboard_data = []

    return render_template('leaderboard.html', leaderboard=leaderboard_data)


if __name__ == "__main__":
    app.run(debug=True)


    #store each user username/score in a dicct
##username=type string; score=type int 