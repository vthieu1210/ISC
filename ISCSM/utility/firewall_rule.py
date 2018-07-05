from ISCSM.models import FirewallRule
from datetime import datetime

def importFirewallRuleDB(data):
    for rule in data['Sheet1']:
        length = len(rule)
        if length == 4:
            FirewallRule.objects.create(src_ip=rule[1], dest_ip=rule[2], port=rule[3])
        if length == 5:
            FirewallRule.objects.create(src_ip=rule[1], dest_ip=rule[2], port=rule[3], description=rule[4])
        if length == 6:
            FirewallRule.objects.create(src_ip=rule[1], dest_ip=rule[2], port=rule[3], description=rule[4], datecreate=rule[5])
def delFirewallRule(id):
    FirewallRule.objects.filter(id=id).delete()

def editFirewallRule(id, rule):
    FirewallRule.objects.filter(id=id).update(src_ip=rule['src_ip'],dest_ip=rule['dest_ip'],port=rule['port'],description=rule['description'],datecreate=rule['datecreate'])

def searchFirwallRule(listrule, src_ip, dest_ip, port, description, search_by_date_type, is_datecreate, between_datecreate_from, between_datecreate_to):
    if src_ip:
        listrule = [rules for rules in listrule if src_ip in rules.src_ip]
    if dest_ip:
        listrule = [rules for rules in listrule if dest_ip in rules.dest_ip]
    if port:
        listrule = [rules for rules in listrule if port in rules.port]
    if description:
        listrule = [rules for rules in listrule if description in rules.description.lower()]
    if search_by_date_type == "is" and is_datecreate:
        tmp = datetime.strptime(is_datecreate, '%Y-%m-%d')
        listrule = [rules for rules in listrule if tmp.date() == rules.datecreate]
    if search_by_date_type == "between":
        if between_datecreate_from and between_datecreate_to:
            from_date = datetime.strptime(between_datecreate_from, '%Y-%m-%d')
            to_date = datetime.strptime(between_datecreate_to, '%Y-%m-%d')
            listrule = [rules for rules in listrule if rules.datecreate]
            listrule = [rules for rules in listrule if rules.datecreate >= from_date.date()]
            listrule = [rules for rules in listrule if rules.datecreate <= to_date.date()]
        elif between_datecreate_from or between_datecreate_to:
            if between_datecreate_from:
                between_datecreate_to = between_datecreate_from
            if between_datecreate_to:
                between_datecreate_from = between_datecreate_to
            from_date = datetime.strptime(between_datecreate_from, '%Y-%m-%d')
            to_date = datetime.strptime(between_datecreate_to, '%Y-%m-%d')
            listrule = [rules for rules in listrule if rules.datecreate]
            listrule = [rules for rules in listrule if rules.datecreate >= from_date.date()]
            listrule = [rules for rules in listrule if rules.datecreate <= to_date.date()]
    return listrule
