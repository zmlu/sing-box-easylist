import json
import os
import re

import requests
import bs4


def is_valid_cidr(cidr):
    # CIDR的正则表达式
    cidr_pattern = re.compile(
        r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(3[0-2]|[12]?[0-9])$')
    return cidr_pattern.match(cidr) is not None


def get_clash_rules():
    resp = requests.get("https://ruleset.skk.moe/")
    soup = bs4.BeautifulSoup(resp.text, features="html.parser")
    aDoms = soup.select("body > main > ul > li > ul > li > ul > li > a[href^='Clash']")
    rtn = []
    for aDom in aDoms:
        href = aDom.attrs['href']
        file_name = aDom.text
        if href.startswith("Clash"):
            full_href = "https://ruleset.skk.moe/" + href
            rtn.append({
                "full_href": full_href,
                "file_name": file_name.replace(".txt", ".json"),
                "output_file_subpath": href.replace("Clash/", "/sing-box/").replace(file_name, ""),
                "is_domainset": "/domainset/" in href
            })
    return rtn


def gen_sing_box_file(file_name: str, output_file_subpath: str, content: str, is_domainset: bool):
    path = os.getcwd()
    print("generating " + path + output_file_subpath + file_name)

    dict = {"version": 1}
    domain_list = []
    domain_suffix_list = []
    domain_keyword_list = []
    ipcidr_list = []
    process_name_list = []
    port_list = []
    if is_domainset:
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            domain_list.append(line)
    else:
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("#") or line.endswith(".ruleset.skk.moe"):
                continue
            if line.endswith(",no-resolve"):
                line = line.replace(",no-resolve", "")

            if line.startswith("DOMAIN,"):
                item = line.replace("DOMAIN,", "")
                domain_list.append(item)
                pass
            elif line.startswith("DOMAIN-SUFFIX,"):
                item = line.replace("DOMAIN-SUFFIX,", "")
                domain_suffix_list.append(item)
                pass
            elif line.startswith("DOMAIN-KEYWORD,"):
                item = line.replace("DOMAIN-KEYWORD,", "")
                domain_keyword_list.append(item)
                pass
            elif line.startswith("IP-CIDR,"):
                item = line.replace("IP-CIDR,", "")
                ipcidr_list.append(item)
                pass
            elif line.startswith("IP-CIDR6,"):
                item = line.replace("IP-CIDR6,", "")
                ipcidr_list.append(item)
                pass
            elif line.startswith("PROCESS-NAME,"):
                item = line.replace("PROCESS-NAME,", "")
                process_name_list.append(item)
                pass
            elif line.startswith("DST-PORT,"):
                item = line.replace("DST-PORT,", "")
                port_list.append(item)
                pass
            elif is_valid_cidr(line):
                ipcidr_list.append(line)
            else:
                print(line)
    rules = []
    rule_domain = {"domain": domain_list}
    rule_domain_suffix = {"domain_suffix": domain_suffix_list}
    rule_domain_keyword = {"domain_keyword": domain_keyword_list}
    rule_ipcidr = {"ip_cidr": ipcidr_list}
    rule_process_name = {"process_name": process_name_list}
    rule_port = {"port": port_list}
    if domain_list:
        rules.append(rule_domain)
    if domain_suffix_list:
        rules.append(rule_domain_suffix)
    if domain_keyword_list:
        rules.append(rule_domain_keyword)
    if ipcidr_list:
        rules.append(rule_ipcidr)
    if process_name_list:
        rules.append(rule_process_name)
    if port_list:
        rules.append(rule_port)
    dict["rules"] = rules

    path_without_filename = path + output_file_subpath
    if not os.path.exists(path_without_filename):
        os.makedirs(path_without_filename)
    with open(path_without_filename + file_name, 'w') as write_f:
        write_f.write(json.dumps(dict, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    clash_rules = get_clash_rules()
    for rule in clash_rules:
        full_href = str(rule["full_href"])
        file_name = str(rule["file_name"])
        output_file_subpath = str(rule["output_file_subpath"])
        is_domainset = bool(rule["is_domainset"])
        resp = requests.get(full_href)
        content = resp.text
        gen_sing_box_file(file_name, output_file_subpath, content, is_domainset)
