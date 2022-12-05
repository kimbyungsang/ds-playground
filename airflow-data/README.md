# Airflow개발 환경 시나리오
개발 시나리오는 먼저 로컬 개발 환경에서 IDE 를 통하여 task 단위 개발하고 로컬 검증 환경을 통하여 dags 검증후 운영환경으로 배포한다.
* 로컬 개발 환경: 로컬 파이썬 가상 환경을 기준으로 한다.
  * https://opensource.com/article/19/5/python-3-default-mac
  * https://docs.python.org/ko/3/library/venv.html
```
python -m venv ~/venv/airflow
source ~/venv/airflow/bin/activate
```

* 로컬 검증 환경: 로컬 도커 환경에서 진행한다.
  * (ubuntu) https://docs.docker.com/engine/install/ubuntu/
  * (non-root) https://docs.docker.com/engine/install/linux-postinstall/
* 운영 배포 환경: cloud build 를 통한 자동 배포한다. (TBD)

##로컬 개발 환경(using python venv)
* 코드 개발은 Pycharm 혹은 VSCode 로 가능하다.
* 컴포저 개발 환경 기준으로 파이썬 가상 환경 생성한다 (composer-1.18.7-airflow-2.2.3, python-3.8)

###설치
* https://airflow.apache.org/docs/apache-airflow/2.2.3/start/local.html 참고
```bash
## 내부적으로 AIRLOW_HOME 중요하니 반드시 export 확인

export AIRFLOW_HOME=~/github/python/airflow-data
# 가상환경이랑 AIRFLOW_HOME 은 script 로 저장해놓고 써도 좋다 (venv.sh 참조)

# 아래를 실행 시켜서 파이썬버전에 맞는 airflow 를 설치한다.
AIRFLOW_VERSION=2.2.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# 로컬에서 airflow 실행시킨다. 기본 DB 가 sqlite3 이며 사용자 계정 admin 의 비밀번호를 포함한 파일이 하나 생성된다.
airflow standalone
```

###테스트
위와 같이 설치하면 airflow 화면에 접근하여 dag 실행하는것이 가능하다. 개발을 할때 task 마다의 개발테스트는 아래와 같이 진행한다.
```
# example_bash_operator Dag 의 runme_0 Task 가 정상 동작하는지 확인하는 테스트
airflow tasks test example_bash_operator runme_0 2015-01-01
```

###선택사항
sqlite3 를 db 로 사용할경우 sequentialExecutor 밖에 사용할수 없다. 필요하면 아래처럼 postgres 를 사용하면 LocalExecutor 로 실행하는것이 가능하다.
```bash

# Optional #############
# 로컬 개발 환경시 pgsql 을 사용하고자 하면 아래와 같이 database 및 권한 추가한다,
# install pgsql library
 pip install psycopg2-binary

# sqlite 대시 postgresql 사용 (postgresql db 준비되어있어야 함)
CREATE DATABASE airflow_local;
CREATE USER airflow WITH PASSWORD 'airflow';
GRANT ALL PRIVILEGES ON DATABASE airflow_local TO airflow_user;

# in airflow.cfg 에서 아래 부분을 수정한후 airflow init db 재수행
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost/airflow_local
#########################


# Optional #########################
# 로컬에서 airflow 웹서버/스케줄러 설치해서 진행할수도 있으나 장단점이 있다.
# (장점) 별도로 도커 환경 관리할 필요 없다. 필요한 라이브러리 설치 및 바로 dag 검증 가능하다.
airflow webserver --port 8080 &
airflow scheduler &
# (단점) 위의 프로세스를 재시작 하려면 프로세스를 찾아서 kill -9 해야 한다. (하위 프로세스까지 다 kill 해야 하는 번거로움)
# (단점) airflow DB 로 sqlite 사용할경우 sequentialExecutor 만 사용 가능하다.
####################################
```

###개발
* dag: 파이프라인 개발
* data: 관련 데이터 저장
* plugins: 파이썬 클래스, 라이브러리, Custom Operator 개발

###태스크 단위 테스트
```angular2html
# airflow tasks test $DAG_ID $TASK_ID $execution_date
airflow tasks test sc_bash_operator run_this 2021-11-04# Airflow개발 환경 시나리오
개발 시나리오는 먼저 로컬 개발 환경에서 IDE 를 통하여 task 단위 개발하고 로컬 검증 환경을 통하여 dags 검증후 운영환경으로 배포한다.
* 로컬 개발 환경: 로컬 파이썬 가상 환경을 기준으로 한다.
  * https://opensource.com/article/19/5/python-3-default-mac
  * https://docs.python.org/ko/3/library/venv.html
```
python -m venv ~/venv/airflow
source ~/venv/airflow/bin/activate
```

* 로컬 검증 환경: 로컬 도커 환경에서 진행한다.
  * (ubuntu) https://docs.docker.com/engine/install/ubuntu/
  * (non-root) https://docs.docker.com/engine/install/linux-postinstall/
* 운영 배포 환경: cloud build 를 통한 자동 배포한다. (TBD)

##로컬 개발 환경(using python venv)
* 코드 개발은 Pycharm 혹은 VSCode 로 가능하다.
* 컴포저 개발 환경 기준으로 파이썬 가상 환경 생성한다 (composer-1.18.7-airflow-2.2.3, python-3.8)

###설치
* https://airflow.apache.org/docs/apache-airflow/2.2.3/start/local.html 참고
```bash
## 내부적으로 AIRLOW_HOME 중요하니 반드시 export 확인

export AIRFLOW_HOME=~/github/python/airflow-data
# 가상환경이랑 AIRFLOW_HOME 은 script 로 저장해놓고 써도 좋다 (venv.sh 참조)

# 아래를 실행 시켜서 파이썬버전에 맞는 airflow 를 설치한다.
AIRFLOW_VERSION=2.2.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# 로컬에서 airflow 실행시킨다. 기본 DB 가 sqlite3 이며 사용자 계정 admin 의 비밀번호를 포함한 파일이 하나 생성된다.
airflow standalone
```

###테스트
위와 같이 설치하면 airflow 화면에 접근하여 dag 실행하는것이 가능하다. 개발을 할때 task 마다의 개발테스트는 아래와 같이 진행한다.
```
# example_bash_operator Dag 의 runme_0 Task 가 정상 동작하는지 확인하는 테스트
airflow tasks test example_bash_operator runme_0 2015-01-01
```

###선택사항
sqlite3 를 db 로 사용할경우 sequentialExecutor 밖에 사용할수 없다. 필요하면 아래처럼 postres 를 사용하면 LocalExecutor 로 실행하는것이 가능하다.
```bash

# Optional #############
# 로컬 개발 환경시 pgsql 을 사용하고자 하면 아래와 같이 database 및 권한 추가한다,
# install pgsql library
 pip install psycopg2-binary

# sqlite 대시 postgresql 사용 (postgresql db 준비되어있어야 함)
CREATE DATABASE airflow_local;
CREATE USER airflow WITH PASSWORD 'airflow';
GRANT ALL PRIVILEGES ON DATABASE airflow_local TO airflow_user;

# in airflow.cfg 에서 아래 부분을 수정한후 airflow init db 재수행
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost/airflow_local
#########################


# Optional #########################
# 로컬에서 airflow 웹서버/스케줄러 설치해서 진행할수도 있으나 장단점이 있다.
# (장점) 별도로 도커 환경 관리할 필요 없다. 필요한 라이브러리 설치 및 바로 dag 검증 가능하다.
airflow webserver --port 8080 &
airflow scheduler &
# (단점) 위의 프로세스를 재시작 하려면 프로세스를 찾아서 kill -9 해야 한다. (하위 프로세스까지 다 kill 해야 하는 번거로움)
# (단점) airflow DB 로 sqlite 사용할경우 sequentialExecutor 만 사용 가능하다.
####################################
```

###개발
* dag: 파이프라인 개발
* data: 관련 데이터 저장
* plugins: 파이썬 클래스, 라이브러리, Custom Operator 개발

###태스크 단위 테스트
```angular2html
# airflow tasks test $DAG_ID $TASK_ID $execution_date
airflow tasks test sc_bash_operator run_this 2021-11-04