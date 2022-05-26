import datetime
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticStie(Sitemap):
    changefreq = "daily"
    priority = 0.9
    lastmod = datetime.date.today()
    protocol = "https"
    
    def items(self):
        return ['addG', 'subG', 'mulG', 'divG']

    def location(self, item):
        return reverse(item)

class AddSite(Sitemap):
    changefreq = "daily"
    priority = 0.9
    lastmod = datetime.date.today()
    protocol = "https"
    
    def items(self):
        return [i for i in range(1,101)]

    def location(self, item):
        return reverse('add', kwargs={'a':item})



class SubSite(Sitemap):
    changefreq = "daily"
    priority = 0.9
    lastmod = datetime.date.today()
    protocol = "https"
    
    def items(self):
        return [i for i in range(1,101)]

    def location(self, item):
        return reverse('sub', kwargs={'a':item})
    


class MultiplySite(Sitemap):
    changefreq = "daily"
    priority = 0.9
    lastmod = datetime.date.today()
    protocol = "https"
    
    def items(self):
        return [i for i in range(1,101)]

    def location(self, item):
        return reverse('multiply', kwargs={'a':item})
    


class DivisionSite(Sitemap):
    changefreq = "daily"
    priority = 0.9
    lastmod = datetime.date.today()
    protocol = "https"
    
    def items(self):
        return [i for i in range(1,101)]

    def location(self, item):
        return reverse('division', kwargs={'a':item})

    
        