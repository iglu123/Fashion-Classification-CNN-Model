import imageio
import pymysql
from flask import Flask, request, render_template
#hihihihihihihi
from keras.models import load_model

import tensorflow
# --------------------------- Flask & PyMySQL
app = Flask(__name__)
db = pymysql.connect(host='deepocean.cdlurfzj5gl4.ap-northeast-2.rds.amazonaws.com',
                    port=3306,
                    user='kaist',
                    passwd='85698569',
                    db='fashion',
                    charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)


# index 페이지 라우팅
@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')


@app.route('/stylecls')
def predict():
    return render_template('index.html')


# 여자 이미지 업로드에 대한 예측값 반환
@app.route('/predictgirl', methods=['POST'])
def make_prediction():
    if request.method == 'POST':

        # 업로드 파일 처리 분기
        file = request.files['image']
        if not file:
            return render_template('index.html', label="No Files")

        # 이미지 픽셀 정보 읽기
        # 알파 채널 값 제거 후 1차원 Reshape

        img = imageio.v2.imread(file)

        x = tensorflow.keras.preprocessing.image.img_to_array(img)
        x.resize((128,128,3))
        x = x.reshape((1,) + x.shape)
        # img = img[:, :, :3]
        # img = img.reshape(1, -1)

        # 입력 받은 이미지 예측
        prediction = model_girl.predict(x).flatten()
        print(prediction)
   # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환

        labels= ['casual', 'chic', 'formal', 'girlish', 'sports', 'street']
        confidences = {labels[i]: float(prediction[i]) for i in range(6)}

        print(confidences)
        for i,num in enumerate(prediction):
            if num==prediction.max():
                fashion = labels[i]
                styleresult= labels[i]
                print(fashion)


        # db에서 예측결과인 스타일 이미지 가져오기
        sql = "select * from girl_table where style=%s"
        cursor.execute(sql, fashion)
        rows = cursor.fetchmany(64)

        # for row in rows:
        #    print(row['url'])
        # db.close()


        # 결과 리턴
        return render_template('predictgirl.html', label=styleresult, imagerows=rows)
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 남자 이미지 업로드에 대한 예측값 반환
@app.route('/predictboy', methods=['POST'])
def mmake_prediction():
        if request.method == 'POST':

            # 업로드 파일 처리 분기
            file = request.files['image']
            if not file:
                return render_template('index.html', label="No Files")

            # 이미지 픽셀 정보 읽기
            # 알파 채널 값 제거 후 1차원 Reshape

            img = imageio.v2.imread(file)

            x = tensorflow.keras.preprocessing.image.img_to_array(img)
            x.resize((128, 128, 3))
            x = x.reshape((1,) + x.shape)
            # img = img[:, :, :3]
            # img = img.reshape(1, -1)

            # 입력 받은 이미지 예측
            prediction = model_boy.predict(x).flatten()
            print(prediction)
            # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환

            labels = ['americancasual', 'casual', 'formal', 'street']
            confidences = {labels[i]: float(prediction[i]) for i in range(4)}

            print(confidences)
            for i, num in enumerate(prediction):
                if num == prediction.max():
                    mfashion = labels[i]
                    mstyleresult = labels[i]
                    print(mfashion)

            # db에서 예측결과인 스타일 이미지 가져오기
            sql = "select * from boy_table where style=%s"
            cursor.execute(sql, mfashion)
            rows = cursor.fetchmany(64)

            # for row in rows:
            #    print(row['url'])
            # db.close()

            # 결과 리턴
            return render_template('predictboy.html', label=mstyleresult, imagerows=rows)



# 미리 학습시켜서 만들어둔 모델 로드
if __name__ == '__main__':
    model_boy = load_model('./my_model2.h5')
    model_girl = load_model('./my_model2.h5')
    app.run  (port=5000, debug=True)

