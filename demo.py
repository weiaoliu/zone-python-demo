import json
import requests

from flask import Flask, request, jsonify


app = Flask(__name__)


class Main:
    def __init__(self) -> None:
        self.base_url = "https://0.zone/"
        self.data_url = self.base_url + "api/plug/data/"  # 数据url
        self.aggs_url = self.base_url + "api/plug/aggs/"  # 聚合数据url

    def getData(self, data: dict, request_type: int=0) -> dict:
        if request_type:
            request_url = self.data_url
        else:
            request_url = self.aggs_url

        try:
            response = requests.post(url=request_url, json=data, timeout=10)
        except Exception as e:
            raise e
        
        return json.loads(response.text)


@app.route("/data", methods=["POST"])
def data():
    data = request.json
    request_data = dict(
        title=data.get("title", ""), # 搜索条件
        title_type=data.get("title_type", ""), # 搜索类型 目前只支持site(信息系统), domain(域名)
        company=data.get("company", ""), # 认证公司
        page=data.get("page", 1), # 页数
        pagesize=data.get("pagesize", 10), # 页大小
        key="" # 0.zone key
    )
    try:
        data = Main().getData(request_data, request_type=1)      
    except:
        return jsonify(dict(code=1, message="获取数据失败"))

    return jsonify(data)

@app.route("/aggs", methods=["POST"])
def aggs():
    data = request.json
    request_data = dict(
        title=data.get("title", ""),
        title_type=data.get("title_type", ""),
        company=data.get("company", ""),
        key=""
    )
    try:
        data = Main().getData(request_data)
    except:
        return jsonify(dict(code=1, message="获取聚合数据失败"))
    
    return jsonify(data)


if __name__ == "__main__":
    app.run()
