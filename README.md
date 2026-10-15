# Burlington Snow Co.

Website for [burlingtonsnowco.ca](https://burlingtonsnowco.ca), served by GitHub Pages from the repository root.

- `src/page.html` is the page source (body content, styles and script).
- `src/build.py` wraps it into `index.html` with the SEO head, structured data, `llms.txt`, `robots.txt`, `sitemap.xml` and `CNAME`.

Rebuild after editing the source:

```
python3 src/build.py src/page.html .
```
