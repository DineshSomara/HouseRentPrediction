import json
import pickle
import numpy as np
import sklearn

__data_columns = None
__area_locality = None
__model = None


def get_location_names():
    return __area_locality


def load_saved_artifacts():
    global __data_columns
    global __area_locality
    global __model
    with open("./artifacts/columns.json") as f:
        __data_columns = json.load(f)['data_columns']
        __area_locality = __data_columns[10:]
        print("Loaded columns:")

    with open("./artifacts/home_rent_best_model_rfr.pkl", 'rb') as f:
        __model = pickle.load(f)
        print("Model loaded:", __model)
    print("loading saved artifacts... done")
    print(__model)


def get_estimated_price(bhk, size, floor, area_type, area_location, city, furnishing_status, tenant_preferred,
                              bathroom,
                              point_of_contact):
    print(f"Input values: bhk={bhk}, size={size}, floor={floor}, area_type={area_type}, area_location={area_location}, city={city}, furnishing_status={furnishing_status}, tenant_preferred={tenant_preferred}, bathroom={bathroom}, point_of_contact={point_of_contact}")

    global __data_columns
    global __area_locality
    global __model
    with open("./artifacts/columns.json") as f:
        __data_columns = json.load(f)['data_columns']
        __area_locality = __data_columns[10:]
    with open("./artifacts/home_rent_best_model_rfr.pkl", 'rb') as f:
        __model = pickle.load(f)
        print("Model loaded:", __model)
    try:
        loc_index = __data_columns.index(area_location)
    except:
        loc_index = -1

    with open('./artifacts/le_area_type.pkl', 'rb') as f:
        le_area_type = pickle.load(f)

    with open('./artifacts/le_city.pkl', 'rb') as f:
        le_city = pickle.load(f)

    with open('./artifacts/le_furnishing.pkl', 'rb') as f:
        le_furnishing = pickle.load(f)

    with open('./artifacts/le_tenant.pkl', 'rb') as f:
        le_tenant = pickle.load(f)

    with open('./artifacts/le_contact.pkl', 'rb') as f:
        le_contact = pickle.load(f)

    area_type_transformed = le_area_type.transform([area_type])[0]
    city_transformed = le_city.transform([city])[0]
    furnishing_status_transformed = le_furnishing.transform([furnishing_status])[0]
    tenant_preferred_transformed = le_tenant.transform([tenant_preferred])[0]
    point_of_contact_transformed = le_contact.transform([point_of_contact])[0]

    X = np.zeros(len(__data_columns) - 1)
    X[0] = bhk
    X[1] = size
    X[2] = floor
    X[3] = area_type_transformed
    X[4] = city_transformed
    X[5] = furnishing_status_transformed
    X[6] = tenant_preferred_transformed
    X[7] = bathroom
    X[8] = point_of_contact_transformed

    if loc_index >= 0:
        X[loc_index] = 1

    return __model.predict([X])[0]

