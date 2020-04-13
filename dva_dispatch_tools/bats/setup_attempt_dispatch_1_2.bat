@echo off
REM --- Web Resources ---
REM ---- VATSIM Info ----
start "" chrome --new-window "http://www.vattastic.com/"
timeout /t 2
REM ---- Weather Resources ----
start "" chrome --new-window "https://www.aviationweather.gov/"
timeout /t 2
start "" chrome "https://www.aviationweather.gov/briefing"
start "" chrome "https://www.weather.gov/ztl/"
REM ---- Route Finding Resources ----
start "" chrome --new-window "https://www.deltava.org/airportinfo.do?id=KCLT"
timeout /t 2
start "" chrome "https://flightaware.com/"
start "" chrome "https://flightaware.com/statistics/ifr-route/"
start "" chrome "https://www.fly.faa.gov/rmt/nfdc_preferred_routes_database.jsp"
start "" chrome "https://skyvector.com/"
start "" chrome "https://www.simbrief.com/system/dispatch.php?newflight=1"
REM ---- Chart Resources ----
start "" chrome --new-window "https://www.vatsim.net/charts/"
timeout /t 2
start "" chrome "http://jeppesen.com/icharts/index.jsp"
REM --- Dispatch Program ---
start "" "D:\Program Files (x86)\Delta Virtual\ACARSDispatch\DVADispatch.exe"
timeout /t 2
REM --- Flight Path Weather Tool Java Applet --- 
start "" "D:\coxna\Documents\Flight Sim\Java\fpt.jnlp"	
timeout /t 2
REM --- Start VATSpy ---
start "" "C:\Users\coxna\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\VATSpy\VATSpy.lnk"