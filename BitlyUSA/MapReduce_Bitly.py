 #http://www.usa.gov/About/developer-resources/1usagov.shtml
  #{
        #"a": USER_AGENT, 
        #"c": COUNTRY_CODE, # 2-character iso code
        #"nk": KNOWN_USER,  # 1 or 0. 0=this is the first time we've seen this browser
        #"g": GLOBAL_BITLY_HASH, 
        #"h": ENCODING_USER_BITLY_HASH,
        #"l": ENCODING_USER_LOGIN,
        #"hh": SHORT_URL_CNAME,
        #"r": REFERRING_URL,
        #"u": LONG_URL,
        #"t": TIMESTAMP,
        #"gr": GEO_REGION,
        #"ll": [LATITUDE, LONGITUDE],
        #"cy": GEO_CITY_NAME,
        #"tz": TIMEZONE # in http://en.wikipedia.org/wiki/Zoneinfo format
        #"hc": TIMESTAMP OF TIME HASH WAS CREATED, 
        #"al": ACCEPT_LANGUAGE http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4 
    #}
from disco.job import Job
from disco.worker.classic.func import chain_reader
from disco.core import result_iterator

class TopLinks(Job):
    partitions = 4
    input=["bitly:03:13:13",]
     
    @staticmethod
    def map(line, params):
        import json
        try:
            record = json.loads(line) 
            if ('u' in record) and 'll' in record:
                link = record['u']
                yield '%s' % (link.encode('utf-8')), record 
        except ValueError: #Some lines are malformed.  Done in the absence of good error handling in Disco.
            pass
        
        
    
    @staticmethod
    def reduce(link_iter, out, params):
        from collections import defaultdict    
        counts = defaultdict(int)
        recDictArray = defaultdict(list)
        
        #store link count and record 
        for link,rec in link_iter:
            counts[link] += 1
            recDictArray[link].append( (rec['t'],rec['ll'][0], rec['ll'][1]) )
        
        
        #sort the links 
        sortedCounts = sorted(counts.iteritems(), key=operator.itemgetter(1), reverse=True)

        #yield top 10 URLs with the highest click count 
        for top10 in sortedCounts[:10]:
            out.add(top10, recDictArray[top10[0]])
        
        

        
if __name__ == '__main__':
    import os
    from MapReduce_Bitly import TopLinks

    topLinks = TopLinks().run()

    #gather top 10 from each reducer
    unsortedRecords = [(link_count[0], link_count[1], rec) for link_count, rec in result_iterator(topLinks.wait(show=True))]
    for events in unsortedRecords:
        print '\t', len(events[2])
    
    #sort the top 10 of each reducer and get the top 10
    sortedRecords = sorted(unsortedRecords, key = lambda count: count[1], reverse=True)[:10]
    
    #get list of numpyarrays
    import numpy as np
        
    import matplotlib
    matplotlib.use('Agg')
    
    import matplotlib.pyplot as plt
    import pytz
    import datetime
    import time, math

    #create 3x3 plot of top 9 links with highest clicks
    # plt.subplots_adjust(hspace=5.4, wspace=5.6)
    for index,events in enumerate(sortedRecords[:-1]):
        plt.figure()
        filePath = '/tmp/' #FILL IN
        out = open(filePath+'link_'+str(index)+'.out', 'w')
        
        #store time/location of click
        out.write('%s \n' % events[0])
        for rec in events[2]:
            out.write('%s \n' % (str(rec)))
        
        out.close()
        
        timestamps = np.array(events[2])[:,0] #get timestamps
        print events[0], len(timestamps)
        bins, binnedTimes = np.histogram(timestamps, bins=10) 
        
        
        est=pytz.timezone('US/Eastern') 
        total_time = (timestamps[-1]-timestamps[0])/60.
        
        dates=[datetime.datetime.fromtimestamp(ts,est) for ts in binnedTimes[:-1]] #convert utc time to US/Eastern
    
        
        plt.xticks(rotation=25,fontsize = 8)
        plt.title(sortedRecords[index][0] + '   t: '+str(len(timestamps)),fontsize = 6)
        plt.plot_date(dates,bins,tz=est,linestyle='dashed')
        

        plt.savefig(str(index)+'_top_USA-GOV_links.png')
