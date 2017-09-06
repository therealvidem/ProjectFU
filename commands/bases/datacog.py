import data
from . import BaseCog

class DataCog(BaseCog):
    '''
    Essentially BaseCog, but with settings and data features.
    '''

    def __init__(self, bot, cogname):
        super().__init__(bot, cogname)
        data.check_data_folder(self.cogname)
        self.settings_path = 'data/{}/settings.json'.format(self.cogname)
        self.settings = data.load_json(self.settings_path)

    async def save_settings(self):
        data.save_json(self.settings_path, self.settings)
