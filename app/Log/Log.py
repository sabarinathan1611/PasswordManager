import datetime
class Log:
    def writeLog(event,id="NO ID",msg=""):
        log_date=datetime.datetime.now()
        
        file='log.txt'
        message=f"Date: {str(log_date.date())}\tTime: {str(log_date.hour)}:{str(log_date.minute)}\t Event: {event} by User:{id} \t Message: {msg}"
        with open(file,'a') as fil:
            fil.write(message)

            

        
 