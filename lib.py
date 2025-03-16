import os
import re
import hashlib
import time

class WatcherOption:
    dir: str
    regex: str
    REGEX: str
    after_action: str
    daction: str
    maction: str
    caction: str
    before_action: str
    period: float
    use_hash: bool
    verbose: bool
    def __init__(self,config_dict):
        self.setDefault()
        for i in [
            'dir',
            'regex',
            'REGEX',
            'after_action',
            'daction',
            'maction',
            'caction',
            'before_action',
            'period',
            'use_hash',
            'verbose',
        ]:
            if config_dict[i]:
                self.__dict__[i]=config_dict[i]

    def setDefault(self):
        self.dir='.'
        self.regex=['.*']
        self.REGEX=[]
        self.after_action='echo done;'
        self.daction='echo file {} deleted'
        self.maction='echo file {} modified'
        self.caction='echo file {} created'
        self.before_action='echo changed;'
        self.period=1
        self.use_hash=False
        self.verbose=False

    def __str__(self):
        return str(self.__dict__)

class Watcher:
    def __init__(self,option:WatcherOption):
        self.option=option
        self.matcher=Matcher(self.option.regex,self.option.REGEX)
        if self.option.verbose:
            print(self.option)

    def startLoop(self):
        self.last_collection=self.collect()
        while True:
            collection=self.collect()
            change_report=self.diff(self.last_collection,collection)
            self.last_collection=collection
            self.execute(*change_report)
            time.sleep(self.option.period)

    def diff(self,old,new):
        deleted=[*filter(lambda i: not i in new,old)]
        modified=[*filter(lambda i: i in old and new[i]!=old[i],new)]
        created=[*filter(lambda i: not i in old,new)]
        return (len(deleted)+len(modified)+len(created)>0,
            deleted,
            modified,
            created,
        )

    def collect(self):
        ret={}
        for cur,_,file_names in os.walk(self.option.dir):
            for i in file_names:
                fname=cur+'/'+i
                if self.matcher.match(fname):
                    ret[fname]=self.getFileState(fname)
        return ret

    def getFileState(self, fname):
        if self.option.use_hash:
            with open(fname,'rb') as f:
                return hashlib.md5(f.read()).digest()
        else:
            return os.path.getmtime(fname)

    def execute(self,any_changes,deleted,modified,created):
        if not any_changes:
            if self.option.verbose:
                print(
                    time.strftime('%y-%m-%d %H:%M:%S')+' no changes'
                )
            return

        os.system(self.option.before_action)
        for i in deleted:
            os.system(self.option.daction.replace('{}',i))
        for i in modified:
            os.system(self.option.maction.replace('{}',i))
        for i in created:
            os.system(self.option.caction.replace('{}',i))
        os.system(self.option.after_action)

class Matcher:
    def __init__(self,regexes,REGEXes):
        self.regexes=regexes
        self.REGEXes=REGEXes

    def match(self, s):
        return self.matchOneOfregexes(s)\
            and self.matchNoneOfREGEXes(s)

    def matchOneOfregexes(self, s):
        for i in self.regexes:
            if re.match(i,s):
                return True
        return False

    def matchNoneOfREGEXes(self,s):
        for i in self.REGEXes:
            if re.match(i,s):
                return False
        return True
