# -*- coding: utf-8 -*-
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("DrSeussBot",
        database="./database.sqlite3",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        input_adapter='chatterbot.input.TerminalAdapter',
        output_adapter='chatterbot.output.TerminalAdapter',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        logic_adapters=[
                'chatterbot.logic.BestMatch',
                {
                      'import_path':  'chatterbot.logic.LowConfidenceAdapter',
                      'threshold':  0.9,
                      'default_response':  'Fox in Socks!'
                 }],
        filters=['chatterbot.filters.RepetitiveResponseFilter']
        )
if len(sys.argv) > 1:
        print(sys.argv[1])
        if sys.argv[1]=="-init":
                print('\nInitializing new generic corpus training.')
                chatbot.train("chatterbot.corpus.english")
                #Load core of specifc corpus for initial training
                #The text file should be a conversation that is newlined only with no extra markings
                data = open('AllSeuss.txt').read()
                conversations = data.strip().split('\n')
                chatbot.set_trainer(ListTrainer)
                chatbot.train(conversations)
        else:
                print('\nThe program will utilize its latest learning interactions.')
else:
        print('\nUsage is: DrSeussBot.py -init  for an initial corpus incorporation.')
#print('\nAdmiral Rickover Chatbot Started:')
count=0
CONVERSATION_ID = chatbot.storage.create_conversation()

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

def get_betterResponse(input_statement, CONVERSATION_ID):
        from chatterbot.utils import input_function
        print('\n What would be a better response?\n')
        betterResponse = input_function()
        if len(betterResponse)>1:
                betterResponse1=chatbot.input.process_input_statement(betterResponse)
                chatbot.learn_response(betterResponse1, input_statement)
                # Update the conversation history for the bot
                chatbot.storage.add_to_conversation(CONVERSATION_ID, input_statement, betterResponse1)
                print('conv_id', CONVERSATION_ID, 'input', input_statement, 'Response', betterResponse, '\n')
                chatbot.output.process_response(betterResponse1)
                return True
        else:
                return False
        
while True:
        count = count + 1
        try:
                print(" -> You")
                input_statement = chatbot.input.process_input_statement()
                print("-> SeussBot")
                statement,response = chatbot.generate_response(input_statement, CONVERSATION_ID)
                print(response)
               # print('\n Is "{}" a good Seussian response to "{}"? \n Type Y or N'.format(response, input_statement))
               # if get_feedback():
               #         chatbot.learn_response(response, input_statement)
                #        # Update the conversation history for the bot
                #        chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, response)
                #        chatbot.output.process_response(response)
                #else:
                #        get_betterResponse(input_statement, CONVERSATION_ID)
                #        print("Sweet!")
        except:
                break
