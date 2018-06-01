# Data Documentation

##### Data structure:
- **CoMoFoD_small**: Original and tampered files from CoMoFoD_small database (200/200).
- **CoMoFoD_large**: Original and tampered files from CoMoFoD_large database (60/60).
- **TIFS**: Original and tampered files from TIFS database (48/48).
- **converted**: All converted files (JPEG, JPEG2000, JPEG XR, BPG)
- **temporary**: Temporary files (e.g.: when BPG is converted to png to be read with imageio)
- **output**: Output files are saved here.

##### Reference Copy-Move Attack Databases:
- Tralic D., Zupancic I., Grgic S., Grgic M., "CoMoFoD - New Database for Copy-Move Forgery Detection", in Proc. 55th International Symposium ELMAR-2013, pp. 49-54, September 2013.
http://www.vcl.fer.hr/comofod/index.html
- V. Christlein, C. Riess, J. Jordan, C. Riess, E. Angelopoulou: "An Evaluation of Popular Copy-Move Forgery Detection Approaches", IEEE Transactions on Information Forensics and Security, vol. 7, no. 6, pp. 1841-1854, 2012.
http://www5.cs.fau.de/research/data/image-manipulation/

##### Preprocess Database
Use the powershell command inside the folder with all pictures (e.g.: use regex "*_F.png"):
```sh
ls -filter "pattern as regex" | copy-item -destination "absolute path"
```

```sh
ls -filter "pattern as regex" | del
```