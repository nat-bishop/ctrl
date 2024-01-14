from typing import Optional
import ctrl.database.utils as db_utils
import ctrl.database.query as query
import ctrl.new.new_utils as new_utils


def edit(project_name: str, tags: Optional[list[str]], description: str, creators: Optional[list[str]]) -> None:
    db_utils.perform_db_op(_edit_db, project_name, tags, description, creators)


def _edit_db(cursor, project_name: str, tags: Optional[list[str]], description: str, creators: Optional[list[str]]):
    if not tags and not description and not creators:
        raise ValueError('no values provided to update')

    proj_id = query.get_project_id(cursor, project_name)

    if not proj_id:
        raise ValueError(f"project: {project_name} not found")

    if description:
        update_data = {'description': description}
        query.update_records(cursor, 'Projects', update_data, 'ProjectID', proj_id)

    if creators:
        data = {'ProjectID': proj_id}
        query.delete_record(cursor, 'Project_Users', 'ProjectID', proj_id)
        for user in creators:
            user_id = query.get_user_id(cursor, user)
            data['UserID'] = user_id
            query.insert_record(cursor, 'Project_Users', data)

    if tags:
        query.delete_record(cursor, 'Project_Tags', 'ProjectID', proj_id)
        updated_tags = new_utils.create_tags(cursor, tags)
        data = {'ProjectID': proj_id}
        for id in updated_tags:
            data['TagID'] = id
            query.insert_record(cursor, 'Project_Tags', data)
