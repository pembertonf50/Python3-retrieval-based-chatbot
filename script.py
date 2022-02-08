from scipy.spatial.distance import cosine
from nltk import pos_tag
from responses import responses
from functions import preprocess, compare_overlap, \
    extract_nouns, nlp, \
    handle_initial_message, make_exit, question1,\
    question2


class ChatBot:

    def intro(self):
        self.name = ''
        initial_message = input("""
Hello there! My name is Program Buddy.
What is your name?
(if at any point you wish to leave please type 'exit')
""")
        if make_exit(self.name, initial_message):
            return
        else:
            user_message, self.name = handle_initial_message(initial_message)
            if not user_message or make_exit(self.name, user_message):
                return
            self.build_up_chat(user_message)


    def build_up_chat(self, user_message):
        answer1 = question1(self.name, user_message)

        if not answer1:
            return
        user_message =input("Oh nice! How long have you been studying {}?\n".format(answer1))
        if make_exit(self.name, user_message):
            return
        answer2 = question2(self.name, user_message)
        if not answer2:
            return
        print(f"{answer2}, that's pretty solid.\n")
        progression_answer = input("""I have most experience in Python but also things such as Java,
C++, Command line, SQL and GIT. Do you know any of these?
""")
        self.chat(progression_answer)



    def chat(self, user_message):
        while not make_exit(self.name, user_message):
            user_message = self.respond(user_message)


    def find_intent_match(self, responses, user_message):
        bow_user_message = set(preprocess(user_message))
        processed_responses = [set(preprocess(j)) for i, j, k in responses]
        similarity_list = [compare_overlap(bow_user_message, response) for response in processed_responses]
        response_index = similarity_list.index(max(similarity_list))
        return responses[response_index][2], response_index


    def find_entities(self, user_message, index):
        tagged_user_message = pos_tag(preprocess(user_message))
        message_nouns = extract_nouns(tagged_user_message)
        message_nouns_vectors = [nlp(noun).vector for noun in message_nouns]
        topic = responses[index][0]
        topic_vector = nlp(topic).vector
        best_match = ""
        closest_vector = 1
        for i, vector in enumerate(message_nouns_vectors):
            a = cosine(vector, topic_vector)
            if a < closest_vector:
                closest_vector = a
                best_match = message_nouns[i]
        return best_match


    def respond(self, user_message):
        best_response, best_response_index = self.find_intent_match(responses, user_message)
        entity = self.find_entities(user_message, best_response_index)
        print(best_response.format(entity))
        input_message = input()  # any other questions?
        return input_message

chatbot = ChatBot()
chatbot.intro()

'''
       tokens = nlp(" ".join(message_nouns))
       category = nlp(responses[index][0])
       word2vec_result = compute_similarity(tokens, category)
       word2vec_result.sort(key=lambda x: x[2])
       if len(word2vec_result) < 1:
           return responses[index][0]
       else:A
           return word2vec_result[-1][0]
       '''