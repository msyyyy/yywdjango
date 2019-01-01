## **git学习**

###### 创建版本库 

先创建一个空目录 然后 git init

```
git add <file> 添加文件到暂存区
```

```
git commit  -m  "说明"   把暂存区的东西都上传到库，并添加说明  （如果不加说明会进入vim模式）
```

`git status 查看当前库状态`

```
git diff 查看有什么修改
例如 git diff HEAD -- readme.tx  查看工作区和版本库里面最新版本的区别

-----------------------版本库--------------------------------------------
                                         |                           |
                                 git diff --cached           |
                                         |                           |
-------------暂存区----------------------       git diff HEAD
                        |                                            |
                     git diff                                      |
                        |                                            |
-----工作区--------------------------------------------------------------
```

##### 时光机穿梭·

###### 版本回退

```
git log 查看历史版本记录 也可以加上 --pretty=oneline 参数
```

在git 中 用 HEAD表示当前版本   HEAD^表示上一版本  HEAD~100 往上100个版本

```
git reset --hard HEAD^  回退到上个版本
```

```
git reset --hard <file>  回退到某个指定版本
```

```
git reflog  查看历史命令
```

###### 撤销修改

```
git checkout -- file  可以丢弃工作区的修改 回到最后一次git commit 或 git add 的状态
```

```
git reset HEAD <file> 可以把暂存区的修改撤销掉，重新放回工作区
```

如果已经提交到本地版本库 可以使用版本回退

###### 删除文件

```
先rm test.txt 在工做区中删除
如果要把版本库的也删除  git rm test.txt 然后  git commit
如果误删 git checkout -- test.txt  用版本库里的版本替换工作区的版本
```

##### 远程仓库

###### 添加/克隆远程库

```
git remote add origin git@github.com:账号名/项目名.git 把本地库和远程库关联
```

```
git push -u origin master 把本地库内容推送到远程库  -u不仅推送而且相关联以后可以不加
```

```
git clone git@github.com:账号名/项目名.git  克隆一个远程库到本地
```

##### 分支管理

###### 创建和合并分支

```
git checkout -b <name>  创建分支并切换到那个分支
git branch  <name>  创建分支
```

```
git branch   查看当前分支   git branch命令会列出所有分支，当前分支前面会标一个*号
```

```
git checkout <name> 切换到name分支   git checkout master
```

```
git merge <name> 合并name分支到当前分支
```

```
git branch -d <name>  删除分支
```

领先分支如 dev  想要 merge   落后分支master 好像不行



同一份文件，在你提交时，有人比你更早更新了文件并上传，使你的本地文件并非最新。因此，在你想上传自己修改后的文件时，第一步git pull时，会报错误：

* git stash 隐藏本地修改

- git pull  下载最新代码 
- git stash pop 从Git栈中读取最近一次保存的内容，恢复自己的本地修改
- 提示有无冲突
  - 若有冲突，则解决冲突
  - 若无，则直接提交 
    - git add * 
    - git commit * -m "comments"