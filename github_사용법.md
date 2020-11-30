> github를 이용한 공동 작업을 어떤 식으로 진행하면 되는지 간단히 정리한 부분



> 기본적으로 같은 파일을 수정하지 않으면 충돌이 발생하는 일이 없기 때문에 수월하게 작동합니다. 이 외에 상황에 대한 서술입니다.



### 1. 상대가 작업한 내용을 merge해서 master에 변경이 있을 때

> 1. 내가 작업 중이지 않는 상황

```bash
# 여기서 주의해야할 점은 브런치(frontend)가 이미 만들어진 다음 pull을 하게되면 master와
# frontend가 파일 구조가 달라집니다!

# 먼저 서버에서 변경된 자료를 받아옵니다.
$ git pull origin master

# 그 다음 브런치를 만들어 줍니다.
# (master에서 파일을 다 받은 다음 만들어 주면 브런내에서도 파일 구조가 동일합니다.)
$ git branch frontend

# 해당 브런치로 이동 후 작업합니다!
$ git switch frontend
```

> 2. 내가 작업 중인 상황

```
굳이 중간에 pull을 받을 필요가 없습니다.
만약 중요한 변경으로 인해 필요할 때는 서로 커뮤니케이션을 통해 상황을 해결합니다.
작업을 완료한 후 내 브런치로 push를 하고 파일 변경사항 이력을 확인해서 merge request 실시
만약 문제 발생시 커뮤니케이션합니다.
```



### 2. 내가 작업한 다음 push할 때

> 전체적인 진행 코드입니다.

```bash
# 현재 bash창(terminal)을 확인했을 때 frontend인 시점에서 서술

# 필요한 파일 stage에 올리기
$ git add .
# 특정 파일을 올린 뒤 commit을 해서 commit 메세지를 세분화할 수 있습니다! -변경 많을 때
$ git add <특정파일 이름>

# commit 메세지 작성(자세히)
$ git commit -m "Modify base.html nav-bar"

# 해당 브런치 이름으로 push
$ git push origin frontend
```

> 여기부터는 서버에서 진행할 부분입니다.

```
1. repo에서 내 브런치로 들어간 다음 코드가 잘 올라갔는지 확인한다.
2. 이상이 없다면 pull request 탭에 들어가서 요청을 보낸다
3. merge하기에도 이상이 없다면 merge까지 해준다
	*여기서 이상이 있거나 헷갈리는 부분이 있다면 상대방에게 조언을 구합니다!
4. 머지가 완료되었다면 브런치를 볼 수 있는 드롭다운에서 view all branchs를 click
5. merge가 완료되었다는 표시가 나왔다면 해당 브런치를 삭제해줍니다.
```

> 다시 로컬환경으로 돌아옵니다
>
> 이하의 부분은 다시 프로젝트 작업을 하기 위해서 현재 가지고 있는 브런치를 삭제해주고 변경된 마스터 데이터를 로컬로 가져오는 부분입니다.

```bash
# 1.기존의 branch 제거
$ git switch master

# (optional) branch 목록 확인
$ git branch

# 마스터로 이동됨을 확인했다면 이전의 브런치 삭제
$ git branch -D fronted

# --------- 해당부분까지 브런치 삭제 부분 -------

# 2. 새로운 코드 받아오기

# 코드 가져오기 - 현재 위치는 마스터입니다.
$ git pull origin master

# 변경된 부분 가져와졌는지 확인

# 새로 작업할 브런치를 만들고 이동
$ git branch frontend

$ git switch frontend

# (optional) 정상작동하였다면 현재 변경된 파일이 브런치내에도 마스터와 동일!
$ git pull origin master
# [output] already-up-to-date

# 작업 다시 시작!
```



> 추가로 알아두면 좋은 부분

아직 사용이 서툴기 때문에 파일 백업을 다른데에 하는 것을 까먹지 않도록 합니다!

`git status`로 **현재 상태를 확인하는 것을 습관화**합니다.

`git log --oneline`를 통해 변경 이력(commit)을 확인할 수 있습니다.



