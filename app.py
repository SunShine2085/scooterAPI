# from flask import Flask, render_template, request, redirect, url_for, make_response
# from geopy.distance import distance as geodesic
# import json, werkzeug, traceback
# from http import HTTPStatus


# app=Flask(__name__)

# # root
# @app.route('/')
# def home():
# 	return redirect(url_for('view_all_available'))

# #view all scooters
# @app.route('/inventory')
# def inventory():
#     db = init_db()
#     db_dictlist = convert_db_to_dictlist(db)
#     return json.dumps(db_dictlist), HTTPStatus.OK.value, {'Content-Type':'application/json'}
	
# @app.route('/view_all_available')
# def view_all_available():
# 	db = init_db()
# 	available_scooters = [scooter for scooter in db if not scooter.is_reserved]
# 	available_scooters_dictlist = convert_db_to_dictlist(available_scooters)
# 	return json.dumps(available_scooters_dictlist), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return a json-ified list of all the scooters with status 200


# # Search for scooters
# @app.route('/search', methods=['GET'])
# def search():
# 	# Search for scooters in the database
# 	# parse request params
# 	try:
# 		search_lat, search_lng, search_radius = \
# 			float(request.args['lat']), \
# 			float(request.args['lng']), \
# 			float(request.args['radius'])	# parse request for search criteria
# 	except werkzeug.exceptions.BadRequestKeyError:
# 		# the required parameters are not present in the search query
# 		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
# 	except ValueError:
# 		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

# 	# validate lat and long values
# 	if not -90 <= search_lat <= 90:
# 		error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
# 	if not -180 <= search_lng <= 180:
# 		error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	
# 	db = init_db()	# initialize db

# 	search_results = []
# 	for scooter in db:
# 		# Calculate distance between the scooter location point and the search location point, in metres
# 		distance = geodesic((scooter.lat, scooter.lng), (search_lat, search_lng)).m
# 		if distance <= search_radius and not scooter.is_reserved:
# 			# this scooter is available and within the search area
# 			search_results.append({	'id':scooter.id, 
# 									'lat':scooter.lat, 
# 									'lng':scooter.lng
# 								  })
			
# 	return json.dumps(search_results), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return json-ified search results list with status 200

	
# # Start a reservation 
# @app.route('/reservation/start', methods=['GET'])
# def start_reservation():
# 	# parse request params
# 	try:
# 		reserve_id = request.args['id']	# parse request for id of scooter to be reserved
# 	except werkzeug.exceptions.BadRequestKeyError:
# 		# the required parameters are not present in the search query
# 		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

# 	db = init_db()
	
# 	# try and find the scooter with specified id
# 	scooter = get_scooter_with_id(reserve_id, db)
# 	if scooter:
# 		# reserve if possible
# 		if not scooter.is_reserved:
# 			# scooter can be reserved
# 			scooter.is_reserved = True
# 			write_db(db)	# update db
# 			success = { 'msg': f'Scooter {reserve_id} was reserved successfully.' }
# 			return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# respond with status 200

# 		else:
# 			# the scooter is already reserved
# 			error = { 'msg': f'Error 422 - Scooter with id {reserve_id} is already reserved.' }
# 			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
# 	else:
# 		# no scooter with the reserve id was found
# 		error = { 'msg': f'Error 422 - No scooter with id {reserve_id} was found.' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422


# # End a reservation
# @app.route('/reservation/end', methods=['GET'])
# def end_reservation():
# 	# parse request params
# 	try:
# 		scooter_id_to_end = request.args['id']	# parse request for id of scooter whose reservation to be ended
# 		end_lat, end_lng = \
# 			float(request.args['lat']), \
# 			float(request.args['lng'])
# 		db = init_db()
# 	except werkzeug.exceptions.BadRequestKeyError:
# 		# the required parameters are not present in the search query
# 		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
# 	except ValueError:
# 		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

# 	# validate lat and long values
# 	if not -90 <= end_lat <= 90:
# 		error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
# 	if not -180 <= end_lng <= 180:
# 		error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
		
# 	# try and find the scooter with specified id
# 	scooter = get_scooter_with_id(scooter_id_to_end, db)
# 	if scooter:
# 		# end reservation if possible
# 		if scooter.is_reserved:
# 			# scooter is reserved and can be ended
			
# 			# initiate payment
# 			payment_response = pay(scooter, end_lat, end_lng)
# 			if payment_response['status']:
# 				# the payment was completed successfully
				
# 				# update scooter's reserved status and location
# 				scooter.is_reserved = False
# 				scooter.lat, scooter.lng = end_lat, end_lng
# 				write_db(db)
# 				# construct successful response
# 				success =	{	'msg': f'Payment for scooter {scooter_id_to_end} was made successfully and the reservation was ended.',
# 								'txn_id': payment_response['txn_id']
# 							}
# 				return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# respond with status 200
# 			else:
# 				# the payment failed for some reason
# 				error = { 'msg': payment_response['msg'] }
# 				response_code = payment_response['code']
# 				return json.dumps(error), response_code, {'Content-Type':'application/json'}
# 		else:
# 			# the scooter is not currently reserved
# 			error = { 'msg': f'Error 422 - No reservation for scooter {scooter_id_to_end} presently exists.' }
# 			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
# 	else:
# 		# no scooter with the id was found
# 		error = { 'msg': f'Error 422 - No scooter with id {scooter_id_to_end} was found.' }
# 		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422


# # ==================
# #  HELPER FUNCTIONS	
# # ==================


# def pay(scooter, end_lat, end_lng):
# 	# Initialise the payment process
# 	# construct location point tuples
# 	old_location = (scooter.lat, scooter.lng)
# 	new_location = (end_lat, end_lng)
# 	# calculate distance between points, in metres
# 	distance_ridden = geodesic(old_location, new_location).m
# 	distance_ridden = round(distance_ridden)
# 	# calculate cost (currently a dummy function that returns the distance as the cost)
# 	cost = calculate_cost(distance_ridden)	# returns cost = distance for now
# 	# redirect to payment gateway and return response (currently a dummy function that returns a hypothetical transaction id)
# 	return payment_gateway(cost)	# returns hypothetical success and txn id for now
	
# def payment_gateway(cost):
	# TODO: Implement real payment processing in future
# 	txn_id = 379892831
# 	return 	{	'status': True,
# 				'txn_id': txn_id
# 			}

# def calculate_cost(distance):
# 	# TODO: Implement meaningful cost calculation in future
# 	return distance

		
# def init_db():
# 	db_json = open('scooter_db.json', 'r').read()
# 	db_list = json.loads(db_json)
# 	# populate Scooter objects for easier access later
# 	db = []
# 	for scooter in db_list:
# 		scooter_obj = Scooter(	scooter['id'], 
# 								scooter['lat'], 
# 								scooter['lng'], 
# 								scooter['is_reserved']
# 							 )
# 		db.append(scooter_obj)
# 	return db
	
	
# def get_scooter_with_id(search_id, db):
# 	try:
# 		scooter = next(scooter for scooter in db if scooter.id == search_id)	# get the scooter with specified id
# 		return scooter
# 	except StopIteration:
# 		# no scooter with the id was found
# 		return None
	

# def write_db(db):
# 	# serialize Scooter objects 
# 	db_list = convert_db_to_dictlist(db)
# 	db_json = json.dumps(db_list)
# 	open('scooter_db.json', 'w').write(db_json)
# 	return True
		
# # class scooter for internal use
# class Scooter:
# 	def __init__(self, scooter_id, lat, lng, is_reserved):
# 		self.id = scooter_id
# 		self.lat = lat
# 		self.lng = lng
# 		self.is_reserved = is_reserved
	
# 	def to_dict(self):
# 		return {	'id':self.id, 
# 					'lat':self.lat, 
# 					'lng':self.lng, 
# 					'is_reserved':self.is_reserved
# 			   }
		
# def convert_db_to_dictlist(db):
# 	db_list = []
# 	for scooter in db:
# 		db_list.append(scooter.to_dict())
# 	return db_list
		


# if __name__== "__main__":
# 	# TDOO: Turn debug flag off for production system
# 	app.run('localhost', 8080)

# ---------------------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, request, redirect, url_for
from geopy.distance import distance as geodesic
import json, werkzeug
from http import HTTPStatus
from logger_config import get_logger

app = Flask(__name__)

# get configured logger (console + rotating file)
logger = get_logger("scooter_app")

def breadcrumb(*args):
    if app.debug:
        print("BREADCRUMB:", *args)

# root
@app.route('/')
def home():
    logger.debug("Entered home()")
    breadcrumb("home -> redirect to view_all_available")
    return redirect(url_for('view_all_available'))

# view all scooters
@app.route('/inventory')
def inventory():
    logger.debug("Entered inventory()")
    breadcrumb("inventory -> init_db")
    try:
        db = init_db()
        breadcrumb("inventory -> convert_db_to_dictlist")
        db_dictlist = convert_db_to_dictlist(db)
        logger.info("Returning inventory with %d scooters", len(db_dictlist))
        return json.dumps(db_dictlist), HTTPStatus.OK.value, {'Content-Type':'application/json'}
    except Exception as e:
        logger.exception("Unhandled exception in inventory(): %s", e)
        breadcrumb("inventory -> exception", str(e))
        error = {'msg': 'Internal Server Error'}
        return json.dumps(error), HTTPStatus.INTERNAL_SERVER_ERROR.value, {'Content-Type':'application/json'}

@app.route('/view_all_available')
def view_all_available():
    logger.debug("Entered view_all_available()")
    breadcrumb("view_all_available -> init_db")
    try:
        db = init_db()
        available_scooters = [scooter for scooter in db if not scooter.is_reserved]
        breadcrumb("view_all_available -> found available", len(available_scooters))
        available_scooters_dictlist = convert_db_to_dictlist(available_scooters)
        logger.info("Returning %d available scooters", len(available_scooters_dictlist))
        return json.dumps(available_scooters_dictlist), HTTPStatus.OK.value, {'Content-Type':'application/json'}
    except Exception as e:
        logger.exception("Unhandled exception in view_all_available(): %s", e)
        breadcrumb("view_all_available -> exception", str(e))
        error = {'msg': 'Internal Server Error'}
        return json.dumps(error), HTTPStatus.INTERNAL_SERVER_ERROR.value, {'Content-Type':'application/json'}

# Search for scooters
@app.route('/search', methods=['GET'])
def search():
    logger.debug("Entered search() with args: %s", dict(request.args))
    breadcrumb("search -> parse params", dict(request.args))
    try:
        search_lat, search_lng, search_radius = \
            float(request.args['lat']), \
            float(request.args['lng']), \
            float(request.args['radius'])
        breadcrumb("search -> parsed params", search_lat, search_lng, search_radius)
        logger.debug("Parsed search params lat=%s lng=%s radius=%s", search_lat, search_lng, search_radius)
    except werkzeug.exceptions.BadRequestKeyError:
        logger.warning("search() missing required parameters")
        breadcrumb("search -> missing params")
        error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
    except ValueError:
        logger.warning("search() invalid param value, non-numeric lat/lng/radius")
        breadcrumb("search -> invalid numeric")
        error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}

    if not -90 <= search_lat <= 90:
        logger.warning("search() latitude out of range: %s", search_lat)
        breadcrumb("search -> lat out of range", search_lat)
        error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
    if not -180 <= search_lng <= 180:
        logger.warning("search() longitude out of range: %s", search_lng)
        breadcrumb("search -> lng out of range", search_lng)
        error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}

    try:
        db = init_db()
        breadcrumb("search -> init_db done")
        search_results = []
        for scooter in db:
            distance = geodesic((scooter.lat, scooter.lng), (search_lat, search_lng)).m
            if distance <= search_radius and not scooter.is_reserved:
                search_results.append({ 'id':scooter.id, 'lat':scooter.lat, 'lng':scooter.lng })
        logger.info("search() found %d matching scooters", len(search_results))
        breadcrumb("search -> results count", len(search_results))
        return json.dumps(search_results), HTTPStatus.OK.value, {'Content-Type':'application/json'}
    except Exception as e:
        logger.exception("Unhandled exception in search(): %s", e)
        breadcrumb("search -> exception", str(e))
        error = {'msg': 'Internal Server Error'}
        return json.dumps(error), HTTPStatus.INTERNAL_SERVER_ERROR.value, {'Content-Type':'application/json'}

# Start a reservation
@app.route('/reservation/start', methods=['GET'])
def start_reservation():
    logger.debug("Entered start_reservation() with args: %s", dict(request.args))
    breadcrumb("start_reservation -> parse params", dict(request.args))
    try:
        reserve_id = request.args['id']
        breadcrumb("start_reservation -> reserve_id", reserve_id)
    except werkzeug.exceptions.BadRequestKeyError:
        logger.warning("start_reservation() missing id param")
        breadcrumb("start_reservation -> missing id")
        error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}

    try:
        db = init_db()
        breadcrumb("start_reservation -> init_db")
        scooter = get_scooter_with_id(reserve_id, db)
        if scooter:
            breadcrumb("start_reservation -> scooter found", reserve_id, "is_reserved:", scooter.is_reserved)
            logger.debug("start_reservation() found scooter id=%s reserved=%s", reserve_id, scooter.is_reserved)
            if not scooter.is_reserved:
                scooter.is_reserved = True
                write_db(db)
                success = { 'msg': f'Scooter {reserve_id} was reserved successfully.' }
                logger.info("start_reservation() reserved scooter %s", reserve_id)
                breadcrumb("start_reservation -> reserved", reserve_id)
                return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}
            else:
                logger.warning("start_reservation() scooter %s already reserved", reserve_id)
                breadcrumb("start_reservation -> already reserved", reserve_id)
                error = { 'msg': f'Error 422 - Scooter with id {reserve_id} is already reserved.' }
                return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
        else:
            logger.warning("start_reservation() no scooter found with id %s", reserve_id)
            breadcrumb("start_reservation -> not found", reserve_id)
            error = { 'msg': f'Error 422 - No scooter with id {reserve_id} was found.' }
            return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
    except Exception as e:
        logger.exception("Unhandled exception in start_reservation(): %s", e)
        breadcrumb("start_reservation -> exception", str(e))
        error = {'msg': 'Internal Server Error'}
        return json.dumps(error), HTTPStatus.INTERNAL_SERVER_ERROR.value, {'Content-Type':'application/json'}

# End a reservation
@app.route('/reservation/end', methods=['GET'])
def end_reservation():
    logger.debug("Entered end_reservation() with args: %s", dict(request.args))
    breadcrumb("end_reservation -> parse params", dict(request.args))
    try:
        scooter_id_to_end = request.args['id']
        end_lat, end_lng = float(request.args['lat']), float(request.args['lng'])
        db = init_db()
        breadcrumb("end_reservation -> parsed params", scooter_id_to_end, end_lat, end_lng)
    except werkzeug.exceptions.BadRequestKeyError:
        logger.warning("end_reservation() missing required params")
        breadcrumb("end_reservation -> missing params")
        error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
    except ValueError:
        logger.warning("end_reservation() invalid numeric params")
        breadcrumb("end_reservation -> invalid numeric")
        error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}

    if not -90 <= end_lat <= 90:
        logger.warning("end_reservation() latitude out of range: %s", end_lat)
        breadcrumb("end_reservation -> lat out of range", end_lat)
        error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
    if not -180 <= end_lng <= 180:
        logger.warning("end_reservation() longitude out of range: %s", end_lng)
        breadcrumb("end_reservation -> lng out of range", end_lng)
        error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
        return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}

    try:
        scooter = get_scooter_with_id(scooter_id_to_end, db)
        if scooter:
            breadcrumb("end_reservation -> scooter found", scooter_id_to_end, "is_reserved:", scooter.is_reserved)
            logger.debug("end_reservation() found scooter id=%s reserved=%s", scooter_id_to_end, scooter.is_reserved)
            if scooter.is_reserved:
                breadcrumb("end_reservation -> initiating payment", scooter_id_to_end)
                logger.info("end_reservation() initiating payment for scooter %s", scooter_id_to_end)
                payment_response = pay(scooter, end_lat, end_lng)
                breadcrumb("end_reservation -> payment_response", payment_response)
                if payment_response['status']:
                    scooter.is_reserved = False
                    scooter.lat, scooter.lng = end_lat, end_lng
                    write_db(db)
                    success = { 'msg': f'Payment for scooter {scooter_id_to_end} was made successfully and the reservation was ended.', 'txn_id': payment_response['txn_id'] }
                    logger.info("end_reservation() payment success for scooter %s txn=%s", scooter_id_to_end, payment_response['txn_id'])
                    breadcrumb("end_reservation -> success", scooter_id_to_end, payment_response['txn_id'])
                    return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}
                else:
                    logger.warning("end_reservation() payment failed: %s", payment_response.get('msg'))
                    breadcrumb("end_reservation -> payment failed", payment_response)
                    error = { 'msg': payment_response['msg'] }
                    response_code = payment_response['code']
                    return json.dumps(error), response_code, {'Content-Type':'application/json'}
            else:
                logger.warning("end_reservation() scooter %s not reserved", scooter_id_to_end)
                breadcrumb("end_reservation -> not reserved", scooter_id_to_end)
                error = { 'msg': f'Error 422 - No reservation for scooter {scooter_id_to_end} presently exists.' }
                return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
        else:
            logger.warning("end_reservation() no scooter found with id %s", scooter_id_to_end)
            breadcrumb("end_reservation -> not found", scooter_id_to_end)
            error = { 'msg': f'Error 422 - No scooter with id {scooter_id_to_end} was found.' }
            return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}
    except Exception as e:
        logger.exception("Unhandled exception in end_reservation(): %s", e)
        breadcrumb("end_reservation -> exception", str(e))
        error = {'msg': 'Internal Server Error'}
        return json.dumps(error), HTTPStatus.INTERNAL_SERVER_ERROR.value, {'Content-Type':'application/json'}

# ==================
#  HELPER FUNCTIONS
# ==================

def pay(scooter, end_lat, end_lng):
    logger.debug("pay() called for scooter %s to (%s,%s)", scooter.id, end_lat, end_lng)
    breadcrumb("pay -> calc distance", scooter.id)
    try:
        old_location = (scooter.lat, scooter.lng)
        new_location = (end_lat, end_lng)
        distance_ridden = geodesic(old_location, new_location).m
        distance_ridden = round(distance_ridden)
        breadcrumb("pay -> distance_ridden", distance_ridden)
        logger.debug("pay() distance_ridden=%s", distance_ridden)
        cost = calculate_cost(distance_ridden)
        breadcrumb("pay -> cost", cost)
        logger.debug("pay() cost=%s", cost)
        return payment_gateway(cost)
    except Exception as e:
        logger.exception("Unhandled exception in pay(): %s", e)
        breadcrumb("pay -> exception", str(e))
        return {'status': False, 'msg': 'Payment processing error', 'code': HTTPStatus.INTERNAL_SERVER_ERROR.value}

def payment_gateway(cost):
    logger.debug("payment_gateway() called with cost=%s", cost)
    breadcrumb("payment_gateway -> called", cost)
    txn_id = 379892831
    logger.info("payment_gateway() returning dummy txn_id=%s", txn_id)
    return {'status': True, 'txn_id': txn_id}

def calculate_cost(distance):
    logger.debug("calculate_cost() called distance=%s", distance)
    breadcrumb("calculate_cost -> called", distance)
    return distance

def init_db():
    logger.debug("init_db() called")
    breadcrumb("init_db -> read scooter_db.json")
    try:
        db_json = open('scooter_db.json', 'r').read()
        db_list = json.loads(db_json)
        db = []
        for scooter in db_list:
            scooter_obj = Scooter(scooter['id'], scooter['lat'], scooter['lng'], scooter['is_reserved'])
            db.append(scooter_obj)
        breadcrumb("init_db -> loaded count", len(db))
        logger.debug("init_db() loaded %d scooters", len(db))
        return db
    except Exception as e:
        logger.exception("init_db() failed: %s", e)
        breadcrumb("init_db -> exception", str(e))
        return []

def get_scooter_with_id(search_id, db):
    logger.debug("get_scooter_with_id() searching for id=%s", search_id)
    breadcrumb("get_scooter_with_id ->", search_id)
    try:
        scooter = next(scooter for scooter in db if scooter.id == search_id)
        breadcrumb("get_scooter_with_id -> found", search_id)
        return scooter
    except StopIteration:
        breadcrumb("get_scooter_with_id -> not found", search_id)
        logger.debug("get_scooter_with_id() not found id=%s", search_id)
        return None
    except Exception as e:
        logger.exception("get_scooter_with_id() exception: %s", e)
        breadcrumb("get_scooter_with_id -> exception", str(e))
        return None

def write_db(db):
    logger.debug("write_db() called")
    breadcrumb("write_db -> serialize db")
    try:
        db_list = convert_db_to_dictlist(db)
        db_json = json.dumps(db_list)
        open('scooter_db.json', 'w').write(db_json)
        breadcrumb("write_db -> wrote file", len(db_list))
        logger.info("write_db() wrote %d scooters", len(db_list))
        return True
    except Exception as e:
        logger.exception("write_db() failed: %s", e)
        breadcrumb("write_db -> exception", str(e))
        return False

class Scooter:
    def __init__(self, scooter_id, lat, lng, is_reserved):
        self.id = scooter_id
        self.lat = lat
        self.lng = lng
        self.is_reserved = is_reserved

    def to_dict(self):
        return {'id':self.id, 'lat':self.lat, 'lng':self.lng, 'is_reserved':self.is_reserved}

def convert_db_to_dictlist(db):
    logger.debug("convert_db_to_dictlist() called with %d items", len(db))
    breadcrumb("convert_db_to_dictlist -> called", len(db))
    db_list = []
    for scooter in db:
        db_list.append(scooter.to_dict())
    return db_list

if __name__== "__main__":
    app.debug = True
    logger.info("Starting app with debug=%s", app.debug)
    app.run('localhost', 8080)


