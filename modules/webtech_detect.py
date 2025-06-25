import requests
from bs4 import BeautifulSoup

def detect_technologies(url):
    techs = {
        'server': None,
        'x_powered_by': None,
        'cms': [],
        'frameworks': [],
        'languages': []
    }

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        techs['server'] = headers.get('Server', None)
        techs['x_powered_by'] = headers.get('X-Powered-By', None)

        soup = BeautifulSoup(response.text, 'html.parser')

        generator = soup.find('meta', attrs={'name':'generator'})
        if generator and generator.get('content'):
            content = generator['content'].lower()
            if 'wordpress' in content:
                techs['cms'].append('WordPress')
            elif 'joomla' in content:
                techs['cms'].append('Joomla')
            elif 'drupal' in content:
                techs['cms'].append('Drupal')
            else:
                techs['cms'].append(content)

        html_text = response.text.lower()
        if 'wp-content' in html_text or 'wp-includes' in html_text:
            if 'WordPress' not in techs['cms']:
                techs['cms'].append('WordPress')
        if 'joomla' in html_text:
            if 'Joomla' not in techs['cms']:
                techs['cms'].append('Joomla')
        if 'drupal' in html_text:
            if 'Drupal' not in techs['cms']:
                techs['cms'].append('Drupal')

        if 'express' in html_text:
            techs['frameworks'].append('Express.js')
        if 'django' in html_text:
            techs['frameworks'].append('Django')

        if techs['x_powered_by']:
            xpb = techs['x_powered_by'].lower()
            if 'php' in xpb:
                techs['languages'].append('PHP')
            if 'asp.net' in xpb:
                techs['languages'].append('ASP.NET')
            if 'python' in xpb:
                techs['languages'].append('Python')

        if 'php' in html_text:
            if 'PHP' not in techs['languages']:
                techs['languages'].append('PHP')

        return techs

    except requests.RequestException as e:
        print(f"[!] Erreur lors de la requête HTTP : {e}")
        return None
