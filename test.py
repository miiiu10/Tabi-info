from flask import Flask, render_template, request
from GeoCode import get_position
from weather import get_weather

def main():
	place = "仙台"
	lng, lat = get_position(place)
	weather = get_weather(lat, lng)
	return weather

if __name__ == "__main__":
	print(main())
