import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QFileDialog, QMenu, QInputDialog,
    QDockWidget, QListWidget, QListWidgetItem, QLabel
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QPalette, QColor, QAction
from typing import Dict

class MultiSearchBrowser(QMainWindow):
    # Full set of engines (for this example, Text, Image, File, Audio, Code, AI, Maps, Trends)
    ENGINES: Dict[str, Dict[str, str]] = {
        "Text": {
            "Google": "https://www.google.com/search?q={}", "Bing": "https://www.bing.com/search?q={}",
            "Yahoo": "https://search.yahoo.com/search?p={}", "DuckDuckGo": "https://duckduckgo.com/?q={}",
            "Yandex": "https://yandex.com/search/?text={}", "Baidu": "https://www.baidu.com/s?wd={}",
            "Ask": "https://www.ask.com/web?q={}", "AOL": "https://search.aol.com/aol/search?q={}",
            "Ecosia": "https://www.ecosia.org/search?q={}", "Startpage": "https://www.startpage.com/sp/search?query={}",
            "Qwant": "https://www.qwant.com/?q={}", "Swisscows": "https://swisscows.com/web?query={}",
            "Lycos": "http://www.lycos.com/search?q={}", "Excite": "http://www.excite.com/search/web?q={}",
            "Dogpile": "http://www.dogpile.com/search/web?q={}", "Yippy": "http://www.yippy.com/search?q={}",
            "MetaCrawler": "http://www.metacrawler.com/search/web?q={}", "Mojeek": "https://www.mojeek.com/search?q={}",
            "Exalead": "https://www.exalead.com/search/results/?q={}", "Info.com": "http://www.info.com/search?q={}",
            "Metager": "https://www.metager.de/meta/meta.ger3?eingabe={}", "Oscobo": "https://oscobo.com/search/?q={}",
            "Search Encrypt": "https://www.searchencrypt.com/search?q={}", "Peekier": "https://peekier.com/?q={}",
            "Gibiru": "https://www.gibiru.com/results?q={}", "Searx": "https://searx.org/search?q={}",
            "GoodSearch": "https://www.goodsearch.com/search?q={}", "Lukol": "https://www.lukol.com/search?q={}",
            "Infinity Search": "https://infinitysearch.co/?q={}", "Unbubble": "https://unbubble.eu/search?q={}",
            "Search.com": "https://www.search.com/?q={}", "Clusty": "https://clusty.com/search?q={}",
            "KartOO": "https://www.kartoo.com/search?q={}", "WebCrawler": "https://www.webcrawler.com/serp?q={}",
            "HotBot": "https://hotbot.com/search?q={}", "Rediff": "https://www.rediff.com/search?q={}",
            "Entireweb": "https://www.entireweb.com/search?q={}", "MagicSeek": "https://www.magicseek.com/search?q={}",
            "GigaBlast": "https://www.gigablast.com/search?q={}", "SearchLock": "https://www.searchlock.com/search?q={}",
            "MetaLib": "https://metalibsearch.com/?q={}", "OpenFind": "https://www.openfind.com/search?q={}",
            "Findx": "https://www.findx.com/search?q={}", "Szukaj": "https://www.szukaj.com/search?q={}",
            "TheFind": "https://www.thefind.com/search?q={}", "InfoTiger": "http://www.infotiger.com/search?q={}",
            "FreeFind": "https://www.freefind.com/find.html?query={}", "LookSmart": "http://www.looksmart.com/?q={}",
            "Web Searcher": "https://www.websearcher.com/search?q={}", "SearchPlus": "https://www.searchplus.com/?q={}"
        },
        "Image": {
            "Google Images": "https://www.google.com/search?tbm=isch&q={}",
            "Bing Images": "https://www.bing.com/images/search?q={}",
            "Yandex Images": "https://yandex.com/images/search?text={}",
            "TinEye": "https://tineye.com/search?url={}",
            "Pinterest": "https://www.pinterest.com/search/pins/?q={}",
            "Flickr": "https://www.flickr.com/search/?text={}",
            "Shutterstock": "https://www.shutterstock.com/search?searchterm={}",
            "Getty Images": "https://www.gettyimages.com/photos/{}",
            "Unsplash": "https://unsplash.com/s/photos/{}",
            "Pixabay": "https://pixabay.com/images/search/{}",
            "Pexels": "https://www.pexels.com/search/{}",
            "Openverse": "https://openverse.org/search/?q={}",
            "500px": "https://500px.com/search?q={}",
            "StockSnap": "https://stocksnap.io/search/?q={}",
            "Canva Photos": "https://www.canva.com/search/photos?q={}",
            "Picsearch": "http://www.picsearch.com/?q={}",
            "PhotoPin": "http://photopin.com/?s={}",
            "FreeImages": "https://www.freeimages.com/search/{}",
            "Dreamstime": "https://www.dreamstime.com/photos-images/{}.html",
            "Adobe Stock": "https://stock.adobe.com/search?k={}",
            "iStock": "https://www.istockphoto.com/search/2/image?phrase={}",
            "Depositphotos": "https://depositphotos.com/stock-photos/{}.html",
            "Alamy": "https://www.alamy.com/search.html?qt={}",
            "Bigstock Photo": "https://www.bigstockphoto.com/search/?contributor=&keyword={}",
            "Fotolia": "https://us.fotolia.com/search?k={}",
            "Picjumbo": "https://picjumbo.com/?s={}",
            "Rawpixel": "https://www.rawpixel.com/search?q={}",
            "Stockvault": "https://www.stockvault.net/search?q={}",
            "Morguefile": "https://morguefile.com/?s={}",
            "Picfair": "https://www.picfair.com/search?q={}",
            "EyeEm": "https://www.eyeem.com/search?q={}",
            "Twenty20": "https://www.twenty20.com/search?utf8=%E2%9C%93&search[query]={}",
            "Photocase": "https://www.photocase.com/en/search?query={}",
            "Stocksy": "https://www.stocksy.com/search?q={}",
            "Offset": "https://www.offset.com/search?query={}",
            "Burst by Shopify": "https://burst.shopify.com/photos/search?utf8=%E2%9C%93&q={}",
            "Reshot": "https://www.reshot.com/search/?q={}",
            "Gratisography": "https://gratisography.com/?s={}",
            "Life of Pix": "https://www.lifeofpix.com/?s={}",
            "Picspree": "https://picspree.com/?s={}",
            "Kaboompics": "https://kaboompics.com/gallery?search={}",
            "LibreShot": "https://libreshot.com/?s={}",
            "Picography": "https://picography.co/?s={}",
            "Foodiesfeed": "https://www.foodiesfeed.com/?s={}",
            "Public Domain Pictures": "https://www.publicdomainpictures.net/en/search.php?query={}",
            "New Old Stock": "https://nos.twnsnd.co/?s={}",
            "ImageFinder": "http://www.imagefinder.net/?q={}",
            "Wikimedia Commons": "https://commons.wikimedia.org/w/index.php?search={}",
            "StockPhotos": "https://www.stockphotos.com/search?q={}"
        },
        "File": {
            "Google Files": "https://www.google.com/search?q=filetype:pdf+site:*.edu+OR+site:*.org+-inurl:(signup+OR+login)+{}",
            "IndexOf": "https://www.google.com/search?q=inurl:(index.of+OR+dir)+{}",
            "FilePursuit": "https://filepursuit.com/pursuit?q={}",
            "DocSearch": "https://www.google.com/search?q=filetype:doc+OR+filetype:docx+-inurl:(signup+OR+login)+{}",
            "PDF Drive": "https://www.pdfdrive.com/search?q={}",
            "Scribd": "https://www.scribd.com/search?query={}",
            "SlideShare": "https://www.slideshare.net/search/slideshow?searchfrom=header&q={}",
            "Z-Library": "https://z-lib.is/s/?q={}",
            "GetIntoPC": "https://getintopc.com/?s={}",
            "Archive": "https://archive.org/search.php?query={}",
            "4Shared": "https://www.4shared.com/web/q/search?q={}",
            "MediaFire": "https://www.mediafire.com/search/?q={}",
            "Library Genesis": "http://libgen.rs/search.php?req={}",
            "Open Library": "https://openlibrary.org/search?q={}",
            "Project Gutenberg": "https://www.gutenberg.org/ebooks/search/?query={}",
            "ResearchGate": "https://www.researchgate.net/search/publication?q={}",
            "DocDroid": "https://www.docdroid.net/search?q={}",
            "Academia.edu": "https://www.academia.edu/search?q={}",
            "PDF Search Engine": "https://www.pdf-search-engine.com/search?q={}",
            "FileHorse": "https://www.filehorse.com/?s={}",
            "Softonic": "https://www.softonic.com/s/{}",
            "SourceForge Files": "https://sourceforge.net/directory/?q={}",
            "Issuu": "https://issuu.com/search?q={}",
            "Calameo": "https://www.calameo.com/books?q={}",
            "SlideServe": "https://www.slideserve.com/search?searchword={}",
            "HathiTrust Digital Library": "https://www.hathitrust.org/search?q={}",
            "Digital Public Library of America": "https://dp.la/search?q={}",
            "Europeana": "https://www.europeana.eu/en/search?query={}",
            "OpenDOAR": "http://www.opendoar.org/search/results.php?search={}",
            "CORE": "https://core.ac.uk/search?q={}",
            "arXiv": "https://arxiv.org/search/?query={}&searchtype=all&source=header",
            "Semantic Scholar": "https://www.semanticscholar.org/search?q={}",
            "J-STAGE": "https://www.jstage.jst.go.jp/result/global/-char/en?kw={}",
            "OAIster": "https://www.oclc.org/oaister.en.html?q={}",
            "FreeFullPDF": "https://www.freefullpdf.com/?s={}",
            "Paperity": "https://paperity.org/search?q={}",
            "BASE": "https://www.base-search.net/Search/Results?lookfor={}",
            "Digital Commons Network": "https://network.bepress.com/search/?q={}",
            "Open Access Button": "https://openaccessbutton.org/search?url={}",
            "JSTOR": "https://www.jstor.org/action/doBasicSearch?Query={}",
            "ScienceDirect": "https://www.sciencedirect.com/search?qs={}",
            "Wiley Online Library": "https://onlinelibrary.wiley.com/action/doSearch?AllField={}",
            "SpringerLink": "https://link.springer.com/search?query={}",
            "SAGE Journals": "https://journals.sagepub.com/action/doSearch?AllField={}",
            "IEEE Xplore": "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={}",
            "ACM Digital Library": "https://dl.acm.org/action/doSearch?AllField={}"
        },
        "Audio": {
            "SoundCloud": "https://soundcloud.com/search?q={}",
            "YouTube": "https://www.youtube.com/results?search_query={}",
            "Spotify": "https://open.spotify.com/search/{}",
            "Jamendo": "https://www.jamendo.com/search?qs=q={}",
            "FreeMusicArchive": "https://freemusicarchive.org/search/?search-genre={}",
            "Bandcamp": "https://bandcamp.com/search?q={}",
            "Last.fm": "https://www.last.fm/search?q={}",
            "Mixcloud": "https://www.mixcloud.com/search/?q={}",
            "ReverbNation": "https://www.reverbnation.com/main/search?q={}",
            "Audiomack": "https://audiomack.com/search?q={}",
            "CCMixter": "http://ccmixter.org/search?search_text={}",
            "SoundClick": "https://www.soundclick.com/search/default.cfm?searchterm={}",
            "Deezer": "https://www.deezer.com/search/{}",
            "iHeartRadio": "https://www.iheart.com/search/?q={}",
            "7Digital": "https://www.7digital.com/search?q={}",
            "AllMusic": "https://www.allmusic.com/search/all/{}",
            "Tidal": "https://tidal.com/browse/search?q={}",
            "Napster": "https://us.napster.com/search?query={}",
            "Beatport": "https://www.beatport.com/search?q={}",
            "Jango": "https://www.jango.com/search?q={}",
            "RadioPublic": "https://radiopublic.com/search?q={}",
            "Slacker Radio": "https://www.slacker.com/search?q={}",
            "Radio.com": "https://www.radio.com/search?q={}",
            "TuneIn": "https://tunein.com/search/?q={}",
            "Podcast Addict": "https://podcastaddict.com/search/?q={}",
            "Podbean": "https://www.podbean.com/microsite-search?q={}",
            "Anchor": "https://anchor.fm/s/{}",
            "Castbox": "https://castbox.fm/search?q={}",
            "Podchaser": "https://www.podchaser.com/search?q={}",
            "Listen Notes": "https://www.listennotes.com/search/?q={}",
            "Player FM": "https://player.fm/search?q={}",
            "Acast": "https://www.acast.com/search?q={}",
            "Audioboom": "https://audioboom.com/search?q={}",
            "Mixcrate": "https://www.mixcrate.com/search?q={}",
            "8tracks": "https://8tracks.com/search/all/{}",
            "Radiooooo": "https://radiooooo.com/#/search/{}",
            "Hypemachine": "https://hypem.com/search/{0}",
            "Discogs": "https://www.discogs.com/search/?q={}",
            "MusicBrainz": "https://musicbrainz.org/search?query={}&type=recording",
            "Pandora": "https://www.pandora.com/search/{}",
            "Shazam": "https://www.shazam.com/search?q={}",
            "Musixmatch": "https://www.musixmatch.com/search/{0}",
            "Genius": "https://genius.com/search?q={}",
            "Boomplay": "https://www.boomplaymusic.com/search/{}",
            "Anghami": "https://www.anghami.com/search/{}",
            "Qobuz": "https://www.qobuz.com/search?q={}",
            "YouTube Music": "https://music.youtube.com/search?q={}"
        },
        "Code": {
            "GitHub": "https://github.com/search?q={}",
            "GitLab": "https://gitlab.com/search?search={}",
            "BitBucket": "https://bitbucket.org/repo/all?name={}",
            "StackOverflow": "https://stackoverflow.com/search?q={}",
            "CodePen": "https://codepen.io/search/pens?q={}",
            "SourceForge": "https://sourceforge.net/directory/?q={}",
            "Gist": "https://gist.github.com/search?q={}",
            "Pastebin": "https://pastebin.com/search?q={}",
            "CodeProject": "https://www.codeproject.com/search.aspx?q={}",
            "Reddit Programming": "https://www.reddit.com/r/programming/search?q={}",
            "HackerRank": "https://www.hackerrank.com/community?q={}",
            "LeetCode": "https://leetcode.com/problemset/all/?search={}",
            "Codementor": "https://www.codementor.io/search?q={}",
            "CodeChef": "https://www.codechef.com/search?search={}",
            "TopCoder": "https://www.topcoder.com/search/?q={}",
            "Rosetta Code": "http://rosettacode.org/wiki/Special:Search?search={}",
            "GeeksforGeeks": "https://www.geeksforgeeks.org/?s={}",
            "Dev.to": "https://dev.to/search?q={}",
            "DZone": "https://dzone.com/search?q={}",
            "Programmers Heaven": "http://www.programmersheaven.com/search?q={}",
            "CSDN": "https://so.csdn.net/so/search/s.do?q={}",
            "Juejin": "https://juejin.cn/search?query={}",
            "StackExchange": "https://stackexchange.com/search?q={}",
            "LeetFree": "https://www.leetfree.com/search?q={}",
            "CodeRunner": "https://www.coderunner.com/search?q={}",
            "CodeSandbox": "https://codesandbox.io/search?q={}",
            "Replit": "https://replit.com/search?q={}",
            "HackerEarth": "https://www.hackerearth.com/practice/search/?q={}",
            "Codewars": "https://www.codewars.com/search?q={}",
            "Exercism": "https://exercism.io/search?query={}",
            "Edabit": "https://edabit.com/challenges/search?q={}",
            "CodeSignal": "https://codesignal.com/search?q={}",
            "AtCoder": "https://atcoder.jp/search?q={}",
            "SPOJ": "https://www.spoj.com/search/?query={}",
            "UVa Online Judge": "https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&limit=50&limitstart=0&q={}",
            "CodeChef Discuss": "https://discuss.codechef.com/search?q={}",
            "CodeForces": "https://codeforces.com/search?query={}",
            "ACM ICPC": "https://icpc.global/search?q={}",
            "Project Euler": "https://projecteuler.net/problem=",
            "CodeAbbey": "https://www.codeabbey.com/index/task_list",
            "Codingame": "https://www.codingame.com/multiplayer",
            "Timus Online Judge": "https://acm.timus.ru/search.aspx?space=1&search={}",
            "CS Academy": "https://csacademy.com/ide/?tool=editors",
            "USACO Guide": "https://usaco.guide/search?q={}",
            "Code Golf Stack Exchange": "https://codegolf.stackexchange.com/search?q={}",
            "Open Kattis": "https://open.kattis.com/problems?search={}",
            "E-olymp": "https://www.e-olymp.com/en/search?q={}",
            "LightOJ": "https://lightoj.com/volume_showproblem.php?problem=",
            "COJ": "https://www.beecrowd.com.br/judge/en/problems/index/"
        },
        "AI": {
            "Grok": "https://x.ai/grok?q={}",
            "Perplexity": "https://www.perplexity.ai/?q={}",
            "You.com": "https://you.com/search?q={}",
            "ChatGPT": "https://chat.openai.com/?q={}",
            "HuggingFace": "https://huggingface.co/models?search={}",
            "WolframAlpha": "https://www.wolframalpha.com/input/?i={}",
            "Kagi": "https://kagi.com/search?q={}",
            "Andi": "https://andisearch.com/?q={}",
            "Writesonic": "https://writesonic.com/?s={}",
            "Jasper": "https://www.jasper.ai/?q={}",
            "Claude": "https://anthropic.com/claude?q={}",
            "Bard": "https://bard.google.com/?q={}",
            "OpenAI Playground": "https://platform.openai.com/playground?query={}",
            "DeepAI": "https://deepai.org/machine-learning-model/text-generator?query={}",
            "InferKit": "https://inferkit.com/demo?text={}",
            "Copy.ai": "https://www.copy.ai/?q={}",
            "Snazzy AI": "https://snazzy.ai/?q={}",
            "AI Dungeon": "https://play.aidungeon.io/main/adventure?q={}",
            "ChatSonic": "https://writesonic.com/chat?query={}",
            "Poe": "https://poe.com/search?q={}",
            "HuggingChat": "https://huggingchat.ai/?q={}",
            "Cohere": "https://cohere.ai/examples?query={}",
            "IBM Watson Assistant": "https://www.ibm.com/cloud/watson-assistant/",
            "Microsoft Bing Chat": "https://www.bing.com/new",
            "Replika": "https://replika.ai/",
            "YouChat": "https://you.com/search?q={}&tbm=youchat",
            "Character.AI": "https://beta.character.ai/chat?__cf_chl_jschl_tk__=1",
            "AI21 Studio": "https://studio.ai21.com/playground",
            "OpenAssistant": "https://open-assistant.io/"
        },
        "Maps": {
            "Google Maps": "https://www.google.com/maps/search/{}",
            "OpenStreetMap": "https://www.openstreetmap.org/search?query={}",
            "Bing Maps": "https://www.bing.com/maps?q={}",
            "MapQuest": "https://www.mapquest.com/search/results?query={}",
            "Waze": "https://www.waze.com/live-map/?q={}",
            "Here WeGo": "https://wego.here.com/search/{}",
            "Apple Maps": "https://maps.apple.com/?q={}",
            "Yandex Maps": "https://yandex.com/maps/?text={}",
            "Mapbox": "https://www.mapbox.com/search/?q={}",
            "TomTom": "https://www.tomtom.com/en_us/search/?q={}",
            "2GIS": "https://2gis.com/search/{}",
            "What3Words": "https://what3words.com/{}",
            "Baidu Maps": "https://map.baidu.com/?q={}",
            "Sygic Maps": "https://maps.sygic.com/search?q={}",
            "OpenCycleMap": "https://www.opencyclemap.org/?search={}",
            "MapMyIndia": "https://www.mapmyindia.com/search?q={}",
            "Navmii": "https://www.navmii.com/en/search?q={}",
            "ArcGIS Online": "https://www.arcgis.com/home/search.html?q={}",
            "Maps.me": "https://maps.me/search?q={}",
            "Citymapper": "https://citymapper.com/search?q={}",
            "Moovit": "https://moovitapp.com/ul?q={}",
            "Komoot": "https://www.komoot.com/search?q={}",
            "Navitel": "https://navitel.ru/search?q={}",
            "Wikimapia": "https://wikimapia.org/#lang=en&lat=0&lon=0&z=2&m=b&search={}",
            "USGS Topo Maps": "https://ngmdb.usgs.gov/topoview/?extent={}",
            "Mapillary": "https://www.mapillary.com/app/?focus=map&mapStyle=none&lat=0&lng=0&z=2&q={}",
            "CyclOSm": "https://www.cyclosm.org/search?q={}",
            "AllTrails": "https://www.alltrails.com/search?q={}",
            "Strava": "https://www.strava.com/search?query={}",
            "Gaia GPS": "https://www.gaiagps.com/map/search?q={}",
            "Outdooractive": "https://www.outdooractive.com/en/search/?q={}",
            "Trailforks": "https://www.trailforks.com/search/?q={}"
        },
        "Trends": {
            "Google Trends": "https://trends.google.com/trends/explore?q={}",
            "Twitter Trends": "https://twitter.com/search?q={}",
            "Reddit Trends": "https://www.reddit.com/search/?q={}&sort=hot",
            "YouTube Trends": "https://www.youtube.com/results?search_query={}&sp=CAM%253D",
            "TikTok Trends": "https://www.tiktok.com/search?q={}",
            "Instagram Trends": "https://www.instagram.com/explore/tags/{}",
            "Pinterest Trends": "https://trends.pinterest.com/?q={}",
            "BuzzSumo": "https://app.buzzsumo.com/research/content?type=articles&q={}",
            "Ahrefs": "https://app.ahrefs.com/keywords-explorer/google/us/all?keywords={}",
            "SEMRush": "https://www.semrush.com/analytics/keywordoverview/?q={}",
            "TrendHunter": "https://www.trendhunter.com/search?q={}",
            "Exploding Topics": "https://explodingtopics.com/search?term={}",
            "Trendsmap": "https://www.trendsmap.com/?q={}",
            "Talkwalker": "https://www.talkwalker.com/analytics/trending?query={}",
            "Social Searcher": "https://www.social-searcher.com/?q={}",
            "Keyhole": "https://keyhole.co/search?q={}",
            "Brand24": "https://brand24.com/search/?q={}",
            "Mention": "https://mention.com/en/search/?q={}",
            "Sprout Social": "https://sproutsocial.com/insights/search/?q={}",
            "Iconosquare": "https://pro.iconosquare.com/keyword?q={}",
            "SocialBakers": "https://www.socialbakers.com/search?q={}",
            "CrowdTangle": "https://www.crowdtangle.com/search?q={}",
            "Klear": "https://klear.com/search?q={}",
            "Trendolizer": "https://www.trendolizer.com/search?q={}",
            "BuzzStream": "https://www.buzzstream.com/search?q={}",
            "Riffle": "https://www.riffle.com/search?q={}",
            "TrendWatching": "https://trendwatching.com/?s={}",
            "TrendSpottr": "https://trendspottr.com/search?q={}",
            "TrendForce": "https://trendforce.com/search?q={}",
            "NetBase Quid": "https://www.netbasequid.com/search?q={}",
            "Meltwater": "https://www.meltwater.com/en/search?q={}",
            "BrandMentions": "https://brandmentions.com/search?q={}",
            "Digimind": "https://www.digimind.com/search?q={}",
            "Brandwatch": "https://www.brandwatch.com/search/?q={}"
        }
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("HyperSearch Browser")
        self.setGeometry(100, 100, 1400, 900)
        self.settings_file = "search_settings.json"
        self.uploaded_file: str | None = None
        self.tab_urls: Dict[int, str] = {}
        self.current_query: str = ""

        self.setup_dock()
        self.setup_ui()
        self.load_settings()

    def setup_ui(self) -> None:
        self.setStyleSheet("""
            QMainWindow { background:#1e1e2f; color:#fff; }
            QComboBox, QLineEdit { background:#3b3b58; border:1px solid #5b5b7b; border-radius:5px; padding:8px; color:#fff; }
            QPushButton { background:#007bff; border:none; border-radius:5px; padding:8px 20px; color:#fff; font-weight:bold; }
            QPushButton:hover { background:#0056b3; }
            QTabBar::tab { background:#3b3b58; color:#fff; padding:10px; }
            QTabBar::tab:selected { background:#007bff; }
            QListWidget { background:#3b3b58; color:#fff; border:1px solid #5b5b7b; }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        search_layout.setContentsMargins(20, 10, 20, 10)

        self.search_type = QComboBox()
        self.search_type.addItems(self.ENGINES.keys())
        self.search_type.currentTextChanged.connect(self.update_ui)
        search_layout.addWidget(QLabel("Type:"))
        search_layout.addWidget(self.search_type)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter query...")
        search_layout.addWidget(self.search_input)

        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setVisible(False)
        search_layout.addWidget(self.upload_btn)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_btn)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.settings_btn.customContextMenuRequested.connect(self.show_settings_menu)
        search_layout.addWidget(self.settings_btn)

        layout.addLayout(search_layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.load_tab_content)
        self.tabs.setTabBarAutoHide(False)
        self.tabs.setUsesScrollButtons(True)
        layout.addWidget(self.tabs)

    def setup_dock(self) -> None:
        self.dock = QDockWidget("Scoped Search Engines", self)
        self.dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.dock_widget = QWidget()
        self.dock_layout = QVBoxLayout()

        self.engine_list = QListWidget()
        self.engine_list.itemDoubleClicked.connect(self.perform_scoped_search)
        self.dock_layout.addWidget(self.engine_list)

        self.scope_search_input = QLineEdit()
        self.scope_search_input.setPlaceholderText("Enter query for scoped search...")
        self.scope_search_input.returnPressed.connect(self.perform_scoped_search)
        self.dock_layout.addWidget(self.scope_search_input)

        self.dock_widget.setLayout(self.dock_layout)
        self.dock.setWidget(self.dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

    def load_settings(self) -> None:
        # Default to using all engines for each category.
        default_settings = {cat: list(engines.keys()) for cat, engines in self.ENGINES.items()}
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                self.active_engines = json.load(f)
                self.active_engines = {cat: self.active_engines.get(cat, default_settings[cat])
                                         for cat in self.ENGINES}
        except (FileNotFoundError, json.JSONDecodeError, IOError):
            self.active_engines = default_settings

        # Uncomment the following line to force loading all engines (for debugging)
        # self.active_engines = {cat: list(self.ENGINES[cat].keys()) for cat in self.ENGINES}

        self.update_active_engines()

    def save_settings(self) -> None:
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.active_engines, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")

    def update_active_engines(self) -> None:
        self.search_engines = {
            cat: {n: u for n, u in self.ENGINES[cat].items() if n in self.active_engines[cat]}
            for cat in self.ENGINES
        }
        self.update_dock_list()

    def update_dock_list(self) -> None:
        if not hasattr(self, 'engine_list'):
            return
        self.engine_list.clear()
        current_type = self.search_type.currentText()
        for engine in self.search_engines[current_type].keys():
            self.engine_list.addItem(QListWidgetItem(engine))

    def show_settings_menu(self, pos) -> None:
        menu = QMenu(self)
        search_type = self.search_type.currentText()
        for engine in self.ENGINES[search_type]:
            action = QAction(engine, self, checkable=True)
            action.setChecked(engine in self.active_engines[search_type])
            action.triggered.connect(lambda checked, e=engine: self.toggle_engine(search_type, e, checked))
            menu.addAction(action)
        menu.addSeparator()
        menu.addAction("Add Custom Engine", lambda: self.add_custom_engine(search_type))
        menu.exec(self.settings_btn.mapToGlobal(pos))

    def toggle_engine(self, category: str, engine: str, checked: bool) -> None:
        engines = self.active_engines[category]
        if checked and engine not in engines:
            engines.append(engine)
        elif not checked and engine in engines:
            engines.remove(engine)
        self.update_active_engines()
        self.save_settings()

    def add_custom_engine(self, category: str) -> None:
        name, ok1 = QInputDialog.getText(self, "Add Engine", "Engine Name:")
        if ok1 and name:
            url, ok2 = QInputDialog.getText(self, "Add Engine", "Search URL (use {} for query):")
            if ok2 and url:
                self.ENGINES[category][name] = url
                self.active_engines[category].append(name)
                self.update_active_engines()
                self.save_settings()

    def update_ui(self) -> None:
        search_type = self.search_type.currentText()
        is_uploadable = search_type in {"Image", "File", "Audio"}
        self.upload_btn.setVisible(is_uploadable)
        self.search_input.setPlaceholderText(
            "Enter query..." if not is_uploadable else "Upload file or enter query..."
        )
        self.update_dock_list()

    def upload_file(self) -> None:
        file_types = {
            "Image": "Images (*.png *.jpg *.jpeg *.gif *.bmp)",
            "File": "Documents (*.pdf *.doc *.docx *.txt)",
            "Audio": "Audio (*.mp3 *.wav *.ogg)"
        }
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_types[self.search_type.currentText()])
        if file_path:
            self.uploaded_file = file_path
            self.search_input.setText(os.path.basename(file_path))

    def perform_search(self) -> None:
        query = self.search_input.text().strip()
        search_type = self.search_type.currentText()
        if not query and not self.uploaded_file and search_type != "Trends":
            return

        self.tabs.clear()
        self.tab_urls.clear()
        self.current_query = query

        engines = self.search_engines.get(search_type, {})
        if not engines:
            return

        if self.uploaded_file and search_type in {"Image", "File", "Audio"}:
            query = f"{query} {os.path.basename(self.uploaded_file)}" if query else os.path.basename(self.uploaded_file)

        # Create a QWebEngineView tab for each engine without immediately loading its URL.
        for name, url in engines.items():
            formatted_url = url.format(query.replace(" ", "+") if query else "")
            web_view = QWebEngineView()
            index = self.tabs.addTab(web_view, name)
            # Store the URL for lazy loading when the tab is clicked.
            self.tab_urls[index] = formatted_url

        print(f"Added {self.tabs.count()} tabs for search: {query}")
        self.uploaded_file = None
        self.search_input.clear()
        # Tabs do not load their content until clicked.

    def perform_scoped_search(self) -> None:
        selected_items = self.engine_list.selectedItems()
        if not selected_items:
            return

        query = self.scope_search_input.text().strip() or self.current_query
        if not query:
            return

        engine_name = selected_items[0].text()
        search_type = self.search_type.currentText()
        url_template = self.search_engines[search_type].get(engine_name)
        if not url_template:
            return

        formatted_url = url_template.format(query.replace(" ", "+"))
        web_view = QWebEngineView()
        web_view.load(QUrl(formatted_url))
        index = self.tabs.addTab(web_view, f"{engine_name} - {query}")
        self.tabs.setCurrentIndex(index)

    def load_tab_content(self, index: int) -> None:
        if index < 0 or index not in self.tab_urls:
            return
        web_view = self.tabs.widget(index)
        url = self.tab_urls[index]
        if web_view.url().toString() != url:
            web_view.load(QUrl(url))

    def close_tab(self, index: int) -> None:
        self.tabs.removeTab(index)
        if index in self.tab_urls:
            del self.tab_urls[index]

def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e2f"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
    app.setPalette(palette)
    browser = MultiSearchBrowser()
    browser.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
