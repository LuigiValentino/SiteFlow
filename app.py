from flask import Flask, render_template, request, jsonify, send_file
from sitemap_generator import generate_sitemap
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_sitemap', methods=['POST'])
def generate_sitemap_route():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'Invalid URL'})
    
    sitemap = generate_sitemap(url)
    return jsonify(sitemap)

@app.route('/export_sitemap_txt', methods=['POST'])
def export_sitemap_txt():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'Invalid URL'})

    sitemap = generate_sitemap(url)
    filename = 'sitemap.txt'

    with open(filename, 'w') as f:
        for link in sitemap['nodes']:
            f.write(f"{link}\n")

    return send_file(filename, as_attachment=True, download_name=filename)

@app.route('/export_sitemap_xml', methods=['POST'])
def export_sitemap_xml():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'Invalid URL'})

    sitemap = generate_sitemap(url)
    filename = 'sitemap.xml'

    with open(filename, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="">\n')
        
        for link in sitemap['nodes']:
            escaped_link = link.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            f.write('  <url>\n')
            f.write(f'    <loc>{escaped_link}</loc>\n')
            f.write('  </url>\n')

        f.write('</urlset>')

    return send_file(filename, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
