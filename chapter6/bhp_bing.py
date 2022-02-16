# Issues: burp does not like request from urllib
# Works in a test script I made but using .parse or .requests exits the code
# Trying to brute force burp into accepting those modules 

from burp import IBurpExtender
from burp import IContextMenuFactory

from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib
API_KEY = ""
API_HOST = "https://api.bing.microsoft.com/v7.0/search?q="

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)
        
        return
        
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        return menu_list
        
    def bing_menu(self, event):
        http_traffic = self.context.getSelectedMessages()
        
        print("%d requests highlighted" % len(http_traffic))
        
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            
            print("User selected host: %s" % host)
            self.bing_search(host)
        
        return
        
    def bing_search(self, host):
        try:
            is_ip = bool(socket.inet_aton(host))
        except socket.error:
            is_ip = False
        
        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        
        start_new_thread(self.bing_query, ('ip:%s' % ip_address,))
        
        if domain:
            start_new_thread(self.bing_query, ('domain:%s' % host,))
    
    def bing_query(self,bing_query_string):
        print('Performing Bing search: %s' % bing_query_string)
        test = urllib.request.urlopen('https://google.com')
        print(test)
        
        query = urllib.parse.urlencode(bing_query_string)
        
        req = urllib.request.Request(url=API_HOST+query)
        req.add_header("Ocp-Apim-Subscription-Key", API_KEY)
        
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        try:
            r = data
            sites = r['webPages']['value']
            if len(sites):
                for site in sites:
                    print("*"*100)
                    print(site['name'])
                    print(site['url'])
                    print(site['snippet'])
                    print("*"*100)
                    new_url = URL(site['url'])
                    if not self._callbacks.isInScope(new_url):
                        print("Adding %s to Burp scope." % new_url)
                        self._callbacks.includeInScope(new_url)
        except:
            print('No results from Bing.')
            pass          
        return
    
