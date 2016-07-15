# tools

整理一些实用的python脚本

1、burpUnicode
   在xdxd的https://github.com/stayliv3/burpsuite-changeU 基础上改的，添加多处unicode解码。

2、docker
   用法参见：http://zone.wooyun.org/content/27335 后续会继续尝试实现新功能
   现在的bug: docker低版本支持不好C

3、反向shell
   hacker.py模拟nc在本地监听一个端口
   target.py在目标上执行，会反向连接我们hacker.py监听的端口。
   targetNC.py是收集的google团队写的用于nc反弹shell用的脚本,比我的轮子高级。

   
待续...


参考：
https://github.com/averagesecurityguy/scripts   