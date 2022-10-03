# sing-box 搭建全局代理-Tun隧道模式

配置：shadowtls 模式，使用正常网站的TLS证书混淆流量，绕过GFW。
原理参考：
https://www.youtube.com/watch?v=o-IFEu4GENE

Mac下测试有效，

优点：
   1、不需要借助Proxies将不支持代理的软件加入使用代理

缺点：
   2、代理断了，会出现请求不走代理直接请求的情况。
