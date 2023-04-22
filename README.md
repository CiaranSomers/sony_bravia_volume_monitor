# sony_bravia_volume_monitor
simple python 3 script to poll the volume of a sony bravia smart tv and if it's too loud lowers it.
It's lock down I'm working from home and my kids are watching YouTube in the next room which is getting louder and louder... so I've written this simple sctipt in python 3 as it uses the bravia-tv python library (https://pypi.org/project/bravia-tv/). It takes the settings from the top of the file but it could easily be modified to pass them in. 

The first time you connect to the TV from a device the TV displays a code on the screen. This pin number has to be passed in to operate the TV over the network. In theroy you only need it once. Note it must be tied the MAC so if you connect from one devicie over Ethernet and switch to wifi you get a new code.

The priciple is simple between star_mins (6 am)  and stop_mins (7 pm) the volume can't be greater than vax_vol (18) and it polls the TV to see if it's on then checks the volume every 20 seconds.
