import cv2
import splat_recognition as de

if __name__ == '__main__':

    wait = 0
    # cap = cv2.VideoCapture(0, cv2.CAP_MSMF);cap.set(cv2.CAP_PROP_FPS, 60);wait=1
    cap = cv2.VideoCapture(r"C:\Users\morea\Desktop\Python\splat_public\assets\ready.avi")

    while cap.isOpened():
        # キャプチャボードから画像取得
        ret, frame  = cap.read()

        if ret:
            de.ゲーム開始画面がチェックしイカアイコンを保存(frame, "./icons")
            
        key = cv2.waitKey(wait) & 0xFF
        if key == ord('c'):
            pass
        elif key == ord('q'):
            #qキーで終了
            break
                

    # メモリを解放して終了
    cap.release()
    cv2.destroyAllWindows()