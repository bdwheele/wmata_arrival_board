#!/bin/env python3

import argparse
import logging
import configparser
import sys
import pygame
from pygame_led import LEDPanel
from wmata_api import Wmata_API
import time

stations = {
    # code: [name, lines, platforms]
    "A01": ["Metro Center",["RD"],2],
    "A02": ["Farragut North",["RD"],2],
    "A03": ["Dupont Circle",["RD"],2],
    "A04": ["Woodley Park-Zoo/Adams Morgan",["RD"],2],
    "A05": ["Cleveland Park",["RD"],2],
    "A06": ["Van Ness-UDC",["RD"],2],
    "A07": ["Tenleytown-AU",["RD"],2],
    "A08": ["Friendship Heights",["RD"],2],
    "A09": ["Bethesda",["RD"],2],
    "A10": ["Medical Center",["RD"],2],
    "A11": ["Grosvenor-Strathmore",["RD"],2],
    "A12": ["White Flint",["RD"],2],
    "A13": ["Twinbrook",["RD"],2],
    "A14": ["Rockville",["RD"],2],
    "A15": ["Shady Grove",["RD"],2],
    "B01": ["Gallery Pl-Chinatown",["RD"],2],
    "B02": ["Judiciary Square",["RD"],2],
    "B03": ["Union Station",["RD"],2],
    "B04": ["Rhode Island Ave-Brentwood",["RD"],2],
    "B05": ["Brookland-CUA",["RD"],2],
    "B06": ["Fort Totten",["RD"],2],
    "B07": ["Takoma",["RD"],2],
    "B08": ["Silver Spring",["RD"],2],
    "B09": ["Forest Glen",["RD"],2],
    "B10": ["Wheaton",["RD"],2],
    "B11": ["Glenmont",["RD"],2],
    "B35": ["NoMa-Gallaudet U",["RD"],2],
    "C01": ["Metro Center",["BL", "OR", "SV"],2],
    "C02": ["McPherson Square",["BL", "OR", "SV"],2],
    "C03": ["Farragut West",["BL", "OR", "SV"],2],
    "C04": ["Foggy Bottom-GWU",["BL", "OR", "SV"],2],
    "C05": ["Rosslyn",["BL", "OR", "SV"],2],
    "C06": ["Arlington Cemetery",["BL"],2],
    "C07": ["Pentagon",["BL", "YL"],2],
    "C08": ["Pentagon City",["BL", "YL"],2],
    "C09": ["Crystal City",["BL", "YL"],2],
    "C10": ["Ronald Reagan Washington National Airport",["BL", "YL"],3],
    "C12": ["Braddock Road",["BL", "YL"],2],
    "C13": ["King St-Old Town",["BL", "YL"],2],
    "C14": ["Eisenhower Avenue",["YL"],2],
    "C15": ["Huntington",["YL"],2],
    "D01": ["Federal Triangle",["BL", "OR", "SV"],2],
    "D02": ["Smithsonian",["BL", "OR", "SV"],2],
    "D03": ["L'Enfant Plaza",["BL", "OR", "SV"],2],
    "D04": ["Federal Center SW",["BL", "OR", "SV"],2],
    "D05": ["Capitol South",["BL", "OR", "SV"],2],
    "D06": ["Eastern Market",["BL", "OR", "SV"],2],
    "D07": ["Potomac Ave",["BL", "OR", "SV"],2],
    "D08": ["Stadium-Armory",["BL", "OR", "SV"],2],
    "D09": ["Minnesota Ave",["OR"],2],
    "D10": ["Deanwood",["OR"],2],
    "D11": ["Cheverly",["OR"],2],
    "D12": ["Landover",["OR"],2],
    "D13": ["New Carrollton",["OR"],2],
    "E01": ["Mt Vernon Sq 7th St-Convention Center",["GR", "YL"],2],
    "E02": ["Shaw-Howard U",["GR", "YL"],2],
    "E03": ["U Street/African-Amer Civil War Memorial/Cardozo",["GR", "YL"],2],
    "E04": ["Columbia Heights",["GR", "YL"],2],
    "E05": ["Georgia Ave-Petworth",["GR", "YL"],2],
    "E06": ["Fort Totten",["GR", "YL"],2],
    "E07": ["West Hyattsville",["GR"],2],
    "E08": ["Prince George's Plaza",["GR"],2],
    "E09": ["College Park-U of Md",["GR"],2],
    "E10": ["Greenbelt",["GR"],2],
    "F01": ["Gallery Pl-Chinatown",["GR", "YL"],2],
    "F02": ["Archives-Navy Memorial-Penn Quarter",["GR", "YL"],2],
    "F03": ["L'Enfant Plaza",["GR", "YL"],2],
    "F04": ["Waterfront",["GR"],2],
    "F05": ["Navy Yard-Ballpark",["GR"],2],
    "F06": ["Anacostia",["GR"],2],
    "F07": ["Congress Heights",["GR"],2],
    "F08": ["Southern Avenue",["GR"],2],
    "F09": ["Naylor Road",["GR"],2],
    "F10": ["Suitland",["GR"],2],
    "F11": ["Branch Ave",["GR"],2],
    "G01": ["Benning Road",["BL", "SV"],2],
    "G02": ["Capitol Heights",["BL", "SV"],2],
    "G03": ["Addison Road-Seat Pleasant",["BL", "SV"],2],
    "G04": ["Morgan Boulevard",["BL", "SV"],2],
    "G05": ["Largo Town Center",["BL", "SV"],2],
    "J02": ["Van Dorn Street",["BL"],2],
    "J03": ["Franconia-Springfield",["BL"],2],
    "K01": ["Court House",["OR", "SV"],2],
    "K02": ["Clarendon",["OR", "SV"],2],
    "K03": ["Virginia Square-GMU",["OR", "SV"],2],
    "K04": ["Ballston-MU",["OR", "SV"],2],
    "K05": ["East Falls Church",["OR", "SV"],2],
    "K06": ["West Falls Church-VT/UVA",["OR"],3],
    "K07": ["Dunn Loring-Merrifield",["OR"],2],
    "K08": ["Vienna/Fairfax-GMU",["OR"],2],
    "N01": ["McLean",["SV"],2],
    "N02": ["Tysons Corner",["SV"],2],
    "N03": ["Greensboro",["SV"],2],
    "N04": ["Spring Hill",["SV"],2],
    "N06": ["Wiehle-Reston East",["SV"],2],
    "N07": ["Reston Town Center",["SV"],2],
    "N08": ["Herndon",["SV"],2],
    "N09": ["Innovation Center",["SV"],2],
    "N10": ["Dulles Airport",["SV"],2],
    "N11": ["Loudoun Gateway",["SV"],2],
    "N12": ["Ashburn",["SV"],2],
}

colors = {
    'black': "#000000",
    'white': "#ffffff",
    "red": "#ff0000",
    'RD': "#ff0000",
    'OR': "#ff5500",
    'YL': '#ffff00',
    'GR': "#00ff00",
    'BL': "#0000ff",
    'SV': "#aaaaaa"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")
    parser.add_argument("--conf", type=str, default=sys.path[0] + "/metro_arrival.conf", help="alternate configuration file")
    parser.add_argument("--fullscreen", default=False, action="store_true", help="Use full screen")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    # read the configuration
    config = configparser.ConfigParser()
    config.read(args.conf)

    if config['metro']['station'] not in stations or not (1 <= int(config['metro']['platform']) <= stations[config['metro']['station']][2]):
        logging.error("Station or platform is out of range")

    logging.info(f"Using station {stations[config['metro']['station']][0]}({config['metro']['station']}), platform {config['metro']['platform']}")


    panel = LEDPanel(128, 32, 12, (pygame.FULLSCREEN | pygame.SCALED) if args.fullscreen else 0)
    api = Wmata_API(config['api']['url'], config['api']['key'])
    next_fetch = time.time() - 1
    trains = []
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        if time.time() > next_fetch:
            trains = api.fetch_predition(config['metro']['station'], config['metro']['platform'])
            next_fetch = time.time() + 30

        # draw the header
        panel.clear()
        panel.text(0, 0, "LN CAR DEST       MIN", colors['RD'])
        cy = 8
        # draw the predictions
        for t in trains:
            # line name
            panel.text(0, cy, t[0], colors['YL'])
            # cars
            panel.text(18, cy, t[1], colors['GR'] if t[1] == '8' else colors['YL'])
            # destination
            panel.text(30, cy, t[2], colors['YL'])
            # min
            panel.text(108, cy, t[3], colors['YL'])
            cy += 8

       
        # flip() the display to put your work on screen
        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()