# main.py
from chatbot.chatbot import speak, recognize_speech
from chatbot.knowledge_base import knowledge_base
import spacy
import wikipediaapi

# Initialize spaCy and Wikipedia-API with a user-agent string
nlp = spacy.load("en_core_web_sm")
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="Your_User_Agent_String"  # Replace with your own user-agent string
)


def search_knowledge(knowledge_base, search):
    current_pos = knowledge_base
    for item in search:
        if item in current_pos:
            current_pos = current_pos[item]
        else:
            return None
    return current_pos


search = []

# Function to search Wikipedia and return a summary based on user input


def search_wikipedia(query, words):
    try:
        page = wiki_wiki.page(query)
        if page.exists():
            # Return the first 500 characters of the summary
            return page.summary[:words]
        else:
            return "I couldn't find information on that topic."
    except Exception as e:
        return "An error occurred while searching Wikipedia."


def one_level_up():
    search.pop()


prevTopic = None
# Main chat loop


def main():
    def back_to_top():
        flag = False
        search.clear()
        print(search)
    flag = False
    while True:
        # speak("Ask Me your query...")
        user_input = input("You: ").strip()  # Remove leading/trailing spaces

        # Use spaCy to analyze the user's input
        doc = nlp(user_input)

        print("\n")

        # Initialize variables to store intent and topic
        intent = None
        topic = None

        # Define intents and their corresponding verb phrases
        intents = {
            "tell_me_about": ["tell me about", "describe", "explain", "give me information about", "some information about"],
            "what_is": ["what is", "define", "explain to me"],
        }

        # Detect user intent and extract the topic
        for intent_name, verb_phrases in intents.items():
            for verb_phrase in verb_phrases:
                if user_input.lower().startswith(verb_phrase):
                    topic = user_input[len(verb_phrase):].strip()
                    intent = intent_name
                    break

        # Process the user's intent and search Wikipedia
        # If no intent is detected, consider the input as a direct topic search
        if not intent and user_input:
            intent = "tell_me_about"
            topic = user_input

        # print(str(intent)+" "+str(topic))

        if (topic == "courses" or flag == True):
            # for course-------------------------------------------------
            if (topic == "0"):
                print("00000")
                back_to_top()
                continue
            elif (topic == "-1"):
                one_level_up()
            elif (topic == "courses" or flag == True):
                flag = True
                if (topic != "-1" and topic != "0"):
                    search.append(topic)
                result = search_knowledge(knowledge_base, search)

                if result:
                    ans = result.get(
                        "information", "No information available")+"\n Some Suggestions"+str(result.get("suggestions", []))
                    response = ans
                    # print("Some Information: " +
                    #       result.get("information", "No information available"))
                    # print("Some Suggestions: " +
                    #       str(result.get("suggestions", [])))
                elif (topic == "elaborate"):
                    response = search_wikipedia(prevTopic, 1000)
                else:
                    print(search)
                    search.pop()
                    response = search_wikipedia(topic, 300)
                    print("No information found from DB.")
                    # print(
                    #     "You can go back to the beginning by entering '0'.\n Or you can go back one level by entering '-1'")

            elif (topic):
                response = search_wikipedia(topic, 300)
        elif (topic == "elaborate"):
            response = search_wikipedia(prevTopic, 1000)
        elif (topic):
            response = search_wikipedia(topic, 300)

        else:
            response = "I'm not sure how to respond to that. Please try asking a specific question."

        print("Chatbot: ", response+" ...")
        speak(response)
        print("If you want to know more on that then enter 'elaborate'")

        # set the value of prev Topic
        prevTopic = topic

        print("\n\n")


if __name__ == "__main__":
    main()
