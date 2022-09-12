import PIL.Image
import imageio
import pymysql
from flask import Flask, request, render_template
#hi
from keras.models import load_model
import numpy as np
from PIL import Image
import tensorflow
import zzz
import os
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
    return render_template('sub1.html')


# 여자 이미지 업로드에 대한 예측값 반환
@app.route('/predictgirl', methods=['POST'])
def make_prediction():
    if request.method == 'POST':

        # 업로드 파일 처리 분기
        file = request.files['image']
        if not file:
            return render_template('sub1.html', label="No Files")

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
        # print(prediction)
   # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환

        labels= ['casual', 'chic', 'formal', 'girlish', 'street']
        confidences = {labels[i]: float(prediction[i]) for i in range(5)}

        print(confidences)
        for i,num in enumerate(prediction):
            if num==prediction.max():
                fashion = labels[i]
                styleresult= labels[i]
                print(fashion)

        path = "C:/Users/sm/Desktop/image/removed/" + fashion
        target_img = zzz.resizeImg(file)
        dists = zzz.giveWholeCosDist(fashion, target_img, path)
        idxs = zzz.returnArgsort(dists)

        cnt = 1
        rows = []
        for idx in idxs[:16]:
            idx = int(idx)
            img_name = os.listdir(path)[idx]
            # print(f"{cnt}번째로 가까운 이미지의 이름: {img_name}")
            # print(f"target 이미지와의 거리: {dists[idx]}")
            # print("================")
            cnt += 1

            infos = ["dates", "user", "location", "clicks"]
            img_name = img_name.split("`")
            for_sql_dict = dict(zip(infos, img_name))

            # db에서 예측결과인 스타일 이미지 가져오기
            sql = "select * from girl_table where style=%s and dates=%s and user=%s and location=%s"
            cursor.execute(sql, [fashion, for_sql_dict['dates'], for_sql_dict['user'], for_sql_dict['location']])
            # print(cursor.fetchmany(1)[0])
            rows.append(cursor.fetchmany(1)[0])



        # db에서 예측결과인 스타일 이미지 가져오기
        # sql = "select * from girl_table where style=%s"
        # cursor.execute(sql, fashion)
        # rows = cursor.fetchmany(64)

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
                return render_template('sub1.html', label="No Files")

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
            # print(prediction)
            # 예측 값을 1차원 배열로부터 확인 가능한 문자열로 변환

            labels = ['americancasual', 'casual', 'dandy', 'formal', 'street']
            confidences = {labels[i]: float(prediction[i]) for i in range(5)}

            print(confidences)
            for i, num in enumerate(prediction):
                if num == prediction.max():
                    mfashion = labels[i]
                    mstyleresult = labels[i]
                    print(mfashion)

            path = "C:/Users/sm/Desktop/image/boy_removed/" + mfashion
            target_img = zzz.resizeImg(file)
            dists = zzz.giveWholeCosDist(mfashion, target_img, path)
            idxs = zzz.returnArgsort(dists)

            cnt = 1
            rows = []
            for idx in idxs[:16]:
                idx = int(idx)
                img_name = os.listdir(path)[idx]
                # print(f"{cnt}번째로 가까운 이미지의 이름: {img_name}")
                # print(f"target 이미지와의 거리: {dists[idx]}")
                # print("================")
                cnt += 1

                infos = ["dates", "user", "location", "clicks"]
                img_name = img_name.split("`")
                for_sql_dict = dict(zip(infos, img_name))

                # db에서 예측결과인 스타일 이미지 가져오기
                sql = "select * from b_df_withDandy where style=%s and dates=%s and user=%s and location=%s"
                cursor.execute(sql, [mfashion, for_sql_dict['dates'], for_sql_dict['user'], for_sql_dict['location']])
                rows.append((cursor.fetchmany(1))[0])


            # for row in rows:
            #    print(row['url'])
            # db.close()

            # 결과 리턴
            return render_template('predictboy.html', label=mstyleresult, imagerows=rows)



# 미리 학습시켜서 만들어둔 모델 로드
if __name__ == '__main__':
    model_boy = load_model('./my_model2.h5')
    model_girl = load_model('./my_model2.h5')
    app.run  (host='0.0.0.0', port=8080, debug=True)