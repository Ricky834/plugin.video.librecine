# coding: utf-8

# IMPORTS
from xbmcswift2 import Plugin
import requests, re
import CommonFunctions
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui
import urllib2
import urllib
import cookielib
import urlresolver
import os
from bs4 import BeautifulSoup
from operator import itemgetter

# OBJECTS()
plugin = Plugin('LibreCiné', 'plugin.video.libreCine')
common = CommonFunctions
common.plugin = "plugin.video.libreCine"
webSession = requests.Session()
# VARIABLE
varToken = plugin.get_setting('token')
varEMail = plugin.get_setting('email')
varPassword = plugin.get_setting('password')
varforumviewfilms = plugin.get_setting('forum_view_film')
VarModelaunch = plugin.get_setting('launch')
varForumName = plugin.get_setting('forum_name')
varOneFichier = plugin.get_setting('OneFichier')
varf4mTester = plugin.get_setting('f4mTester')
varDownFichier = 'Non'
varIconDir = "http://libretv.me/icon/"
varIsEnabled = False
varIsFrom = None
modes = 'false'
__addonID__           = "plugin.video.libreCine"
__addon__             = xbmcaddon.Addon(__addonID__)
__language__          = __addon__.getLocalizedString
__addonDir__          = __addon__.getAddonInfo("path")
__version__           = __addon__.getAddonInfo("version")
__lastopenedversion__ = __addon__.getSetting("lastopenedversion")

def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Libreciné","Téléchargement",url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

html = webSession.get('http://libretv.me/maj/addon.xml').text
found = re.compile('version="(.+?)" provider-name="FEL">').findall(html)
version_maj = found[0]

if __version__ == version_maj:
    update = 'false'
    tag =__version__
    icon = 'update.png'
    parseAuto = 'parse_noUpdate'
else :
    update = 'true'
    tag ='[COLOR yellow]'+version_maj+' Disponible[/COLOR]'
    icon = 'update.png'
    parseAuto = 'parse_autoupdate'


if varEMail == '':
    plugin.open_settings()


# ------------------------------------
# -------------ROUTES-----------------
# ------------------------------------
@plugin.route('/')
def index():
    items = [
        {'label': 'TV', 'icon': varIconDir + 'theme/tv.png', 'path': plugin.url_for('parse_tv_menu'),'info':{'Title':'',"Plot":'Télévision en streaming'}},
        {'label': 'RADIO', 'icon': varIconDir + 'theme/radio.png', 'path': plugin.url_for('parse_chanel_list', url='http://libretv.me/phpbb/viewforum.php?f=70'),'info':{'Title':'',"Plot":'Radio en streaming'}},
        {'label': 'FILMS', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=%3CLABEL%3E*&terms=any&author=&fid%5B%5D=72&sc=1&sf=firstpost&sr=posts&sk=t&sd=d&st=7&ch=2000&t=0&submit=Rechercher',modes_search='false',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
        {'label': 'FILMS DP (BETA)','icon':varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp_menu'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},

        {'label': 'SÉRIES','icon':varIconDir + 'theme/emission.png','path':plugin.url_for('parse_emission_first_page', url='http://libretv.me/phpbb/search.php?keywords=%3CLABEL%3E*&terms=any&author=&fid%5B%5D=73&sc=1&sf=firstpost&sr=posts&sk=t&sd=d&st=7&ch=1000&t=0&submit=Rechercher',modes_search='True',subMenu='true',mode_rd='true',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
        {'label': 'MANGAS','icon':varIconDir + 'theme/mangas.png','path':plugin.url_for('parse_emission_first_page', url='http://libretv.me/phpbb/search.php?keywords=%3CLABEL%3E*&terms=any&author=&fid%5B%5D=83&sc=1&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',subMenu='False',mode_rd='true',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
        #{'label': 'RECHERCHE', 'icon': varIconDir + 'theme/search.png','path': plugin.url_for('parse_genre_menu')},
        {'label': 'RÉGLAGE ', 'icon': varIconDir + 'theme/resolver.png','path': plugin.url_for('parse_resolver'), 'thumbnail':'','info':{'Title':'',"Plot":"Réglage du resolver obligatoire pour les sections films et émissions"},'info_type':'video'},
        {'label': tag, 'icon': varIconDir + 'theme/'+icon,'path': plugin.url_for(parseAuto), 'thumbnail':'','info':{'Title':'',"Plot":"Mettez à jour votre extension"},'info_type':'video'},
    ]
    return items

@plugin.route('/parse_dp_menu/')
def parse_dp_menu():
    items = [

            {'label': '[COLOR green]Derniers ajouts[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='film.html'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Action[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Action'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Animation[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Animation'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Aventure[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Aventure'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Biopic[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Biopic'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Catastrophe[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Catastrophe'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Comédie[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Ann%C3%A9es&categorie=Com%C3%A9die'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Court-métrage[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Court-métrage'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Crime[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Crime'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Divertissement [/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Divertissement'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Documentaire[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Documentaire'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Drame[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Drame'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Epouvante-horreur[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Epouvante-horreur'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Famille[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Ann%C3%A9es&categorie=Famille'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Fantastique[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Fantastique'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Guerre[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Guerre'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Histoire[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Histoire'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Humour[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Humour'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Infos[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Infos'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Judiciaire[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Judiciaire'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Musical[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Musical'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Mystère[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Mystère'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Médical[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Médical'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Paranormal[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Paranormal'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Policier[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Policier'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Romance[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Romance'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Science-fiction[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Science-fiction'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Spectacle[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Spectacle'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Sport[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Sport'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Thriller[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Thriller'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Téléréalité[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Téléréalité'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Ufologie[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Ufologie'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Western[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_dp', search='films-recherche?orderby=Années&categorie=Western'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
              ]
    return items


@plugin.route('/parse_autoupdate/')
def parse_autoupdate():
        DownloaderClass('http://libretv.me/maj/addon.py',__addonDir__+"/addon.py")
        DownloaderClass('http://libretv.me/maj/addon.py',__addonDir__+"/addon.py")
        DownloaderClass('http://libretv.me/maj/icon.png',__addonDir__+"/icon.png")
        DownloaderClass('http://libretv.me/maj/addon.xml',__addonDir__+"/addon.xml")
        DownloaderClass('http://libretv.me/maj/settings.xml',__addonDir__+"/resources/settings.xml")
        xbmcgui.Dialog().ok('Libreciné','Installation effectuée avec succès.\nAttention requiert un redémarrage de Kodi.')
        #addonfolder = __addonDir__.replace('plugin.video.libreCine','')
        #os.makedirs(addonfolder+'/repository.shani/', mode=0777)
        #DownloaderClass('http://libretv.me/maj/addonS.xml',addonfolder+'/repository.shani/addon.xml')
        #DownloaderClass('http://libretv.me/maj/changelogS.txt',addonfolder+'/repository.shani/changelog.txt')
        #DownloaderClass('http://libretv.me/maj/iconS.png',addonfolder+'/repository.shani/icon.png')
        #xbmcgui.Dialog().ok('Libreciné','Installation effectuée avec succès.\nAttention requiert un redémarrage de Kodi.')
        quit()
@plugin.route('/parse_noUpdate/')
def parse_noUpdate():
        xbmcgui.Dialog().ok('Libreciné','Votre extension est à jour')

@plugin.route('/parse_genre_menu/')
def parse_genre_menu():
    items = [
            {'label': '[COLOR green]Action[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Action&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Animation[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Animation&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Arts Martiaux[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Arts%20Martiaux&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Aventure[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Aventure&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Biopic[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Biopic&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Comédie dramatique[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Comédie%20dramatique&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Comédie musicale[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Comédie%20musicale&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Comédie[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Comédie&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Divers[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Divers&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Documentaire[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Documentaire&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Drame[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Drame&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Epouvante-horreur[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Epouvante-horreur&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Espionnage[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Espionnage&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Famille[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Famille&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Fantastique[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Fantastique&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Guerre[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Guerre&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Historique[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Historique&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Musical[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Musical&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Péplum[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Péplum&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Policier[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Policier&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Romance[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Romance&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Science fiction[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Science%20fiction&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Thriller[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Thriller&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
            {'label': '[COLOR green]Western[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=<GENRE>Western&terms=all&author=&fid%5B%5D=72&sc=0&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=1000&t=0&submit=Rechercher',modes_search='False',fulllist='False'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}},
  ]
    return items






@plugin.route('/parse_tv_menu/')
def parse_tv_menu():
    items = [
            {'label': 'Thématique', 'icon': varIconDir + 'theme/tv.png', 'path': plugin.url_for('parse_thematic_list', url='http://libretv.me/phpbb/viewforum.php?f=44'),'info':{'Title':'',"Plot":'Télévision en streaming'}},
            {'label': 'Rattrapage télé','icon':varIconDir + 'theme/play.png','path':plugin.url_for('parse_replay_first_page', url='http://libretv.me/phpbb/search.php?keywords=%3CLABEL%3E*&terms=any&author=&fid%5B%5D=81&sc=1&sf=firstpost&sr=posts&sk=t&sd=d&st=0&ch=10000&t=0&submit=Rechercher'),'info':{'Title':'',"Plot":'REVOIR UN PROGRAMME TV,EMISSIONS,FILMS EN REPLAY ET EN STREAMING'}},
			{'label': 'Liste libre','icon': varIconDir + 'theme/listelibre.png','path': plugin.url_for('parse_chanel_list', url='http://libretv.me/phpbb/viewforum.php?f=29')},
			{'label': 'TVA (Zone Vidéo)','icon': varIconDir + 'theme/listelibre.png','path': plugin.url_for('parse_tva_decode',url='http://tva.canoe.ca/video/encore-plus-de-videos/plus-recentes/1267225057001')},
			{'label': 'CASA (Zone Vidéo)','icon': varIconDir + 'theme/listelibre.png','path': plugin.url_for('parse_tva_decode',url='http://www.casatv.ca/videos/les-videos/les-plus-recentes/1086445296001')},
			{'label': 'TVA Nouvelle (Zone Vidéo)','icon': varIconDir + 'theme/listelibre.png','path': plugin.url_for('parse_tva_n_decode',url='http://www.tvanouvelles.ca/videos')},

			#{'label': 'LibreSports (Instable)','icon': varIconDir + 'theme/antenna.png','path': plugin.url_for('parse_wss')},
            #{'label': 'Ce mois ci (pastbin)', 'icon': varIconDir + 'theme/listelibre.png','path': plugin.url_for('parse_today_ltv', modeltv='1')},
            #{'label': 'Antérieur (pastbin)', 'icon': varIconDir + 'theme/listelibre.png','path': plugin.url_for('parse_today_ltv', modeltv='0')},
			]
    return items


@plugin.route('/parse_resolver/')
def parse_resolver():
    import urlresolver
    urlresolver.display_settings()

######real-debrid debrid via url resolver #####
@plugin.route('/parse_rd_deb/<url>/<title>/<icon>/<down>/')
def parse_rd_deb(url,title,icon,down):
    pl = xbmc.PlayList(1)
    pl.clear()
    items = []
    onefichiermatch=re.compile('(1fichier.com)').findall(url)

    if onefichiermatch and varOneFichier == 'Oui' :
            listitem = xbmcgui.ListItem('1FICHIER PREMIUM',
            thumbnailImage=icon)
            url = url
            xbmc.PlayList(1).add(url, listitem)
            xbmc.Player().play(pl)
    else:
        debridurl = urlresolver.HostedMediaFile(url=url).resolve()
        if debridurl :
            titre_officiel=re.compile('http://.*?.rdeb.io/.*?/.*?/(.*?)$').findall(debridurl)
            listitem = xbmcgui.ListItem(title,
            thumbnailImage=icon)
            url = debridurl
            xbmc.PlayList(1).add(url, listitem)
            if down == 'true':
                dialog = xbmcgui.Dialog()
                value = dialog.browse(0, 'Select your download folder', 'myprograms')
                DownloaderClass(url,value+titre_officiel[0])
                line7 = "Téléchargement terminé"
                #xbmcgui.Dialog().ok('Libreciné',line7)

            else:
                xbmc.Player().play(pl)

        else:
            xbmc.executebuiltin('XBMC.Notification("Libreciné","Erreur lors du débridage de la video",5000,)')
#####

@plugin.route('/parse_dp/<search>/')
def parse_dp(search):
    items = []
    source= "http://www.dpstream.net/"+search
    req = urllib2.Request(source, headers=hdr)
    page = urllib2.urlopen(req)
    html = page.read()
    html=html.replace("//static","http://static")

    soup = BeautifulSoup(html)
    for source in soup.find_all('li', {'id': ['item_19']}):
        #print(source)
        desc = ''
        name = source.find('a').text.encode('utf-8')
        link = source.find('a').get('href')
        img_ = source.find('img').get('src')
        desc_ = source.find_all('span')
        if desc_ :
            desc = desc_[4].find(text=True).encode('utf-8')
            date = desc_[3].find(text=True).encode('utf-8')

        print(name)
        print(link)
        print(img_)
        print(desc)
        print(date)
        items.append({'label':name,'icon':img_,'path':plugin.url_for('parse_dp_decode', url='http://dpstream.net'+link, title=name),'thumbnail':img_,'info':{'Title':name,"Plot":desc},'info_type':'video'})

    return items


@plugin.route('/parse_dp_decode/<url>/<title>/')
def parse_dp_decode(url,title):
    items = []
    site= url
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    html = page.read()
    title=re.compile('Disponible sur <b>(.*?)</b> <a href="(.*?)" target="_blank">ici</a>').findall(html)
    for heb,url in title:
        print('<titre>'+heb+' (Dpstream)</titre><tmb>na</tmb><url>'+url+'</url><desc>na</desc>')
        url = url.replace('?m=embed&id=','v/')#purevid filtre
        items.append({'label':heb,'icon':'','path':plugin.url_for('parse_rd_deb', url=url+'/', title=url, icon='http://',down='false'),'thumbnail':'','info':{'Title':'',"Plot":''},'info_type':'video'})


    return items

##### libretv classique####
@plugin.route('/parse_today_ltv/<modeltv>')
def parse_today_ltv(modeltv):
    items = []
    desc = 'Aucune information'
    load_film = urllib2.urlopen('http://libretv.me/Liste-m3u/token_'+varToken+'/add_item.dat')
    link2 = load_film.read()
    url_film_list=re.compile('<url>(.*?)</url><title>(.*?)</title><order>'+modeltv+'</order><icon>(.*?)</icon>').findall(link2)
    for url,display_name,tmb in url_film_list:
        tmb = tmb.replace('/','_')
        url = url.replace(' ','%20')
        items.append({'label': display_name, 'icon': 'http://libretv.me/icon/date/'+tmb+'.png', 'path': url})
    return items




@plugin.route('/parse_tva_decode/<url>/')
def parse_tva_decode(url):
    desc = ''
    items = []
    source=url
    req = urllib2.Request(source, headers=hdr)
    page = urllib2.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html)
    for source in soup.find_all('div', {'class': ['video-image']}):
        display_name = source.find('img').get('alt').encode('utf-8')
        VideoId = source.find('a').get('rel')[0]
        img_ = source.find('img').get('src')
        items.append({'label':display_name,'icon':img_,'path':'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+VideoId+'&playerId=4824701429001&lineupId=&affiliateId=&pubId=1747170368','is_playable': True,'thumbnail':img_,'info':{'Title':display_name,"Plot":''},'info_type':'video'})
    return items

@plugin.route('/parse_tva_n_decode/<url>/')
def parse_tva_n_decode(url):
    desc = ''
    items = []
    source=url
    req = urllib2.Request(source, headers=hdr)
    page = urllib2.urlopen(req)
    html = page.read()
    soup = BeautifulSoup(html)
    for source in soup.find_all('div', {'class': ['news_unit-text video']}):
        #print(source)
        display_name = source.find('h4').encode('utf-8')
        VideoId = source.find('li').get('data-bcid')
        #img_ = source.find('img').get('src')
        #items.append({'label':display_name,'icon':img_,'path':'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+VideoId+'&playerId=4824701429001&lineupId=&affiliateId=&pubId=1747170368','is_playable': True,'thumbnail':img_,'info':{'Title':display_name,"Plot":''},'info_type':'video'})
        print(VideoId)
        print(display_name)
    return items


##################################################################### fin de la section films et series


########### SECTION STREAM LISTE LIBRE
########### SECTION STREAM LISTE LIBRE
########### SECTION STREAM LISTE LIBRE


@plugin.route('/parse_chanel_list/<url>/')
def parse_chanel_list(url):
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open(url, login_data)
    titre = opener.open(url)
    html = titre.read()
    found = re.compile('./viewtopic.php.+?f=(.+?)&amp;t=(.+?)" class="topictitle">(.+?)</a>').findall(html)
    for forurl, forurll, fortittle in found:
        items.append({'label': fortittle, 'icon': 'http://', 'path': plugin.url_for('parse_topic_list',
                                                                                    url='http://libretv.me/phpbb/viewtopic.php?f=' + forurl + '&t=' + forurll)})
    return items


########### RECUPERE LES LIENS STREAM
@plugin.route('/parse_topic_list/<url>/')
def parse_topic_list(url):
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open(url, login_data)
    titre = opener.open(url)
    html = titre.read()
    html = html.replace('<br /><br />#','<br /><img src="http://vignette3.wikia.nocookie.net/shokugekinosoma/images/6/60/No_Image_Available.png/revision/latest?cb=20150708082716"<br />#')
    found = re.compile('#EXTINF:.+?,(.+?)<br />(.+?)<br /><img src="(.+?)"<br />').findall(html)
    contents_=re.compile('&lt;titre&gt;(.+?)&lt;/titre&gt;&lt;tmb&gt;(.+?)&lt;/tmb&gt;&lt;url&gt;(.+?)&lt;/url&gt;&lt;desc&gt;(.+?)&lt;/desc&gt;').findall(html)
    for title, stream, icon in found:
        if varf4mTester == 'Oui':
            found = re.compile('(.ts)').findall(stream)
            if found :
                stream = 'plugin://plugin.video.f4mTester?streamtype=TSDOWNLOADER&url='+stream
                title = '[COLOR green]f4mTester[/COLOR] '+title
        items.append({'label': '[COLOR aqua]%s[/COLOR]' % title, 'icon': icon, 'path': stream, 'is_playable': True,})

    for title, icon,stream,plot in contents_:
        if varf4mTester == 'Oui':
            found = re.compile('(.ts)').findall(stream)
            if found :
                stream = 'plugin://plugin.video.f4mTester?streamtype=TSDOWNLOADER&url='+stream
                title = '[COLOR green]f4mTester[/COLOR] '+title
        items.append({'label':title,'icon':icon,'path':stream,'is_playable': True,'thumbnail':icon,'info':{'Title':title,"Plot":plot},'info_type':'video'})



    return items


########### SECTION STREAM THEMATIQUE
########### SECTION STREAM THEMATIQUE
########### SECTION STREAM THEMATIQUE

########### RECUPERE LES CATEGORIES

@plugin.route('/parse_thematic_list/<url>/')
def parse_thematic_list(url):
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open(url, login_data)
    titre = opener.open(url)
    html = titre.read()
    found = re.compile('./viewforum.php.+?f=(.+?)" class="forumtitle">(.+?)</a>').findall(html)
    for forurl, fortittle in found:
        fortittleicon = fortittle.replace(' ', '%20')
        items.append({'label': fortittle, 'icon': 'http://libretv.me/icon/' + fortittleicon + '.jpg',
                      'path': plugin.url_for('parse_chanel_list_the',
                                             url='http://libretv.me/phpbb/viewforum.php?f='+forurl)})
    return items


### section replay avec derniere ajout en page principale + section liste complete et recherche
@plugin.route('/parse_replay_first_page/<url>/')
def parse_replay_first_page(url):
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open('http://libretv.me/phpbb/ucp.php?mode=login', login_data)
    titre_ = opener.open(url)
    html = titre_.read()
    contents_=re.compile('&lt;titre&gt;(.+?)&lt;/titre&gt;&lt;tmb&gt;(.+?)&lt;/tmb&gt;&lt;url&gt;(.+?)&lt;/url&gt;&lt;desc&gt;(.+?)&lt;/desc&gt;').findall(html)
    for title,icon,stream,plot in contents_:
            plot = plot.replace('&quot;','"')
            items.append({'label':title,'icon':icon,'path':stream,'is_playable': True,'thumbnail':icon,'info':{'Title':title,"Plot":plot},'info_type':'video'})
    return items


### section emissions avec derniere ajout en page principale + section liste complete et recherche
@plugin.route('/parse_emission_first_page/<url>/<modes_search>/<subMenu>/<mode_rd>/<fulllist>/')
def parse_emission_first_page(url,modes_search,subMenu,mode_rd,fulllist):
    found = 'false'
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open('http://libretv.me/phpbb/ucp.php?mode=login', login_data)
    if fulllist == 'True':
        modes_search = 'False'
        titre_ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=0')
        #titre__ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=200')
        #titre___ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=400')
        #titre____ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=600')
        #titre_____ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=800')
        #titre______ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=1000')
        #titre_______ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=73&sf=firstpost&ch=2000&start=1200')

        sourceUn = titre_.read()
        #sourceDeux = titre__.read()
        #sourceTrois = titre___.read()
        #sourceQuatre = titre____.read()
        #sourceCinq = titre_____.read()
        #sourceSix = titre______.read()
        #sourceSept = titre_______.read()

        html = sourceUn #+ sourceDeux + sourceTrois + sourceQuatre + sourceCinq + sourceSix + sourceSept
    else:
        titre_ = opener.open(url)
        sourceUn = titre_.read()
        html = sourceUn



    htmlb = html.replace('&lt;','<')
    htmlb = htmlb.replace('&gt;','>')
    htmlb = htmlb.replace('&#58;',':')
    htmlb = htmlb.replace('&#46;','.')
    htmlb = htmlb.replace('<br /><span class="posthilit">','')
    htmlb = htmlb.replace('</span>','')
    htmlb = htmlb.replace('<br />','')
    htmlb = htmlb.replace('> <','><')
    htmlb = htmlb.replace('<div class="content">','')
    htmlb = htmlb.replace('<desc>','')
    htmlb = htmlb.replace('</desc>','')
    htmlb = htmlb.replace('<url>','')
    htmlb = htmlb.replace('</url>','')
    htmlb = htmlb.replace('<tmb>','')
    htmlb = htmlb.replace('</tmb>','')
    htmlb = htmlb.replace('<div class="postbody">','')
    htmlb = htmlb.replace('</dl>','')
    htmlb = htmlb.replace('<h3><a href="','')


    contents_=re.compile('&lt;titre&gt;(.+?)&lt;/titre&gt;&lt;tmb&gt;(.+?)&lt;/tmb&gt;&lt;url&gt;(.+?)&lt;/url&gt;&lt;desc&gt;(.+?)&lt;/desc&gt;').findall(html)
    extern_source = re.compile('&lt;ext&gt;(.+?)&lt;/ext&gt;').findall(html)
    contents_new_balise=re.compile('./(.+?)">.+?</a></h3>\n.+?<LABEL>(.+?)</LABEL><THUMBNAIL>(.+?)</THUMBNAIL><DESC>(.+?)</DESC>').findall(htmlb)
    if modes_search == 'False':
        modes_search = 'False'
    else:
        items.append({'label': '[COLOR green]Liste complète[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_emission_first_page', url='http://libretv.me/phpbb/search.php?keywords=%3CLABEL%3E*&terms=any&author=&fid%5B%5D=72&sc=1&sf=firstpost&sr=posts&sk=t&sd=d&st=7&ch=2000&t=0&submit=Rechercher',modes_search='false',subMenu='true',mode_rd='true',fulllist='True'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}})

    for topic_url,label,thumb,plot in contents_new_balise:
            trl = topic_url.split(';')
            items.append({'label': label,'icon':thumb,'path':plugin.url_for('parse_topic_list_the', url='http://libretv.me/phpbb/viewtopic.php?f=72&'+trl[1]+'&'+trl[2],mode_rd='true'),'info' : {'genre': 'Action', 'credits': '5', 'date': '', 'outline': plot, 'plot': plot, 'trailer': plot},'properties' : {'fanart_image' : thumb, 'banner' :  thumb, 'clearlogo':  thumb, 'poster':  thumb, 'Plot':plot},'info_type':'video',"is_playable": False})
    for title, icon,stream,plot in contents_:
            plot = plot.replace('&quot;','"')
            items.append({'label':title,'icon':icon,'path':plugin.url_for('parse_rd_deb', url=stream, title=title, icon=icon),'thumbnail':icon,'info':{'Title':title,"Plot":plot},'info_type':'video'})
    if extern_source :
        for url in extern_source:
            html = webSession.get(url).text
            match = re.compile('<titre>(.+?)</titre><tmb>(.+?)</tmb><url>(.+?)</url><desc>(.+?)</desc>').findall(html)
            for title,tmb,url,desc in match:
                items.append({'label':title,'icon':tmb,'path':plugin.url_for('parse_rd_deb', url=url, title=title, icon=tmb ,down='false'),'thumbnail':tmb,'info':{'Title':title,"Plot":desc},'info_type':'video'})
    if modes_search == 'False':
        by_label = itemgetter('label')
        items_ = sorted(items, key=by_label)
        return items_
    else:
        return items
    #return plugin.finish(items, sort_methods=['playlist_order', 'label'])

@plugin.route('/parse_chanel_list_the/<url>/')
def parse_chanel_list_the(url):
    if varforumviewfilms == 'Date':
        url = url+'st=0&sk=t&sd=d&sort=Valider'
    if varforumviewfilms == 'Alphabétique':
        url = url+'st=0&sk=s&sd=a&sort=Valider'
    if varforumviewfilms == 'Les plus vues':
        url = url+'st=0&sk=v&sd=d&sort=Valider'
    mode_rd = 'false'
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open(url, login_data)
    titre = opener.open(url)
    html = titre.read()
    found = re.compile('./viewtopic.php.+?f=(.+?)&amp;t=(.+?)" class="topictitle">(.+?)</a>').findall(html)
    ext = '.png'
    foldericon = 'icon'
    for forurl, forurll, fortittle in found:
        fortittleicon = fortittle.replace(' ', '%20')
        if forurl == '72' or forurl == '73' or forurl == '77':
            ext = '.jpg'
            foldericon = 'icon/sclub'
            mode_rd = 'true'
        items.append({'label': fortittle, 'icon': 'http://libretv.me/' + foldericon + '/' + fortittleicon + ext,
                'path': plugin.url_for('parse_topic_list_the',
                                             url='http://libretv.me/phpbb/viewtopic.php?f=' + forurl + '&t=' + forurll, mode_rd=mode_rd)})


    return items


####Section films derniere ajout premiere page + ajout de section liste complete et recherche
@plugin.route('/parse_chanel_list_the_/<url>/<modes_search>/<fulllist>/')
def parse_chanel_list_the_(url,modes_search,fulllist):
    found = 'false'
    items = []
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open('http://libretv.me/phpbb/ucp.php?mode=login', login_data)
    if fulllist == 'True':
        modes_search = 'False'
        titre_ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=0')
        titre__ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=200')
        titre___ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=400')
        titre____ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=600')
        titre_____ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=800')
        titre______ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=1000')
        titre_______ = opener.open('http://libretv.me/phpbb/search.php?st=0&sk=t&sd=d&sr=posts&keywords=%3CLABEL%3E%2A&terms=any&fid%5B%5D=72&sf=firstpost&ch=2000&start=1200')

        sourceUn = titre_.read()
        sourceDeux = titre__.read()
        sourceTrois = titre___.read()
        sourceQuatre = titre____.read()
        sourceCinq = titre_____.read()
        sourceSix = titre______.read()
        sourceSept = titre_______.read()

        html = sourceUn + sourceDeux + sourceTrois + sourceQuatre + sourceCinq + sourceSix + sourceSept
    else:
        titre_ = opener.open(url)
        sourceUn = titre_.read()
        html = sourceUn

        #print(html)
        #soup = BeautifulSoup(html)
        #for source in soup.find_all('div', {'class': ['inner']}):
        #   print(source)
        #   author = source.find('a').text
        #   link = source.find_all('dl', {'class': {'postprofile'}})
        #   print (link)


        #img_ = source.find('img').get('src')
        #desc = source.find('span', {'class': {'itemIntroInfo','span'}})
        #print(author)
        #print(link)


    htmlb = html.replace('&lt;','<')
    htmlb = htmlb.replace('&gt;','>')
    htmlb = htmlb.replace('&#58;',':')
    htmlb = htmlb.replace('&#46;','.')
    htmlb = htmlb.replace('<br /><span class="posthilit">','')
    htmlb = htmlb.replace('</span>','')
    htmlb = htmlb.replace('<br />','')
    htmlb = htmlb.replace('> <','><')
    htmlb = htmlb.replace('<div class="content">','')
    htmlb = htmlb.replace('<desc>','')
    htmlb = htmlb.replace('</desc>','')
    htmlb = htmlb.replace('<url>','')
    htmlb = htmlb.replace('</url>','')
    htmlb = htmlb.replace('<tmb>','')
    htmlb = htmlb.replace('</tmb>','')
    htmlb = htmlb.replace('<div class="postbody">','')
    htmlb = htmlb.replace('</dl>','')
    htmlb = htmlb.replace('<h3><a href="','')


    contents_=re.compile('&lt;titre&gt;(.+?)&lt;/titre&gt;&lt;tmb&gt;(.+?)&lt;/tmb&gt;&lt;url&gt;(.+?)&lt;/url&gt;&lt;desc&gt;(.+?)&lt;/desc&gt;').findall(html)
    extern_source = re.compile('&lt;ext&gt;(.+?)&lt;/ext&gt;').findall(html)
    contents_new_balise=re.compile('./(.+?)">.+?</a></h3>\n.+?<LABEL>(.+?)</LABEL><THUMBNAIL>(.+?)</THUMBNAIL><DESC>(.+?)</DESC>').findall(htmlb)

    items.append({'label':'[COLOR green]Recherche thématique[/COLOR]', 'icon': varIconDir + 'theme/genre.png','path': plugin.url_for('parse_genre_menu')})

    if modes_search == 'False':
        modes_search = 'False'
    else:
        items.append({'label': '[COLOR green]Liste complète[/COLOR]', 'icon': varIconDir + 'theme/films.png','path':plugin.url_for('parse_chanel_list_the_', url='http://libretv.me/phpbb/search.php?keywords=%3CLABEL%3E*&terms=any&author=&fid%5B%5D=72&sc=1&sf=firstpost&sr=posts&sk=t&sd=d&st=7&ch=2000&t=0&submit=Rechercher',modes_search='false',fulllist='True'),'info':{'Title':'',"Plot":'Films Débrideur Requis'}})

    for topic_url,label,thumb,plot in contents_new_balise:
            trl = topic_url.split(';')
            items.append({'label': label,'icon':thumb,'path':plugin.url_for('parse_topic_list_the', url='http://libretv.me/phpbb/viewtopic.php?f=72&'+trl[1]+'&'+trl[2],mode_rd='true'),'info' : {'genre': 'Action', 'credits': '5', 'date': '', 'outline': plot, 'plot': plot, 'trailer': plot},'properties' : {'fanart_image' : thumb, 'banner' :  thumb, 'clearlogo':  thumb, 'poster':  thumb, 'Plot':plot},'info_type':'video',"is_playable": False})


    for title, icon,stream,plot in contents_:
            plot = plot.replace('&quot;','"')
            items.append({'label':title,'icon':icon,'path':plugin.url_for('parse_rd_deb', url=stream, title=title, icon=icon),'thumbnail':icon,'info':{'Title':title,"Plot":plot},'info_type':'video'})
    if extern_source :
        for url in extern_source:
            html = webSession.get(url).text
            match = re.compile('<titre>(.+?)</titre><tmb>(.+?)</tmb><url>(.+?)</url><desc>(.+?)</desc>').findall(html)
            for title,tmb,url,desc in match:
                items.append({'label':title,'icon':tmb,'path':plugin.url_for('parse_rd_deb', url=url, title=title, icon=tmb ,down='false'),'thumbnail':tmb,'info':{'Title':title,"Plot":desc},'info_type':'video'})
    if modes_search == 'False':
        by_label = itemgetter('label')
        items_ = sorted(items, key=by_label)
        return items_
    else:
        return items
    #return plugin.finish(items, sort_methods=['playlist_order', 'label'])

@plugin.route('/parse_topic_list_the/<url>/<mode_rd>/')
def parse_topic_list_the(url,mode_rd):
    mode_rd=mode_rd
    pl = xbmc.PlayList(1)
    pl.clear()
    items = []
    labelDown = ''
    import hashlib
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_data = urllib.urlencode({'username': varEMail, 'password': varPassword,
                                   "autologin": "on", 'login': 'Login'})
    opener.open(url, login_data)
    titre = opener.open(url)
    html = titre.read()
    ##filtre pour la balise de recherche dp
    htmlb = html.replace('&lt;','<')
    htmlb = htmlb.replace('&gt;','>')
    htmlb = htmlb.replace('&#58;',':')
    htmlb = htmlb.replace('&#46;','.')
    htmlb = htmlb.replace('<br /><span class="posthilit">','')
    htmlb = htmlb.replace('</span>','')
    htmlb = htmlb.replace('<br />','')
    htmlb = htmlb.replace('> <','><')
    htmlb = htmlb.replace('<div class="content">','')
    htmlb = htmlb.replace('<desc>','')
    htmlb = htmlb.replace('</desc>','')
    htmlb = htmlb.replace('<url>','')
    htmlb = htmlb.replace('</url>','')
    htmlb = htmlb.replace('<tmb>','')
    htmlb = htmlb.replace('</tmb>','')
    htmlb = htmlb.replace('<div class="postbody">','')
    htmlb = htmlb.replace('</dl>','')
    htmlb = htmlb.replace('<h3><a href="','')
    html = html.replace('<br /><br />#','<br /><img src="http://vignette3.wikia.nocookie.net/shokugekinosoma/images/6/60/No_Image_Available.png/revision/latest?cb=20150708082716"<br />#')
    found = re.compile('#EXTINF:.+?,(.+?)<br />(.+?)<br /><img src="(.+?)"<br />').findall(html)
    contents_=re.compile('&lt;titre&gt;(.+?)&lt;/titre&gt;&lt;tmb&gt;(.+?)&lt;/tmb&gt;&lt;url&gt;(.+?)&lt;/url&gt;&lt;desc&gt;(.+?)&lt;/desc&gt;').findall(html)
    contents_new_balise=re.compile('>&lt;LABEL&gt;(.+?)&lt;/LABEL&gt;<br />&lt;THUMBNAIL&gt;(.+?)&lt;/THUMBNAIL&gt;<br />&lt;DESC&gt;(.+?)&lt;/DESC&gt;<br />&lt;URL1&gt;(.+?)&lt;/URL1&gt;<br />&lt;URL2&gt;(.+?)&lt;/URL2&gt;<br />&lt;URL3&gt;(.+?)&lt;/URL3&gt;<br />&lt;URL4&gt;(.+?)&lt;/URL4&gt;<br />&lt;URL5&gt;(.+?)&lt;/URL5&gt;.+?').findall(html)
    ###balise utiliser seulement pour le liens avec la recherche dp
    contents_new_balise_dp=re.compile('<LABEL>(.+?)</LABEL><THUMBNAIL>(.+?)</THUMBNAIL><DESC>(.+?)</DESC>').findall(htmlb)
    extern_source = re.compile('&lt;ext&gt;(.+?)&lt;/ext&gt;').findall(html)
    if mode_rd == 'false':
        for title, icon,stream,plot in contents_:
            listitem = xbmcgui.ListItem(stream,thumbnailImage=icon)
            url = stream
            xbmc.PlayList(1).add(url, listitem)
            items.append({'label': '[COLOR aqua]%s[/COLOR]' % title, 'icon': icon, 'path': stream, 'is_playable': True,})
        for title, stream, icon in found:
            fortittleicon = title.replace(' ', '%20')
            listitem = xbmcgui.ListItem(stream,thumbnailImage='http://libretv.me/icon/' + fortittleicon + '.png')
            url = stream
            xbmc.PlayList(1).add(url, listitem)
            items.append({'label': '[COLOR aqua]%s[/COLOR]' % title, 'icon': icon, 'path': stream, 'is_playable': True,})
        if VarModelaunch == 'Automatique':
            xbmc.Player().play(pl)
        if VarModelaunch == 'Manuel':
            return items
    if mode_rd == 'true':
            for label,thumb,plot in contents_new_balise_dp:
                plot = plot.replace('&quot;','"')
                if label == '=Titre=':
                    label = 'titre'
                else:
                    items.append({'label': 'Rechercher ('+label+') sur Dpstream','icon':thumb,'path':plugin.url_for('parse_dp', search='films-recherche?q='+label),'info' : {'genre': 'Action', 'credits': '5', 'date': '', 'outline': plot, 'plot': plot, 'trailer': plot},'properties' : {'fanart_image' : thumb, 'banner' :  thumb, 'clearlogo':  thumb, 'poster':  thumb, 'Plot':plot},'info_type':'video',"is_playable": False})

            for label,thumb,plot,url_,url__,url___,url____,url_____ in contents_new_balise:
                plot = plot.replace('&quot;','"')
                null = 'vide'
                labelDown = ''
                if url_=='na':
                    null

                else :
                        hebergeur = url_.split('/')
                        url_ = url_.replace('X264','')
                        url_ = url_.replace('X265','')
                        url_ = url_.replace(' ','')
                        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url_, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
                if url__=='na':
                         null
                else :
                        hebergeur = url__.split('/')
                        url__ = url__.replace('X264','')
                        url__ = url__.replace('X265','')
                        url__ = url__.replace(' ','')
                        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url__, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
                if url___=='na':
                        null
                else :
                        hebergeur = url___.split('/')
                        url___ = url___.replace('X264','')
                        url___ = url___.replace('X265','')
                        url___ = url___.replace(' ','')
                        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url___, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
                if url____=='na':
                        null
                else :
                        hebergeur = url____.split('/')
                        url____ = url____.replace('X264','')
                        url____ = url____.replace('X265','')
                        url____ = url____.replace(' ','')
                        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url____, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
                if url_____=='na':
                         null
                else :
                        hebergeur = url_____.split('/')
                        url_____ = url_____.replace('X264','')
                        url_____ = url_____.replace('X265','')
                        url_____ = url_____.replace(' ','')
                        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url_____, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})

            for title, stream, icon in found:
                fortittleicon = title.replace(' ', '%20')
                items.append({'label': title+labelDown, 'info': icon, 'path': plugin.url_for('parse_rd_deb', url=stream, title=title, icon=icon ,down='false')})
            for title, icon,stream,plot in contents_:
                plot = plot.replace('&quot;','"')
                items.append({'label':title+labelDown,'icon':icon,'path':plugin.url_for('parse_rd_deb', url=stream, title=title, icon=icon ,down='false'),'thumbnail':icon,'info':{'Title':title,"Plot":plot},'info_type':'video'})
            if extern_source :
                for url in extern_source:
                    html = webSession.get(url).text
                    match = re.compile('<titre>(.+?)</titre><tmb>(.+?)</tmb><url>(.+?)</url><desc>(.+?)</desc>').findall(html)
                    for title,tmb,url,desc in match:
                        items.append({'label':title,'icon':tmb,'path':plugin.url_for('parse_rd_deb', url=url, title=title, icon=tmb ,down='false'),'thumbnail':tmb,'info':{'Title':title,"Plot":desc},'info_type':'video'})
            return items


@plugin.route('/parse_select_hoster/<label>/<thumb>/<url_>/<url__>/<url___>/<url____>/<url_____>/<plot>/')
def parse_select_hoster(label,thumb,url_,url__,url___,url____,url_____,plot):
    items = []
    null = 'vide'
    labelDown = ''
    if url_=='na':
        null
    else :
        hebergeur = url_.split('/')
        url_ = url_.replace('X264','')
        url_ = url_.replace('X265','')
        url_ = url_.replace(' ','')
        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url_, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
    if url__=='na':
         null
    else :
        hebergeur = url__.split('/')
        url__ = url__.replace('X264','')
        url__ = url__.replace('X265','')
        url__ = url__.replace(' ','')
        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url__, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
    if url___=='na':
        null
    else :
        hebergeur = url___.split('/')
        url___ = url___.replace('X264','')
        url___ = url___.replace('X265','')
        url___ = url___.replace(' ','')
        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url___, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
    if url____=='na':
        null
    else :
        hebergeur = url____.split('/')
        url____ = url____.replace('X264','')
        url____ = url____.replace('X265','')
        url____ = url____.replace(' ','')
        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url____, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
    if url_____=='na':
         null
    else :
        hebergeur = url_____.split('/')
        url_____ = url_____.replace('X264','')
        url_____ = url_____.replace('X265','')
        url_____ = url_____.replace(' ','')
        items.append({'label':hebergeur[2]+labelDown,'icon':thumb,'path':plugin.url_for('parse_rd_deb', url=url_____, title=label, icon=thumb,down='false'),'thumbnail':thumb,'info':{'Title':label,"Plot":plot},'info_type':'video'})
    return items

@plugin.route('/parse_wss/')
def parse_wss():
    items = []
    html = webSession.get('http://wss.press/').text
    match = re.compile('"https://cartoonthemes.us/WSSv1.6/(.+?)/(.+?).html"><img src="(https://cartoonthemes.us/WSSv1.6/images/.+?.png)"').findall(html)
    for Title,Stream, icon in match:
                url = 'https://cartoonthemes.us/WSSv1.6/'+Title+'/'+Stream+'.html'
                Title= Title.replace('wss','')
                Title= Title.replace('skysports1','Sky Sports 1')
                Title= Title.replace('skysport1hdgerman','Sky Sport 1 HD (German)')
                Title= Title.replace('btsport1','Bt Sport 1')
                Title= Title.replace('beurosport1','Euro Sport 1')
                Title= Title.replace('skysports2','Sky Sports 2')
                Title= Title.replace('skysport2hdgerman','Sky Sport 2 HD (German)')
                Title= Title.replace('btsport2','Bt Sport 2')
                Title= Title.replace('beurosport2','Eurosport 2')
                Title= Title.replace('skysports3','Sky Sports 3')
                Title= Title.replace('skybundesligahd1','Sky Bundesliga HD 1')
                Title= Title.replace('btsporteurope','Bt Sport europe')
                Title= Title.replace('foxsports1','Fox Sports 1')
                Title= Title.replace('skysports4','Sky Sports 4')
                Title= Title.replace('btsportespn','Bt Sport Espn')
                Title= Title.replace('foxsports2','Fox Sports 2')
                Title= Title.replace('skysports5','Sky Sports 5')
                Title= Title.replace('tsn1','Tsn 1')
                Title= Title.replace('skysportsf1','Sky Sports f1')
                Title= Title.replace('tsn2','Tsn 2')
                Title= Title.replace('skysportsnews','Sky Sports News')
                Title= Title.replace('premiersports','Premier Sports')
                Title= Title.replace('astro1','Astro 1')
                Title= Title.replace('attheraces','At The Races')
                Title= Title.replace('setantaireland','Setanta Ireland')
                Title= Title.replace('astro2','Astro 2')
                Title= Title.replace('skyitaly1hd','Sky Italy1 HD')
                Title= Title.replace('chelseatv','Chelsea Tv')
                Title= Title.replace('astro3','Astro 3')
                Title= Title.replace('skyitaly2hd','Sky italy 2 HD')
                Title= Title.replace('espnusa','Espn Usa')
                Title= Title.replace('espn2','Espn 2')
                Title= Title.replace('wwe','Wwe')
                Title= Title.replace('skyitaly3hd','Sky Italy 3 HD')
                Title= Title.replace('boxnation','Box Nation')
                Title= Title.replace('nhlnetwork','NHL Network')
                Title= Title.replace('nflnetwork','NFL Network')
                Title= Title.replace('skyitaly24hd','Sky Italy 24 HD')
                Title= Title.replace('sportklub1','Sport Klub 1')
                Title= Title.replace('sportklub2','Sport Klub 2')
                Title= Title.replace('sportklub3','Sport Klub 3')
                Title= Title.replace('nbcsn','NBC SN')
                Title= Title.replace('sporttv1','Sport TV 1')
                Title= Title.replace('nbcsn','NBC SN')
                Title= Title.replace('sporttv3','Sport TV 3')
                Title= Title.replace('btn','Btn')
                Title= Title.replace('starsports1','Star Sports 1')
                Title= Title.replace('starsports2','Star Sports 2')
                Title= Title.replace('starsports3','Star Sports 3')
                Title= Title.replace('starsports4','Star Sports 4')
                Title= Title.replace('tencricket','Ten Cricket')
                Title= Title.replace('tensports','Ten Sports')
                Title= Title.replace('sonysix','Sony Six')
                Title= Title.replace('ptv','Ptv Sports')
                Title= Title.replace('beinsports1','Bein Sports 1')
                Title= Title.replace('beinsports2','Bein Sports 2')
                Title= Title.replace('beinsports3','Bein Sports 3')
                Title= Title.replace('beinsports4','Bein Sports 4')
                Title= Title.replace('beinsports5','Bein Sports 5')
                Title= Title.replace('beinsports6','Bein Sports 6')
                Title= Title.replace('beinsports7','Bein Sports 7')
                Title= Title.replace('beinsports8','Bein Sports 8')
                Title= Title.replace('beinsports9','Bein Sports 9')
                Title= Title.replace('beinsports10','Bein Sports 10')
                Title= Title.replace('beinsports11','Bein Sports 11')
                Title= Title.replace('beinsports12','Bein Sports 12')
                Title= Title.replace('ch1to30','PPV LIVE')
                Title= Title.replace('itv1','Itv 1')
                Title= Title.replace('itv2','Itv 2')
                Title= Title.replace('itv3','Itv 3')
                Title= Title.replace('itv4','Itv 4')
                icon= icon.replace('https://cartoonthemes.us/WSSv1.6/images/ch1to30.png','http://www.payperviewliveevents.com/wp-content/uploads/ppv-events-10.png')

                items.append({'label':Title, 'icon':icon,'path':plugin.url_for('parse_wss_decode',url=url,icon=icon),'thumbnail':icon,'info':{'Title':Title,"Plot":''},'info_type':'video'})
    return items

@plugin.route('/parse_wss_decode/<url>/<icon>/')
def parse_wss_decode(url,icon):
    items = []
    source__ = urllib2.urlopen(url)
    html= source__.read()
    match = re.compile('(http://s1.wssiptv.com:8000/live/.+?/.+?/.+?)">(.+?)</a>').findall(html)
    for url, Title in match:
        Title= Title.replace('1)','')
        Title= Title.replace('2)','')
        Title= Title.replace('3)','')
        Title= Title.replace('4)','')
        Title= Title.replace(' (WSS Server-Beta)','')
        Title= Title.replace(' (Backup)','')
        items.append({'label':Title, 'icon':icon,'path':url+'|User-Agent=Mozilla/5.0 (Linux; U; Android 3.1; en-ca; MZ604 Build/H.6.4-20) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13','is_playable': True,'thumbnail':'','info':{'Title':Title,"Plot":''},'info_type':'video'})
    return items

# ------------------------------------
# -----------FUNCTIONS----------------
# ------------------------------------
def authenticate():
    isLogged = False
    isFrom = None
    # routine pour utilisateur forum Libretv.me
    if varForumName == 'Libretv.me':
        isLogged = login('http://libretv.me/phpbb/ucp.php?mode=login', varEMail, varPassword)
        if isLogged: isFrom = 'Libretv'
    # routine pour utilisateur forum Eric-lafontaine.com
    elif varForumName == 'E-lafontaine.com':
        isLogged = login('http://forum.eric-lafontaine.com/ucp.php?mode=login', varEMail, varPassword)
        if isLogged:
            html = webSession.get('http://forum.eric-lafontaine.com/viewtopic.php?f=41&t=1462').text
            match = re.compile('Port&amp;t=(.+?)#p5205').findall(html)
            if match:
                isLogged = login('http://libretv.me/phpbb/ucp.php?mode=login', 'Port', match[0])
                if isLogged: isFrom = 'E-lafontaine'
            else:
                isLogged = False
    # routine si erreur de connexion ou invités
    if not isLogged:
        html = webSession.get('http://libretv.me/key9a7FZjb9EvPf9kFSbyFvpaEs/XRtbjmUn.php').text
        match = re.compile('<pass>(.*?)</pass>').findall(html)
        if match:
            isLogged = login('http://libretv.me/phpbb/ucp.php?mode=login', 'invite', match[0])
            if isLogged: isFrom = 'Invite'
    return isLogged, isFrom


def isLogged(url):
    html = webSession.get(url).text
    if 'Connexion' in html:
        return False
    else:
        return True


def login(url, username, password):
    if not isLogged(url):
        payload = {'username': username, 'password': password, "autologin": "on", 'login': 'Connexion'}
        webSession.post(url, data=payload)
    return isLogged(url)


# ------------------------------------
# -------------MAIN-------------------
# ------------------------------------
if __name__ == '__main__':
    # print 'COOKIES START : '+str(webSession.cookies)
    # varIsEnabled, varIsFrom = authenticate()
    # if varIsEnabled :
    plugin.run()
    # print 'COOKIES END : '+str(webSession.cookies)
