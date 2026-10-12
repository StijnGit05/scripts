import gpxpy
import math

# Constants
INPUT_GPX_FILE = "final route.gpx"
OUTPUT_GPX_FILE = "output.gpx"
INTERVAL_METERS = 10

def haversine(lat1, lon1, lat2, lon2):
    # Straal van de aarde in meters
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def interpolate_points(lat1, lon1, lat2, lon2, distance):
    # Bereken de totale afstand tussen de twee punten
    total_distance = haversine(lat1, lon1, lat2, lon2)
    if total_distance <= distance:
        return [(lat2, lon2)]

    # Bereken het aantal nieuwe punten
    num_points = int(total_distance / distance)

    # Interpoleer nieuwe punten
    new_points = []
    for i in range(1, num_points):
        ratio = i / num_points
        lat = lat1 + ratio * (lat2 - lat1)
        lon = lon1 + ratio * (lon2 - lon1)
        new_points.append((lat, lon))

    return new_points

def process_gpx(input_file=INPUT_GPX_FILE, output_file=OUTPUT_GPX_FILE, interval=INTERVAL_METERS):
    with open(input_file, 'r') as f:
        gpx = gpxpy.parse(f)

    new_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(new_track)
    new_segment = gpxpy.gpx.GPXTrackSegment()
    new_track.segments.append(new_segment)

    for track in gpx.tracks:
        for segment in track.segments:
            points = segment.points
            for i in range(len(points) - 1):
                lat1, lon1 = points[i].latitude, points[i].longitude
                lat2, lon2 = points[i + 1].latitude, points[i + 1].longitude

                # Voeg het huidige punt toe
                new_segment.points.append(points[i])

                # Interpoleer nieuwe punten
                new_points = interpolate_points(lat1, lon1, lat2, lon2, interval)
                for lat, lon in new_points:
                    new_point = gpxpy.gpx.GPXTrackPoint(lat, lon)
                    new_segment.points.append(new_point)

    # Voeg het laatste punt toe
    new_segment.points.append(points[-1])

    with open(output_file, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == "__main__":
    # Voorbeeldgebruik / CLI entry
    process_gpx()