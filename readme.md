# scrapy 爬取研招网信息

[toc]

## 系统环境
- python3+
- mysql

## 安装python第三方库

```
pip install scrapy
pip install pymysql
pip install pandas
```

## 配置相关信息

ssml.py



![image-20220114132934720](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202201141329792.png)

![image-20220114132022754](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202201141320829.png)

其中mldm与yjxkmd来自

![image-20220114133015730](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202201141330786.png)

middlewares.py 采用快代理的隧道代理ip

![未命名](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202201141326244.png)

![image-20220114132203267](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202201141322321.png)

pipelines.py

配置数据库

![image-20220114133141999](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/202201141331067.png)



## 运行程序 
运行start.py

