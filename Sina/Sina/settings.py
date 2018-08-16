# encoding=utf-8
# BOT_NAME = 'Sina'
#

SPIDER_MODULES = ['Sina.spiders']
NEWSPIDER_MODULE = 'Sina.spiders'

DOWNLOADER_MIDDLEWARES = {
    "Sina.middleware.UserAgentMiddleware": 401,
    "Sina.middleware.CookiesMiddleware": 402,
}

ITEM_PIPELINES = {
    'Sina.pipelines.WeiboPipeline': 1,
}
LOG_LEVEL = 'INFO'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3  # 间隔时间
DOWNLOAD_TIMEOUT = 5
# MYSQL_HOSTS = '127.0.0.1'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = '123456'
# MYSQL_PORT = '3306'
# MYSQL_DB = 'sinaweibo'

