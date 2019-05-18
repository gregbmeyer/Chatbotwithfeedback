# -*- coding: utf-8 -*-
import sys
import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement

chatbot = ChatBot(
        "DrSeussBot",
        database="./database.sqlite3",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        input_adapter='chatterbot.input.TerminalAdapter',
        output_adapter='chatterbot.output.TerminalAdapter',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        logic_adapters=[
                {
                        'import_path': 'chatterbot.logic.BestMatch',
                        'default_response': 'Fox in Socks!',
                        'maximum_similarity_threshold': 0.90
                }],
        filters=['chatterbot.filters.RepetitiveResponseFilter']
        )

# Suppress warnings before each response:
chatbot.logger.setLevel(logging.ERROR)

if len(sys.argv) > 1:
        print(sys.argv[1])
        if sys.argv[1]=="-init":
                print('\nInitializing new generic corpus training.')
                corpus_trainer = ChatterBotCorpusTrainer(chatbot)
                corpus_trainer.train('chatterbot.corpus.english')

                #Load core of specifc corpus for initial training
                #The text file should be a conversation that is newlined only with no extra markings
                with open('AllSeuss.txt', 'rb') as all_seuss:
                    data = all_seuss.read().decode(encoding='cp1252')

                conversations = data.strip().split('\n')
                list_trainer = ListTrainer(chatbot)
                list_trainer.train(conversations)
        else:
                print('\nThe program will utilize its latest learning interactions.')
else:
        print('\nUsage is: DrSeussBot.py -init  for an initial corpus incorporation.')
#print('\nAdmiral Rickover Chatbot Started:')
count=0

def get_feedback():
    from chatterbot.utils import input_function
    text = input_function()
    if 'y' in text.lower():
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Please type either "Y" or "N"')
        return get_feedback()

def get_betterResponse(input_statement):
        from chatterbot.utils import input_function
        print('\n What would be a better response?\n')
        betterResponse = input_function()
        if len(betterResponse)>1:
                betterResponse1=chatbot.input.process_input_statement(betterResponse)
                chatbot.learn_response(betterResponse1, input_statement)
                # Update the conversation history for the bot
                chatbot.storage.add_to_conversation(input_statement, betterResponse1)
                print('input', input_statement, 'Response', betterResponse, '\n')
                chatbot.output.process_response(betterResponse1)
                return True
        else:
                return False

try:
        while True:
                count = count + 1
                print(" -> You")
                input_statement = Statement(text=input())
                print(" -> SeussBot")
                response = chatbot.generate_response(input_statement)
                print(response)
                #print('\n Is "{}" a good Seussian response to "{}"? \n Type Y or N'.format(response, input_statement))
                #if get_feedback():
                #        chatbot.learn_response(response, input_statement)
                #        # Update the conversation history for the bot
                #        chatbot.storage.add_to_conversation(statement, response)
                #        chatbot.output.process_response(response)
                #else:
                #        get_betterResponse(input_statement)
                #        print("Sweet!")
except (KeyboardInterrupt, EOFError, SystemExit):
        pass
