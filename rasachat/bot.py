from rasa.core.agent import Agent
from rasa.core.channels.socketio import SocketIOInput
#
# load your trained agent
agent = Agent.load('models')

input_channel = SocketIOInput(
    # event name for messages sent from the user
    user_message_evt="user_uttered",
    # event name for messages sent from the bot
    bot_message_evt="bot_uttered",
    # socket.io namespace to use for the messages
    namespace=None
)

# set serve_forever=False if you want to keep the server running
s = agent.handle_channels([input_channel], 5500)
