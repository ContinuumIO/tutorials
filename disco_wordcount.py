from disco.job import Job
from disco.worker.classic.func import chain_reader
from disco.core import result_iterator

class WordCount(Job):
    
    partitions = 4
    input=["book:rats",] 
                    
    @staticmethod
    def map(line, params):
        for word in line.split():
            yield word, 1

    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup
        for word, counts in kvgroup(sorted(iter)):
            yield word, sum(counts)
 
if __name__ == "__main__":
    from disco_wordcount import WordCount

    wordcount = WordCount().run()
    
    
    for (word, counts) in result_iterator(wordcount.wait(show=True)):
        print word, counts
        