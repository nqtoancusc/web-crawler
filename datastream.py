#!/usr/bin/env python
import re

class DataStream:
    """
    Data Stream class provides a set of methods to work with a data stream.

    Attributes:
        cur_str: data stream cursor
        buffer: data buffer
        size: data stream size
        position: current position of data stream cursor
    """

    def __init__(self, str):
        self.buffer = None
        self.size = None
        self.position = None
        self.cur_str = ""
        self.setdata(str)
        self.mo = None

    def setdata(self, data):
        # Set data to stream.
        self.buffer = data
        self.size = len(data)
        self.position = 0
        self.move_pos(0)

    def move_pos(self, offset):
        # Move to offset position in stream.
        p = self.position + offset
        return self.setpos(p);

    def setpos(self, p):
        # Set cusor position.
        if p >= self.size:
            self.size = self.position
            self.cur_str = ""
            return False
        else:
            self.position = p
            self.cur_str = self.buffer[self.position:]
            return True

    def size(self):
        # Return stream size.
        return self.size

    def pos(self):
        # Return cursor position.
        return self.position

    def eof(self):
        # Check end of stream.
        return self.size == self.position

    def skipws(self):
        # Skip white spaces.
        while not self.eof():
            if self.buffer[self.position] == ' ':
                self.move_pos(1)
            elif self.buffer[self.position] == '\t':
                self.move_pos(1)
            elif self.buffer[self.position] == '\r':
                self.move_pos(1)
            elif self.buffer[self.position] == '\n':
                self.move_pos(1)
            else:
                return
    
    def read_dq(self, name):
        # Read attribute value inside double quote.
        id = "%s=\"" % name
        self.getnextre(id)
        return self.getto("\"").strip()
    
    def read_sq(self, name):
        # Read attribute value inside single quote.
        id = "%s='" % name
        self.getnextre(id)
        return self.getto("'").strip()
    
    def read_et(self, name):
        # Read attribute value inside element tag.
        if self.getnextre(name):
            return self.getto("<").strip()
        else:
            return None
        
    def read_hx_et(self, name):
        # Read attribute value inside element tag after ignoring nested tags.
        if self.getnextre(name):
            self.hx()
            return self.getto("<").strip()
        else:
            return None
    
    def go(self, restr):
        # Read attribute value inside element tag after ignoring nested tags.
        pat = re.compile(restr, re.IGNORECASE)
        self.mo = re.search(pat, self.cur_str)
        if self.mo == None:
            return False

        i = self.cur_str.find(self.mo.group(0))
        if i == -1:
            return False
        self.move_pos(i)
        return True

    def findre(self, restr):
        # Return true if find data matches regular expression string
        self.mo = re.search(re.compile(restr, re.IGNORECASE), self.cur_str)
        return self.mo != None

    def getnextre(self, restr):
        # Get data matches regular expression string and move the cursor to new postion from the first found one + number of characters are read.
        pat = re.compile(restr, re.IGNORECASE)
        self.mo = re.search(pat, self.cur_str)
        if self.mo == None:
            return None

        i = self.cur_str.find(self.mo.group(0))
        if i == -1:
            return None

        self.move_pos(i + len(self.mo.group(0)))
        return self.mo.group(0)


    def getto(self, restr):
        # Get next data from current position to matches regular expression string
        pat = re.compile(restr, re.IGNORECASE)
        self.mo = re.search(pat, self.cur_str)
        if self.mo == None:
            return self.cur_str

        i = self.cur_str.find(self.mo.group(0))
        if i == -1:
            return self.cur_str

        rtn = self.cur_str[0:i]
        self.move_pos(i)
        return rtn

    def getdata(self):
        # Get all data
        return self.buffer

    def getdataleft(self):
        # Get data left
        return self.cur_str

    def getn(self, n):
        # Get n characters in stream
        return self.cur_str[0:n]

    def getre(self, restr):
        # Get data matches regular expression string and move the cursor to new postion from current postion.
        pat = re.compile(restr, re.IGNORECASE)
        self.mo = pat.match(self.cur_str)
        if self.mo == None:
            return None

        self.move_pos(len(self.mo.group(0)))
        return self.mo.group(0)

    def get(self, str):
        # Get data matches a string and move the cursor to new postion from current postion.
        i = self.cur_str.find(str)
        if i == 0:
            return self.move_pos(len(str))

        return False


    def readint(self):
        # Get an integer.
        if len(self.cur_str) == 0:
            return None
        restr = r'\d+'
        pat = re.compile(restr, re.IGNORECASE)
        self.skipws()
        f = False
        if self.cur_str[0] == '+':
            self.getre(".")
        elif self.cur_str[0] == '-':
            self.getre(".")
            f = True    

        self.mo = pat.match(self.cur_str)
        if self.mo == None:
            return None

        self.move_pos(len(self.mo.group(0)))
        if f == True:
            return 0 - int(self.mo.group(0))
        else:
            return int(self.mo.group(0))

    def readdouble(self):
        # Get an double.
        if len(self.cur_str) == 0:
            return None
        
        is_neg = False  
        if self.cur_str[0] == "+":
            self.move_pos(1)
        elif self.cur_str[0] == "-":
            self.move_pos(1)
            is_neg = True 
          
        restr = r'\d+[\.]?\d*'
        pat = re.compile(restr, re.IGNORECASE)
        self.skipws()
        self.mo = pat.match(self.cur_str)
        if self.mo == None:
            return None
        
        
        self.move_pos(len(self.mo.group(0)))
        if not is_neg:
            return float(self.mo.group(0))
        else:
            return 0 - float(self.mo.group(0))

    def hx(self):
        # Skip all next consecutive tags
        self.getnextre(">")
        self.skipws()
        while self.get("<") == True:
            self.getnextre(">")
            self.skipws()

    def readmstr(self, mstr):
        mset = mstr.split(";")
        self.skipws()
        rtn = 1
        for ms in mset:
            pat = re.compile(ms, re.IGNORECASE)
            self.mo = pat.match(self.cur_str)
            if self.mo:
                self.move_pos(len(self.mo.group(0)))
                return rtn
            rtn = rtn + 1

        return None

    def getn(self, n):
        len_left = len(self.cur_str)
        if n >= len_left:
            rtn = self.cur_str
            self.move_pos(len_left)
        else:
            rtn = self.cur_str[0:n]
            self.move_pos(n)

        return rtn
    
    def read_block(self, re_start, re_end):
        # Read a block from regular expression start to regular expression end.
        if not self.getnextre(re_start):
            return None
        
        return self.getto(re_end)
    

    def read_nested_block(self, re_start, re_end):
        if not self.getto(re_start):
            return None

        pos_start = self.position
        st = self.position
        left = 0
        while True:
            if not self.getnextre(re_end):
                return None

            ed = self.position
            c = self.buffer[st:ed]
            pat = re.compile(re_start, re.IGNORECASE)
            count = 0
            while True:
                self.mo = re.search(pat, c)
                if not self.mo:
                    break
                count = count + 1
                i = c.find(self.mo.group(0))
                i = i + len(self.mo.group(0))
                c = c[i:]

            left = left + count - 1
            if left ==  0:
                break
            st = self.position

        final_pos = self.position
        return self.buffer[pos_start:final_pos]
