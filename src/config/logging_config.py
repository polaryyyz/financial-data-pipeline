import logging.config

config = {
     "version": 1,
     "formatters": {
         "standard": {
             "format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
     },
     "handlers": {
         "file": {
               "class": "logging.FileHandler",
               "filename": "logs/pipeline.log",
               "level": "DEBUG",
               "formatter": "standard"
          },
          "console": {
               "class": "logging.StreamHandler",
               "stream": "ext://sys.stdout",
               "level": "INFO",
               "formatter": "standard"
          },
    },
     "root": {
         "level": "DEBUG",
         "handlers": ["file", "console"]
        }         
}
logging.config.dictConfig(config)