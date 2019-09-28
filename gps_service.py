import math

class GPSPoint:
	
        #constructor
	def __init__(self, lat, lon, alt):
		self.lat = lat
		self.lon = lon
		self.alt = alt
		
	
	def distanceTo(self, point, radius=6371e3):
    		R = radius
    		phi1 = math.radians(self.lat)
    		lambda1 = math.radians(self.lon)
    		phi2 = math.radians(point.lat)
    		lambda2 = math.radians(point.lon)
    		delta_phi = phi2 - phi1
    		delta_lambda = lambda2 - lambda1

   		#distance calculation with haversine formula
    		a = math.sin(delta_phi/2)*math.sin(delta_phi/2) + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)*math.sin(delta_lambda/2)

    		c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    		d = R * c  # in meters
    
		#distance: Spherical Law of cosines
		#d2 = math.acos( math.sin(phi1)*math.sin(phi2) + math.cos(phi1)*math.cos(phi2) * math.cos(deltaLambda) ) * R;

		#distance: Equirectangular approximation
		#x = (lambda2-lambda1) * math.cos((phi1+phi2)/2);
		#y = (phi2-phi1);
		#d3 = math.sqrt(x*x + y*y) * R;
		return d

	
	def bearingAngle(self, point):

		phi1 = math.radians(self.lat)
		lambda1 = math.radians(self.lon)
		phi2 = math.radians(point.lat)
		lambda2 = math.radians(point.lon)
		delta_lambda = lambda2 - lambda1
		#bearing calculation
		y = math.sin(delta_lambda) * math.cos(phi2)
		x = math.cos(phi1)*math.sin(phi2) - math.sin(phi1)*math.cos(phi2)*math.cos(delta_lambda)
		i_bearing = math.degrees(math.atan2(y, x))
		f_bearing = i_bearing + 180
		return int(i_bearing), int(f_bearing)
		#return wrap360 function used here

	def elevationAngle(self, point):
		delta_height = point.alt - self.alt  #if in meters
		distance = self.distanceTo(point)
		elevation = math.atan(delta_height/distance) #check degrees or radian
		return int(elevation)

#if __name__ == '__main__':
	#test	
	#obj = GPSPoint(42.338639, -71.086194, 0)
	#print(obj.lat, obj.lon)
	#obj2 = GPSPoint(42.338641, -71.086109, 0)
	#print(obj.distanceTo(obj2))
	#print(obj.bearingAngle(obj2))


JAMMING_ANTENNAS = { 
	'jam1' :GPSPoint(42.338639, -71.086194, 0),
	'jam2' :GPSPoint(42.338639, -71.086194, 0),
	'jam3' :GPSPoint(42.338639, -71.086194, 0),
	'jam4' :GPSPoint(42.338639, -71.086194, 0),
	'jam5' :GPSPoint(42.338639, -71.086194, 0),
}
			
		
