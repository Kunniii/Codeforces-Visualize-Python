from requests import *
import json, sys, os
from time import sleep, localtime

def getRank(rankJson):
    rating = rankJson['result'][-1]['newRating']
    if rating >= 3000:
        color = '#a00'
    elif rating >= 2600:
        color = '#f33'
    elif rating >= 2400:
        color = '#f77'
    elif rating >= 2300:
        color = '#fb5'
    elif rating >= 2100:
        color = '#fc8'
    elif rating >= 1900:
        color = '#f8f'
    elif rating >= 1600:
        color = '#aaf'
    elif rating >= 1400:
        color = '#7db'
    elif rating >= 1200:
        color ='#7f7'
    else:
        color = '#ccc'
    return color


def unique_list(l):
    temp = []
    for i in l:
        if i not in temp:
            temp.append(i)
    return temp

problem_unique_name = []
not_done_problem = {}
solved_problem = {}
u_languages = []
languages = []

try:
    handle = str(sys.argv[1])
except IndexError:
    handle = input('handle = ')

if handle == '.':
    handle = 'poiminhcanh08092001'

url = 'https://codeforces.com/api/user.status?handle=' + handle + '&from=1&count=6000'
rankUrl = 'https://codeforces.com/api/user.rating?handle=' + handle
print(url)
loclTime = localtime()
rawJson = json.loads(get(url).text)
rankJson = json.loads(get(rankUrl).text)

status = rawJson['status']
print(f'{loclTime.tm_year}-{loclTime.tm_mon}-{loclTime.tm_mday} @ {loclTime.tm_hour}:{loclTime.tm_min} | status: {status}')
status = rankJson['status']
print(f'{loclTime.tm_year}-{loclTime.tm_mon}-{loclTime.tm_mday} @ {loclTime.tm_hour}:{loclTime.tm_min} | status: {status}')

result = rawJson['result']
rankColor = getRank(rankJson)

del rankJson
del status

with open('submission_.html', 'a') as f:
    pass
with open('yes_.html', 'a') as f:
    pass
with open('no_.html', 'a') as f:
    pass

# collect problems that are having the WRONG_ANSWER verdict
for content in result:
    if content['problem']['name'] not in not_done_problem and content['verdict'] != 'OK':
        not_done_problem.update({str(content['problem']['contestId']) + '/' + content['problem']['index'] : content['problem']['name']})

# collect problems that have been solved
for content in result:
    if content['problem']['name'] not in solved_problem and content['verdict'] == 'OK':
        solved_problem.update({str(content['problem']['contestId']) + '/' + content['problem']['index'] : content['problem']['name']})
        languages.append(content['programmingLanguage'])

# collect unique problem's name
for content in result:
    if content['problem']['name'] not in problem_unique_name:
        problem_unique_name.append(content['problem']['name'])

# check if problem has been solved
not_done_problem = {url:name for (url,name) in not_done_problem.items() if name not in solved_problem.values()}

u_languages = unique_list(languages)

with open('submission_.html','w', encoding='utf8') as f:
    print('<html>', file=f)
    
    print('<head>', file=f)
    print(f"<title>{handle} Submission</title>", file=f)
    print('<link rel="stylesheet" type="text/css" href="./style.css">', file=f)
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">', file=f)
    # print('<meta http-equiv="refresh" content="1"/>', file=f)
    print(f'<h1><a style="color:{rankColor};" href="https://codeforces.com/profile/{handle}" target="_blank">{handle}</a> Submission</h1>', file=f)
    print('</head>', file=f)
    
    print('<body>', file=f)
    print(f'<br><br><h1><span style="color:{rankColor};">{handle}</span> has solved <span class="done"><a href="./yes_.html">{len(solved_problem)}</a></span> in total, unable to solve <span class="not-done"><a href="./no_.html">{len(not_done_problem)}</a></span></h1>', file=f)
    print('<hr>', file=f)
    
    print('<table>', file=f)
    print("<tr><th>Problem's name</th></tr>", file=f)
    written = []
    for name in problem_unique_name:
        if name in solved_problem.values() and name not in written:
            print(f'<tr><td><a class="done" href="https://codeforces.com/problemset/problem/{list(solved_problem.keys())[list(solved_problem.values()).index(name)]}" target="_blank">{name}</a></td></tr>', file=f)
            written.append(name)
        elif name in not_done_problem.values() and name not in written:
            print(f'<tr><td><a class="not-done" href="https://codeforces.com/problemset/problem/{list(not_done_problem.keys())[list(not_done_problem.values()).index(name)]}" target="_blank">{name}</a></td></tr>', file=f)
            written.append(name)
    print('</table><table>', file=f)


    print('<div id="piechart"></div><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load(\'current\', {\'packages\':[\'corechart\']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = google.visualization.arrayToDataTable([',file=f)
    print("['Language', 'In total'],",file=f)
    for i in u_languages:
        print(f"['{i}', {int(languages.count(i))}],",file=f)
    print(']);',file=f)
    print("var options = {'title':'Programing Language', pieSliceText: 'label',};\nvar chart = new google.visualization.PieChart(document.getElementById('piechart'));\nchart.draw(data, options);}</script>", file=f)


    print('<div id="YNpiechart"></div><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load(\'current\', {\'packages\':[\'corechart\']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = google.visualization.arrayToDataTable([',file=f)
    print(f"['Language', 'In total'],['YES', {len(solved_problem)}],['NO', {len(not_done_problem)}]]);",file=f)
    print("var options = {'title':'Solved Problem', pieSliceText: 'label',};\nvar chart = new google.visualization.PieChart(document.getElementById('YNpiechart'));\nchart.draw(data, options);}</script>", file=f)
    print('</table></body></html>', file=f)

# create file yes_.html and no_.html
with open('yes_.html','w', encoding='utf8') as f:
    print('<html>', file=f)
    
    print('<head>', file=f)
    print(f"<title>{handle} Solved</title>", file=f)
    print('<link rel="stylesheet" type="text/css" href="./style.css">', file=f)
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">', file=f)
    # print('<meta http-equiv="refresh" content="1"/>', file=f)
    print(f'<h1><a href="./submission_.html">Back to <span style="color:{rankColor};">{handle}</span> Submission</a></h1>', file=f)
    print('</head>', file=f)
    
    print('<body>', file=f)
    print(f'<br><br><h1><span style="color:{rankColor}">{handle}</span> solved <span class="done"><a href="./yes_.html">{len(solved_problem)}</a></span></h1>', file=f)
    print('<hr>', file=f)
    
    print('<table>', file=f)
    print('<tr><th>Problem\'s name</th></tr>', file=f)
    written = []
    for name in problem_unique_name:
        if name in solved_problem.values() and name not in written:
            print(f'<tr><td><a class="done" href="https://codeforces.com/problemset/problem/{list(solved_problem.keys())[list(solved_problem.values()).index(name)]}" target="_blank">{name}</a></td></tr>', file=f)
            written.append(name)
    print('</table></body></html>', file=f)
    
    # create no_.html 
    with open('no_.html','w', encoding='utf8') as f1:
        print('<html>', file=f1)
        
        print('<head>', file=f1)
        print(f"<title>{handle}'s Unsolved</title>", file=f1)
        print('<link rel="stylesheet" type="text/css" href="./style.css">', file=f1)
        print('<meta name="viewport" content="width=device-width, initial-scale=1.0">', file=f1)
        # print('<meta http-equiv="refresh" content="1"/>', file=f)
        print(f'<h1><a href="./submission_.html">Back to <span style="color:{rankColor};">{handle}</span> Submission</a></h1>', file=f1)
        print('</head>', file=f1)
        
        print('<body>', file=f1)
        print(f'<br><br><h1><span style="color:{rankColor}">{handle}</span> unable to solve <span class="not-done"><a href="./no_.html">{len(not_done_problem)}</a></span></h1>', file=f1)
        print('<hr>', file=f1)
        
        print('<table>', file=f1)
        print("<tr><th>Problem's name</th></tr>", file=f1)
        
        for name in problem_unique_name:
            if name in not_done_problem.values() and name not in written:
                print(f'<tr><td><a class="not-done" href="https://codeforces.com/problemset/problem/{list(not_done_problem.keys())[list(not_done_problem.values()).index(name)]}" target="_blank">{name}</a></td></tr>', file=f1)
                written.append(name)
        print('</table></body></html>', file=f1)

fileDir = os.path.dirname(os.path.realpath('submission_.html')) + '/submission_.html'
os.system(f'start chrome "{fileDir}"')
