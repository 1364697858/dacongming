from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

# 初始化Flask应用
app = Flask(__name__)
# 允许所有跨域请求
CORS(app, resources={r"/*": {"origins": "*"}})

# 访问数据存储文件
VISIT_FILE = "visit_count.json"
INITIAL_COUNT = 3000  # 初始访问次数

def get_visit_count():
    """获取当前访问次数"""
    if not os.path.exists(VISIT_FILE):
        # 首次运行，创建文件并设置初始值
        with open(VISIT_FILE, "w", encoding="utf-8") as f:
            json.dump({"count": INITIAL_COUNT}, f)
        return INITIAL_COUNT
    
    with open(VISIT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("count", INITIAL_COUNT)

def update_visit_count():
    """更新访问次数（+1）"""
    count = get_visit_count()
    count += 1
    with open(VISIT_FILE, "w", encoding="utf-8") as f:
        json.dump({"count": count}, f)
    return count

# 访问统计接口
@app.route("/visits", methods=["GET"])
def visits():
    count = update_visit_count()  # 每次访问都增加计数
    return jsonify({"count": count})

if __name__ == "__main__":
    # 启动服务，端口5001避免与评论服务冲突
    app.run(host="0.0.0.0", port=5001, debug=False)