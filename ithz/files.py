import ithz.data
import ithz.mimetypes as mime



class generateFile(object):
    def __init__(self, id):
        r = ithz.data.queryFile(id)
        if r == None:
            self.success = False
        else:
            self.success = True
            self.content = r.data
            self.mime = bytes(r.mime)

class generateImageFile(object):
    def __init__(self, id):
        r = ithz.data.queryImageFile(id)
        if r == None:
            self.success = False
        else:
            self.success = True
            self.content = r.thumbnail
            self.mime = mime.png[0]

