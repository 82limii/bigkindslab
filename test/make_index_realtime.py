import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from newsml_to_json import make_json
from elasticsearch import Elasticsearch
from custom_log import Logger
from insert_log import success_log, error_log
from datetime import datetime as dt
import traceback

es = Elasticsearch('http://localhost:9199')

mapping = {
    "settings" : {
        "number_of_shards": 6,
        "number_of_replicas": 1
    }
}

logger = Logger()

realtime_logger = logger.initLogger()

class Target:

    def __init__(self, path):
        #watchDir에 감시하려는 디렉토리를 명시한다.
        os.chdir(path)
        self.watchDir = os.getcwd()

        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        st_dtm = dt.now()
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
                    #json 변환
                    json_dict = make_json(event.src_path)
                    realtime_logger.info(json_dict)
                    # index명 생성
                    index = "kpf_bigkindslab_v1.1_" + Fname.split(".")[1][:4]
                    realtime_logger.info(index)

                    # index가 존재하는 지 확인
                    # index 없을 경우 index 생성 후 doc 추가
                    if es.indices.exists(index=index)==False:
                        es.indices.create(index=index, body=mapping)    # index 생성
                        realtime_logger.info('index create : '+index)

                    # index에 doc 추가
                    result = es.index(index=index, doc_type="_doc", body=json_dict, id='log_test')  # id는 Fname

                    end_dtm = dt.now()
                    success_log(Fname, 'A', index, st_dtm, end_dtm)
                    realtime_logger.info(result)

            except Exception as e: # 에러 처리
                error_log(Fname, st_dtm, 'err999', '실시간 등록 에러 log 확인 필요')
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