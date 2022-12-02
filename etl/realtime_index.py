import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime as dt
import traceback
from custom_log import Logger
from es_module import insert_doc
from db_log_module import ins_suc_log, err_log

logger = Logger()

realtime_logger = logger.initLogger()

class Target:

    def __init__(self, path):
        #watchDir에 감시하려는 디렉토리를 명시한다.
        os.chdir(path)
        self.watchDir = os.getcwd()

        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        # schedule 실행
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except Exception as e:
            self.observer.stop()
            realtime_logger.info("Error")
            trace_back = traceback.format_exc()
            message = str(e)+ "\n" + str(trace_back)
            realtime_logger.error('[FAIL] %s', message)
            self.observer.join()

class Handler(FileSystemEventHandler):
#FileSystemEventHandler 클래스를 상속받음.
#아래 핸들러들을 오버라이드 함

    #파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        realtime_logger.info('move')
        realtime_logger.info(event)

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        st_dtm = dt.now()   # 시작 일시
        realtime_logger.info('create')

        if event.is_directory : # 디렉토리가 생성될 경우
            realtime_logger.info('----------------- directory 추가 -----------------')
            realtime_logger.info(event.src_path)

        else : # 파일이 생성될 경우
            try:
                realtime_logger.info('----------------- file 추가 -----------------')
                Fname, Extension = os.path.splitext(os.path.basename(event.src_path))
                realtime_logger.info(Fname)

                if Extension == '.xml': #파일의 확장자가 xml일 경우
                    # es에 xml 데이터 등록
                    news_id, index = insert_doc(event.src_path)
                    end_dtm = dt.now()
                    ins_suc_log(Fname, '0', index, st_dtm, end_dtm)
                    realtime_logger.info(index + ' : ' + id + ' : end_dtm')

            except Exception as e: # 에러 처리
                err_log(Fname, st_dtm, 'err999', '실시간 등록 에러 log 확인 필요')
                trace_back = traceback.format_exc()
                message = str(e)+ "\n" + str(trace_back)
                realtime_logger.error('[FAIL] %s', message)


    def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
        realtime_logger.info('delete')
        realtime_logger.info(event)

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        realtime_logger.info('modified')
        realtime_logger.info(event.src_path)

if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
    # 실제 디렉토리 경로
    # w = Target('/hadoop/newsml/data')
    w = Target('../data')
    w.run()