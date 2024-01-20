# 4 Wire SPI interface

RASPBERRY PI GPIO >>> SH1106 1.3 inch display

| Pin  | GPIO  | SPI     | SH1106 | Description                                                     |
|------|-------|---------|--------|-----------------------------------------------------------------|
| 3.3v | P1-17 | 3.3v    | VCC    | power supply 3.3 Volts                                          |
| RES  | P1-18 | GPIO-24 | RES    | reset of the display to initial state (reset)                   |
| MOSI | P1-19 | GPIO-10 | MOSI   | data output to the display                                      |
| MISO | P1-21 | GPIO-09 |        | data input: not used                                            |
| A0   | P1-22 | GPIO-25 | SDC    | GPIO to indicate whether writing to registers or display memory |
| SCLK | P1-23 | GPIO-11 | CLK    | data synchronization clock                                      |
| CE0  | P1-24 | GPIO-08 | CCS    | display selection                                               |
| GND  | P1-25 | GND     | GND    | electrical ground                                               |
| CE1  | P1-26 | GPIO-07 |        | selection for another SPI device (not used)                     |
