import ctrl.database.utils as utils
import ctrl.database.query as query


def delete_user(name):
    utils.perform_db_op(query.delete_record, 'Users', 'Name', name)
    #TODO delete project_users, asset_users