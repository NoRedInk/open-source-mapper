import requests
import json


def main(org):
    url = "https://api.github.com/orgs/{org}/repos?page=".format(org=org)


    i = 1
    repos = []

    while True:
        r = requests.get(url + str(i))
        current_repos = r.json()
        if not current_repos:
            break

        repos.extend(current_repos)
        i += 1

    tailored_repos = {}

    for repo in repos:
        tailored_repos[repo['name']] = {
            'name': repo['name'],
            'stars': repo['stargazers_count'],
            'language': repo['language'],
            'forks': repo['forks_count'],
            'issues': repo['open_issues'],
            'description': repo['description']
        }

    languages = [v['language'] for v in tailored_repos.values()]
    unique_languages = set(languages)
    languages_by_count = { lang : languages.count(lang) for lang in unique_languages }

    with open('map.md', 'w') as f:
        f.write('We have {} repos written in {} languages\n'.format(len(tailored_repos), len(unique_languages)))

        f.write('\n\n\n')
        f.write('## Language breakdown\n')


        f.write('| Language | Count |\n')
        f.write('|----------|-------|\n')
        for number, lang in sorted(languages_by_count.items(), key=lambda x: x[1], reverse=True):
            f.write('| {} | {} |\n'.format(lang, number))

        f.write('\n\n\n')
        f.write('## Repo breakdown\n')

        f.write('| Repo | Stars | Language | Forks | Issues | Description |\n')
        f.write('|------|-------|----------|-------|--------|-------------|\n')
        for repo in sorted(tailored_repos.values(), key=lambda x: x['stars'], reverse=True):
            f.write(
                '| [{name}](http://github.com/{org}/{name}) | {stars} | {language} | {forks} | {issues} | {description} |\n'.format(
                    org=org,
                    name=repo['name'],
                    stars=repo['stars'],
                    language=repo['language'],
                    forks=repo['forks'],
                    issues=repo['issues'],
                    description=repo['description']
                )
            )

if __name__ == '__main__':
    org = "NoRedInk"
    main(org)

