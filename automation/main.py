from bs4 import BeautifulSoup
import requests, json, os


def getGithubReleases(url):
    releases = []
    css_path = "div.Box-body.p-0 > div > div > div"
    content_tags = BeautifulSoup(requests.get(url).content, 'html.parser')
    release_tags = content_tags.select(css_path)
    if release_tags:
        for r in release_tags:
            version = r.find_next("div").find_next("h4").find_next("a")
            date = r.find_next("ul").find_next("li").find_next("relative-time")
            download = "https://github.com/%s" %(version["href"])
            releases.append({ 
                "version": version.text.strip(), 
                "date": date.text.strip(),
                "download": download 
            })
    return releases


def generateGithubReleasesData(save_directory, filename, matches, category = None):
    githubReleases = {}
    if category: matches = [r for r in matches if r["category"] is category]
    for m in matches:
        releases = getGithubReleases(m["url"])
        if releases: githubReleases[m["name"]] = { "category": m["category"], "releases": releases }
    if not os.path.exists(save_directory): os.makedirs(save_directory)
    filepath = save_directory + "/%s" %filename
    with open(filepath, 'w', encoding='utf-8') as f: json.dump(githubReleases, f, ensure_ascii=False, indent=4)


# Standard
# { "name": "aaa", "category": "aaa", "url": "https://github.com/aaa/aaa/tags" },
config_filepath = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_filepath, 'r') as c_file: 
    content = json.load(c_file)
    if content.get("github_matches"): 
        generateGithubReleasesData("releases", "github_releases.json", content.get("github_matches"))
