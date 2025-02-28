import requests
from init.PrintEntity import PrintEntity
import ssl
import socket
from urllib.parse import urlparse



headers = {'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
}
#屏蔽SSl警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HeaderVlun:
    printEntity=PrintEntity(2)#设置2级显示块
    def __init__(self):
        pass
    def getHeaders(self,url):

        try:
            res = requests.get(url, verify=False, timeout=3, stream=True, headers=headers, )

            return res.headers
        except Exception as e:
            print(url+"错误"+str(e))
            return None
        pass
    def getHeadersVuln(self,headers):
        '探测响应头缺失以及信息泄露'
        result=[]
        #响应头缺失类
        vulnheaders={
            'X-Frame-Options':'.*',
            'Content-Security-Policy':'.*',
            'Set-Cookie':'.*',
            'Strict-Transport-Security':'.*',
        }

        for vulnheader in vulnheaders.keys():
            if vulnheader in headers:
                # print()
                self.printEntity.showInfo("[*] "+vulnheader+" : "+headers[vulnheader])
                if vulnheader == 'Set-Cookie':
                    values=['Httponly','Secure']
                    for i in values:
                        if str.lower(i) not in str.lower(headers[vulnheader]):
                            # print("[+] Find vuln:"+i+"头缺失")
                            self.printEntity.showVulnInfo("[+] (响应头缺失类)\tFind vuln: "+i+"头缺失")

                            result.append("(响应头缺失类) "+i+"头缺失")
                        else:
                            # print()
                            self.printEntity.showInfo("[*] Cookie "+i+"丢失不存在")
                else:
                    pass
                    # print("来了",headers[vulnheader],'Set-Cookie',headers[vulnheader] is 'Set-Cookie')

            elif vulnheader!='Set-Cookie':
                # print("[+] Find vuln:"+vulnheader+"头缺失")
                self.printEntity.showVulnInfo("[+] (响应头缺失类)\tFind vuln: "+vulnheader+"头缺失")
                result.append("(响应头缺失类) "+vulnheader+"头缺失")

        #信息泄露类
        #key响应头键，值正则表达式
        vulnheaders2={'Server':'.',
                     'X-Powered-By':'.',
                      'Access-Control-Allow Origin':'*'
                     }
        for vulnheader2 in vulnheaders2.keys():
            if vulnheader2  in headers: #寻找头是否存在于headers中
                import re
                isvuln=re.match(vulnheaders2.get(vulnheader2),headers[vulnheader2],re.I)
                if isvuln:
                    # print("[+] Find vuln:"+vulnheader2+":",headers[vulnheader2])
                    self.printEntity.showVulnInfo("[+] (信息泄露类)\tFind vuln: "+vulnheader2+" : "+headers[vulnheader2])
                    result.append("(信息泄露类)\t"+vulnheader2+" : "+headers[vulnheader2])
                else:
                    # print("[*] ------------>"+vulnheader2,headers[vulnheader2])
                    pass
            else:
                # print()
                self.printEntity.showInfo("[*] "+vulnheader2+"信息泄露不存在")
        return result
    def getOptionsVlun(self,url):
        result=[]
        try:
            res=requests.options(url, verify=False, timeout=3, stream=True, headers=headers, )
            if 'Allow' in res.headers:
                self.printEntity.showUnvipInfo2('[*] 支持方法'+res.headers['Allow'])
                # methods=res.headers['Allow'].split(',')
            res=requests.request('trace',url, verify=False, timeout=3, stream=True, headers=headers, )
            if res.status_code==200:
                self.printEntity.showVulnInfo('[+] TRACE 方法启用')
                result.append("(不安全的HTTP方法) TRACE 方法启用")
                for key,value in res.headers.items():
                    self.printEntity.showUnvipInfo2(" "+key+" : "+value)
                #self.printEntity.showUnvipInfo2(res.text)
                print("- "*20)
            else:
                self.printEntity.showInfo("[*] TRACE 方法无效"+str(res.status_code))


        except Exception as e:
            # print()
            # self.printEntity.showUnvipInfo2(url+"错误"+str(e))
            self.printEntity.showUnvipInfo2(url+"错误"+e.__class__.__name__)
        return result
    def getErrorInfoVuln(self,url):
        result=[]
        try:
            import re
            tmp=re.match("http[s]?://[\w\.\-\d:]+[\d]{0,5}",url)  #只取主机端口部分
            url=tmp.group()
            if url[-1:]=="/":                                           #去掉主机末尾的/
                url=url[0:-1]
            url=url+"/esssdad"
            res=requests.get(url, verify=False, timeout=3, stream=True, headers=headers, )
            if res.status_code==404 or res.status_code==500 or res.status_code==403:
                paths=(re.findall(r"[cdexf]:\\[\w]+\\[\w]+[\\\w\.]+",res.text,re.I))
                paths=tuple(set(paths))#去重
                for path in paths:
                    self.printEntity.showVulnInfo("[+] 绝对路径泄露 "+url+'\t'+path)
                    # self.printEntity.showVulnInfo("\t"+path)
                    result.append("(绝对路径泄露) "+url+" "+path)
                #Apache版本泄露
                paths2=(re.findall("Apache Tomcat/[\d\.]+",res.text,re.I))
                paths2=tuple(set(paths2))
                for path in paths2:
                    self.printEntity.showVulnInfo("[+] Apache版本泄露 "+url+'\t'+path)
                    # self.printEntity.showVulnInfo("\t"+path)
                    result.append("(Apache版本泄露) "+url+" "+path)
                #weblogic默认报错页面
                paths3=(re.findall("The server understood the",res.text,re.I))
                for path in paths3:
                    self.printEntity.showVulnInfo("[+] weblogic默认报错页面 "+url+'\t'+path)
                    # self.printEntity.showVulnInfo("\t"+path)
                    result.append("(weblogic默认报错页面) "+url+" "+path)
            else:
                self.printEntity.showInfo("[*] 报错信息无效"+str(res.status_code))
        except Exception as e:
            print(url+"错误"+e.__class__.__name__)

        return result
    def check_tls_version(self,url):
        # 解析URL，提取主机名
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = 443  # 默认HTTPS端口
        result = []
        if not hostname:
            print("Invalid URL")
            return

        # 定义支持的TLS版本
        tls_versions = {
            ssl.PROTOCOL_TLSv1: "TLSv1.0",
            ssl.PROTOCOL_TLSv1_1: "TLSv1.1",
            ssl.PROTOCOL_TLSv1_2: "TLSv1.2",
            ssl.PROTOCOL_TLS: "TLSv1.3",  # 在Python 3.7中，PROTOCOL_TLS通常指TLS 1.3
        }

        # 检测每个TLS版本
        vulnerable_versions = []
        for version, version_name in tls_versions.items():
            try:
                # 创建SSL上下文
                context = ssl.SSLContext(version)
                # 创建套接字并包装为SSL套接字
                sock = socket.create_connection((hostname, port))
                ssock = context.wrap_socket(sock, server_hostname=hostname)
                ssock.close()
                self.printEntity.showInfo(f"{version_name} is enabled.")
                if version_name in ["TLSv1.0", "TLSv1.1"]:
                    vulnerable_versions.append(version_name)
            except ssl.SSLError as e:
                self.printEntity.showInfo(f"{version_name} is not enabled: {e}")
            except Exception as e:
                self.printEntity.showInfo(f"An error occurred while checking {version_name}: {e}")

        # 判断是否存在漏洞版本
        if vulnerable_versions:
            self.printEntity.showVulnInfo("[+] (不安全的SSL版本)\tFind vuln: " + str(vulnerable_versions[0])+","+str(vulnerable_versions[1]))
            result.append("(不安全的SSL版本) " + str(vulnerable_versions[0])+", "+str(vulnerable_versions[1])+" Enabled")
        else:
            self.printEntity.showInfo("[*] SSL版本安全")

        return result
    def check_http_access(self,url):
        result = []
        # 将URL的协议替换为http
        http_url = url.replace('https://', 'http://')
        try:
            # 发送HTTP GET请求
            response = requests.get(http_url, timeout=5)
            # 判断响应状态码是否为200
            if response.status_code == 200:
                self.printEntity.showVulnInfo("[+] (允许使用HTTP访问)\tFind vuln: " + http_url)
                result.append("(未加密的链接) " + http_url)
            else:
                self.printEntity.showInfo("http access failed with status code: "+ str(response.status_code))
        except requests.exceptions.RequestException as e:
            self.printEntity.showInfo("failed with exception:" + str(e))
        return result