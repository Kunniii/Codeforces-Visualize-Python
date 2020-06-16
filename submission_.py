from requests import get
import json, sys, os
from time import sleep, localtime

def unique_list(l):
    temp = []
    for i in l:
        if i not in temp:
            temp.append(i)
    return temp

problem_unique_name = []
not_done_problem = []
solved_problem = []
u_languages = []
languages = []

try:
    handle = str(sys.argv[1])
except IndexError:
    handle = input('handle = ')

if handle == '.':
    handle = 'poiminhcanh08092001'
url = 'https://codeforces.com/api/user.status?handle=' + handle + '&from=1&count=6000';
print(url)
loclTime = localtime()
rawJson = json.loads(get(url).text)

os.system('start chrome "submission_.html"')

status = rawJson['status']
print(f'{loclTime.tm_year}-{loclTime.tm_mon}-{loclTime.tm_mday} @ {loclTime.tm_hour}:{loclTime.tm_min} | status: {status}')

result = rawJson['result']

sleep(1)

# collect problems that are having the WRONG_ANSWER verdict
for content in result:
    if content['problem']['name'] not in not_done_problem and content['verdict'] != 'OK':
        not_done_problem.append(content['problem']['name'])

# collect problems that have been solved
for content in result:
    if content['problem']['name'] not in solved_problem and content['verdict'] == 'OK':
        solved_problem.append(content['problem']['name'])
        languages.append(content['programmingLanguage'])

# collect unique problem's name
for content in result:
    if content['problem']['name'] not in problem_unique_name:
        problem_unique_name.append(content['problem']['name'])

# check if problem has been solved
not_done_problem = [name for name in not_done_problem if name not in solved_problem]

u_languages = unique_list(languages)

with open('submission_.html','w', encoding='utf8') as f:
    print('<html>', file=f)
    
    print('<head>', file=f)
    print('<title>{}\'s Submission</title>'.format(handle), file=f)
    print('<link rel="stylesheet" type="text/css" href="./style.css">', file=f)
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">', file=f)
    # print('<meta http-equiv="refresh" content="1"/>', file=f)
    print('<h1><span class="handle">{}</span> Submission</h1>'.format(handle), file=f)
    print('</head>', file=f)
    
    print('<body>', file=f)
    print(f'<br><br><h1><span class="handle">{handle}</span> has solved <span class="done">{len(solved_problem)}</span> in total, unable to solve <span class="not-done">{len(not_done_problem)}</span></h1>', file=f)
    print('<hr>', file=f)
    
    print('<table>', file=f)
    print('<tr><th>Problem\'s name</th><th>Solved</th><br><br></tr>', file=f)
    yes = 0
    no = 0
    written = []
    for name in problem_unique_name:
        if name in solved_problem and name not in written:
            print(f'<tr><td>{name}</td><td class="done">YES</td></tr>', file=f)
            written.append(name)
            yes += 1
        elif name in not_done_problem and name not in written:
            print(f'<tr><td>{name}</td><td class="not-done">NO</td></tr>', file=f)
            written.append(name)
            no += 1

    print('</table>', file=f)


    print('<div id="piechart"></div><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load(\'current\', {\'packages\':[\'corechart\']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = google.visualization.arrayToDataTable([',file=f)
    print('[\'Language\', \'In total\'],',file=f)
    for i in u_languages:
        print(f'[\'{i}\', {int(languages.count(i))}],',file=f)
    print(']);',file=f)
    print('var options = {\'title\':\'Programing Language\', is3D: true, pieSliceText: \'label\',};\nvar chart = new google.visualization.PieChart(document.getElementById(\'piechart\'));\nchart.draw(data, options);}</script>', file=f)


    print('<div id="YNpiechart"></div><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load(\'current\', {\'packages\':[\'corechart\']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = google.visualization.arrayToDataTable([',file=f)
    print('[\'Language\', \'In total\'],[\'YES\', {}],[\'NO\', {}]]);'.format(yes, no),file=f)
    print('var options = {\'title\':\'Solved Problem\', is3D: true, pieSliceText: \'label\',};var chart = new google.visualization.PieChart(document.getElementById(\'YNpiechart\'));chart.draw(data, options);}</script>', file=f)
    print('</body>\n</html>', file=f)

