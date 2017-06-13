### 数据库管理工具命令
1. `python manage.py db init`创建迁移仓库 
2. `python manage.py db migrate -m 'init migrate'` 创建迁移脚本 （只要migrations文件存在[同一个数据库，且migrations文件夹保存的上一个状态一定要和数据库一致，修改数据库一般得删掉migrations，重新执行]，一般从这一步开始）
3. `python manage.py db upgrade` 更新数据库