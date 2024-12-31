from pathlib import Path
import re
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "songs"

    def start_requests(self):
        urls = [ "https://www.nepalichristiansongs.com/a.php", "https://www.nepalichristiansongs.com/aa.php", "https://www.nepalichristiansongs.com/i.php", "https://www.nepalichristiansongs.com/ii.php", "https://www.nepalichristiansongs.com/u.php", "https://www.nepalichristiansongs.com/uu.php", "https://www.nepalichristiansongs.com/R_.php", "https://www.nepalichristiansongs.com/e.php", "https://www.nepalichristiansongs.com/ai.php", "https://www.nepalichristiansongs.com/o.php", "https://www.nepalichristiansongs.com/au.php", "https://www.nepalichristiansongs.com/k.php", "https://www.nepalichristiansongs.com/kh.php", "https://www.nepalichristiansongs.com/g.php", "https://www.nepalichristiansongs.com/gh.php", "https://www.nepalichristiansongs.com/Ng.php", "https://www.nepalichristiansongs.com/ch.php", "https://www.nepalichristiansongs.com/chh.php", "https://www.nepalichristiansongs.com/j.php", "https://www.nepalichristiansongs.com/jh.php", "https://www.nepalichristiansongs.com/Nj.php", "https://www.nepalichristiansongs.com/T_.php", "https://www.nepalichristiansongs.com/T_h.php", "https://www.nepalichristiansongs.com/D_.php", "https://www.nepalichristiansongs.com/D_h.php", "https://www.nepalichristiansongs.com/N_.php", "https://www.nepalichristiansongs.com/t.php", "https://www.nepalichristiansongs.com/th.php", "https://www.nepalichristiansongs.com/d.php", "https://www.nepalichristiansongs.com/dh.php", "https://www.nepalichristiansongs.com/n.php", "https://www.nepalichristiansongs.com/p.php", "https://www.nepalichristiansongs.com/ph.php", "https://www.nepalichristiansongs.com/b.php", "https://www.nepalichristiansongs.com/bh.php", "https://www.nepalichristiansongs.com/m.php", "https://www.nepalichristiansongs.com/y.php", "https://www.nepalichristiansongs.com/r.php", "https://www.nepalichristiansongs.com/l.php", "https://www.nepalichristiansongs.com/w.php", "https://www.nepalichristiansongs.com/sh.php", "https://www.nepalichristiansongs.com/S_h.php", "https://www.nepalichristiansongs.com/s.php", "https://www.nepalichristiansongs.com/h.php", "https://www.nepalichristiansongs.com/kSh.php", "https://www.nepalichristiansongs.com/tr.php", "https://www.nepalichristiansongs.com/Gy.php"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        page = response.url.split("/")[-2]
        pageName = response.url.split("/")[-1]
        filename = f"songs-{page + pageName}.html"
        pattern = r'\bkb:([^,]+)'
        noscriptelements = response.xpath('//noscript')

        for noscript in noscriptelements: 
            kb_value = ''
            dd_element = noscript.xpath('following-sibling::dd[1]')
            info = noscript.css("dt").css("span.songDetails::text").get()
            
            if info is not None:
                if info.strip():
                    match = re.search(pattern, info)
                    if match:
                        kb_value = match.group(1).strip()
            
            yield {
                "name": noscript.css("dt.nepali::text").get(),
                "number": kb_value,
                "song": dd_element.css("pre::text").get()
            }


        #Path(filename).write_bytes(response.body)
        #self.log(f"Saved file {filename}")