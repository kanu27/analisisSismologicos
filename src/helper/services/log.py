from platform import system
from datetime import date
import logging
import os

class Log():
    def __init__(self,
                 vMenssage:str,
                 vTypes:str,
                 vProyect:str,
                 vFunction:str):
        """
        vType = (debug,info,warning,error,critical)
        """
        self.menssage = vMenssage
        self.types = vTypes
        self.proyect = vProyect
        self.function = vFunction
        self.sO = system()
        self.fullPath = os.getcwd()
        self.sl = ""
        if self.sO == "Linux" or self.sO == "MacOs":
            self.sl = "/"
        else:
            self.sl = "\\"

    def console(self):
        if self.validateFolder() == False:
            os.mkdir(self.fullPath + self.sl + "config" + self.sl +"log")
            Log.console(Log("Carpeta log Creada","info","Log","console"))
        fileToday = self.fullPath + self.sl + "config" + self.sl +"log"+ self.sl + str(date.today())+ ".log"            
        if self.types == "debug":
            logger = logging.getLogger(self.proyect)
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler(fileToday)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - '+self.function+' - %(name)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.debug(self.menssage)
        elif self.types == "info":
            logger = logging.getLogger(self.proyect)
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler(fileToday)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - '+self.function+' - %(name)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.info(self.menssage)
        elif self.types == "warning":
            logger = logging.getLogger(self.proyect)
            logger.setLevel(logging.WARNING)
            fh = logging.FileHandler(fileToday)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - '+self.function+' - %(name)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.warning(self.menssage)
        elif self.types == "error":
            logger = logging.getLogger(self.proyect)
            logger.setLevel(logging.ERROR)
            fh = logging.FileHandler(fileToday)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - '+self.function+' - %(name)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.error(self.menssage)
        elif self.types == "critical":
            logger = logging.getLogger(self.proyect)
            logger.setLevel(logging.CRITICAL)
            fh = logging.FileHandler(fileToday)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - '+self.function+' - %(name)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.critical(self.menssage)
    
    def validateFolder(self):
        return os.path.isdir(self.fullPath + self.sl + "config"+self.sl +"log")


if __name__ == "__main__":
    log = Log("prueba de error","debug","Log","validateFolder")
    log.console()
