import requests
from django.conf import settings
import re
import json
import collections
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from datetime import timedelta, datetime
from machines.models import ClassifiedInterval, Equipment, Hour_interval


sort_order = {
    '40252 - FERRARI  A155-Е, цех 7': 0,
    '40251 - OKUMA MB-46VAE, цех 7': 1,
    '30428 - Sodic AQ 537 LQ 33W, цех 7': 2,
    '32615 - Верт.-фрез. 6М12П, цех 7': 3,
    '40619 - MAZAK VCS-530C, цех 20': 4
}


def prepare_data_for_google_charts_bar(data):
    charts_data = {}
    charts_data['details'] = {}
    for key in data.keys():
        chart = data[key]['auto_stats']
        chart2 = data[key]['user_stats']
        legend = ['Kind']
        graph_data = [key]
        user_data = [['user_reason', 'min']]
        # Need to sort
        for k in sorted(chart.keys()):
            legend += [k]
            graph_data += [chart[k]]
        for k in chart2.keys():
            user_data += [[k, chart2[k]]]
        legend += [{'role': 'annotation'}]
        graph_data += ['']
        if key == 'total':
            charts_data[key] = {'auto_data': [legend, graph_data], 'user_data': user_data}
        else:
            charts_data['details'][key] = {'auto_data': [legend, graph_data], 'user_data': user_data}

    details_sorted = dict(collections.OrderedDict(sorted(charts_data['details'].items(),
                                                    key=lambda k: sort_order.get(k[0], 400))))
    charts_data['details'] = details_sorted
    return charts_data


def get_ci_data_timeline():
    """
    :return: dict with classified intervals for last 24 hours, keys - equipment
    """
    def time_for_js(time):
        ltime = timezone.localtime(time)
        return datetime(ltime.year, ltime.month, ltime.day, ltime.hour, ltime.minute, 0)
    end = timezone.now()
    start = end - timedelta(days=1)
    graph_data = {}
    for eq in Equipment.objects.all():
        if eq.problem_machine==False:
            cis = ClassifiedInterval.objects.filter(end__gte=start, equipment=eq).order_by('start')
            data = [['-', ci.automated_classification.description if ci.user_classification==None else ci.user_classification.description , ci.automated_classification.code ,
                     max(ci.start, start), ci.end] for ci in cis]
            graph_data[eq.id] = data
        elif eq.problem_machine==True:
            cis = Hour_interval.objects.filter(ending__gte=start, equipment=eq).order_by('starting')
            data = [['-','Оборудование работает' if ci.work_check == True else 'Простой','000' if ci.work_check == True else '001',max(ci.starting,start),ci.ending] for ci in cis]
            graph_data[eq.id] = data
    return json.dumps(graph_data, cls=DjangoJSONEncoder)


def SendSMS(phone, pattern, message):
    """
    sends SMS to number 'phone'
    :param phone: string +7(912)3492849
    :param message:
    :return: Http code
    """
    # *************************************************
    """!!!Формирование текста СМС и номеров получателей!!!"""
    ph = re.sub(r'([-\s\+\(\)]*)', "", phone)
    assert (ph)[:2] == '79', 'phone should start with 79'
    try:
        ph = int(ph)
    except ValueError as e:
        raise ValueError("invalid phone number {0}".format(phone))
    assert isinstance(pattern, int) and pattern >= 0 and pattern < len(settings.SMS_PATTERNS), "invalid pattern"

    if re.search(r'\{\d\}', settings.SMS_PATTERNS[pattern]):
        msg = settings.SMS_PATTERNS[pattern].format(message)
    else:
        msg = settings.SMS_PATTERNS[pattern]

    sms = {
        "from": "PZMONITOR",
        "to": ph,
        "message": msg
    }

    # заголовок
    head = {
        "Authorization": "Basic %s" % settings.SMS_PASS_PHRASE
    }

    # отправка запроса
    r = requests.post(settings.SMS_API_URL, headers=head, json=sms)

    # статус и отчет о выполнении, не обязательно
    print(r.status_code)
    print(r.text)

    return r.status_code

