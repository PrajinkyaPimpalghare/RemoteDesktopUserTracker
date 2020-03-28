# RemoteDesktopUserTracker
It monitors Users taking/Utilizing Remote Desktop by using "SAME" or "DIFFERENT" credentials. Developed in Python and generates database in Json file which can be integrated with any website or tool.
I have integrated generated Json Database into Django Based Portal.
  Note: I have to hide the data , due to which it s looking little ugly.
![alt text](https://github.com/PrajinkyaPimpalghare/RemoteDesktopUserTracker/blob/master/Results/RemoteDesktopMonitorGUI.png)
![alt text](https://github.com/PrajinkyaPimpalghare/RemoteDesktopUserTracker/blob/master/Results/NewUserGUI.PNG)
![alt text](https://github.com/PrajinkyaPimpalghare/RemoteDesktopUserTracker/blob/master/Results/PortalDisplay.PNG)

Summary: 
  Whenever there is Remote Desktop login by common user name used by group of developers or by seperate user name, tool will prompt the tool where ever remote desktop login user has to fill his data, as well user can see who was the last user. Same things get updated in the Json datbase which can be connected to portal or any other display tool. Where user can see which build machines are free and who is current or last user.
  If machine is idle for 30 minutes , tool sends automatic signal to database and update sin portal as build machine is free, which helps the another user for the usage of same.
  
Usage:
  RemoteDesktopMonitor.exe  Without any argument - Creates a local database which gets filled as user login.
                            Withdatabase path "-d or --database"   - Provide the path of the database which can be shared by multiple user
                            Extra Parameter "-m or  --manual_user" - If manual User selected it set the machine as free from current state.
                            
 Files Description:
 RemoteDesktopUserMonitor.xml  - Task Scheduler xml file to create task of every remote login [Change respective username in it while importing]
 RemoteDesktopUserMonitoridle.xml  - Task Scheduler xml file to create task of 30 minute idle machine [Change respective username in it while importing]
 
ExecuteMonitor.bat , ExecuteMonitorIdle.bat and RemoteDesktopmonitor.exe - keep them in "C:\Program Files\RemoteDesktopMonitor" folder same mentined in Task Scheduler task.

#HappyWFH
 
