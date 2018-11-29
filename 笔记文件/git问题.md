##### 一

如果输入$ git remote add origin [git@github.com:djqiang（github帐号名）/gitdemo（项目名）.git](mailto:git@github.com:djqiang/gitdemo.git)  提示出错信息：fatal: remote origin already exists.

   解决办法如下：

    1、先输入$ git remote rm origin //删除远程配置

    2、再输入$ git remote add origin git@github.com:djqiang/gitdemo.git 就不会报错了！

    3、如果输入$ git remote rm origin 还是报错的话，error: Could not remove config section 'remote.origin'. 我们需要修改gitconfig文件的内容

    4、找到你的github的安装路径，我的是C:\Users\ASUS\AppData\Local\GitHub\PortableGit_ca477551eeb4aea0e4ae9fcd3358bd96720bb5c8\etc

    5、找到一个名为gitconfig的文件，打开它把里面的[remote "origin"]那一行删掉就好了！

##### 二

###### [由于github仓库中提前建立readme文件，导致git push报错error: failed to push some refs to 'git@github.com:](https://www.cnblogs.com/zlcxbb/p/6407451.html)

原因： 

*GitHub远程仓库中的README.md文件不在本地仓库中。*

解决方案：

```
$ git pull --rebase origin master 从远程更新到本地
$ git push -u origin master
```

##### 三