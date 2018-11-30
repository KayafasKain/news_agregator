from telegram.ext import Updater, CommandHandler, Dispatcher
from settings import TelegramBotToken
import re
from bot_database import DBOperator

from settings import NewsAggregatorClient
class BotCore():

    bot_dict = {
        'start': 'Wellcome! Here you can get some news. You can learn about commands when type: "/commands"',
        'commands': '''
            1) everypony.ru - "/watch everypony" to start recieving news from everypony or "/unwatch_everypony" to stop watching pony news 
        '''
    }

    watch_dict = {
        'everypony': r'ever[i|y]pon[i|y]'
    }

    preferences = [
        'everypony'
    ]

    def __init__(self, token, bot_dict=None, db=None, job_interval=600):
        self.token = token
        self.updater = Updater(token=TelegramBotToken)
        self.jobs = self.updater.job_queue
        self.dispatcher = self.updater.dispatcher
        self.job_interval = job_interval

        if bot_dict:
            self.bot_dict = bot_dict
        if db:
            self.db = db
        else:
            raise ValueError('Please, provide db-collection instance')
        self.set_up_updaters()

    def set_up_updaters(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('commands', self.commands))
        self.dispatcher.add_handler(CommandHandler('watch', self.watch, pass_args=True))
        self.updater.start_polling()

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.bot_dict['start'])
        self.db.execute_task(self.db.create_subscriber({
            'chat_id': update.message.chat_id,
            'preferences': []
        }))

    def commands(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.bot_dict['commands'])

    def watch(self, bot, update, args):
        command = " ".join(args)
        if re.match(self.watch_dict['everypony'], command):
            subscriber = self.db.execute_task(self.db.find_subscriber(update.message.chat_id))
            if 'everypony' not in subscriber['preferences']:
                subscriber['preferences'].append('everypony')
                self.db.execute_task(self.db.update_subscriber(subscriber))

    def send_news(self):
        pass

    def take_news(self, bot, update,  collection='everypony'):
        news = self.db.execute_task(self.db.get_fresh_items(collection=collection))
        for post in news:
            bot.send_message(chat_id=update.message.chat_id, text='''
                {title}
                {link}            
            '''.format(title=post['title'], link=post['link']))

BotCore(TelegramBotToken, db=DBOperator(NewsAggregatorClient))
