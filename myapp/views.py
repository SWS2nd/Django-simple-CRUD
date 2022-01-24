from django.shortcuts import redirect, HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt

nextId = 4
topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ..'},
    {'id':2, 'title':'view', 'body':'View is ..'},
    {'id':3, 'title':'model', 'body':'Model is ..'},
]

def HTMLTemplate(articleTag, id=None):
    global topics
    context_ui = ''
    # delete 버튼이 해당 항목으로 들어갔을 때만(url에 id값이 있어야만) 보이도록 하기 위함
    if id != None:
        context_ui = f'''
                <li>
                    <form action="/delete/" method="post">
                        <input type="hidden" name="id" value={id}>
                        <input type="submit" value="delete">
                    </form>
                </li>
                <li>
                    <a href="/update/{id}">update</a>
                </li>
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
        <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
                {context_ui}
            </ul>
        </body>
        </html>
        '''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == id:
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))

# csrf를 면제하겠다는 데코레이터
@csrf_exempt
def create(request):
    global nextId
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></b>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        new_topic = {'id': nextId, 'title': title, 'body': body}
        topics.append(new_topic)
        # nextId 값이 갱신되기 이전의 nextId 값으로 redirect
        # create하여 새로 만든 url로 이동하기 위함
        url = '/read/' + str(nextId)
        nextId += 1
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        # id 변수에 저장된 값은 str 형식
        id = request.POST['id']
        # -- 삭제 레퍼토리 --
        # for 문을 돌면서 삭제하고 싶은 항목의 id 값과 id가 일치하는 항목만
        # 제외하고 나머지를 newTopics 리스트에 추가
        # id가 일치하는 항목이 제외된 newTopics 리스트를
        # topics로 교체함
        newTopics = []
        for topic in topics:
            # 비교를 위해 int 형으로 바꿔줌
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == id:
                selected_topic = {
                    'title': topic['title'],
                    'body': topic['body']
                }
        article = f'''
                    <form action="/update/{id}/" method="post">
                        <p><input type="text" name="title" placeholder="title" value={selected_topic['title']}></p>
                        <p><textarea name="body" placeholder="body">{selected_topic['body']}</textarea></p>
                        <p><input type="submit"></b>
                    </form>
                '''
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == id:
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')