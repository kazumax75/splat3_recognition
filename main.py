import cv2
import splat_recognition as de

import random, string
import os
import collections

if __name__ == '__main__':
    writingFlag = False
    write_count = 0
    dir_name = ""

    wait = 0
    # cap = cv2.VideoCapture(0, cv2.CAP_MSMF);cap.set(cv2.CAP_PROP_FPS, 60);wait=1
    cap = cv2.VideoCapture(r'./assets/ready.avi')

    while cap.isOpened():
        # キャプチャボードから画像取得
        ret, frame  = cap.read()

        if ret:
            frame2 = frame.copy()
            
            de.マップ開いてるかチェックしギア読み上げ(frame)
            de.ゲーム開始画面かチェックしブキを分類(frame)
            de.ゲーム開始画面がチェックしイカアイコンを保存(frame)
            
            isPlaying = de.アイコン位置認識可能状態かどうか(frame)
            if isPlaying:
                de.アイコンの位置検出と取得(frame, frame2)
            
            de.プレイヤー状況を画面に表示する()
            # cv2.imshow("game", frame)
            cv2.imshow("game2", frame2)
        
            if writingFlag:
                fn = r"./capture/%s/%d.bmp" % (dir_name, write_count)
                cv2.imwrite(fn, frame)
                write_count += 1
        key = cv2.waitKey(wait) & 0xFF
        if key == ord('c'):
            pass
        elif key == ord('q'):
            #qキーで終了
            break
        elif key == 32:
            if writingFlag:
                print("録画停止。")
                writingFlag = False
                write_count = 0
                
            elif writingFlag == False and ret :
                print("録画開始！")
                writingFlag = True
                dir_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                os.makedirs('./capture/'+dir_name, exist_ok=True)
                

    # メモリを解放して終了
    cap.release()
    cv2.destroyAllWindows()