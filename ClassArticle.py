class Article():
    def __init__(self, id, title, datetime, image_source, description):
        self.title = title
        self.id = id
        self.datetime = datetime
        self.image_source = image_source
        self.description = description

    def get_id(self):
        return self.id