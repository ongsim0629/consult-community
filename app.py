from flask import Flask,jsonify
from apps.concern import concern_bp
from apps.user import user_bp
from apps.rendering_test import rendering_bp


app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(concern_bp)
app.register_blueprint(rendering_bp)

# 더미 데이터 생성
def generate_worries():
    worries = []
    for i in range(1, 101):  # 100개의 고민 글 생성
        worries.append({
            "title": f"제목 {i}",
            "author": f"작성자 {i}",
            "content": f"내용 {i}.",
            "views": 100 - i,  # 조회수를 임의로 할당
            "date": f"2023-01-{i:02d}"  # 날짜를 임의로 할당
        })
    return worries

# 고민 목록을 반환하는 API
@app.route('/api/worries')
def get_worries():
    worries = generate_worries()
    # 최신순 정렬
    worries_sorted_by_date = sorted(worries, key=lambda x: x['date'], reverse=True)
    return jsonify({"worries": worries, "worries_sorted_by_date": worries_sorted_by_date})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)