编写关于豆瓣站点的各类爬虫

# 豆瓣模拟登录
抓取数据的过程中有时候需要完成模拟登录的操作。本次模拟登录使用`requests`库完成，并在登录后保存`Cookie`，方便下次直接登录。之后通过访问豆瓣的个人主页验证当前状态是否为已登录状态。验证码的处理使用手动的方式。

### 代码地址：[douban_login_1.py](https://github.com/Cloving/Douban-Spider/blob/master/%E8%B1%86%E7%93%A3%E7%99%BB%E5%BD%95/douban_login_1.py)

### 使用方式
```python
douban = DoubanLogin()
# 开始登录，并保存cookie
douban.login()
# 携带cookie进行登录
douban.get_index()
# 判断是否为已登录状态
print(douban.is_login())
```
根据需要自行选择执行项



### 详细介绍：[豆瓣登录（一）](http://yaodongsheng.com/2018/11/30/Python%E6%A8%A1%E6%8B%9F%E8%B1%86%E7%93%A3%E7%99%BB%E5%BD%95%EF%BC%88%E4%B8%80%EF%BC%89/)
