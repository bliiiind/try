from flask import Flask, request, json
from flask import Response
from flask import stream_with_context
from io import StringIO
import csv


#	测试数据
data = [
        ['Title','Jan','Feb'],
		['element1','1','1'],
		['element2','8','8'],
		['element3','30','30']
	]

app = Flask(__name__)


@app.route('/json', methods=['POST'])
def sendjson():
    data = json.loads(request.get_data())
    print('connect')
    return 'ok'

@app.route('/api/uwbget', methods=['POST'])
def add():
    x = request.json['a']
    y = request.json['b']
    return "ok"

@app.route('/api/uwblocate', methods=['GET'])
def exportEmails():
	#	定义一个生成器 (generate)，逐行生成，实现流式传输
    def generate():
    	#	用 StringIO 在内存中写，不会生成实际文件
        io = StringIO()	#在 io 中写 csv
        w = csv.writer(io)
        for i in data:      #对于 data 中的每一条
            w.writerow(i)   #传入的是一个数组 ['xxx','xxx@xxx.xxx'] csv.writer 会把它处理成逗号分隔的一行
            				#需要注意的是传入仅一个字符串 '' 时，会被逐字符分割，所以要写成 ['xxx'] 的形式
            yield io.getvalue()		#返回写入的值
            io.seek(0)		#io流的指针回到起点
            io.truncate(0)	#删去指针之后的部分，即清空所有写入的内容，准备下一行的写入
    #	用 generate() 构造返回值
    response = Response(stream_with_context(generate()), mimetype='text/csv')
    #	设置Headers: Content-Disposition: attachment 表示默认会直接下载。 指定 filename。
    response.headers.set("Content-Disposition","attachment",filename="uwblocate.csv")
    #	将 response 返回
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)