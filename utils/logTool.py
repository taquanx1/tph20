import os

class Print():
    def __init__(self, log_path = None, text = None):
        print(text)
        if log_path != None:
            text = text if text != None else ''

            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(text)
                f.write('\n')
