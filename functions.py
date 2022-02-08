import re
import spacy
from random import randint
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nlp = spacy.load("en_core_web_md")
lemmatizer = WordNetLemmatizer()


def make_exit(name, user_message):
    exit_commands = ("quit", "goodbye", "exit", " no", " bored", "to leave", "to go", "bye")

    exit_responses = ("Talk to you later {}!", "It's been nice getting to know you {}",
                      "Hopefully hear from you soon",
                      "Feel free to come back if you have anymore questions",
                      "Always here when you need me {}",
                      "Nice chatting, all the best {}")

    for exit_command in exit_commands:
        if exit_command in user_message.lower():
            exit_response_index = randint(0, len(exit_responses) - 1)
            print(exit_responses[exit_response_index].format(name))
            return True


def handle_initial_message(message):
    a = r"name is ([a-zA-Z-']+( |\.)?([a-zA-Z-']+)?)"
    b = r"called ([a-zA-Z-']+( |\.)?([a-zA-Z-']+)?)"
    c = r"^([a-zA-Z-']+( |\.)?([a-zA-Z-']+)?)\.?$"
    abc = [a, b, c]
    name = ""
    i = 0
    j = 0
    while len(name) == 0:
        if make_exit(name, message):
            return False, False
        elif re.search(abc[i], message.lower()):
            name = re.search(abc[i], message.lower()).group(1)
            break
        elif i == 3:
            clarification_messages = ("I don't know what to call you :)\nPlease simplify\n",
                                      "I'm really sorry please can you retry.\nIf you type\
                                       just your firstname this should work.")
            message = input(clarification_messages[j])
            if j == 0:
                j += 1
            i = 0
        else:
            i += 1
    user_message = input(f"""Great to be talking with you {name.title()} :)
Like I said earlier, I am Program Buddy and would love to talk with you.
What software skills have you been looking into recently?
""")
    return user_message, name.title()


def question1(name, user_message):
    list_user_message = word_tokenize(user_message)
    pos_user_message = pos_tag(list_user_message)
    answers_re = (r"looking into ([-a-zA-Z ']+)",
                  r"learning ([-a-zA-Z ']+)",
                  r"learnt ([-a-zA-Z ']+)",
                  r"learn ([-a-zA-Z ']+)")
    initial_phrase = ""
    for phrase in answers_re:
        if re.search(phrase, user_message.lower()):
            initial_phrase = re.search(phrase, user_message.lower()).group(1)
            break

    if len(initial_phrase) > 0:
        entities = re.findall(r"[a-z-']+", user_message.lower())
        for word, pos in pos_user_message:
            for entity in entities:
                if (word.lower() == entity) and (not pos[0] =="N"):
                    entities.remove(entity)
        if len(entities) == 1:
            return entities[0]
        elif len(entities) == 2:
            return entities[0] + " and " + entities[1]
        elif len(entities) > 2:
            first_entity = entities[0]
            last_entity = " and " + entities[-1]
            for entity in entities[1:-1]:
                first_entity += ", " + entity
            return_entities = first_entity + last_entity
            return return_entities
    # Keep the above code for now as otherwise larger sentences maybe captured.
    elif len(initial_phrase) == 0:
        entities = ""
        for word, pos in pos_user_message:
            if pos[0] == "N":
                entities += word + ", "
        entities = entities.strip().strip(",")
        last_comma_index = entities.rfind(", ")
        entities = entities[:last_comma_index] + " and" + entities[last_comma_index + 1:]
        print("I wasn't too sure what you have been working on but I thought it may be related to these:")
        print(entities)
        check = input("Please comma seperate the topics you've been working on.\n")
        if make_exit(name, check):
            return False
        elif re.findall(r"[a-zA-Z-']+", check):
            entities = re.findall(r"[a-zA-Z-']+", check)
            return_entities = ""
            for entity in entities[:-1]:
                return_entities += entity + ", "
            return_entities = return_entities.strip().strip(",")
            return_entities += " and " + entities[-1]
            return return_entities
        else:
            return entities

def question2(name, user_message):
    answers_re = r"(\w+) (weeks|week|days|day|months|month|years|year|hours|hour|minutes|minute)"
    while True:
        if re.search(answers_re, user_message.lower()):
            full_match = re.search(answers_re, user_message.lower())
            entity = full_match.group(1) + " " + full_match.group(2)
            return entity
        check = input("""I'm sorry I couldn't quite understand how long you've been working for.
            Please may you rephrase.\n""")
        if make_exit(name, check):
            return False
        else:
            user_message = check


def preprocess(input_sentence):
    input_sentence = input_sentence.lower()
    tokens = word_tokenize(input_sentence)
    pos_tagged_tokens = pos_tag(tokens)

    input_sentence = [lemmatizer.lemmatize(
        i, pos_swap(j)) for i, j in pos_tagged_tokens]
    return input_sentence


def pos_swap(pos):
    if re.search(r'VB.?', pos):
        return 'v'
    elif re.search(r'JJ.?', pos):
        return 'a'
    elif re.search(r'RB.?', pos):
        return 'r'
    else:
        return 'n'


def compare_overlap(user_message, possible_response):
    similar_words = 0
    for token in user_message:
        if token in possible_response:
            similar_words += 1
    return similar_words


def extract_nouns(tagged_message):
    message_nouns = list()
    for token, tag in tagged_message:
        if tag.startswith("N"):
            message_nouns.append(token)
    return message_nouns
