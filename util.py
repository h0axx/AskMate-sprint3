import data_handling, csv, database_manager, basic_db_usage

def id_generator(filename):
# Function to generate an ID number, for the next record in file

    id = database_manager.highest_id()
    id += 1
    # Has to be bigger than highest

    return id

def is_id_in_file(datafile,id):

    ID_INDEX = 0

    for record in datafile:
        if id == record[ID_INDEX]:
            return True

    return False

def by_view(e):
    VIEW_NUMBER_INDEX = 2
    return e[VIEW_NUMBER_INDEX]

def by_vote(e):
    VOTE_NUMBER_INDEX = 3
    return e[VOTE_NUMBER_INDEX]

def sort(by):


    if by == 'id':
        data = database_manager.sort_by_id()
        return data
    elif by == 'view_number':
    # Sort by view number
        data = database_manager.sort_by_view()
        return data

    elif by == 'vote_number':
    # Sort by vote number
        data = database_manager.sort_by_vote()
        return data

def what_index_by_id(datafile,id):

    enumerate = 0
    ID_INDEX = 0

    for record in datafile:
        if record[ID_INDEX] == id:
            return enumerate
        else:
            enumerate += 1

    return False

def search_results(data,search):

    search_result = []
    search = search.lower()

    for record in data:
        for element in record:
            element = str(element)
            element = element.lower()
            if search in element:
                search_result.append(record)

    return search_result










