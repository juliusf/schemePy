import string
class Stream(object):
    """docstring for ClassName"""
    def __init__(self, data):
        super(Stream, self).__init__()
        self.data = data
        self.i = 0

    def peek(self):
        return self.data[self.i]

    def skip_whitespace(self):
        while self.data[self.i] in string.whitespace:
            self.i += 1

    def read_until_whitespace(self):
        offset = 0
        while (not self.data[self.i + offset] in string.whitespace) and  (self.data[self.i + offset] != ')'):
            offset += 1
        local_ret = self.data[self.i:self.i+offset]
        self.i += offset
        return local_ret

    def check_until_whitespace(self, cond):
        offset = 0
        while(True):
            if string.whitespace.contains(self.data[self.i + offset]):
                return True
            if not cond(self.data[i + offset]):
                return False

    def read_until(self, cond):
        offset = 0
        while cond(self.data[self.i+offset], self.data[self.i:self.i+offset]):
            offset += 1
        local_ret = self.data[self.i:self.i+offset]
        self.i += offset
        return local_ret

    def skip(self, nr_chars):
        assert(self.i + nr_chars < len(self.data))
        self.i += nr_chars

    def is_EOF(self, offset=None):
        if offset !=None:
            return self.i + offset >= len(self.data)
        else:
            return self.i >= len(self.data)

