#-*- coding:utf-8 -*-

class Contact:
    '''
        a single contact
    '''
    def __init__(self, rank, frame, x, y, stime=-1, etime=-1, max_force=0, pixels=0, avg_force=0):
        self.x = x
        self.y = y
        self.rank = rank
        self.frames = []
        self.frames.append(frame)
        self.new = True # appears at this timestamp
        self.stime = stime #start time
        self.etime = etime #end time
        self.max_force = max_force
        self.pixels = pixels
        self.avg_force = avg_force
        self.palm = True
        self.valid = False
        self.sts = self.ets = 0
    def update(self, frame, x, y, etime, max_force, pixels, avg_force):
        self.new = False
        self.x = x
        self.y = y
        self.etime = etime
        self.frames.append(frame)
        if max_force > self.max_force:
            self.max_force = max_force
        if pixels > self.pixels:
            self.pixels = pixels
        if avg_force > self.avg_force:
            self.avg_force = avg_force
    def set_palm(self, is_palm):
        self.palm = is_palm
    def set_finger(self, finger): # 0-4 represent 5 finger
        self.finger = finger
    def toString(self):
        return str(self.rank) + " " + str(self.palm) + " " + str(self.x) + " " + str(self.y) + " " + str(self.max_force) + " " + str(self.avg_force) + " " + str(self.pixels) + " " + str(self.etime-self.stime+1)
    def __str__(self):
        return str(self.rank) + " " + str(self.palm) + " " + str(self.x) + " " + str(self.y) + " " + str(self.max_force) + " " + str(self.avg_force) + " " + str(self.pixels) + " " + str(self.stime) + " " + str(self.etime)
