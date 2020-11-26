from django.shortcuts import render
from django.http import JsonResponse
import socket
import time

host = ''
port = 9898
data = []
all_connections = []
all_address = []
s = socket.socket()
s.settimeout(5)
s.bind((host, port))
s.listen(5)


def create():
    global host, port, s, all_connections, all_address, data

    s1 = int(time.time())
    s2 = s1

    while (s2 - s1) <= 15:
        try:
            conn, address = s.accept()
            all_connections.append(conn)
            all_address.append(address)
            data.append('test')

        except socket.error:
            pass
        s2 = int(time.time())

    if len(all_connections) == 0:
        return 'No Clients Found'
    else:
        i = 0
        result = []
        while i < len(all_connections):
            try:
                all_connections[i].send(str.encode('check4live'))
                txt = str(all_connections[i].recv(2048), 'utf-8')
                txt = txt.split(',')
                data[i] = txt
                i += 1
            except socket.error:
                all_connections.pop(i)
                all_address.pop(i)
                data.pop(i)

        for i in range(len(all_address)):
            result.append([i + 1, all_address[i][0], data[i][0], data[i][2]])
        return result


def home(request):
    return render(request, "home.html")


def scan(request):
    global s, all_connections

    if request.method == 'POST':
        try:
            msg = create()

            if type(msg) == type('a') and len(msg) > 0 and msg[0] == 'N':
                return render(request, "result.html", context={'message': msg})
            else:
                return render(request, "result.html", context={'result': msg})
        except socket.error as ee:
            for i in all_connections:
                i.close()
            s.close()
            return render(request, "result.html", context={'message': str(ee)})
    return render(request, "result.html")


def select(request):
    global s, all_connections, all_address, data

    if request.method == 'POST':
        x = request.POST.get('serial')
        if x.isnumeric:
            x = int(x) - 1
            if 0 <= x < len(all_connections):
                return render(request, "query.html", context={'result': x + 1})
            elif x == -1:
                return render(request, "query.html", context={'result': x})
            else:
                return render(request, "query.html", context={'message': 'Choosed serial is out of range'})
        else:
            return render(request, "query.html", context={'message': 'Invalid Serial Provided'})
    else:
        return render(request, "query.html", context={'message': 'Method was not post'})


def query(request, ind):
    global s, all_connections, all_address, data

    if request.method == 'POST':
        qu = request.POST.get('qy')
        if ind.isnumeric and 0 <= int(ind) <= len(data) and len(qu) > 0:
            ind = int(ind) - 1
            if qu == 'list':
                return JsonResponse({'msge': True})
            elif qu == 'quit':
                all_connections[ind].send(str(qu).encode())
                all_connections[ind].close()
                return JsonResponse({'reply': 'Connection is closed', 'msge': True})
            else:
                all_connections[ind].send(str(qu).encode())
                mess = str(all_connections[ind].recv(1024), 'utf-8')
                response = dict()
                response['reply'] = mess.strip()
                return JsonResponse(response)
        else:
            return JsonResponse({'message': 'Invalid Data provided!!!'})
    return JsonResponse({'message': 'Invalid method!!!'})


def queryAll(request):
    global s, all_connections, all_address, data

    if request.method == 'POST':
        qu = request.POST.get('qy')
        if len(qu) > 0:
            if qu == 'list':
                return JsonResponse({'msge': True})
            elif qu == 'quit':
                for i in all_connections:
                    i.send(str(qu).encode())
                    try:
                        i.close()
                    except socket.error:
                        pass
                return JsonResponse({'reply': 'Connection is closed', 'msge': True})
            else:
                response = {}
                for j, i in enumerate(all_connections):
                    i.send(str(qu).encode())
                    mess = str(i.recv(1024), 'utf-8')
                    response[j+1] = mess.strip()
                return JsonResponse(response)
        else:
            return JsonResponse({'message': 'Invalid Data Provided!!!'})
    return JsonResponse({'message': 'Invalid method!!!'})
