# -*- coding: utf-8 -*-
import pyttsx
engine = pyttsx.init()
engine.getProperty('rate')
engine.getProperty('volume')
engine.setProperty('rate', -50)
engine.setProperty('volume', +0.25)
# check what voices are available
voices = engine.getProperty('voices')
for voice in voices:
	print(voice.id)
	engine.setProperty('voice', voice.id)
	engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()

def admRickSpeak(inputTt):
    q = ''
    tlist = list(inputT)
    if len(tlist) > 0:
        for q in tlist:
            if q == '':
                tlist.remove(q)
    txt = ''.join(tlist)
    if txt != "":
        speech_engine.say(txt)
        speech_engine.runAndWait()

def narratorSpeak(inputTt):
    z = ''
    tlist = list(inputT)
    if len(tlist) > 0:
        for z in tlist:
            if z == '':
                tlist.remove(z)
    txt = ''.join(tlist)
    if txt != "":
        speech_engine.say(txt)
        speech_engine.runAndWait()

from chatterbot import ChatBot
chatbot = ChatBot("Admiral Rickover",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    logic_adapters=[
	'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ],
    database='./database.sqlite3')

#Load known Admiral Rickover conversations and quotes

from chatterbot.trainers import ListTrainer
conversation = ['Would you describe the start of your Atomic Sub Career?', 
'I was assigned a job by myself in an ex ladies powder room.', 
'Do you smoke?',  
'I do not smoke.',
'How big was your office?',
'I had a small and unpretentious office.',
'Who are you married to?',  
'My first wife was Ruth.',
'Who was your second wife?', 
'My second wife was Elonore.',
'Do you have any kids?',  
'I had one child, Robert.',
'What are your hobbies?',  
'My only hobby is reading.',
'How much do you weigh?',  
'I weigh 125 pounds.',
'What color is your hair? ', 
'I have grey hair.',
'How do you like the rain?',  
'Its wet.',
'May I ask you a question?',  
'Why dont you turn in a sheet of blank paper?',
'Can responsibility be delegated?', 
'You may delegate responsibility, but it is still with you.',
'What does Success teach us?',  
'Success teaches us nothing; only failure teaches.',
'What do you think about optimistic people?',  
'Optimism and stupidity are nearly synonymous.',
'Should one pay attention to detail in doing their job?', 
'The Devil is in the details, but so is salvation.',
'How can one creatively solve a problem?',  
'Sit down before fact with an open mind.',
'What is your thought on good research?',
'Follow humbly to whatever abyss Nature leads or you learn nothing.', 
'What do you think of bureaucracy?',  
'More than ambition or ability, it is rules that limit contribution.',
'What is your thought on military readiness?',  
'The more you sweat in peace the less you bleed in war.',
'Is being consistent an asset? ', 
'Do not be consistent, consistency is the refuge of fools.',
]
chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)
print('Admiral Rickover Chatbot Started:')
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
    print('\n Please type in a better response:\n')
    narratorSpeak("Please type in a better response.")
    betterResponse = input_function()
    if len(betterResponse)>1:
	betterResponse1=chatbot.input.process_input_statement(betterResponse)
	chatbot.learn_response(betterResponse1, input_statement)
	# Update the conversation history for the bot
	chatbot.storage.add_to_conversation(CONVERSATION_ID, input_statement, betterResponse1)
	chatbot.output.process_response(betterResponse1)
	return True
    else:
	return False

while True:
    count = count + 1
    try:
        print("Type a question for Admiral Rickover:")
        narratorSpeak("Type a question for Admiral Rickover.")
        input_statement = chatbot.input.process_input_statement()
        statement,response = chatbot.generate_response(input_statement, CONVERSATION_ID)
        admRickSpeak(response)
        print('\n Is "{}" this a coherent response to "{}"? \n Type Y or N'.format(response, input_statement))

	if get_feedback():
		chatbot.learn_response(response, input_statement)
		# Update the conversation history for the bot
		chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, response)
		chatbot.output.process_response(response)
	else:
		if get_betterResponse(input_statement, CONVERSATION_ID):
			print("Thank you.")
			narratorSpeak("Thank you")
		else:
			print("Don't be dumb! Ask better questions.")
			admRickSpeak("Don't be dumb! Ask better questions.")



    # Press ctrl-c or ctrl-d to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break