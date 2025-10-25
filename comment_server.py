from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

# 初始化Flask应用
app = Flask(__name__)
# 允许所有跨域请求（公网访问必备）
CORS(app, resources={r"/*": {"origins": "*"}})

# 评论数据存储文件（自动创建）
DATA_FILE = "messages.json"

def load_comments():
    """加载评论数据"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_comments(comments):
    """保存评论数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

# 获取所有评论（前端调用此接口）
@app.route("/comments", methods=["GET"])
def get_comments():
    return jsonify(load_comments())

# 提交新评论（前端调用此接口）
@app.route("/comments", methods=["POST"])
def add_comment():
    comments = load_comments()
    new_comment = {
        "id": len(comments) + 1,
        "content": request.json.get("content"),
        "time": datetime.now().isoformat(),
        "replies": []
    }
    comments.append(new_comment)
    save_comments(comments)
    return jsonify({"status": "success"})

# 回复评论（前端调用此接口）
@app.route("/comments/<int:comment_id>/replies", methods=["POST"])
def add_reply(comment_id):
    comments = load_comments()
    for comment in comments:
        if comment["id"] == comment_id:
            comment["replies"].append({
                "content": request.json.get("content"),
                "time": datetime.now().isoformat()
            })
            save_comments(comments)
            return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "评论不存在"}), 404

# 删除评论（前端调用此接口）
@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comments = load_comments()
    new_comments = [c for c in comments if c["id"] != comment_id]
    save_comments(new_comments)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    # 启动后端服务（公网可访问）
    app.run(host="0.0.0.0", port=5000, debug=False)