"""Build the standalone burlingtonsnowco.ca site from the artifact source page."""
import sys, json, re, os
src, out = sys.argv[1], sys.argv[2]  # optional argv[3]: booking web app URL
os.makedirs(out, exist_ok=True)
D = "https://burlingtonsnowco.ca/"
body = open(src).read()
if len(sys.argv) > 3 and sys.argv[3]:
    body = body.replace('var BOOKING_URL = "";', 'var BOOKING_URL = ' + json.dumps(sys.argv[3]) + ';', 1)
body = re.sub(r'<title>.*?</title>\n', '', body, count=1)
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
body = re.sub(r'<meta name="description"[^>]*>\n', '', body, count=1)
HOODS = ["Aldershot","Alton Village","Brant Hills","Downtown Burlington","Headon Forest","Millcroft","Orchard","Palmer","Roseland","Shoreacres","Tansley","Tyandaga"]
PRICES = [("Townhouse",499),("Single car",649),("Double car",799),("Large (5+ cars)",999)]
biz = {"@type":["LocalBusiness","HomeAndConstructionBusiness"],"@id":D+"#business","name":"Burlington Snow Co.","url":D,
 "logo":D+"logo.png","image":D+"og-image.png","telephone":"+1-647-504-5210","priceRange":"$499-$999 per season","currenciesAccepted":"CAD",
 "description":"Seasonal residential snow removal in Burlington, Ontario. Driveway, walkway and front steps cleared every time 5 cm falls, November to April. Cleared within 6 hours of the snow stopping or the visit is free.",
 "address":{"@type":"PostalAddress","addressLocality":"Burlington","addressRegion":"ON","addressCountry":"CA"},
 "geo":{"@type":"GeoCoordinates","latitude":43.3255,"longitude":-79.799},
 "areaServed":[{"@type":"City","name":"Burlington","containedInPlace":{"@type":"AdministrativeArea","name":"Halton Region, Ontario"}}]+[{"@type":"Place","name":n+", Burlington, ON"} for n in HOODS],
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}],
 "knowsAbout":["Snow removal","Driveway snow clearing","Walkway shovelling","Snow plowing","Windrow clearing"],
 "hasOfferCatalog":{"@type":"OfferCatalog","name":"Seasonal snow removal packages, driveway and walkway included","itemListElement":[
   {"@type":"Offer","itemOffered":{"@type":"Service","serviceType":"Residential snow removal","name":f"{n} driveway and walkway, seasonal snow removal","areaServed":"Burlington, ON"},"price":str(p),"priceCurrency":"CAD","eligibleDuration":{"@type":"QuantitativeValue","name":"November to April season"}} for n,p in PRICES]}}
site = {"@type":"WebSite","@id":D+"#website","url":D,"name":"Burlington Snow Co.","inLanguage":"en-CA","publisher":{"@id":D+"#business"}}
faq = [{"@type":"Question","name":re.sub('<[^>]+>','',q),"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}}
       for q,a in re.findall(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', body)]
graph = {"@context":"https://schema.org","@graph":[biz, site, {"@type":"FAQPage","@id":D+"#faq","mainEntity":faq}]}
desc = "Snow removal in Burlington, ON. Driveway and walkway cleared every time 5 cm falls, within 6 hours or it's free. Townhouse $499 a season. Text 647 504 5210."
head = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Snow Removal Burlington ON | From $499 a Season | Burlington Snow Co.</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{D}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_CA">
<meta property="og:site_name" content="Burlington Snow Co.">
<meta property="og:title" content="Burlington Snow Co. | Snow removal from $499 a season">
<meta property="og:description" content="Driveway and walkway cleared every time 5 cm falls. Cleared in 6 hours or it's free. Text 647 504 5210.">
<meta property="og:url" content="{D}">
<meta property="og:image" content="{D}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Burlington Snow Co. homepage: snow removal in Burlington with season prices from $499">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Burlington">
<meta name="geo.position" content="43.3255;-79.7990">
<meta name="ICBM" content="43.3255, -79.7990">
<meta name="theme-color" content="#0D2F5C">
<link rel="icon" href="/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/logo.png">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM summary">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
'''
open(f'{out}/index.html','w').write(head + body + '\n</body>\n</html>\n')
bots = ["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-SearchBot","PerplexityBot","Google-Extended","Applebot-Extended","Bingbot","Googlebot"]
open(f'{out}/robots.txt','w').write("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {D}sitemap.xml\n")
open(f'{out}/sitemap.xml','w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{D}</loc><lastmod>2026-10-15</lastmod><changefreq>weekly</changefreq></url>\n</urlset>\n')
open(f'{out}/CNAME','w').write("burlingtonsnowco.ca\n")
open(f'{out}/.nojekyll','w').write("")
faqtxt = "\n".join(f"- **{f['name']}** {f['acceptedAnswer']['text']}" for f in faq)
open(f'{out}/llms.txt','w').write(f"""# Burlington Snow Co.

> Burlington Snow Co. is a local, insured snow removal company in Burlington, Ontario, Canada. Season plans (November to April) clear the driveway, walkway and front steps every time 5 cm or more of snow falls, including the snowbank the city plow leaves. Driveways are cleared within 6 hours of the snow stopping (12 hours for storms over 20 cm) or that visit is free.

## Contact
- Call or text: 647 504 5210
- Website: {D}
- Service area: Burlington, Ontario only

## Season prices (CAD, plus HST, walkway and front steps included)
""" + "".join(f"- {n}: ${p}\n" for n,p in PRICES) + """- Payment: nothing due when booking online; after confirmation by text, pay by Interac e-Transfer, half up front and half on January 1
- Commercial sites (condos, plazas, offices): quoted per site

## Neighbourhoods served
""" + ", ".join(HOODS) + """

## Customer reviews
5 reviews from Burlington customers, all 5 stars, shown on the homepage.

## FAQ
""" + faqtxt + "\n")
open(f'{out}/logo.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><circle cx="15" cy="15" r="15" fill="#FFC93C"/><path d="M15 6v18M7.2 10.5l15.6 9M22.8 10.5l-15.6 9" stroke="#0D2F5C" stroke-width="2.4" stroke-linecap="round"/></svg>\n')
print("built", out, len(faq), "faq")
