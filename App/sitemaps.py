import datetime
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticStie(Sitemap):
    changefreq = "daily"
    priority = 0.9
    lastmod = datetime.date.today()
    
    

    def items(self):
        return ['addG', 'subG', 'mulG', 'divG']

    def location(self, item):
        return reverse(item)

class DynamicSite(Sitemap):
    priority = 0.9
    
    def items(self):
        return [i for i in range(1,101)]

    def location(self, item):
        return reverse('add', kwargs={'a':item})
        