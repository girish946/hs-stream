BASEURL = "http://account.hotstar.com/AVS/besc?action=GetAggregatedContentDetails&channel=PCTV&contentId={0}"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36',
           'Accept': 'text/html'}
CDNURL = "http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=TABLET&id={0}&type=VOD"
