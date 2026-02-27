from skyfield.api import load
import calendar
import math

def get_moon_phase(year, month, day):
    eph = load('de421.bsp')
    ts = load.timescale()

    t_today = ts.utc(year, month, day)
    t_next = ts.utc(year, month, day + 1)

    earth = eph['earth']
    moon = eph['moon']
    sun = eph['sun']

    # Get elongation (angular separation) today
    angle = earth.at(t_today).observe(moon).apparent().separation_from(
        earth.at(t_today).observe(sun).apparent()
    ).degrees

    # Get vector from Earth to Moon and Earth to Sun
    r_moon = earth.at(t_today).observe(moon).apparent().position.km
    r_sun = earth.at(t_today).observe(sun).apparent().position.km

    # Dot product method to determine waxing or waning
    dot = sum(m * s for m, s in zip(r_moon, r_sun))
    waxing = dot < 0  # Negative dot = waxing, Positive = waning

    # Determine moon phase based on angle
    if angle < 22.5:
        phase = 'New Moon'
        emoji = 'images/new_moon.png'
    elif angle < 67.5:
        phase = 'Waxing Crescent' if waxing else 'Waning Crescent'
        emoji = 'images/waxing_crescent_moon.png' if waxing else 'images/waning_crescent_moon.png'
    elif angle < 112.5:
        phase = 'First Quarter' if waxing else 'Last Quarter'
        emoji = 'images/first_quarter_moon.png' if waxing else 'images/last_quarter_moon.png'
    elif angle < 157.5:
        phase = 'Waxing Gibbous' if waxing else 'Waning Gibbous'
        emoji = 'images/waxing_gibbous_moon.png' if waxing else 'images/waning_gibbous_moon.png'
    else:
        phase = 'Full Moon'
        emoji = 'images/full_moon.png'

    #Calculate moon illumination percentage
    illumination = (1 - math.cos(math.radians(angle))) / 2
    illumination_percent = round(illumination * 100, 1)

    #Average moon age is 29.53 days, so we can calculate the age of the moon in days
    synodic_month = 29.53058867 
    moon_age = (synodic_month * angle / 360) % synodic_month

    # Phase ages in days
    phase_ages = {
        "New Moon": 0,
        "First Quarter": synodic_month * 0.25,
        "Full Moon": synodic_month * 0.5,
        "Last Quarter": synodic_month * 0.75
    }

    return {
        'phase': phase,
        'angle': f'Moon Elongation: {round(angle, 2)}°',
        'emoji': emoji,
        'Dtoday': f' {calendar.month_name[month]} {day}, {year}',
        'illumination': f'Moon Illumination: {illumination_percent}%',
    }

if __name__ == "__main__":
    import datetime
    today = datetime.date.today()
    result = get_moon_phase(today.year, today.month, today.day)
    print(result)