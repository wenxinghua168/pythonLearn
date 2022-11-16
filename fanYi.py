import json
import urllib.request as ur
import urllib.parse as up
import ssl

class fanYi:

	# 正确链接将链接中的  translate 后面  _o  去掉。
	url = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
	word = 'おはようございます'
	ssl._create_default_https_context = ssl._create_unverified_context
	# data数据传入的Form Data表单数据可以是其中的全部，其实有用的就以下两个。
	data = {
		'i': word,
		'from': 'zh-CH',
		'to': 'ja',
		'doctype': 'json'
	}
	data_url = up.urlencode(data).encode('utf-8')
	request = ur.Request(url=url,data=data_url)
	response = ur.urlopen(request).read()
	ret = json.loads(response)
	translate = ret['translateResult'][0][0]['tgt']
	print('翻译结果为：%s'%translate)
