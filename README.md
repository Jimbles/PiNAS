# PiNAS π💾 🍆🍓

All-in-one Raspberry Pi Media box handling torrents, game streaming, media and storage. VESA mounted on the back of the Telly with external HDD.

Featuring:

- Moonlight streams games from desktop PC
- DLNA server used for watching movies/TV on smart TV or laptop
- Torrents through VPN
- Sonarr/Radarr/Jackett for searching and downloading torrents
- Airsonic for music streaming i.e. replace google music
- SAMBA network drive for media
- Syncthing for backing up
- beets for music collection organising

## Parts used

- Raspberry Pi 4GB
- WD Elements 2TB HDD WDBU6Y0020BBK
- 40mm fan and heatsink (I used [this one](https://www.ebay.co.uk/itm/Raspberry-Pi-Fan-Heatsink-Cooling-Kit-rubber-silicone-feet-40mm-5V-Pi4-4b-3-3b/133433997199?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649) )
- Push buttons and an LED
- 3D print case, lids and button holder
- Power, HDMI and Ethernet cable
- USB Hub for controllers ([This one](https://www.amazon.co.uk/gp/product/B07L32B9C2/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) worked ok)

## Hardware Setup

RPi 4 with 2TB USB3 HDD, this was cheaper than SSD but cannot use two HDDs at once due to power limitations so will run into problem if expansion needed.

Case is based on [this excellent case](https://www.thingiverse.com/thing:3723481) with accompanying 40 mm fan and heatsink, expanded to house the HDD and fit 200 mm VESA screw holes. The STEP, STL and 3mf for PrusaSlicer files are found in `cad` folder. Printed with 3 perimeters, no top or bottom layers and with hexagonal infill. I connected used 3.3 V rather than to reduce noise.

<img src="https://raw.githubusercontent.com/Jimbles/PiNAS/main/images/Vesa_Case_SW.png" width=50% height=50%><img src="https://raw.githubusercontent.com/Jimbles/PiNAS/main/images/Vesa_Case_PS.png" width=29% height=29%>

### Shutdown and game stream buttons

Two push buttons and an indicator LED was added to easily shutdown the Pi and also to start Moonlight streaming. Add the following line to `rc.local` before the line `exit 0` to run at startup.

` sudo /usr/bin/python3 /home/pi/PiNAS/code/moonlight_shutdown.py &`

Currently the Moonlight-qt button does not start properly, so it uses moonlight embedded

## Software Setup

The are many steps to this! I have included the ones I can remember and what guides I used to help me. 

### Networking and security

- SSH key for remote access [Pi Docs](https://www.raspberrypi.org/documentation/remote-access/ssh/) and [copying keys](https://www.raspberrypi.org/documentation/remote-access/ssh/)
- Added SSH key to Putty by converting to puttykey through puttygen
- `.ppk` file needed for FTP in Filezilla too
- VNC server using ssh key [here](https://helpdeskgeek.com/how-to/tunnel-vnc-over-ssh/) needed to add IP address in tunnelling settings in Putty due to ssh key
- [Unattended upgrades](https://raspberrypi.stackexchange.com/a/102350/44732)
- Fail2ban, UFW.
- Install [Docker](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl ) and Docker-compose. Remember to use container names not IP addresses for ports and containers in same network. i.e. 192.168.1.1:4040 should be jacket:7878.

### Media Setup

- Mount NTFS drive automatically (I wanted to be able to use the drive in my PC incase of problems so kept it NTFS) [Pidocs](https://www.raspberrypi.org/documentation/configuration/external-storage.md)
- Add SAMBA share [1](https://magpi.raspberrypi.org/articles/raspberry-pi-samba-file-server) [2](https://www.raspberrypi.org/documentation/remote-access/samba.md) ADD UFW RULE. Needed to add smb client in windows 10
- DLNA player [1](https://pimylifeup.com/raspberrypi-minidlna/) [2](https://www.raspberrypi.org/forums/viewtopic.php?t=251651) ADD UFW RULE! Added reference to `poster.jpg` and `fanart.jpg` in album art as thats what Sonarr and Radarr use
- `ncdu` for checking folder size
- On laptop added music folder as samba network drive. Fine to use but indexing was slow

### Torrents

- NordVPN - needed to use the service credentials user and pass as mentioned [here](https://support.nordvpn.com/Connectivity/Linux/1047409422/How-can-I-connect-to-NordVPN-using-Linux-Terminal.htm)
- [Docker-Deluge](https://github.com/Jimbles/docker-deluge-openvpn) Runs Deluge in a container with VPN, ensures all torrent traffic goes through VPN. Possible that docker continuously cannot find a config file for the server, in which case you should rebuild the container, or copy across new configs.
  - Web access through port `8112`.
  - Change password and set move completed downloads to `completed` folder.
  - Set watch folder for torrents, then point jackett to this.
  - Torrent setup, largely based on [this](https://github.com/sebgl/htpc-download-box).
  - Add RuTracker and set blackhole directory in Jackett.
  - Add indexers to Sonarr/Radarr remember to use `Jackett` instead of IP i.e. `http://jackett:9117/api/v2.0/indexers/thepiratebay/results/torznab/`
  - Add Deluge as Download client remember to use `delugevpn` (the container name from above) as the ip/host
  - Bazarr used OpenSubtitles.org

### Cloudstorage/backup

Install syncthing [guide](https://pimylifeup.com/raspberry-pi-syncthing/) 
Current only backup music folder. I dont expose the port externally instead use use ssh port forwarding `ssh -L 9090:127.0.0.1:8384 pi@192.168.x.x`

### Music Streaming or Google Music Replacement

- Used Airsonic behind NGinx server following [this great guide](https://youtu.be/bozkNMUfqKM) 
- I used [duckDNS](https://www.duckdns.org/) for the DNS
- Opened Ports on Router

### Video Game Streaming

- Moonlight-qt [install guide](https://github.com/moonlight-stream/moonlight-docs/wiki/Installing-Moonlight-Qt-on-Raspberry-Pi-4). I like this better than moonlight embedded as it allows multiple apps to open like steam/retroarch and changing stream settings in app. Remember to increase GPU memory
- Moonlight embedded [repo](https://github.com/irtimmer/moonlight-embedded) [guide](https://www.howtogeek.com/220969/turn-a-raspberry-pi-into-a-steam-machine-with-moonlight/). Command is `moonlight stream -1080 -bitrate 50000 -remote -quitappafter -app steam` It defaults to steam, but can swap to `-app retroarch` etc. working with steam, retroarch, psnow and pcsx2
- Steam Link - I found moonlight better but useful for checking network and controllers

#### Controllers

- PS3 Dual Shock wired
- Xbox 360 Wired [drivers](https://github.com/atar-axis/xpadneo)
- Xbox Series X controller [drivers](https://github.com/atar-axis/xpadneo), working wired, but bluetooth would not work, a common issue with these workaround was found [here](https://github.com/atar-axis/xpadneo/issues/259)
- `jstest` useful to check controller inputs
